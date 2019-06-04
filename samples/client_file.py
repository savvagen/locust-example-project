from locust import Locust, HttpLocust, TaskSequence, TaskSet, task, seq_task

base_uri = "http://l5d.k8s.us-west-2.dev.earnin.com"


def get_user(l, uuid):
    return l.client.get("/svc-gateway/svc-user/user/{}".format(uuid))


def get_employment(l, uuid):
    return l.client.get("/svc-gateway/svc-user/user/{}/employment".format(uuid))


def get_employment_details(l, uuid):
    return l.client.get("/svc-gateway/svc-user/user/{}/employmentdetails".format(uuid))


class UserServiceBehavior(TaskSet):

    @task
    def get_user(self):
        resp = get_user(self, 1)
        print("Response status code:", resp.status_code)
        print("Response content:", resp.text)
        print("Response:", resp.content)
        print(resp.apparent_encoding)
        print(resp.cookies)
        print(resp.elapsed)
        print(resp.encoding)
        print(resp.headers)  # Returns headers json: {'Via': '1.1 linkerd, 1.1 linkerd', 'Content-Encoding': 'gzip',
        # 'Date': 'Fri, 31 May 2019 14:12:00 GMT', 'Server': 'Kestrel', 'Content-Length': '227', 'Content-Type':
        # 'application/json; charset=utf-8'}
        print(resp.history)
        print(resp.iter_lines)
        print(resp.json)
        print(resp.ok)  # Should be True
        print(resp.links)
        print(resp.next)
        print(resp.request)
        print(resp.url)
        print(resp.reason)
        assert resp.status_code == 200

    @task
    def get_invalid_user(self):
        with self.client.get("/svc-gateway/svc-user/user/12312", catch_response=True) as resp:
            print("Response status code:", resp.status_code)
            print("Response content:", resp.text)
            print(resp.content)
            if resp.status_code == 404:
                resp.success()

    @task
    def get_invalid_user(self):
        with self.client.get("/svc-gateway/svc-user/user/2", catch_response=True) as resp:
            print("Response status code:", resp.status_code)
            print("Response content:", resp.text)
            print("Response:", resp.content)
            if resp.status_code == 200:
                resp.failure("Got wrong response")


class Websiteuser(HttpLocust):
    host = base_uri
    task_set = UserServiceBehavior
    max_wait = 1000
    min_wait = 500
