from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission
from django.utils.crypto import get_random_string


class User(AbstractUser):
    ROLES = (
        ('BO', 'Business Owner'),
        ('AC', 'Assignment Client'),
        ('AD', 'Assignment Doer'),
    )
    role = models.CharField(max_length=2, choices=ROLES)
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20, unique=True)
    address = models.TextField()
    ratings = models.PositiveIntegerField(default=0)
    nickname = models.CharField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        if not self.nickname:
            # Generate a random animal name ending with digits
            animal = get_random_string(length=6, allowed_chars='abcdefghijklmnopqrstuvwxyz')
            digits = get_random_string(length=2, allowed_chars='0123456789')
            self.nickname = f"{animal}-{digits}"
        return super().save(*args, **kwargs)


class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    subject = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=50)
    client = models.ForeignKey(User, related_name='client_assignments', on_delete=models.CASCADE)
    doer = models.ForeignKey(User, related_name='doer_assignments', null=True, blank=True, on_delete=models.SET_NULL)


class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    doer = models.ForeignKey(User, related_name='bids', on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, related_name='bids', on_delete=models.CASCADE)


class Order(models.Model):
    STATUS_CHOICES = (
        ('P', 'Pending'),
        ('IP', 'In Progress'),
        ('C', 'Completed'),
    )
    client = models.ForeignKey(User, related_name='client_orders', on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, related_name='assignment_orders', on_delete=models.CASCADE)
    doer = models.ForeignKey(User, related_name='doer_orders', null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES)
    payment_info = models.TextField()


class Review(models.Model):
    client = models.ForeignKey(User, related_name='client_reviews', on_delete=models.CASCADE)
    doer = models.ForeignKey(User, related_name='doer_reviews', on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comments = models.TextField()


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


# Add the related_name arguments for the groups and user_permissions fields
User.groups.related_name = 'custom_user_set'
User.user_permissions.related_name = 'custom_user_permissions'