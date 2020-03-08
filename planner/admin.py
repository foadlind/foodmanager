from django.contrib import admin
# importing the model
from planner.models import Recipe, Ingredient

# set up automated slug creation
class RecipeAdmin(admin.ModelAdmin):
	model = Recipe
	list_display = ('name', 'user',)
	prepopulated_fields = {'slug': ('name',)}


class IngredientAdmin(admin.ModelAdmin):
	model = Ingredient
	list_display = ('name', 'amount', 'unit', 'recipe',)


# Register your models here.
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)