from rest_framework import serializers
from Repository.models import QuestionsDb,SubmissionDb

class QuestionsDbSerializer(serializers.Serializer):
    title = serializers.CharField(max_length = 100)
    language = serializers.ChoiceField(choices = QuestionsDb.LANGUAGE_CHOICES)
    difficulty = serializers.ChoiceField(choices = QuestionsDb.DIFFICULTY_CHOICES)
    score = serializers.IntegerField()
    topic = serializers.CharField(max_length = 100)
    published_date = serializers.DateTimeField(read_only=True)
    sample_input = serializers.CharField()
    sample_output = serializers.CharField()
    is_active = serializers.BooleanField()

class SubmissionDbSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer = serializers.CharField()
    owner = serializers.CharField()
    points = serializers.IntegerField(read_only=True)
    submission_date = serializers.DateTimeField(read_only=True)
    remarks = serializers.CharField(read_only=True)

    def validate(self,validated_data):
        print(validated_data)
        question_id = validated_data.get("question_id")
        if not QuestionsDb.objects.filter(id=question_id).exists():
            raise serializers.ValidationError("Qn Doesnot Exists!")
        else:
            return validated_data
