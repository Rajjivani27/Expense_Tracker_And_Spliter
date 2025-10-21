from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.dispatch import receiver
from expense_tracker.models import *

status_choices = [
    ("not_friend","NOT FRIENDS"),
    ("pending","PENDING"),
    ("accepted","ACCEPTED")
]

class Spliter(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="spliter")
    amount = models.IntegerField()
    added_friends = models.ManyToManyField(CustomUser,related_name="added_friends")

class OutgoingRequests(models.Model):
    friend_to_be = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    requester = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="outgoing_requests")
    time = models.DateTimeField(auto_now_add=True)
    delete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.requester} -> {self.friend_to_be}"

class IncomingRequests(models.Model):
    requester = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    accepting_person = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="friend_requests")
    time = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    rejected  = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.accepting_person} <- {self.requester}"

class Friends(models.Model):
    person1 = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="friends_1")
    person2 = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="friends_2")
# Create your models here.
