from django.contrib.auth import get_user_model
from django.db import models

from core.constants import FIELDS_MAX_LENGTH, STR_LENGTH
from core.models import CreatedAt, IsPublishedAndCreatedAt


User = get_user_model()


class Location(IsPublishedAndCreatedAt):
    name = models.CharField(
        max_length=FIELDS_MAX_LENGTH,
        verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Category(IsPublishedAndCreatedAt):
    title = models.CharField(
        max_length=FIELDS_MAX_LENGTH,
        verbose_name='Заголовок'
    )

    description = models.TextField(verbose_name='Описание')

    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; '
                  'разрешены символы латиницы, цифры, дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:STR_LENGTH]


class Post(IsPublishedAndCreatedAt):
    title = models.CharField(
        max_length=FIELDS_MAX_LENGTH,
        verbose_name='Заголовок'
    )

    text = models.TextField(verbose_name='Текст')

    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и '
                  'время в будущем — можно делать отложенные публикации.'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор публикации'
    )

    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Категория'
    )

    location = models.ForeignKey(
        Location,
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        related_name='posts',
        verbose_name='Местоположение'
    )

    image = models.ImageField(
        upload_to='posts_images',
        blank=True,
        verbose_name='Изображение'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title[:STR_LENGTH]


class Comment(CreatedAt):
    text = models.TextField('Текст комментария')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Публикация'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
        related_name='comments'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'

    def __str__(self):
        return f'Комментарий пользователя {self.author}'
