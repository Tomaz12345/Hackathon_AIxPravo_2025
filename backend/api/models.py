from django.db import models
import uuid

class BrandCheck(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('caution', 'Caution'),
        ('rejected', 'Rejected'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brandName = models.CharField(max_length=255)
    territories = models.CharField(max_length=255)
    office = models.CharField(max_length=255)
    goodsServices = models.TextField()
    logo = models.ImageField(upload_to='logos/')
    
    # Results
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    feedback = models.TextField(blank=True)
    euipoResults = models.TextField(blank=True)
    wipoResults = models.TextField(blank=True)
    sipoResults = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.brandName} - {self.status}"
