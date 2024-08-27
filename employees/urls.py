from django.urls import path
from .views import EmployeeListCreate, EmployeeRetrieveUpdateDestroy, ReviewCreate

urlpatterns = [
    path('employees/', EmployeeListCreate.as_view(), name='employee-list-create'),
    path('employees/<int:pk>/', EmployeeRetrieveUpdateDestroy.as_view(), name='employee-retrieve-update-destroy'),
    path('reviews/create/', ReviewCreate.as_view(), name='review-create'),
]
