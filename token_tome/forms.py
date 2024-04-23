from django import forms


class FileUploadForm(forms.Form):
    student = forms.ChoiceField()
    file = forms.FileField()
