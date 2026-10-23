import re
from django import forms
from .models import Supplier, Restaurant, Food, Agents, Customer, OrderDetails, Feedback, OrderItem


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['supplier_name']
        widgets = {
            'supplier_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter supplier or distributor name (e.g., FreshFarm Supplies)'
            }),
        }

    def clean_supplier_name(self):
        name = self.cleaned_data.get('supplier_name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError("Supplier name must be at least 2 characters long.")
        return name


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['restaurant_name', 'restaurant_ph_no', 'restaurant_adrs', 'rating', 'supplier']
        widgets = {
            'restaurant_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Spice Garden Bistro'}),
            'restaurant_ph_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 9876543210'}),
            'restaurant_adrs': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 42 MG Road, Bangalore'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '5', 'placeholder': '4.5'}),
            'supplier': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_restaurant_ph_no(self):
        ph = self.cleaned_data.get('restaurant_ph_no', '').strip()
        if not re.match(r'^[0-9+\-\s]{7,15}$', ph):
            raise forms.ValidationError("Please enter a valid phone number (7-15 digits).")
        return ph


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['food_name', 'food_price', 'food_rating', 'restaurant']
        widgets = {
            'food_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Paneer Butter Masala'}),
            'food_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01', 'placeholder': '249.00'}),
            'food_rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '5', 'placeholder': '4.8'}),
            'restaurant': forms.Select(attrs={'class': 'form-select'}),
        }


class AgentsForm(forms.ModelForm):
    class Meta:
        model = Agents
        fields = ['agent_name', 'agent_ph_number', 'supplier']
        widgets = {
            'agent_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Rahul Sharma'}),
            'agent_ph_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 9123456780'}),
            'supplier': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_agent_ph_number(self):
        ph = self.cleaned_data.get('agent_ph_number', '').strip()
        if not re.match(r'^[0-9+\-\s]{7,15}$', ph):
            raise forms.ValidationError("Please enter a valid phone number (7-15 digits).")
        return ph


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['cust_name', 'cust_adrs', 'cust_ph_no']
        widgets = {
            'cust_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Amit Patel'}),
            'cust_adrs': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Flat 302, Green Park'}),
            'cust_ph_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 9898989898'}),
        }

    def clean_cust_ph_no(self):
        ph = self.cleaned_data.get('cust_ph_no', '').strip()
        if not re.match(r'^[0-9+\-\s]{7,15}$', ph):
            raise forms.ValidationError("Please enter a valid phone number (7-15 digits).")
        return ph


class OrderDetailsForm(forms.ModelForm):
    class Meta:
        model = OrderDetails
        fields = ['customer', 'supplier', 'order_date', 'quantity', 'price']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'supplier': forms.Select(attrs={'class': 'form-select'}),
            'order_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'placeholder': '1'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01', 'placeholder': '0.00'}),
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['customer', 'rating', 'message', 'feedback_date']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'rating': forms.Select(
                choices=[(5, '★★★★★ (5 Stars - Excellent)'),
                         (4, '★★★★☆ (4 Stars - Very Good)'),
                         (3, '★★★☆☆ (3 Stars - Average)'),
                         (2, '★★☆☆☆ (2 Stars - Below Average)'),
                         (1, '★☆☆☆☆ (1 Star - Poor)')],
                attrs={'class': 'form-select'}
            ),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Share customer review or experience...'}),
            'feedback_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
