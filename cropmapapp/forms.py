from django import forms
from django.contrib.auth.models import User

from .models import Image, CroppingImage, CroppingData, Data, CroppingDataDetail, Comparison

class ImageForm(forms.ModelForm):
	image_name = forms.CharField(max_length = 512,widget=forms.TextInput(attrs={'class':"form-control"}))
	image_description = forms.CharField(max_length = 512,widget=forms.Textarea(attrs={'class':"form-control"}))
   
	class Meta:
		model = Image
		fields = ['image_name', 'image_raw', 'image_description']
		
class CroppingForm(forms.ModelForm):
	surveying_area = forms.CharField(max_length = 512,widget=forms.TextInput(attrs={'class':"form-control"}))
	address = forms.CharField(max_length = 512,widget=forms.TextInput(attrs={'class':"form-control"}))
	land_description = forms.CharField(max_length = 512,widget=forms.Textarea(attrs={'class':"form-control"}))
	class Meta:
		model = CroppingImage
		fields = ['surveying_area', 'image_raw', 'address', 'land_description']


class CroppingDataForm(forms.ModelForm):
	croppingdate = forms.DateField(widget=forms.DateInput(format='%m/%d/%Y', attrs={'class':"form-control", 'placeholder':'mm/dd/yyyy'}),input_formats=('%m/%d/%Y',))
	description = forms.CharField(max_length = 512,widget=forms.Textarea(attrs={'class':"form-control"}))
	class Meta:
		model = CroppingData
		fields = ['cropping', 'croppingdate', 'description']


class UserForm(forms.ModelForm):
    password = forms.CharField(max_length = 254,widget=forms.PasswordInput(attrs={'class':"form-control"}))
    confirm_password = forms.CharField(max_length = 254,widget=forms.PasswordInput(attrs={'class':"form-control"}))
    username = forms.CharField(max_length = 254,widget = forms.TextInput(attrs={'class':"form-control"}))
    email = forms.EmailField(max_length = 254,widget = forms.TextInput(attrs={'class':"form-control"}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
    	cleaned_data = super(UserForm, self).clean()
    	password = cleaned_data.get("password")
    	confirm_password = cleaned_data.get("confirm_password")

    	if password != confirm_password:
    		self.add_error('password',"The two passwords do not match.")
    		return cleaned_data


class DataForm(forms.ModelForm):
	class Meta:
		model = Data
		fields = ['raw', 'ndvi', 'osavi', 'ndvi_4x4', 'osavi_4x4', 'graph', 'ndvipiegraph', 'osavipiegraph']

class CroppingDataDetailForm(forms.ModelForm):
	class Meta:
		model = CroppingDataDetail
		fields = ['raw', 'ndvi', 'osavi', 'ndvi_4x4', 'osavi_4x4', 'graph', 'ndvipiegraph', 'osavipiegraph']


class ComparisonForm(forms.ModelForm):
	class Meta:
		model = Comparison
		fields = ['raw', 'croppingdate', 'description', 'graph', 'ndvipiegraph', 'osavipiegraph']
