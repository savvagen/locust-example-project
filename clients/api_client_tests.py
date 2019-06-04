import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, "../..")))


from locust import TaskSet, task
from clients.api_client import LocustRequests


class ApiClientFlow(TaskSet):

    @task(2)
    def get_user(self):
        self.client.get_user(2)

    @task(1)
    def get_employment(self):
        self.client.get_user_employment(3)


class ApiUserBehavior(LocustRequests):
    task_set = ApiClientFlow
    host = "http://l5d.k8s.us-west-2.dev.earnin.com"
    stop_timeout = 20
    min_wait = 100
    max_wait = 500
