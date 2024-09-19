from django.db import models

# Create your models here.

class Order(models.Model):
    quantity = models.IntegerField(default=1)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.CharField(max_length=10)
    state = models.CharField(max_length=2)
    height_feet = models.IntegerField()
    height_inches = models.IntegerField()
    weight = models.IntegerField()
    eyes = models.CharField(max_length=20)
    hair = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    address1 = models.TextField(blank=True)
    address2 = models.TextField(blank=True)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    picture = models.ImageField(upload_to='id_photos/')
    signature = models.ImageField(upload_to='signatures/', blank=True)
    additional = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
