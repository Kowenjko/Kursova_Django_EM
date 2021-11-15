from django import forms
from django.db import models
from django.forms.widgets import Select
from apps.shop.models import Product,Category,Brand
from django.forms import ModelForm, TextInput,Select,FileInput,Textarea,NumberInput,CheckboxInput,ClearableFileInput,CharField
from django import forms

class CategoryForm(ModelForm):
    # slug = SlugFormField(populate_from='name')

    class Meta:
        model = Category
        fields = ['name','slug']
        widgets = {
            'name': TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter...',              
            }),
            'slug': TextInput(attrs={
                'class':'form-control',   
                'value':'slug',                          
                'slug': forms.HiddenInput()                              
            }),
        }
class BrandForm(ModelForm):

    class Meta:
        model = Brand
        fields = ['name','slug']
        widgets = {
            'name': TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter...',
              
            }),
            'slug': TextInput(attrs={
                'class':'form-control',  
                'value':'slug',                            
                'slug': forms.HiddenInput()                              
            }),
        }

class ProductForm(ModelForm):
    
    class Meta:
        model = Product
        fields = ['category','brand','name','slug','main_photo','photo_1','photo_2','photo_3','description','details','price','old_price','stock','available','rait']

        widgets={
            'category': Select(attrs={
                'class':'form-control',
                
            }),
            'brand': Select(attrs={
                'class':'form-control',
                
            }),
            'name': TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter...',
              
            }),
            'slug': TextInput(attrs={
                'class':'form-control',
                'value':'slug',                          
                'slug': forms.HiddenInput() 
                              
            }),
            'main_photo': ClearableFileInput(attrs={
                'class':'custom-file-input',
                'id':"exampleInputFile",
                 'name':"main_photo"               
            }),
            'photo_1': ClearableFileInput(attrs={
                'class':'custom-file-input',
                'id':"exampleInputFile",
                'name':"photo_1"                 
            }),
            'photo_2': ClearableFileInput(attrs={
                'class':'custom-file-input',
                'id':"exampleInputFile" ,
                'name':"photo_2"                
            }),
            'photo_3': ClearableFileInput(attrs={
                'class':'custom-file-input',
                'id':"exampleInputFile" ,
                'name':"photo_3"                
            }),
            'description': Textarea(attrs={
                'class':"form-control",
                 'rows':"3", 
                 'placeholder':'Enter...',                               
            }),
            'details': Textarea(attrs={
                'class':"form-control",
                 'rows':"3", 
                 'placeholder':'Enter...',                               
            }),
            'price': NumberInput(attrs={
                'class':"form-control",                 
                 'placeholder':0,                               
            }),
            'old_price': NumberInput(attrs={
                'class':"form-control",                 
                 'placeholder':0,                               
            }),
            'stock': NumberInput(attrs={
                'class':"form-control",                 
                 'placeholder':0,                               
            }),
            'available': CheckboxInput(attrs={
                'class':"custom-control-input",
                  'id':"customCheckbox2"                                             
            }),
            'rait': NumberInput(attrs={
                'class':"form-control",                 
                 'placeholder':0,                               
            }),


        }

