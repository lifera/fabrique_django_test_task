from django.db import models
from rest_framework import fields


class Poll(models.Model):
    poll_name = models.CharField(max_length=120)
    start_date = models.DateField(auto_now=True)
    end_date = models.DateField()
    description = models.CharField(max_length=400)

    def __str__(self):
        return self.poll_name


class Question(models.Model):
    question_type_choices = [
        ('ответ текстом', 'text_answer'),
        ('ответ с выбором одного варианта', 'one_answer'),
        ('ответ с выбором нескольких вариантов', 'many_answers')
    ]
    poll = models.ForeignKey(Poll, related_name='questions', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=240)
    question_type = models.CharField(max_length=120, choices=question_type_choices)

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    answered_by = models.IntegerField()
    answer_text = models.TextField()
    # choices = fields.MultipleChoiceField()
    # one_choice = fields.ChoiceField()

    class Meta:
        unique_together = ("poll", "question", "answered_by")
