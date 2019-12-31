from django import forms

class ApiForm(forms.Form):
    url = forms.URLField(required=True, widget=forms.URLInput(
        attrs={'class' : 'form-control', 'placeholder' :
        'https://techcrunch.com/2019/12/27/techcrunchs-favorite-things-of-2019/'}
    ), min_length=10, max_length=254)
