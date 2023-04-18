from django import forms
from .models import LoanRequest


class LoanForm(forms.ModelForm):
    class Meta:
        model = LoanRequest
        fields = '__all__'
