FROM python:3-alpine
ADD . /fabrique_polls_api
WORKDIR /fabrique_polls_api
RUN pip install -r requirements.txt
EXPOSE 8000

#RUN python fabrique_polls_api/manage.py runserver
