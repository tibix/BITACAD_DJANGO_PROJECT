from django import forms

class ContactForm(forms.Form):
  contact_name = forms.CharField(required=True)
  contact_email = forms.EmailField(required=True)
  content = forms.CharField(required=True,  widget=forms.Textarea )


from produse.models import Useri


class UserForm(forms.ModelForm):
  class Meta:
    model = Useri
    fields = ['poza', 'email', 'adresa', 'telefon']