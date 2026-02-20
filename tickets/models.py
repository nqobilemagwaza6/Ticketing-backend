from django.db import models
from django.contrib.auth import get_user_model
import os

User = get_user_model()

def ticket_attachment_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/tickets/user_<id>/<filename>
    return f'tickets/user_{instance.user.id}/{filename}'

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]
    
    CATEGORY_CHOICES = [
        ('Hardware', 'Hardware'),
        ('Software', 'Software'),
        ('Network', 'Network'),
        ('Other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    priority = models.CharField(max_length=20, default='Medium')
    
    # Relationships
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    
    # Attachments
    attachment = models.FileField(upload_to=ticket_attachment_path, null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"#{self.id} - {self.title}"
    
    def filename(self):
        return os.path.basename(self.attachment.name) if self.attachment else None
    
    class Meta:
        ordering = ['-created_at']

class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.user.email} on ticket #{self.ticket.id}"
    
    class Meta:
        ordering = ['created_at']