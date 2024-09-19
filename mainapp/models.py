from django.db import models

# Create your models here.

class Order(models.Model):
    product = models.CharField(max_length=100)
    quantity = models.IntegerField()
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    address = models.TextField()
    id_photo = models.ImageField(upload_to='id_photos/')
    id_signature = models.ImageField(upload_to='id_signatures/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.product}"
