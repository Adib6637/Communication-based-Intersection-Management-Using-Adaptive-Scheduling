from job import *

GROUP_A = 0
GROUP_B = 1


class Task:
    """queue of jobs"""

    def __init__(self):
        print(f"creating a task")
        self.sub_task = []
        self.sub_task.append([])
        self.sub_task.append([])

    def __setitem__(self, item, data):
        self.sub_task[item] = data

    def __getitem__(self, item):
        return self.sub_task[item]

    def add_job(self, job: Job, group):
        if group is GROUP_A:
            self.sub_task[GROUP_A].append(job)

        if group is GROUP_B:
            self.sub_task[GROUP_B].append(job)

    def destroy_job(self, job: Job, group):
        if group is GROUP_A:
            self.sub_task[GROUP_A].remove(job)

        if group is GROUP_B:
            self.sub_task[GROUP_B].remove(job)