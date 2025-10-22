from django import forms
from .models import Lesson, Commentaire, Reponse

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('lesson_id', 'nom', 'video', 'fpe', 'pdf', 'position')

    
class ComForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ('corps',)
        lables = {'corps': 'Commentaire'}
        widgets = {
            'corps':forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'cols':70,
                'placeholder':'Entrez votre commentaire ici.'
            })
        }


class RepForm(forms.ModelForm):
    class Meta:
        model = Reponse
        fields = ('corps',)
        lables = {'corps': 'Reponses'}
        widgets = {
            'corps':forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'cols':10,
                'placeholder':'Repondez ici.'
            })
        }
