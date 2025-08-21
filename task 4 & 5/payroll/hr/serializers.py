from rest_framework import serializers
from .models import Department, Employee, LeaveApplication

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'baseSalary', 'department']

class LeaveApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveApplication
        fields = ['employee', 'month', 'year', 'leaves']

class PayableSalarySerializer(serializers.Serializer):
    payable_salary = serializers.FloatField()

class HighEarnerSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name')
    
    class Meta:
        model = Employee
        fields = ['id', 'name', 'baseSalary', 'department_name']

class HighEarnerByMonthSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    employee_name = serializers.CharField()
    payable_salary = serializers.FloatField()