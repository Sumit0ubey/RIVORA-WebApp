from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(label="Name", required=True, widget=forms.TextInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}))
    email = forms.EmailField(label="Email", required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))
    reason = forms.CharField(label="Reason", required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'What"s your concern'}))
    description = forms.CharField(label="Description", required=True, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Elaborate your problem'}))
