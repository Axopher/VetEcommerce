from django.db.models.signals import post_save,post_delete

from django.contrib.auth.models import User
from store.models import Customer




def createCutomer(sender,instance,created,**kwargs):
    if created:
        user = instance
        customer = Customer.objects.create(
            user=user,
            username=user.username,
            email=user.email,
        )


def deleteUser(sender,instance,**kwargs):
    # print("delete signal triggered")
    user = instance.user
    user.delete() 

post_save.connect(createCutomer,sender=User)
post_delete.connect(deleteUser,sender=Customer)