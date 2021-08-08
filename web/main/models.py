from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from .managers import UserManager


class UserClient(models.Model):
    user_id = models.IntegerField(unique=True)
    last_read_date = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def read(self):
        self.last_read_date = timezone.now()
        self.save(update_fields=('last_read_date', ))

    def __str__(self):
        return f'user_id-{self.user_id}'


class User(AbstractUser):
    username = None
    email = models.EmailField(_('Email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def get_user_groups(self):
        return mark_safe("<br/>".join([p.name for p in self.groups.all()]))

    def __str__(self):
        return self.email

