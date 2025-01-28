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

class StariZavetQuerySet(models.QuerySet):
    def search(self, query):
        lookup = (
            Q(content__icontains=query)
            )
        return self.filter(lookup)


class StariZavetManager(models.Manager):
    def get_queryset(self):
        return StariZavetQuerySet(self.model, using=self._db)

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().search(query)


class StariZavetKnjige(models.Model):
    name = models.CharField(max_length=255)
    broj_glava = models.IntegerField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
    	return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self, self.name)
        super().save(*args, **kwargs)

class StariZavetGlave(models.Model):
    knjiga = models.ForeignKey(
        StariZavetKnjige, 
        related_name='glave', 
        on_delete=models.CASCADE,
        default=1
    )
    slug = models.SlugField(unique=True, blank=True, null=True)
    name = models.CharField(max_length=120,blank=True, null=True)  # Adding a non-nullable field

    def __str__(self):
        return f"{self.knjiga.name} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self, self.name)
        super().save(*args, **kwargs)

class StariZavetText(models.Model):
    glava = models.ForeignKey(StariZavetGlave, related_name='texts', on_delete=models.CASCADE, default=1)  # Provide a default value
    content = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    audio = models.FileField(upload_to='audio/citanje/',blank=True, null='')
    
    objects = StariZavetManager()

    def __str__(self):
        return f"{self.glava.knjiga.name} {self.glava.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self, self.glava.name)
        super().save(*args, **kwargs)

class NoviZavetQuerySet(models.QuerySet):
    def search(self, query):
        lookup = (
            Q(content__icontains=query)
            )
        return self.filter(lookup)


class NoviZavetManager(models.Manager):
    def get_queryset(self):
        return NoviZavetQuerySet(self.model, using=self._db)

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().search(query)

class NoviZavetKnjige(models.Model):
    name = models.CharField(max_length=255)
    broj_glava = models.IntegerField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
    	return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self, self.name)
        super().save(*args, **kwargs)

class NoviZavetGlave(models.Model):
    knjiga = models.ForeignKey(
        NoviZavetKnjige, 
        related_name='glave', 
        on_delete=models.CASCADE,
        default=1
    )
    slug = models.SlugField(unique=True, blank=True, null=True)
    name = models.CharField(max_length=120,blank=True, null=True)  # Adding a non-nullable field

    def __str__(self):
        return f"{self.knjiga.name} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self, self.name)
        super().save(*args, **kwargs)

class NoviZavetText(models.Model):
    glava = models.ForeignKey(NoviZavetGlave, related_name='texts', on_delete=models.CASCADE, default=1)  # Provide a default value
    content = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    audio = models.FileField(upload_to='audio/citanje/',blank=True, null='')

    objects = NoviZavetManager()

    def __str__(self):
        return f"{self.glava.knjiga.name} {self.glava.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self, self.glava.name)
        super().save(*args, **kwargs)