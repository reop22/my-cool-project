from locust import HttpUser, task, between

class FastAPIUser(HttpUser):

    wait_time = between(1, 2.5)

    @task
    def read_root(self):
        self.client.get("/")

    @task(3)
    def read_item(self):
        item_id = 42
        self.client.get(f"/items/{item_id}", params={"q": "test"})

    task
    def create_item(self):
        self.client.post("/items", json={"name": "New Item","price": 10.5, "is_offer":True})