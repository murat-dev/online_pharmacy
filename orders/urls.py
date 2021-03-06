from django.urls import path

from . import views


app_name = 'orders'


urlpatterns = [
    path('create/', views.order_create, name='order-create'),
    path('admin/order/<int:order_id>/pdf/', views.admin_order_pdf, name='admin-order-pdf'),
    path('history/', views.get_order_history, name='history'),
    path('history/detail/<int:order_id>/', views.get_history_detail, name='order-history'),

]