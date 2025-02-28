from django.db import models

class BrandCheck(models.Model):
    id = models.AutoField(primary_key=True)
    brandName = models.CharField(max_length=255, blank=True, null=True)
    goodsServices = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='brand_logos/', blank=True, null=True)  # Or FileField if non-image
    euipoResults = models.TextField(null=True, blank=True)
    wipoResults = models.TextField(null=True, blank=True)
    sipoResults = models.TextField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.brandName