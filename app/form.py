from django import forms
from app.models import Job_finder,Employer

class EUpdateForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['company_name', 'user', 'address', 'city', 'introduction']

class JFUpdateForm(forms.ModelForm):
    class Meta:
        model = Job_finder
        fields = ['user', 'address', 'city', 'introduction']
