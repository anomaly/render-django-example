# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Allows us to extend the default user model to add application specific
    behaviour.

    See the following guide where it's easier to abstract user at the start
    of the project:

    https://docs.djangoproject.com/en/6.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
    """

    pass
