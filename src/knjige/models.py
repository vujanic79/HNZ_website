from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
# Create your models here.

def unique_slug_generator(instance, slug_field):
    slug = slugify(slug_field)
    model_class = instance.__class__
    counter = 1
    original_slug = slug
    
    while model_class.objects.filter(slug=slug).exists():
        slug = f"{original_slug}-{counter}"
        counter += 1
        
    return slug


class KnjigeQuerySet(models.QuerySet):
	def search(self, query):
		lookup = (
			Q(title__icontains=query)|
			Q(opis__icontains=query)
			)
		return self.filter(lookup)


class KnjigeManager(models.Manager):
	def get_queryset(self):
		return KnjigeQuerySet(self.model, using=self._db)

	def search(self, query=None):
		if query is None:
			return self.get_queryset().none()
		return self.get_queryset().search(query)



class Knjiga(models.Model):
	knjiga = models.FileField(upload_to='files/knjige/',blank=True, null='')
	title = models.CharField(max_length=120,blank=True, null=True)
	slug = models.SlugField(unique=True,blank=True, null=True)
	opis = models.TextField(null=True,blank=True)
	where_to_buy_link = models.CharField(max_length=120,blank=True, null=True)
	kontakt_za_porudzbine = models.CharField(max_length=140,blank=True, null=True)
	broj_telefona_porudzbine = models.CharField(max_length=140,blank=True, null=True)
	
	objects = KnjigeManager()

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = unique_slug_generator(self, self.title)
		super().save(*args, **kwargs)

	def get_absolute_url(self):
		return f"/knjige-i-spisi/{self.slug}"