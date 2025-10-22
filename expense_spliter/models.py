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
    added_friends = models.ManyToManyField(CustomUser,related_name="added_friends")

class OutgoingRequests(models.Model):
    friend_to_be = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    requester = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="outgoing_requests")
    time = models.DateTimeField(auto_now_add=True)

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

    def __str__(self):
        return f"{self.person1} <-> {self.person2}"

@receiver([post_save],sender=IncomingRequests)
@transaction.atomic
def incoming_friend_request(sender,instance,created,*args,**kwargs):
    if not created:
        try:
            person1 = instance.requester
            person2 = instance.accepting_person
            if instance.accepted == True:
                Friends.objects.create(person1=person1,person2=person2)
                request = OutgoingRequests.objects.get(requester=person1,friend_to_be=person2)

                instance.delete()
                request.delete()
            elif instance.rejected == True:
                request = OutgoingRequests.objects.get(requester=person1,friend_to_be=person2)
                request.delete()
                instance.delete()
        except Exception as E:
            raise E


# Create your models here.
