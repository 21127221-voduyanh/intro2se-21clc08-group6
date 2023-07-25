from django import forms
from app.models import Job_finder,Employer, Comment, Post

class EUpdateForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['company_name', 'address', 'city', 'introduction']

class JFUpdateForm(forms.ModelForm):
    class Meta:
        model = Job_finder
        fields = ['full_name','gender','address', 'city', 'introduction']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Write a comment'}),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['pic_url', 'caption','contact', 'address', 'job', 'description', 'hour', 'salary']