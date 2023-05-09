from taskManager import *
import global_


class Scheduler:
    """"execute each job from each subtask from each task"""

    def __init__(self, job_list, southToNorthNorthToSouth, southToWestNorthToEast, westToEastEastToWest,
                 westToNorthEastToSouth, executor, clock, delay_data, delay_data_high_priority):

        self.southToNorthNorthToSouth = southToNorthNorthToSouth
        self.southToWestNorthToEast = southToWestNorthToEast
        self.westToEastEastToWest = westToEastEastToWest
        self.westToNorthEastToSouth = westToNorthEastToSouth
        self.executor = executor
        self.job_list = job_list
        self.clock = clock

        self.task_set = [southToNorthNorthToSouth, southToWestNorthToEast, westToEastEastToWest, westToNorthEastToSouth]
        self.executing_job = []
        self.executing = False
        self.state = 0

        self.delay_data = delay_data
        self.delay_data_high_priority = delay_data_high_priority

    def __setitem__(self, item, data):
        self.executing_job[item] = data

    def __getitem__(self, item):
        return self.executing_job[item]

    def execute(self, task):
        # run current task until the job is finished
        change_state = False

        # set jobs status to move and put them in executing list
        if len(task[GROUP_A]) > 0:
            if task[GROUP_A][0] is not None:
                if task[GROUP_A][0].status is not MOVE:
                    job_id = task[GROUP_A][0].id
                    task[GROUP_A][0].status = MOVE
                    self.executing_job.append(job_id)

        if len(task[GROUP_B]) > 0:
            if task[GROUP_B][0] is not None:
                if task[GROUP_B][0].status is not MOVE:
                    job_id = task[GROUP_B][0].id
                    task[GROUP_B][0].status = MOVE
                    self.executing_job.append(job_id)

        if not interrupt:
            # if all job are finish remove all executed jobs, otherwise continue in the next loop
            done = self.executor.execute_jobs(self.executing_job)

            if done:
                print(f"job list ({len(self.job_list)}) before removing job: {self.job_list}")
                if len(task[GROUP_B]) > 0:
                    if task[GROUP_B][0].id in self.executing_job:
                        print(f"job {task[GROUP_B][0].id} done!!!")
                        # calculate job's total delay
                        #task[GROUP_B][0].total_delay = task[GROUP_B][0].t_start - task[GROUP_B][0].arrival
                        # store the delay
                        self.delay_data.append(copy.deepcopy(task[GROUP_B][0].total_delay))
                        if task[GROUP_B][0].priority > 0:
                            self.delay_data_high_priority.append(task[GROUP_B][0].total_delay)
                        # remove from executing list
                        self.executing_job.remove(task[GROUP_B][0].id)
                        # remove from job list
                        self.job_list.remove(task[GROUP_B][0])
                        # remove from task job list
                        print(f"removing job {task[GROUP_B][0].id} with {len(task[GROUP_B][0].vehicle_list)} vehicles")
                        task[GROUP_B].remove(task[GROUP_B][0])

                if len(task[GROUP_A]) > 0:
                    if task[GROUP_A][0].id in self.executing_job:
                        print(f"job {task[GROUP_A][0].id} done!!!")
                        # calculate job's total delay
                        task[GROUP_A][0].total_delay = task[GROUP_A][0].t_start - task[GROUP_A][0].arrival
                        # store the delay
                        self.delay_data.append(copy.deepcopy(task[GROUP_A][0].total_delay))
                        if task[GROUP_A][0].priority > 0:
                            self.delay_data_high_priority.append(task[GROUP_A][0].total_delay)
                        # remove from executing list
                        self.executing_job.remove(task[GROUP_A][0].id)
                        # remove from job list
                        self.job_list.remove(task[GROUP_A][0])
                        # remove from task job list
                        print(f"removing job {task[GROUP_A][0].id} with {len(task[GROUP_A][0].vehicle_list)} vehicles")
                        task[GROUP_A].remove(task[GROUP_A][0])
                # reset executing job list
                self.executing_job = []
                print(f"job list ({len(self.job_list)}) after removing job: {self.job_list}")
                # time to execute job from the next task
                change_state = True

        return change_state

    def activate(self):
        """run scheduler in loop"""
        match self.state:
            case 0:
                global_.select_task = 0
                print(f"Executing Task 0")
                done = self.execute(self.southToNorthNorthToSouth)
                if done:
                    self.state = 1

            case 1:
                global_.select_task = 1
                print(f"Executing Task 1")
                done = self.execute(self.southToWestNorthToEast)
                if done:
                    self.state = 2

            case 2:
                global_.select_task = 3
                print(f"Executing Task 2")
                done = self.execute(self.westToEastEastToWest)
                if done:
                    self.state = 3

            case 3:
                global_.select_task = 4
                print(f"Executing Task 3")
                done = self.execute(self.westToNorthEastToSouth)
                if done:
                    self.state = 0
