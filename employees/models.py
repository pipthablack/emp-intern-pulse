from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    position = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.employee.name}'
