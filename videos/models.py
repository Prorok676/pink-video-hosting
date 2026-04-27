from django.db import models
from django.contrib.auth.models import User


class Video(models.Model):
    # Кто загрузил видео
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    # Название видео
    title = models.CharField(max_length=100, verbose_name="Название")
    # Описание
    description = models.TextField(blank=True, verbose_name="Описание")
    # Сам файл видео
    video_file = models.FileField(upload_to='videos/', verbose_name="Файл видео")
    # Превью
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True, verbose_name="Превью")
    # Дата загрузки
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")

    # Количество лайков и дизлайков
    likes = models.IntegerField(default=0, verbose_name="Лайки")
    dislikes = models.IntegerField(default=0, verbose_name="Дизлайки")
    is_blocked = models.BooleanField(default=False, verbose_name="Заблокировано")
    block_reason = models.CharField(max_length=200, blank=True, null=True, verbose_name="Причина блокировки")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"
        ordering = ['-created_at']

class VideoLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    # Тип: True = Лайк, False = Дизлайк
    like_type = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Это чтобы нельзя было лайкнуть одно видео дважды
        unique_together = ('user', 'video')


class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500, verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}: {self.text[:30]}"

    class Meta:
        ordering = ['-created_at']  # Новые сверху
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


# Роли пользователей
class UserRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False, verbose_name="Администратор")

    def __str__(self):
        return f"{self.user.username} - {'Админ' if self.is_admin else 'Пользователь'}"

    class Meta:
        verbose_name = "Роль пользователя"
        verbose_name_plural = "Роли пользователей"

