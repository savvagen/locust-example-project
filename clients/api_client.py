import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import requests
import time
from locust import Locust, TaskSet, events, task


class APIClient:

    def __init__(self, base_uri):
        self.base_uri = base_uri

    def get_request(self, r, path):
        start_time = time.time()
        try:

            r = requests.get("{}{}".format(self.base_uri, path))
            print("Status Code: {}".format(r.status_code))
            print("Headers: {}".format(r.headers))
            print("Response Body: {}".format(r.text))
            assert r.status_code == 200

        except Exception as e:
            print(e)
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="api_call", name="GET {}".format(path), response_time=total_time,
                                        exception="Request failed. Response code matches: {}".format(r.status_code))
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="api_call", name="GET {}".format(path), response_time=total_time,
                                        response_length=0)
        return r

    def get_user(self, uuid):
        path = "/svc-gateway/svc-user/user/{}".format(uuid)
        return self.get_request(requests, path)

    def get_user_employment(self, uuid):
        path = "/svc-gateway/svc-user/user/{}/employment".format(uuid)
        return self.get_request(requests, path)


class LocustRequests(Locust):

    def __init__(self):
        super(LocustRequests).__init__()
        self.client = APIClient(self.host)


class MyClientTest(LocustRequests):
    host = "http://l5d.k8s.us-west-2.dev.earnin.com"
    min_wait = 100
    max_wait = 1000

    class task_set(TaskSet):

        @task(10)
        def get_time(self):
            self.client.get_user(2)
