from django import forms
from .models import VetCategory, VetSupply

class VetSupplyForm(forms.ModelForm):
    class Meta:
        model = VetSupply
        fields = ['name', 'category', 'quantity', 'reorder_level', 'expiration_date', 'description']
        widgets = {
            'expiration_date': forms.DateInput(attrs={'type': 'date'}),
            'reorder_level': forms.NumberInput(attrs={'min': 1}),
            'quantity': forms.NumberInput(attrs={'min': 0}),
        }
        labels = {
            'reorder_level': 'Reorder Level (alert when stock reaches this number)',
            'expiration_date': 'Expiration Date (optional)'
        }

class MassAddForm(forms.Form):
    csv_file = forms.FileField(
        label='Select CSV file',
        help_text="""
        Upload a CSV file with the following columns:
        - name (required)
        - quantity (required, positive number)
        - category (required)
        - reorder_level (optional, defaults to 10)
        - expiration_date (optional, format: DD-MM-YYYY)
        """
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False
    )

    def clean_csv_file(self):
        file = self.cleaned_data['csv_file']
        if not file.name.endswith('.csv'):
            raise forms.ValidationError('File must be a CSV file')
            
        if file.size > 5242880:  # 5MB limit
            raise forms.ValidationError('File size must be under 5MB')
            
        return file

class YourMassAddForm(forms.Form):
    file = forms.FileField(required=True)

class MassOutgoingForm(forms.Form):  # Change from ModelForm to Form
    reason = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        required=True,
        label='Reason for Outgoing'
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        required=False,
        label='Additional Notes'
    )

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('reason'):
            raise forms.ValidationError('Reason is required')
        return cleaned_data

class MassOutgoingItemForm(forms.Form):
    supply = forms.ModelChoiceField(
        queryset=VetSupply.objects.all(),
        required=True,
        label='Item',
        widget=forms.Select(attrs={'class': 'form-select'}),
        error_messages={
            'required': 'Please select an item',
            'invalid_choice': 'Please select a valid item'
        }
    )
    quantity = forms.IntegerField(
        min_value=1,
        required=True,
        label='Quantity',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        error_messages={
            'required': 'Please enter a quantity',
            'min_value': 'Quantity must be at least 1'
        }
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

# Create formset
MassOutgoingItemFormSet = forms.formset_factory(
    MassOutgoingItemForm,
    extra=1,  # Change back to 1
    can_delete=True,
    min_num=1,
    validate_min=True
)