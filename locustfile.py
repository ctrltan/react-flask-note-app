from locust import FastHttpUser, SequentialTaskSet, between, task
import itertools

class TaskWorkflow(SequentialTaskSet):
    get_id = itertools.count(start=1)

    def on_start(self):
        self.note_id = None
        user_id = next(self.get_id)
        user_data = {'username': f'vuser{user_id}', 'email': f'vuser{user_id}@email.com', 'password': f'Vuserpass{user_id}!'}
        response = self.client.post('/signup', json=user_data)
    
    @task
    def make_note(self):
        response = self.client.get('/notes/new-note')
        self.note_id = response.json()['message']['note_id']

    @task
    def delete_note(self):
        if self.note_id:
            self.client.delete(f'/notes/delete?note_id={self.note_id}')
        self.note_id = None

    def on_stop(self):
        self.client.post('/logout')


class LoadTestUser(FastHttpUser):
    tasks = [TaskWorkflow]
    wait_time = between(1, 3)