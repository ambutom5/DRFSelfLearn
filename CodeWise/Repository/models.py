from django.db import models

# Create your models here.

class QuestionsDb(models.Model):
    title = models.CharField(max_length = 100)
    LANGUAGE_CHOICES = (
        ('python','Python'),
        ('java','Java'),
        ('c++','C++')
    )
    language = models.CharField(choices=LANGUAGE_CHOICES)
    DIFFICULTY_CHOICES = (
        ('easy','Easy'),
        ('medium','Medium'),
        ('hard','Hard')
    )
    difficulty = models.CharField(choices = DIFFICULTY_CHOICES)
    score = models.IntegerField()
    topic = models.CharField(max_length = 100)
    published_date = models.DateTimeField(auto_now_add = True)
    sample_input = models.TextField()
    sample_output = models.TextField()
    is_active = models.BooleanField()

class SubmissionDb(models.Model):
    question_id = models.IntegerField()
    answer = models.TextField()
    owner = models.CharField()
    points = models.PositiveIntegerField(null = True)
    submission_date = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(null = True)

