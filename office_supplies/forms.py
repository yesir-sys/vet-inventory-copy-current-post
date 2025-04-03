import csv
import io
from django import forms
from datetime import datetime
from .models import OfficeSupply, OfficeMassOutgoing, OfficeMassOutgoingItem

class OfficeSupplyForm(forms.ModelForm):
    class Meta:
        model = OfficeSupply
        fields = ['name', 'category', 'quantity', 'reorder_level', 'expiration_date', 'description']
        widgets = {
            'expiration_date': forms.DateInput(attrs={'type': 'date'}),
            'reorder_level': forms.NumberInput(attrs={'min': 1}),
            'quantity': forms.NumberInput(attrs={'min': 0}),
        }
        labels = {
            'name': 'Item Name',
            'category': 'Category',
            'quantity': 'Quantity',
            'reorder_level': 'Reorder Level',
            'expiration_date': 'Expiration Date',
            'description': 'Description'
        }

class OfficeMassOutgoingForm(forms.Form):
    reason = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        required=True,
        label='Reason for Outgoing'
    )

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('reason'):
            raise forms.ValidationError('Reason is required')
        return cleaned_data

class OfficeMassOutgoingItemForm(forms.Form):
    supply = forms.ModelChoiceField(
        queryset=OfficeSupply.objects.all(),
        required=True,
        label='Item',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    quantity = forms.IntegerField(
        min_value=1,
        required=True,
        label='Quantity',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1'})
    )

    def clean(self):
        cleaned_data = super().clean()
        supply = cleaned_data.get('supply')
        quantity = cleaned_data.get('quantity')

        if supply and quantity:
            if quantity > supply.quantity:
                raise forms.ValidationError({
                    'quantity': f'Not enough stock. Only {supply.quantity} available.'
                })
        return cleaned_data

OfficeMassOutgoingItemFormSet = forms.formset_factory(
    OfficeMassOutgoingItemForm,
    extra=1,
    min_num=1,
    validate_min=True,
    can_delete=True
)

class MassAddForm(forms.Form):
    csv_file = forms.FileField(
        label='Select CSV file',
        help_text='Must be a CSV file with expiry dates in DD/MM/YYYY format (e.g., 31/12/2025)'
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False
    )

    def clean_csv_file(self):
        file = self.cleaned_data['csv_file']
        if not file.name.endswith('.csv'):
            raise forms.ValidationError('File must be a CSV file')
        return file
    
class YourMassAddForm(forms.Form):
    file = forms.FileField(required=True)