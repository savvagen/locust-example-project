import random
from locust import Locust, HttpLocust, TaskSet, TaskSequence, task, seq_task

base_uri = "http://l5d.k8s.us-west-2.dev.earnin.com"


def get_user(locust, uuid):
    locust.client.get("/svc-gateway/svc-user/user/{}".format(uuid))


def get_employment(locust, uuid):
    locust.client.get("/svc-gateway/svc-user/user/{}/employment".format(uuid))


def get_employment_details(l, uuid):
    l.client.get("/svc-gateway/svc-user/user/{}/employmentdetails".format(uuid))


def print_message(message):
    print(message)

# In the above example, the order is defined to execute get_user,
# then get_user_employment
# and lastly the get_user_employment_details for 10 times.
class UserServiceBehavior(TaskSequence):

    def setup(self):
        print("Tests Started!!!!!!!!!!!!!!!")

    def teardown(self):
        print("Tests Finished!!!!!!!!!!!!!!")

    def on_start(self):
        print("Test Started!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    def on_stop(self):
        print("Test Stopped!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    @seq_task(1)
    def get_user(self):
        get_user(self, 1)

    @seq_task(2)
    def get_user_employment(self):
        get_employment(self, 2)

    @seq_task(3)
    @task(10)
    def get_user_employment_details(self):
        get_employment_details(self, 2)


class UserBehavior(HttpLocust):
    host = base_uri
    stop_timeout = 30
    task_set = UserServiceBehavior
    min_wait = 500
    max_wait = 1000

    def setup(self):
        print("Test Suite Started!!!")

    def teardown(self):
        print("Test Suite Finished!!!")


