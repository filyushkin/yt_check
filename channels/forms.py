from django import forms

#class ChannelForm(forms.Form):
#    pseudonym = forms.CharField(max_length=255, label='Псевдоним канала')

class ChannelForm(forms.Form):
    pseudonym = forms.CharField(max_length=100, label="Псевдоним канала", widget=forms.TextInput(attrs={'class': 'form-control'}))
