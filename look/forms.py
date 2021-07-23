from django import forms

class AddForm(forms):
    first = forms.IntegerField(max_value=11)
    second = forms.IntegerField(min_value=9)
