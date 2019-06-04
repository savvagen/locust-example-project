import random
from locust import Locust, HttpLocust, TaskSet, task

base_uri = "http://l5d.k8s.us-west-2.dev.earnin.com"


def get_user(locust, uuid):
    locust.client.get("/svc-gateway/svc-user/user/{}".format(uuid))


def get_employment(locust, uuid):
    locust.client.get("/svc-gateway/svc-user/user/{}/employment".format(uuid))


def get_employment_details(l, uuid):
    l.client.get("/svc-gateway/svc-user/user/{}/employmentdetails".format(uuid))


def print_message(message):
    print(message)


class UsersPageBehavior(TaskSet):

    @task(8)
    def get_user(self):
        get_user(self, 1)

    @task(4)
    def get_user_employment(self):
        get_employment(self, 2)

    @task(6)
    def stop(self):
        self.interrupt()

    @task(2)
    class SubTaskSet(TaskSet):

        @task
        def sub_task(self):
            get_user(self, 2)


class MainPageBehavior(TaskSet):
    tasks = {UsersPageBehavior: 4}

    @task(2)
    def get_details(self):
        get_employment_details(self, 2)


class UserBehavior(HttpLocust):
    host = base_uri
    stop_timeout = 120
    task_set = MainPageBehavior
    min_wait = 500
    max_wait = 1000


