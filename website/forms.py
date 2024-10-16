from django import forms
from website.models import Contact, Newsletter
from captcha.fields import CaptchaField

class NameForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    subject = forms.CharField(max_length=255)
    message = forms.CharField(widget=forms.Textarea)


class ContactForm(forms.ModelForm):
    captcha = CaptchaField()
    #  last_name = forms.CharField(max_length=255)
    class Meta:
        model = Contact
        fields = '__all__'

    def save(self, commit=True):
        instance = super(ContactForm, self).save(commit=False)
        instance.name = 'Anonymous'
        if commit:
            instance.save()
        return instance

        
class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = '__all__'


