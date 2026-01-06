from django import forms

from .models import Product


class ProductForm(forms.ModelForm) :

    class Meta :

        model = Product

        exclude = ['uuid','active_status']

        widgets = {

            'name' : forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Product Name'}),

            'photo' : forms.FileInput(attrs={'class':'form-control'}),

            'description' : forms.Textarea(attrs={'class':'form-control','rows':3,'placeholder':'Enter Product Description'}),

            'price' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Price'}),

            'rating' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Rating (0 - 5)','step':'0.1'}),

            'quantity' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Available Quantity'}),

            'category' : forms.TextInput(attrs={'class':'form-control','placeholder':'Eg: Shoes, Bat, Jersey'}),

            'brand' : forms.TextInput(attrs={'class':'form-control','placeholder':'Brand Name'}),

            'weight' : forms.TextInput(attrs={'class':'form-control','placeholder':'Eg: 500g, 1kg'}),

            'colour' : forms.TextInput(attrs={'class':'form-control','placeholder':'Product Colour'}),

            'sport' : forms.TextInput(attrs={'class':'form-control','placeholder':'Eg: Football, Cricket'}),

            'material' : forms.TextInput(attrs={'class':'form-control','placeholder':'Eg: Leather, Plastic'}),

        }


    def clean_rating(self) :

        rating = self.cleaned_data.get('rating')

        if rating < 0 or rating > 5 :

            raise forms.ValidationError('Rating must be between 0 and 5')

        return rating
