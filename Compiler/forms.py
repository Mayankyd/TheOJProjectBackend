from django import forms
from .models import CodeSubmission

LANGUAGE_CHOICES = [
    ("py", "Python"),
    ("c", "C"),       # You can remove this if you are not supporting C.
    ("cpp", "C++"),
    ("java", "Java"),  # ✅ Added Java option
]


class CodeSubmissionForm(forms.ModelForm):
    language = forms.ChoiceField(choices=LANGUAGE_CHOICES)

    class Meta:
        model = CodeSubmission
        fields = ["language", "code", "input_data"]

