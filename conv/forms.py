from django import forms
from conv.models import Author

USER_ID = ()
us = tuple(Author.objects.values('id'))
for i in us:
    USER_ID += ((i['id'], i['id']),)


MY_CHOICES = (
    ('Del', 'Delete data'),
    ('Add', 'Add data'),
)


class AddAuthor(forms.Form):
    first_name = forms.CharField(max_length=30,
                                 widget=forms.TextInput(
                                     attrs={'class': "form-control col-12", 'placeholder': 'Andrii'}))
    last_name = forms.CharField(max_length=40,
                                widget=forms.TextInput(attrs={'class': "form-control col-12", 'placeholder': 'Konyuk'}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': "form-control col-12", 'placeholder': 'test@mail.com'}))
    doing = forms.ChoiceField(choices=MY_CHOICES, widget=forms.RadioSelect())
    user_id = forms.ChoiceField(choices=USER_ID, required=False, widget=forms.Select())

    class Meta:
        model = Author

    def __init__(self):
        super().__init__()
        USER_ID = ()
        us = tuple(Author.objects.values('id'))
        for i in us:
            USER_ID += ((i['id'], i['id']),)
        self.fields['user_id'].choices = USER_ID