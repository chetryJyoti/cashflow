from django import forms
from datetime import date
from tracker.models import Transaction,Category

class TransactionForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.RadioSelect()
    )

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <=0:
            raise forms.ValidationError("Amount must be greater than 0")
        return amount

    def clean_date(self):
        date_value = self.cleaned_data["date"]
        if date_value > date.today():
            raise forms.ValidationError("Transaction date cannot be in the future")
        return date_value

    class Meta:
        model = Transaction
        fields = (
            'type',
            'amount',
            'date',
            'category'
        )
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'max': date.today().isoformat()
            })
        }