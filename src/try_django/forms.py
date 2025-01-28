from django import forms




class ContactForm(forms.Form):
    full_name = forms.CharField(
    	label='Ime i Prezime',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ime i Prezime'})
    )
    email = forms.EmailField(
    	label='Email adresa',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email adresa'})
    )
    content = forms.CharField(
    	label='Poruka',
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Poruka', 'rows': 6})
    )