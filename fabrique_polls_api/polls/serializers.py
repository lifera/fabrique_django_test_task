from rest_framework import serializers

from .models import Poll, Question, Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = '__all__'


class PollSerializer(serializers.ModelSerializer):
    choices = QuestionSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Poll
        fields = '__all__'
