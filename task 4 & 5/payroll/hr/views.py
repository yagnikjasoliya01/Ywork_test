from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F
from .models import Department, Employee, LeaveApplication
from .serializers import (
    DepartmentSerializer, EmployeeSerializer, LeaveApplicationSerializer,
    PayableSalarySerializer, HighEarnerSerializer, HighEarnerByMonthSerializer
)

# API 1: Create a department
class DepartmentCreateAPIView(APIView):
    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API 2: Create an employee
class EmployeeCreateAPIView(APIView):
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API 3: Set base salary for an employee
class EmployeeSetSalaryAPIView(APIView):
    def post(self, request, pk):
        try:
            employee = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found.'}, status=status.HTTP_404_NOT_FOUND)

        new_salary = request.data.get('baseSalary')
        if new_salary is None:
            return Response({'error': 'baseSalary is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            employee.baseSalary = int(new_salary)
            employee.save()
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ValueError, TypeError):
            return Response({'error': 'Invalid salary value.'}, status=status.HTTP_400_BAD_REQUEST)

# API 4: Increase leave count of an employee
class UpdateLeaveCountAPIView(APIView):
    def put(self, request, employee_id, month, year):
        try:
            employee = Employee.objects.get(pk=employee_id)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            leave_app, created = LeaveApplication.objects.get_or_create(
                employee=employee,
                month=month,
                year=year,
            )
            leave_app.leaves += 1
            leave_app.save()
            serializer = LeaveApplicationSerializer(leave_app)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# API 5: Calculate payable salary
class CalculatePayableSalaryAPIView(APIView):
    def post(self, request, employee_id, month, year):
        try:
            employee = Employee.objects.get(pk=employee_id)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            leave_app = LeaveApplication.objects.get(
                employee=employee,
                month=month,
                year=year
            )
            base_salary = employee.baseSalary
            leaves = leave_app.leaves
            # (Base salary) - (No of leaves * (Base salary/25) )
            payable_salary = base_salary - (leaves * (base_salary / 25))
            
            serializer = PayableSalarySerializer({'payable_salary': payable_salary})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except LeaveApplication.DoesNotExist:
            # If no leave application exists, payable salary is the base salary
            payable_salary = employee.baseSalary
            serializer = PayableSalarySerializer({'payable_salary': payable_salary})
            return Response(serializer.data, status=status.HTTP_200_OK)

# API 6: Find high earners in a department
class HighEarnerDepartmentAPIView(APIView):
    def get(self, request, department_id):
        try:
            department = Department.objects.get(pk=department_id)
        except Department.DoesNotExist:
            return Response({'error': 'Department not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get all unique salaries for the department, sorted descending
        unique_salaries = (Employee.objects
                          .filter(department=department)
                          .values_list('baseSalary', flat=True)
                          .order_by('-baseSalary')
                          .distinct())
        
        # Get the top 3 unique salaries
        top_salaries = list(unique_salaries[:3])
        
        # Find all employees with a base salary in the top 3
        high_earners = Employee.objects.filter(
            department=department,
            baseSalary__in=top_salaries
        ).order_by('-baseSalary', 'name')
        
        serializer = HighEarnerSerializer(high_earners, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# API 7: Find high earners in a specific month
class HighEarnerMonthAPIView(APIView):
    def get(self, request, month, year):
        all_employees = Employee.objects.all()
        employee_salaries = []

        for employee in all_employees:
            try:
                leave_app = LeaveApplication.objects.get(
                    employee=employee,
                    month=month,
                    year=year
                )
                leaves = leave_app.leaves
            except LeaveApplication.DoesNotExist:
                leaves = 0

            base_salary = employee.baseSalary
            payable_salary = base_salary - (leaves * (base_salary / 25))
            
            employee_salaries.append({
                'employee_id': employee.id,
                'employee_name': employee.name,
                'payable_salary': payable_salary
            })

        # Sort employees by payable salary in descending order
        sorted_employees = sorted(employee_salaries, key=lambda x: x['payable_salary'], reverse=True)
        
        # Get the top 3 high earners
        high_earners = sorted_employees[:3]
        
        serializer = HighEarnerByMonthSerializer(high_earners, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def chat_view(request):
    return render(request, 'hr/chat.html')