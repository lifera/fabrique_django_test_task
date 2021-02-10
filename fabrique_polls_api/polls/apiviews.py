from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import permissions
import datetime

from .models import Poll, Question, Answer
from .serializers import PollSerializer, QuestionSerializer, AnswerSerializer


class PollViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.successful_authenticator:
            queryset = Poll.objects.all()
        else:
            # For not authenticated users fetching only active polls
            queryset = Poll.objects.exclude(end_date__lt=datetime.date.today())
        return queryset

    serializer_class = PollSerializer


class QuestionList(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Question.objects.filter(poll_id=self.kwargs["pk"])
        return queryset

    def retrieve(self, *args, **kwargs):
        queryset = Question.objects.filter(id=self.kwargs["question_pk"])
        question = get_object_or_404(queryset, pk=self.kwargs["question_pk"])
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    serializer_class = QuestionSerializer


class AnswerCreate(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = AnswerSerializer

    def post(self, request, pk, question_pk):
        answered_by = request.data.get("answered_by")
        answer_text = request.data.get("answer_text")
        data = {'question': question_pk, 'poll': pk, 'answered_by': answered_by, 'answer_text': answer_text}
        serializer = AnswerSerializer(data=data)
        if serializer.is_valid():
            answer = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnswerList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = AnswerSerializer

    def get_queryset(self):
        queryset = Answer.objects.filter(answered_by=self.kwargs["pk"])
        return queryset
