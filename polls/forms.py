from django import forms
from polls.models import Membership

class MembershipForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Membership
        fields = ['email', 'username']