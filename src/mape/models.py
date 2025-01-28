from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify

User = settings.AUTH_USER_MODEL

class Mesto(models.Model):
	mesto = models.CharField(max_length=120,blank=True, null=True)
	adresa = models.CharField(max_length=120,blank=True, null=True)
	fotografija = models.ImageField(upload_to='skupstine/', null=True, blank=True)
	opis = models.TextField(blank=True, null=True)
	attenders = models.IntegerField(blank=True, null=True)
	lat = models.FloatField(blank=True, null=True)
	lon = models.FloatField(blank=True, null=True)
	status = models.CharField(max_length=120,blank=True, null=True)

	def __str__(self):
		return self.mesto