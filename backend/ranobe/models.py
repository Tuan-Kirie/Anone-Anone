from django.db import models


class Ranobe(models.Model):
    name = models.TextField(max_length=500)
    description = models.TextField(null=True, blank=True)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    genres = models.ManyToManyField('Genres')
    tags = models.ManyToManyField('Tags')
    image = models.ImageField(upload_to='media/ranobe', default='media/ranobe/default.png', null=True, blank=True)
    publisher = models.ForeignKey('Publisher', on_delete=models.SET_NULL, null=True, blank=True)
    alternate_name = models.TextField(models.TextField, null=True, blank=True)
    adult_status = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.name if self.name is not None else 'Нет имени'

    class Meta:
        verbose_name_plural = 'Ранобэ'
        ordering = ['id']


class Author(models.Model):
    author = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.author if self.author is not None else 'Нет автора'

    class Meta:
        verbose_name_plural = 'Авторы'


class Genres(models.Model):
    genre = models.TextField(max_length=550, null=True, blank=True)

    def __str__(self):
        return self.genre if self.genre is not None else 'Нет жанра'

    class Meta:
        verbose_name_plural = 'Жанры'


class Tags(models.Model):
    tag = models.TextField(max_length=550, null=True, blank=True)

    def __str__(self):
        return self.tag if self.tag is not None else 'Нет тега'

    class Meta:
        verbose_name_plural = 'Тэги'


class Year(models.Model):
    year = models.SmallIntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.year) if self.year is not None else 'Не задан год'

    class Meta:
        verbose_name_plural = 'Года'


class Publisher(models.Model):
    publisher = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.publisher if self.publisher is not None else 'Нет издателя'

    class Meta:
        verbose_name_plural = 'Издатели'


class Chapters(models.Model):
    chapter_name = models.TextField()
    text = models.TextField()
    ranobe = models.ForeignKey('Ranobe', on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Главы'

    def __str__(self):
        return self.chapter_name
