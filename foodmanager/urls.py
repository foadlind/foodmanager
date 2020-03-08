"""foodmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth.views import (
    password_change,
    password_change_done,
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete,
)
from planner import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^recipes/$', views.recipes, name='recipes'),
    url(r'^recipes/create_recipe/$', views.create_recipe,
        name='create_recipe'),
    url(r'^recipes/import_recipe/$', views.import_recipe,
        name='import_recipe'),
    url(r'^recipes/(?P<slug>[-\w]+)/$', views.recipe_detail,
        name='recipe_detail'),
    url(r'^recipes/(?P<slug>[-\w]+)/edit/$', views.edit_recipe,
        name='edit_recipe'),
    url(r'^recipes/(?P<slug>[-\w]+)/deleted/$', views.delete_recipe, name='delete_recipe'),
    url(r'^planner/$', views.planner, name='planner'),
    url(r'^planner/email_sent/$', views.email_sent, name='email_sent'),  # TemplateView.as_view(template_name='planner/email_sent.html')
    url(r'^accounts/password/change/$', password_change,
        {'template_name': 'registration/password_change_form.html'},
        name="password_change"),
    url(r'^accounts/password/change/done/$', password_change_done,
        {'template_name': 'registration/password_change_done.html'},
        name="password_change_done"),
    url(r'^accounts/password/reset/$', password_reset,
        {'template_name': 'registration/password_reset_form.html'},
        name="password_reset"),
    url(r'^accounts/password/reset/done/$', password_reset_done,
        {'template_name': 'registration/password_reset_done.html'},
        name="password_reset_done"),
    url(r'^accounts/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        password_reset_confirm,
        {'template_name': 'registration/password_reset_confirm.html'},
        name="password_reset_confirm"),
    url(r'^accounts/password/done/$', password_reset_complete,
        {'template_name': 'registration/password_reset_complete.html'},
        name="password_reset_complete"),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^admin/', admin.site.urls),
]
