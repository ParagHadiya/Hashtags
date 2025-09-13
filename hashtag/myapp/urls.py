from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),                      # Home Page
    path('generate/', views.generate, name='generate'),     # POST generation action
    path('features/', views.features, name='features'),     # Features Page
    path('about/', views.about, name='about'),              # About Page
    path('contact/', views.contact, name='contact'),        # Contact Page
    path('index/', views.index, name='index'),              # Index Page (data listing)
]
