from django import forms
from .models import SluzbaPost


class SluzbaPostForm(forms.Form):
	title = forms.CharField()
	slug = forms.SlugField()
	content = forms.CharField(widget = forms.Textarea)


class SluzbaPostModelForm(forms.ModelForm):
	class Meta:
		model = SluzbaPost
		fields = ['title','audio','slug','content','publish_date']

	def clean_title(self, *args, **kwargs):
		instance = self.instance
		title = self.cleaned_data.get('title')
		qs = SluzbaPost.objects.filter(title__iexact=title)
		if instance is not None:
			qs =qs.exclude(pk = instance.pk)
		if qs.exists():
			raise forms.ValidationError("This title already exists!")
		return title