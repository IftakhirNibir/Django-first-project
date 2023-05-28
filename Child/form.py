from django.db.models import fields
from django.forms import ModelForm
from .models import *
from django import forms

class DiscussionForm(ModelForm):
    class Meta:
        model = Discussion
        fields = ['topic','name','description','more']

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']

class HelpForm(forms.ModelForm):
	class Meta:
		model = Help
		fields = '__all__'

class OrderForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ['status','payment_status']

class BForm(forms.ModelForm):
	class Meta:
		model = BkashPayment
		fields = ['name','address','option','product_name_and_quentity','bkashNumber','Transaction_ID']

		widgets = {
		   'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Write your name here' }),
		   'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Write your current address here' }),
		   'option': forms.Select(attrs={'class': 'form-control' }),
		   'product_name_and_quentity': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Write your product name and quentity here or leave it blank' }),
		   'bkashNumber' : forms.TextInput(attrs ={'class': 'form-control', 'placeholder':'Write your bkash number here' }),
		   'Transaction_ID' : forms.TextInput(attrs ={'class': 'form-control', 'placeholder':'Write your transaction ID here' }),
		}

class NForm(forms.ModelForm):
	class Meta:
		model = NagadPayment
		fields = ['name','address','option','product_name_and_quentity','nagadNumber','Transaction_ID']

		widgets = {
		   'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Write your name here' }),
		   'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Write your current address here' }),
		   'option': forms.Select(attrs={'class': 'form-control' }),
		   'product_name_and_quentity': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Write your product name and quentity here or leave it blank' }),
		   'nagadNumber' : forms.TextInput(attrs ={'class': 'form-control', 'placeholder':'Write your bkash number here' }),
		   'Transaction_ID' : forms.TextInput(attrs ={'class': 'form-control', 'placeholder':'Write your transaction ID here' }),
		}

class SchoolForm(ModelForm):
	class Meta:
		model = Schooldetails
		fields = ['childname','district','school','contact_no']

		widgets = {
		   'childname' : forms.TextInput(attrs ={'class': 'form-control','placeholder':'Enter children name here'}),
           'district' : forms.Select(attrs ={'class': 'form-control'}),
		   'school' : forms.Select(attrs ={'class': 'form-control' }),
		   'contact_no' : forms.TextInput(attrs ={'class': 'form-control','placeholder':'Write your contact number here'}),
		}

	def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.fields['school'].queryset = School.objects.none()

			if 'school' in self.data:  #If address is request.POST
				try:
					district_id = int(self.data.get('district')) #Fetch Address ID
					self.fields['school'].queryset = School.objects.filter(district_id=district_id).order_by('name')
				except (ValueError, TypeError):
					pass  # invalid input from the client; ignore and fallback to empty School queryset
			elif self.instance.pk:
				self.fields['school'].queryset = self.instance.district.school_set.all()

	