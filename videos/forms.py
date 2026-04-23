from django import forms
from .models import Video

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file', 'thumbnail']
        labels = {
            'title': 'Название видео',
            'description': 'Описание',
            'video_file': 'Файл видео',
            'thumbnail': 'Превью (картинка)',
        }
        help_texts = {
            'video_file': 'Поддерживаются форматы MP4, AVI, MOV',
            'thumbnail': 'Необязательно. Картинка для обложки видео',
        }


class CommentForm(forms.Form):
    text = forms.CharField(
        label='',
        max_length=500,
        widget=forms.TextInput(attrs={
            'placeholder': 'Написать комментарий...',
            'style': 'width: 100%; padding: 8px; border-radius: 20px; border: 1px solid #ccc;'
        })
    )