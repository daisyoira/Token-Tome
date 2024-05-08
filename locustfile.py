from locust import HttpUser, TaskSet, task
from faker import Faker

class UserActions(TaskSet):

    def __init__(self):
        super(UserActions, self).__init__()
        self.csrf_token = None

    def on_start(self):
        response = self.client.get('/')
        self.csrf_token = response.cookies['csrftoken']

    @task
    def create_students(self):
        name = Faker().name()
        self.client('/create-student', {'name': name}, headers={'X-CSRFToken': self.csrf_token})

class ApplicationUser(HttpUser):
    # wait time between user requests
    min_wait = 1
    max_wait = 3

    @task
    def create_students(self):
        name = Faker().name()
        self.client.get('/')