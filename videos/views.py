from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Video
from .forms import VideoForm
from .models import Video, VideoLike, Comment
from .forms import VideoForm, CommentForm

def video_list(request):
    # Показываем только НЕ заблокированные видео
    videos = Video.objects.filter(is_blocked=False)
    comment_form = CommentForm()
    return render(request, 'videos/video_list.html', {
        'videos': videos,
        'comment_form': comment_form
    })
@login_required  # Только для авторизованных пользователей
def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.author = request.user  # Присваиваем автора
            video.save()
            return redirect('home')
    else:
        form = VideoForm()
    return render(request, 'videos/upload.html', {'form': form})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Video, VideoLike
import json


@login_required
@csrf_exempt  # Для простоты AJAX запросов
def like_video(request, video_id):
    if request.method == 'POST':
        try:
            video = Video.objects.get(id=video_id)
            data = json.loads(request.body)
            is_like = data.get('is_like')

            # Проверяем, ставил ли уже пользователь оценку
            existing_like = VideoLike.objects.filter(user=request.user, video=video).first()

            if existing_like:
                # Если оценка уже была и она такая же - ничего не делаем
                if existing_like.like_type == is_like:
                    return JsonResponse({'success': False, 'message': 'Вы уже ставили эту оценку'})
                else:
                    # Если поменял лайк на дизлайк - обновляем счетчики
                    if existing_like.like_type:  # Был лайк
                        video.likes -= 1
                    else:  # Был дизлайк
                        video.dislikes -= 1

                    existing_like.like_type = is_like
                    existing_like.save()

                    if is_like:
                        video.likes += 1
                    else:
                        video.dislikes += 1

                    video.save()
                    return JsonResponse({'success': True, 'likes': video.likes, 'dislikes': video.dislikes})
            else:
                # Если оценки не было - создаем новую
                VideoLike.objects.create(user=request.user, video=video, like_type=is_like)
                if is_like:
                    video.likes += 1
                else:
                    video.dislikes += 1
                video.save()
                return JsonResponse({'success': True, 'likes': video.likes, 'dislikes': video.dislikes})

        except Video.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Видео не найдено'})

    return JsonResponse({'success': False, 'message': 'Неверный запрос'})
@login_required
def add_comment(request, video_id):
    if request.method == 'POST':
        try:
            video = Video.objects.get(id=video_id)
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = Comment.objects.create(
                    video=video,
                    author=request.user,
                    text=form.cleaned_data['text']
                )
                return JsonResponse({
                    'success': True,
                    'author': comment.author.username,
                    'text': comment.text,
                    'created_at': comment.created_at.strftime('%d.%m.%Y %H:%M')
                })
        except Video.DoesNotExist:
            pass
    return JsonResponse({'success': False})

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required  # Только для админов!
def admin_video_list(request):
    videos = Video.objects.all().order_by('-created_at')
    return render(request, 'videos/admin_video_list.html', {'videos': videos})

@staff_member_required
def toggle_block_video(request, video_id):
    try:
        video = Video.objects.get(id=video_id)
        video.is_blocked = not video.is_blocked  # Переключаем статус
        video.save()
    except Video.DoesNotExist:
        pass
    return redirect('admin_video_list')
