from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify

User = settings.AUTH_USER_MODEL

def unique_slug_generator(instance, slug_field):
    slug = slugify(slug_field)
    model_class = instance.__class__
    counter = 1
    original_slug = slug
    
    while model_class.objects.filter(slug=slug).exists():
        slug = f"{original_slug}-{counter}"
        counter += 1
        
    return slug


class FolderSluzbe(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
    	return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self, self.name)
        super().save(*args, **kwargs)

	

class SluzbaPostQuerySet(models.QuerySet):
	def published(self):
		now = timezone.now()
		return self.filter(publish_date__lte=now)

	def search(self, query):
		lookup = (
			Q(title__icontains=query)|
			Q(content__icontains=query)|
			Q(glava__icontains=query)|
			Q(tema__icontains=query)|
			Q(publish_date__icontains=query)
			)
		return self.filter(lookup)


class SluzbaPostManager(models.Manager):
	def get_queryset(self):
		return SluzbaPostQuerySet(self.model, using=self._db)

	def published(self):
		return self.get_queryset().published()

	def search(self, query=None):
		if query is None:
			return self.get_queryset().none()
		return self.get_queryset().published().search(query)


class SluzbaPost(models.Model):
	user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
	audio = models.FileField(upload_to='audio/sluzbe/',blank=True, null='')
	title = models.CharField(max_length=120,blank=True, null=True)
	glava = models.CharField(max_length=120,blank=True, null=True)
	tema = models.CharField(max_length=120,blank=True, null=True)
	slug = models.SlugField(unique=True,blank=True, null=True)
	content = models.TextField(null=True,blank=True)
	publish_date = models.DateField(auto_now=False, auto_now_add=False, null=True,blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	folder = models.ForeignKey(FolderSluzbe, related_name='sluzbe',blank=True, null=True, on_delete=models.CASCADE)

	objects = SluzbaPostManager()

	def save(self, *args, **kwargs):
		if not self.slug:
			# Generate the initial slug
			original_slug = slugify(self.title)
			slug = original_slug
			# Check for existing slugs and append a number if necessary
			num = 1
			while SluzbaPost.objects.filter(slug=slug).exists():
				slug = f"{original_slug}-{num}"
				num += 1
			self.slug = slug
		super(SluzbaPost, self).save(*args, **kwargs)
    
	def __str__(self):
		return self.title

	class Meta:
		ordering = ['-publish_date','-updated','-timestamp']

	def get_absolute_url(self):
		return f"/sluzbe/{self.slug}"

	def get_edit_url(self):
		return f"/sluzbe/{self.slug}/edit"

	def get_delete_url(self):
		return f"/sluzbe/{self.slug}/delete"


class PojanjaPostQuerySet(models.QuerySet):
	def search(self, query):
		lookup = (
			Q(title__icontains=query)|
			Q(album__icontains=query)
			)
		return self.filter(lookup)


class PojanjaPostManager(models.Manager):
	def get_queryset(self):
		return PojanjaPostQuerySet(self.model, using=self._db)

	def search(self, query=None):
		if query is None:
			return self.get_queryset().none()
		return self.get_queryset().search(query)


class Folder(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    language = models.CharField(max_length=120,blank=True, null=True)

    def __str__(self):
    	return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self, self.name)
        super().save(*args, **kwargs)

	
class PojanjaPost(models.Model):
	user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
	audio = models.FileField(upload_to='audio/pojanja/',blank=True, null='')
	title = models.CharField(max_length=120,blank=True, null=True)
	album = models.CharField(max_length=120,blank=True, null=True)
	artist = models.CharField(max_length=120,blank=True, null=True)
	folder = models.ForeignKey(Folder, related_name='songs',blank=True, null=True, on_delete=models.CASCADE)
	
	objects = PojanjaPostManager()

	def __str__(self):
		return self.title

	class Meta:
		ordering = ['album','title']




