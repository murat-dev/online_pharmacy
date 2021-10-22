from django.urls import path

from .views import CatalogView, DrugsListView, drug_detail, addcomment

urlpatterns = [
    path('', CatalogView.as_view(), name='catalog'),
    path('drugs/', DrugsListView.as_view(), name='drugs-list'),
    path('drugs/<int:pk>/', drug_detail, name='drug-detail'),
    path('addcomment/<int:pk>/', addcomment, name='add-comment'),


]

