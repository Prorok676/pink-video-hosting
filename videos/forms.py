from django import forms
from django.core.exceptions import ValidationError
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
            'thumbnail': 'Необязательно. JPG, PNG, GIF. Максимум 2 МБ.',
        }

    def clean_thumbnail(self):
        thumbnail = self.cleaned_data.get('thumbnail')
        if thumbnail:
            if thumbnail.size > 2 * 1024 * 1024:  # 2 МБ
                raise ValidationError("Размер превью не должен превышать 2 МБ.")
        return thumbnail


class CommentForm(forms.Form):
    text = forms.CharField(
        label='',
        max_length=500,
        widget=forms.TextInput(attrs={
            'placeholder': 'Написать комментарий...',
            'style': 'width: 100%; padding: 8px; border-radius: 20px; border: 1px solid #ccc;'
        })
    )