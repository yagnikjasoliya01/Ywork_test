import uuid
from django.db import models

class Department(models.Model):
    # UUIDField is used for the UUID string primary key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    baseSalary = models.IntegerField()
    # foreign key to the Department table
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees')

    def __str__(self):
        return self.name

class LeaveApplication(models.Model):
    # foreign key to the Employee table
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_applications')
    month = models.CharField(max_length=20)
    year = models.CharField(max_length=4)
    leaves = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.employee.name} - {self.month} {self.year}"
