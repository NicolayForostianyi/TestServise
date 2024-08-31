import uuid
import datetime
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Answer(models.Model):
    answer = models.CharField(max_length=255, verbose_name="Ответ")

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
    def __str__(self):
        return self.answer


"""
В тех задании не указано количество правильных ответов в тесте, их может быть несколько,
в таком случае можно показать не все существующие правильные ответы, но хотя бы 1 
"""


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.CharField(max_length=255, verbose_name='Вопрос')
    answer_options = models.ManyToManyField(Answer, related_name='answer_option', verbose_name="варианты ответа",blank=True, null=True) # Django не сохранят
    right_answers = models.ManyToManyField(Answer, related_name='right_answers', verbose_name="правильные ответы", blank=True, null=True)# объекты в manyToMany
    size_of_answers = models.IntegerField(verbose_name="Количество показываемых вариантов", default=4)                      # до того, пока не создаст объект

    def save(self, *args, **kwargs):
        right_answers = set(self.right_answers.all())
        answer_options = set(self.answer_options.all())
        if not right_answers.issubset(answer_options):
            print("right_answers = ", right_answers)
            print("answer_options = ", answer_options)
            raise ValidationError("Правильные ответы обязаны быть в вариантах ответа")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Test(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    questions = models.ManyToManyField(Question, verbose_name="Вопросы теста")
    # Нужно предусмотреть что их может быть физически меньше чем количество
    size_of_pages = models.IntegerField(verbose_name="Количество вопросов", default=20)
    is_active = models.BooleanField(verbose_name="Активен", default=True)

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"


class TestPass(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Пользователь")
    test = models.ForeignKey(Test, on_delete=models.PROTECT, verbose_name="Тест")
    datetime = models.DateTimeField(default=datetime.datetime.now(), verbose_name="Дата выполнения теста" )
    result_ball = models.FloatField(verbose_name="Оценка")

    class Meta:
        verbose_name = "Прохождение теста пользователем"
        verbose_name_plural = "История прохождений пользователями"
