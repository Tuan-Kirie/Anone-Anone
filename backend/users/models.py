from django.contrib.auth.models import User
from django.db import models
from ranobe.models import Chapters, Ranobe


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    profile_img = models.ImageField(upload_to='media/profile', default='media/profile/default.jpg', null=True,
                                    blank=True)
    reading_books = models.ManyToManyField(Chapters, related_name='reading')
    read_books = models.ManyToManyField(Ranobe, related_name='read')
    planned_books = models.ManyToManyField(Ranobe, related_name='planned')
    bookmarked = models.ManyToManyField(Ranobe, related_name='bookmarked')
    read_status = models.ManyToManyField(Ranobe, related_name='book_status', through='BookReadingStatus')

    def __str__(self):
        return self.user.username


class ReadHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ranobe_chapter = models.ForeignKey(Chapters, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ranobe_chapter.id} в ранобэ {self.ranobe_chapter.ranobe.id}"


class BookReadingStatus(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    ranobe = models.ForeignKey(Ranobe, on_delete=models.CASCADE)
    RDG = 'RDG'
    RD = 'RD'
    PL = 'PL'
    NO = 'NO'
    choices = models.CharField(max_length=3, choices=[
        (NO, 'Не выбрано'),
        (RDG, 'Читаю'),
        (RD, 'Прочитано'),
        (PL, 'Запланировано')
    ])

    def __str__(self):
        return f"{self.profile.user.username} - {self.ranobe} - {self.choices}"
