from locust import HttpUser, SequentialTaskSet, TaskSet, task, between
from faker import Faker

class UserActions(SequentialTaskSet):
    # load test on the number of students that
    # can be created simultaneously
    @task
    def create_students(self):
        response = self.client.get("/create-student")
        csrftoken = response.cookies['csrftoken']

        name = Faker().name()
        self.client.post('/create-student',
                         {'name': name},
                         headers={"X-CSRFToken": csrftoken})

class ApplicationUser(HttpUser):
    tasks = [UserActions]
    host = 'http://localhost:8000'

    # wait time between user requests
    # in seconds
    wait_time = between(10, 20)