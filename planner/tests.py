from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from planner.models import Recipe


class PlannerTest(TestCase):
    def setUp(self):
        self.client = Client()
        # create a dummy user
        self.user = User.objects.create_user('tester', 'rester@test.com',
                                             'testpassword')
        # create a dummy Recipe object
        Recipe.objects.create(name='deli', 
                              instructions='add all.', slug='testers-deli', user=self.user)

    def test_index(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_contact(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)

    def test_recipes_loggedin(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('recipes'))
        self.assertEqual(response.status_code, 200)

    def test_recipes_loggedout(self):
        response = self.client.get(reverse('recipes'))
        self.assertRedirects(response, '/accounts/login/?next=/recipes/',
                             status_code=302, target_status_code=200)

    def test_recipe_detail(self):
        self.client.login(username='tester', password='testpassword')
        response = self.client.get('/recipes/testers-deli/')
        self.assertEqual(response.status_code, 200)

    def test_recipe_edit_get(self):
        self.client.login(username='tester', password='testpassword')
        response = self.client.get('/recipes/testers-deli/edit/')
        self.assertEqual(response.status_code, 200)

    #def test_recipe_edit_post(self):
    #    self.client.login(username='tester', password='testpassword')
    #    response = self.client.post('/recipes/testers-deli/edit/', {
    #        'name': 'deli',
    #        'ingredients': 'ing1, ing2',
    #        'instructions': 'add all.'
    #    })
    #    self.assertRedirects(response, '/recipes/testers-deli/',
    #                         status_code=302, target_status_code=200)

    def test_create_recipe_get(self):
        self.client.login(username='tester', password='testpassword')
        response = self.client.get(reverse('create_recipe'))
        self.assertEqual(response.status_code, 200)

    #def test_create_recipe_post(self):
    #    self.client.login(username='tester', password='testpassword')
    #    response = self.client.post(reverse('create_recipe'), {
    #        'name': 'delitest',
    #        'ingredients': 'water, ice',
    #        'instructions': 'mix and match.'
    #    })
    #    self.assertRedirects(response, '/recipes/testers-delitest/',
    #                         status_code=302, target_status_code=200)

    def test_import_recipe_get(self):
        self.client.login(username='tester', password='testpassword')
        response = self.client.get(reverse('import_recipe'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_delete_post(self):
        self.client.login(username='tester', password='testpassword')
        response = self.client.post('/recipes/testers-deli/deleted/', {
            'slug': 'deli',
        })
        self.assertFalse(Recipe.objects.filter(slug='testers-deli').exists())
