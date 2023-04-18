"""Loan request app Forms."""
from django import forms
from .models import LoanRequest


class LoanForm(forms.ModelForm):
    """Form Loan Request."""

    class Meta:
        """Meta class."""

        model = LoanRequest
        fields = "__all__"
