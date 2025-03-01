from django import forms
from page.models import User

class workshopRegistrationForm(forms.ModelForm):    
    class Meta:
        model = User
        fields = ['encurso_id', 'workshop', 'accommodation', 'food']

class Basicform(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone', 'institute','gender','dob','branch','home_town','institute_place']

class eventRegistrationForm(forms.ModelForm):    
    class Meta:
        model = User
        fields = ['encurso_id', 'event', 'accommodation', 'food']


