from django.conf import settings
from django.db import models

class Ticket(models.Model):
    OPEN = 'Open'
    IN_PROGRESS = 'In Progress'
    RESOLVED = 'Resolved'
    TICKET_STATUS_CHOICES = [
        (OPEN, 'Open'),
        (IN_PROGRESS, 'In Progress'),
        (RESOLVED, 'Resolved'),
    ]

    title = models.CharField(max_length=255)
    category = models.CharField(
        max_length=50,
        choices=[('Hardware', 'Hardware'), ('Software', 'Software'), ('Network', 'Network'), ('Other', 'Other')]
    )
    description = models.TextField()
    status = models.CharField(max_length=20, choices=TICKET_STATUS_CHOICES, default=OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Correct reference to custom user model using settings.AUTH_USER_MODEL
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tickets', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='assigned_tickets', null=True, blank=True, on_delete=models.SET_NULL
    )

    attachment = models.FileField(upload_to='tickets/attachments/', null=True, blank=True)

    def __str__(self):
        return self.title
