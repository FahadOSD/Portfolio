from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'custom-input w-full py-3 pl-10 pr-4',
                'placeholder': 'John Doe',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'custom-input w-full py-3 pl-10 pr-4',
                'placeholder': 'john@example.com',
                'required': True
            }),
            'subject': forms.TextInput(attrs={
                'class': 'custom-input w-full py-3 pl-10 pr-4',
                'placeholder': 'Project Inquiry',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'custom-input w-full py-3 pl-10 pr-4 resize-none',
                'placeholder': "Hello, I'd like to talk about...",
                'rows': 5,
                'required': True
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix = "" 