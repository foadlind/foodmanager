from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.mail import send_mail
from time import strftime
from planner.forms import RecipeForm, PlanForm, ShoppingListForm, RecipeUrlForm, IngredientFormSet
from planner.models import Recipe, Ingredient
from planner.recipe_scraper import parse_recipe_from_url
import collections
from planner.utils import ShoppingList

# functions to supply date and weekday to views
def get_date():
    return strftime("%Y-%m-%d")


def get_weekday():
    return strftime("%A")


# Create your views here.
def index(request):
    return render(request, 'index.html', {
        'nbar': 'home'
    })


def about(request):
    return render(request, 'about.html', {
        'nbar': 'about'
    })


def contact(request):
    return render(request, 'contact.html', {
        'nbar': 'contact'
    })


@login_required
def recipes(request):
    recipes = Recipe.objects.filter(user=request.user)
    return render(request, 'recipes.html', {
        'recipes': recipes,
        'nbar': 'recipes',
    })


@login_required
def recipe_detail(request, slug):
    # grab the object...
    recipe = Recipe.objects.get(user=request.user, slug=slug)
    ingreds = Ingredient.objects.filter(recipe=recipe)
    # make sure user owns the object
    if recipe.user != request.user:
        raise Http404
    # and pass the object to the template
    return render(request, 'recipes/recipe_detail.html', {
        'date': get_date(),
        'weekday': get_weekday(),
        'recipe': recipe,
        'ingreds': ingreds,
    })


@login_required
def edit_recipe(request, slug):
    # grab the object...
    recipe = Recipe.objects.get(user=request.user, slug=slug)
    # make sure user owns the object
    if recipe.user != request.user:
        raise Http404
    # set the form we are using...
    form_class = RecipeForm

    # if we are comming to this view from a submitted form,
    if request.method == 'POST':
        # grab the data from the submitted form
        form = form_class(data=request.POST, instance=recipe)
        formset = IngredientFormSet(request.POST, request.FILES)
        if form.is_valid():
            # save the new data
            form.save()
            formset = IngredientFormSet(request.POST, request.FILES, instance=recipe)
            if formset.is_valid():
                formset.save()
                return redirect('recipe_detail', slug=recipe.slug)

    # otherwise just create the form
    else:
        form = form_class(instance=recipe)
        formset = IngredientFormSet(instance=recipe)

    # and render the template
    return render(request, 'recipes/edit_recipe.html', {
        'date': get_date(),
        'weekday': get_weekday(),
        'recipe': recipe,
        'form': form,
        'formset': formset,
    })


@login_required
def delete_recipe(request, slug):
    Recipe.objects.filter(user=request.user, slug=slug).delete()
    return render(request, 'recipes/recipe_deleted.html')


@login_required
def create_recipe(request):
    form_class = RecipeForm
    formset_class = IngredientFormSet

    # if we are coming from a submitted form, do this
    if request.method == 'POST':
        # grab the data from the submitted form and apply to the form
        form = form_class(request.POST)
        formset = formset_class(request.POST, request.FILES)

        if form.is_valid():
            # create an instance but don't save yet
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.slug = slugify(request.user.username + "s " + recipe.name)
            # check if recipe already exists
            if Recipe.objects.filter(user=recipe.user, slug=recipe.slug).exists():
                # flash
                messages.error(request, 'ERROR: You already have a recipe with the same name.')
            else:
                # save the object
                recipe.save()
                formset = IngredientFormSet(request.POST, request.FILES, instance=recipe)
                if formset.is_valid():
                    formset.save()
                    # redirect to our newly created recipe
                    return redirect('recipe_detail', slug=recipe.slug)

    # otherwise just create the form
    else:
        form = form_class()
        formset = formset_class()

    return render(request, 'recipes/create_recipe.html', {
        'date': get_date(),
        'weekday': get_weekday(),
        'form': form,
        'formset': formset,
    })


@login_required
def import_recipe(request):
    form_class = RecipeUrlForm

    # if we are coming from a submitted form, do this
    if request.method == 'POST':
        # grab the data from the submitted form and apply to the form
        recipe_import_error = "Sorry :( Not possible to import from the URL provided!"
        form = form_class(request.POST)

        if form.is_valid():
            # create an instance but don't save yet
            recipe = Recipe()
            # set the additional details
            from_url = form.cleaned_data['from_url']
            try:
                recipe.name, ingreds, parse_successful = parse_recipe_from_url(from_url)
                recipe.instructions = from_url
                recipe.user = request.user
                recipe.slug = slugify(request.user.username + "s " + recipe.name)
                # check if recipe already exists
                if not parse_successful:
                    messages.error(request, recipe_import_error)
                elif Recipe.objects.filter(user=recipe.user, slug=recipe.slug).exists():
                    # flash
                    messages.error(request, 'ERROR: You already have a recipe with the same name.')
                else:
                    # save the object
                    recipe.save()

                    for amount, unit, item in ingreds:
                        Ingredient.objects.create(name=item, amount=amount, unit=unit, recipe=recipe)

                    # redirect to our newly created recipe
                    return redirect('recipe_detail', slug=recipe.slug)

            except TypeError:
                messages.error(request, recipe_import_error)

    # otherwise just create the form
    else:
        form = form_class()

    return render(request, 'recipes/import_recipe.html', {
        'date': get_date(),
        'weekday': get_weekday(),
        'form': form,
    })


@login_required
def planner(request):
    CHOICES = Recipe.objects.filter(user=request.user).values_list('name', 'name')
    form_class = PlanForm(choices=CHOICES)
    # if we are comming from a submitted form, do this
    if request.method == 'POST':
        # grab the data from the submitted form and apply to the form
        form = PlanForm(request.POST, choices=CHOICES)

        if form.is_valid():
            # get the plan from the form in a sorted dict
            plan = collections.OrderedDict(sorted(form.cleaned_data.items()))

            shopping_list = ShoppingList()

            # populate shopping list
            for key, value in plan.items():
                if value != u'':
                    # get the recipes and account for empty selections
                    recipe = Recipe.objects.get(user=request.user, name=value)
                    ingreds = Ingredient.objects.filter(recipe=recipe)

                    for ingred in ingreds:
                        shopping_list.append_ingredient(ingred)
                        
            shopping_items = shopping_list.retrieve()
            shopping_form = ShoppingListForm()
            shopping_form.shopping_list = shopping_items[:]
            return render(request, 'planner/shopping_list.html', {
                'nbar': 'planner',
                'plan': plan,
                'shopping_items': sorted(shopping_items),
                'form': shopping_form,
            })

    # otherwise just create the form
    else:
        form = form_class

    return render(request, 'planner/planner.html', {
        'nbar': 'planner',
        'date': get_date(),
        'weekday': get_weekday(),
        'form': form,
    })


@login_required
def email_sent(request):
    # if we are comming from a submitted form, do this
    if request.method == 'POST':
        # grab the data from the submitted form and apply to the form
        shopping_list = request.POST.get('list')
        subject_line = "Shopping List"
        # send email and redirect to the correct template view
        send_mail(subject_line, shopping_list, 'info@koketsmeny.se',
                  [request.user.email], fail_silently=False,)
        return render(request, 'planner/email_sent.html')

    # otherwise just create the form
    else:
        pass  # I don't know yet

    recipes = Recipe.objects.filter(user=request.user)
    return render(request, 'recipes.html', {
        'recipes': recipes,
        'nbar': 'recipes',
    })
