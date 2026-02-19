from django.urls import path
from . import views

urlpatterns = [
    path('create_ticket/', views.create_ticket, name='create_ticket'),
    path('tickets/<int:pk>/', views.ticket_detail, name='ticket_detail'),  # detail view
    path('tickets/', views.create_ticket, name='create_ticket'),

]
