from django.db import models
from django.conf import settings


class Case(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Escalated', 'Escalated'),
        ('Resolved', 'Resolved'),
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    CATEGORY_CHOICES = [
        ('Appointment', 'Appointment'),
        ('Billing', 'Billing'),
        ('Prescription', 'Prescription'),
        ('Insurance', 'Insurance'),
        ('Complaint', 'Complaint'),
        ('Other', 'Other'),
    ]

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='customer_cases',
        on_delete=models.CASCADE
    )

    assigned_agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='agent_cases',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    specialist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='specialist_cases',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')

    attachment = models.FileField(upload_to='case_attachments/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# TODO: to implement later
class CaseNote(models.Model):
    case = models.ForeignKey(Case, related_name='notes', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    note_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class CaseLog(models.Model):
    case = models.ForeignKey(Case, related_name='logs', on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.case.title} - {self.action}"