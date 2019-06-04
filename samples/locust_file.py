import random
from locust import Locust, HttpLocust, TaskSet, task

base_uri = "http://l5d.k8s.us-west-2.dev.earnin.com"

def get_user(locust, uuid):
    locust.client.get("/svc-gateway/svc-user/user/{}".format(uuid))


def get_employment(locust, uuid):
    locust.client.get("/svc-gateway/svc-user/user/{}/employment".format(uuid))


def print_message(message):
    print(message)


class UserBehavior(TaskSet):
    #tasks = {get_user: 2, get_employment: 1}

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        print_message("Testing Started!!!")

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        print_message("Testing Stopped!!!")

    @task(2)
    def get_user(self):
        get_user(self, 1)

    @task(1)
    def get_user_employment(self):
        get_employment(self, 2)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    # wait_function = lambda self: random.expovariate(1) * 10
    # With the following locustfile, each user would wait between 5 and 15 seconds between tasks:
    min_wait = 5000
    max_wait = 15000





# Run different Users with: locust -f locust_file.py WebUserLocust MobileUserLocust
class WebUserLocust(HttpLocust):
    """Base hostname to swarm. i.e: http://127.0.0.1:1234"""
    host = base_uri
    """Probability of locust being chosen. The higher the weight, the greater is the chance of it being chosen."""
    weight = 3
    """Number of seconds after which the Locust will die. If None it won't timeout."""
    stop_timeout = 30
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 15000


class MobileUserLocust(HttpLocust):
    host = base_uri
    weight = 1
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 15000

