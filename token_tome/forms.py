from django import forms
from token_tome.models import Student, File


class FileUploadForm(forms.Form):

    file = forms.FileField(widget=forms.FileInput(attrs={'accept': 'application/pdf'}),
                           required=True)

    # to_field_name - specifies column to use as value
    student = forms.ModelChoiceField(queryset=Student.objects.all(),
                                     required=True,
                                     to_field_name="token")

    def __init__(self, *args, **kwargs):
        super(FileUploadForm, self).__init__(*args, **kwargs)

        # use student name as the label
        self.fields['student'].label_from_instance = self.label_from_instance

    @staticmethod
    def label_from_instance(student):
        return student.name

