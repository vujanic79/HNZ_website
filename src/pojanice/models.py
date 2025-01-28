from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify


def unique_slug_generator(instance, slug_field):
    slug = slugify(slug_field)
    model_class = instance.__class__
    counter = 1
    original_slug = slug
    
    while model_class.objects.filter(slug=slug).exists():
        slug = f"{original_slug}-{counter}"
        counter += 1
        
    return slug


class PojanicaPostQuerySet(models.QuerySet):
	def search(self, query):
		lookup = (
			Q(title__icontains=query)|
			Q(broj__icontains=query)
			)
		return self.filter(lookup)


class PojanicaPostManager(models.Manager):
	def get_queryset(self):
		return PojanicaPostQuerySet(self.model, using=self._db)

	def search(self, query=None):
		if query is None:
			return self.get_queryset().none()
		return self.get_queryset().search(query)



class Pojanica(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    godina_izdanja = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
    	return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self, self.name)
        super().save(*args, **kwargs)

class ListaPojanja(models.Model):
    broj = models.CharField(max_length=255,blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    folder = models.ForeignKey(Pojanica, related_name='pojanica',blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
    	return f"{self.folder.name} - {self.broj}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self, self.broj)
        super().save(*args, **kwargs)

	
class Pojanje(models.Model):
	pojanje = models.ForeignKey(ListaPojanja, related_name='texts', on_delete=models.CASCADE, default=1)  # Provide a default value
	title = models.CharField(max_length=255, blank=True, null=True)
	broj = models.CharField(max_length=255,blank=True, null=True)
	slug = models.SlugField(unique=True, blank=True, null=True)
	file = models.FileField(upload_to='files/pojanice/',blank=True, null='')
	audio = models.FileField(upload_to='audio/citanje/',blank=True, null='')
	skracenica = models.CharField(max_length=255,blank=True, null=True)

	objects = PojanicaPostManager()
	
	def __str__(self):
		return f"{self.pojanje.folder.name} {self.broj} {self.title}"

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = unique_slug_generator(self, self.title)
		super().save(*args, **kwargs)



class StaraPojanicaFolder(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    izdanje = models.CharField(max_length=255, blank=True, null=True)
    godina_izdanja = models.CharField(max_length=255, blank=True, null=True)
    jezik = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
    	return f"{self.name} {self.godina_izdanja}" 

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self,  f"{self.name} {self.godina_izdanja}")
        super().save(*args, **kwargs)


class StaraPojanica(models.Model):
	pojanje = models.ForeignKey(StaraPojanicaFolder, related_name='texts', on_delete=models.CASCADE, default=1)  # Provide a default value
	title = models.CharField(max_length=255, blank=True, null=True)
	slug = models.SlugField(unique=True, blank=True, null=True)
	file = models.FileField(upload_to='files/pojanice/',blank=True, null='')

	def __str__(self):
		return f"{self.pojanje.name} {self.pojanje.godina_izdanja}"

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = unique_slug_generator(self, self.pojanje.godina_izdanja)
		super().save(*args, **kwargs)
