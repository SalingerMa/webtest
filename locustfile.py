from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):
    @task
    def baidu_page(self):
        self.client.get("/")

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 3000
    max_wait = 6000