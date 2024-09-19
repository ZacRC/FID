from django.db import models
from django.contrib.auth.models import User

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
    tracking_number = models.CharField(max_length=20, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Group(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    creator_member_id = models.CharField(max_length=8)

    def __str__(self):
        return f"Group {self.id}"

class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='members')
    name = models.CharField(max_length=50)
    member_id = models.CharField(max_length=8, unique=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    order_info_completed = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)  # New field

    class Meta:
        unique_together = ('group', 'name')

    def __str__(self):
        return f"{self.name} in {self.group}"

class GroupMemberOrderInfo(models.Model):
    member = models.OneToOneField(GroupMember, on_delete=models.CASCADE, related_name='order_info')
    quantity = models.IntegerField(default=1)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.CharField(max_length=10)
    state = models.CharField(max_length=2)
    height_feet = models.IntegerField(null=True, blank=True, default=0)
    height_inches = models.IntegerField(null=True, blank=True, default=0)
    weight = models.IntegerField(null=True, blank=True, default=0)
    eyes = models.CharField(max_length=20)
    hair = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    address1 = models.TextField(blank=True)
    address2 = models.TextField(blank=True)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    picture = models.ImageField(upload_to='group_id_photos/')
    signature = models.ImageField(upload_to='group_signatures/', blank=True)
    additional = models.TextField(blank=True)

    def __str__(self):
        return f"Order info for {self.member.name}"

class VenmoPayment(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    member = models.ForeignKey(GroupMember, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=20)
    screenshot = models.ImageField(upload_to='venmo_screenshots/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Venmo payment for {self.member.name} in {self.group}"
    
class IndividualVenmoPayment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    venmo_order_id = models.CharField(max_length=20)
    screenshot = models.ImageField(upload_to='individual_venmo_screenshots/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Individual Venmo payment for Order {self.order.id}"