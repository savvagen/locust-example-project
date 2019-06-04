from locust import Locust, HttpLocust, TaskSet


def google(l):
    l.client.get("/")


def google_accounts(l):
    l.client.get("/accounts")


def print_message(message):
    print(message)


class GoogleUserBehavior(TaskSet):
    tasks = {google: 2, google_accounts: 1}

    def on_start(self):
        print_message("Hello Google!!!")

    def on_stop(self):
        print_message("Hello Google!!!")


class GoogleUser(HttpLocust):
    task_set = GoogleUserBehavior
    host = "http://google.com"
    stop_timeout = 120
    min_wait = 500
    max_wait = 1000
