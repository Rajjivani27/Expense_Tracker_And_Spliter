from django.db import models
from django.db.models.signals import post_save
from django.db import transaction
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
    added_friends_new = models.ManyToManyField(CustomUser,related_name="added_friends")


class FriendRequest(models.Model):
    requester = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="sent_requests")
    accepting_person = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="received_requests")
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    sent_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.requester} -> {self.accepting_person}"

class Friends(models.Model):
    person1 = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="friends_1")
    person2 = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="friends_2")

    def __str__(self):
        return f"{self.person1} <-> {self.person2}"
    
@receiver(signal=[post_save],sender=FriendRequest)
def friend_request_accepted_or_rejected(sender,instance,created,*args,**kwargs):
    if not created:
        if instance.accepted == True:
            Friends.objects.create(person1=instance.requester,person2=instance.accepting_person)
            instance.delete()
        elif instance.rejected == True:
            instance.delete()

# Create your models here.
