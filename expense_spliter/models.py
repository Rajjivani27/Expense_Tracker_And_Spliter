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

class Friends(models.Model):
    friends_one = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="friends_one")
    friends_two = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="friends_two")
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.friends_one.username} and {self.friends_two.username} are friends"

class FriendRequest(models.Model):
    requester = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="friend_requsted")
    requested = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="friend_requests")
    status = models.CharField(choices=status_choices,default="pending")

    def __str__(self):
        return f"{self.requester.username} request to be friend with {self.requested.username}"

@receiver(signal=[post_save],sender=FriendRequest)
def request_creator(sender,instance,created,*args,**kwargs):
    if not created:
        if instance.status == "friends":
            Friends.objects.create(instance.requester,instance.requested)
        else:
            print("Here")
            instance.delete()

        

# Create your models here.
