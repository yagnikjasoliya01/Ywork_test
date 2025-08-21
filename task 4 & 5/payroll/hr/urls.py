from django.urls import path
from .views import (
    DepartmentCreateAPIView, EmployeeCreateAPIView, EmployeeSetSalaryAPIView,
    UpdateLeaveCountAPIView, CalculatePayableSalaryAPIView,
    HighEarnerDepartmentAPIView, HighEarnerMonthAPIView, chat_view
)

urlpatterns = [
    # 1. POST to create department
     path('departments/', DepartmentCreateAPIView.as_view(), name='create-department'),

    # 2. POST to create employee
     path('employees/', EmployeeCreateAPIView.as_view(), name='create-employee'),

    # 3. POST to set base salary (using employee ID in URL)
     path('employees/<int:pk>/salary/', EmployeeSetSalaryAPIView.as_view(), name='set-salary'),

    # 4. UPDATE API to increase leave count
     path('employees/<int:employee_id>/leaves/<str:month>/<str:year>/', 
         UpdateLeaveCountAPIView.as_view(), name='update-leaves'),

    # 5. POST to calculate payable salary
     path('employees/<int:employee_id>/salary/<str:month>/<str:year>/',
         CalculatePayableSalaryAPIView.as_view(), name='calculate-salary'),

    # 6. GET high earners in a department
     path('departments/<uuid:department_id>/high-earners/',
         HighEarnerDepartmentAPIView.as_view(), name='high-earners-department'),

    # 7. GET high earners in a specific month
     path('high-earners/<str:month>/<str:year>/',
         HighEarnerMonthAPIView.as_view(), name='high-earners-month'),

     path('chat/', chat_view, name='chat-page'),
]
