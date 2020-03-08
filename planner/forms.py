from django import forms
from planner.models import Recipe, Ingredient


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('name', 'instructions',)


class PlanForm(forms.Form):
    day1 = forms.ChoiceField(choices=(), label="Day 1", required=False)
    day2 = forms.ChoiceField(choices=(), label="Day 2", required=False)
    day3 = forms.ChoiceField(choices=(), label="Day 3", required=False)
    day4 = forms.ChoiceField(choices=(), label="Day 4", required=False)
    day5 = forms.ChoiceField(choices=(), label="Day 5", required=False)
    day6 = forms.ChoiceField(choices=(), label="Day 6", required=False)
    day7 = forms.ChoiceField(choices=(), label="Day 7", required=False)

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', None)
        super(PlanForm, self).__init__(*args, **kwargs)
        if choices is not None:
            self.fields['day1'].choices = choices
            self.fields['day1'].choices.insert(0, ('', 'Select a recipe'))
            self.fields['day2'].choices = choices
            self.fields['day2'].choices.insert(0, ('', 'Select a recipe'))
            self.fields['day3'].choices = choices
            self.fields['day3'].choices.insert(0, ('', 'Select a recipe'))
            self.fields['day4'].choices = choices
            self.fields['day4'].choices.insert(0, ('', 'Select a recipe'))
            self.fields['day5'].choices = choices
            self.fields['day5'].choices.insert(0, ('', 'Select a recipe'))
            self.fields['day6'].choices = choices
            self.fields['day6'].choices.insert(0, ('', 'Select a recipe'))
            self.fields['day7'].choices = choices
            self.fields['day7'].choices.insert(0, ('', 'Select a recipe'))


class ShoppingListForm(forms.Form):
    shopping_list = forms.CharField(strip=False)
    email_address = forms.EmailField()


class RecipeUrlForm(forms.Form):
    from_url = forms.URLField(required=True)


# https://github.com/elo80ka/django-dynamic-formset/blob/master/docs/usage.rst
IngredientFormSet = forms.models.inlineformset_factory(Recipe, Ingredient,
                                                       fields=('amount', 'unit', 'name',),
                                                       can_delete=True,
                                                       extra=3)

