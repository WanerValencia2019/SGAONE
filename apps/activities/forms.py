from django import forms
from .models import Assignment


class AssignmentForm(forms.ModelForm):
    class Meta:
        model=Assignment
        fields=['title','teacher','course','status','start','deadline']
        widgets={
            'title':forms.TextInput(attrs={
                    'class':'form-control',
                    'placeholder':'Título'
                }),
            'teacher':forms.Select(attrs={
                    'class':'form-control',
                    'readonly':True
                }),
            'course':forms.Select(attrs={
                    'class':'form-control'
                }),
            'status':forms.Select(attrs={
                    'class':'form-control'
                }),
            'start':forms.DateInput(attrs={
                    'class':'form-control',
                    'placeholder':'Fecha de inicio'
                }),
            'deadline':forms.DateTimeInput(attrs={
                    'class':'form-control',
                    'placeholder':'Fecha de entrega'
                })
        }