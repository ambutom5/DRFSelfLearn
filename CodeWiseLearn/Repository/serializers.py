from rest_framework import serializers
from Repository.models import QuestionsDb

class QuestionDbSerializer(serializers.Serializer):
    title = serializers.CharField(max_length = 100)
    language = serializers.ChoiceField(choices=QuestionsDb.LANGUAGE_CHOICES)
    difficulty_level = serializers.ChoiceField(choices = QuestionsDb.DIFFICULTY_CHOICES)
    score = serializers.IntegerField()
    topic = serializers.CharField(max_length = 100)
    notes = serializers.CharField(max_length = 100)
    published_data = serializers.DateTimeField(read_only = True)
    sample_input = serializers.CharField(max_length = 100)
    sample_output = serializers.CharField(max_length = 100)
    is_active = serializers.BooleanField(default = True)