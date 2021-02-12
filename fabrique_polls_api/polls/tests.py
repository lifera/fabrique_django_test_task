from django.test import TestCase
from polls.models import Poll, Question, Answer
from django.utils import timezone
import datetime
from django.contrib.auth.models import User


def create_poll():
    end_date = timezone.now() + datetime.timedelta(days=7)
    Poll.objects.create(poll_name='poll name', end_date=end_date, description='poll description')


def create_question():
    create_poll()
    polls = Poll.objects.filter(id=1)
    for poll in polls:
        Question.objects.create(poll=poll, question_text='question text?',
                                question_type='text_answer')


def create_answer(answered_by, answer_text):
    create_question()
    polls = Poll.objects.filter(id=1)
    questions = Question.objects.filter(id=1)
    for poll in polls:
        for question in questions:
            Answer.objects.create(question=question, poll=poll,
                                  answered_by=answered_by, answer_text=answer_text)


class PollTestCase(TestCase):
    def login(self):
        user = User.objects.create_user('admin', 'admin@admin.com', '1')
        self.client.force_login(user)

    def test_get_polls(self):
        create_poll()
        response = self.client.get('/polls/')
        self.assertContains(response, 'poll name')

    def test_add_poll(self):
        end_date = datetime.date.today()
        data = {'poll_name': 'test poll', 'end_date': end_date, 'description': 'poll description'}
        self.login()
        response = self.client.post(r'/polls/', data)
        self.assertContains(response, 'test poll', status_code=201)

    def test_update_poll(self):
        create_poll()
        data = {'poll_name': 'changed poll'}
        self.login()
        response = self.client.patch('/polls/1/', data, 'application/json')
        self.assertContains(response, 'changed poll')

    def test_delete_poll(self):
        create_poll()
        self.login()
        response = self.client.delete('/polls/1/')
        self.assertEqual(response.status_code, 204)
        query = Poll.objects.all()
        self.assertQuerysetEqual(query, [])


class QuestionTestCase(TestCase):
    def login(self):
        user = User.objects.create_user('admin', 'admin@admin.com', '1')
        self.client.force_login(user)

    def test_get_questions(self):
        create_question()
        response = self.client.get('/polls/1/questions/')
        self.assertContains(response, 'question text?')

    def test_add_question(self):
        create_poll()
        data = {'poll': 1, 'question_text': 'text?', 'question_type': 'ответ текстом'}
        self.login()
        response = self.client.post(r'/polls/1/questions/', data)
        self.assertContains(response, "text?", status_code=201)

    def test_update_question(self):
        create_question()
        data = {'question_text': 'changed text'}
        self.login()
        response = self.client.patch('/polls/1/questions/1/', data, 'application/json')
        self.assertContains(response, 'changed text')

    def test_delete_question(self):
        create_question()
        self.login()
        response = self.client.delete('/polls/1/questions/1/')
        self.assertEqual(response.status_code, 204)
        query = Question.objects.all()
        self.assertQuerysetEqual(query, [])


class AnswerTestCase(TestCase):
    def test_answer_create(self):
        create_question()
        data = {'question': 1, 'poll': 1, 'answered_by': 77, 'answer_text': 'text of the answer'}
        response = self.client.post('/polls/1/questions/1/answers/', data)
        self.assertContains(response, 'text of the answer', status_code=201)

    def test_get_answers_by_answered_by(self):
        create_answer(1, 'first')
        create_answer(77, 'not needed')
        response = self.client.get('/answers/1/')
        self.assertContains(response, 'first')
        self.assertNotContains(response, 'not needed')
