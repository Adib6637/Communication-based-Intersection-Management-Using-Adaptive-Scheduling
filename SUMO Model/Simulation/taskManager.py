from jobManager import *
from global_ import *


class TaskManager:
    """mapping job to a specific task"""

    def __init__(self, job_list, road_set, southToNorthNorthToSouth: Task, southToWestNorthToEast: Task, westToEastEastToWest: Task, westToNorthEastToSouth: Task):
        self.counter = 0
        self.job_list = job_list
        self.road_set = road_set
        self.south_road = road_set[0]
        self.north_road = road_set[1]
        self.east_road = road_set[2]
        self.west_road = road_set[3]
        self.southToNorthNorthToSouth = southToNorthNorthToSouth
        self.southToWestNorthToEast = southToWestNorthToEast
        self.westToEastEastToWest = westToEastEastToWest
        self.westToNorthEastToSouth = westToNorthEastToSouth
        self.task_set = [southToNorthNorthToSouth, southToWestNorthToEast, westToEastEastToWest, westToNorthEastToSouth]

    def update_task(self):
        """"remapping job that is stop to an appropriate task"""
        # collect running job
        running_job = []
        for job in self.job_list:
            if job.status is MOVE:
                running_job.append(job)

        # remove all job in task that are not running
        for task in self.task_set:
            for subtask in task:
                for job in subtask:
                    if job in running_job:
                        pass
                    else:
                        subtask.remove(job)

        print(f"Running job ({len(running_job)}) : {running_job}")

        # add all job to appropriate task
        for job in self.job_list:
            if job.status is not MOVE:
                # southToNorthNorthToSouth
                if (job.current_road in self.south_road) and (job.direction is STRAIGHT):
                    self.southToNorthNorthToSouth.sub_task[GROUP_A].append(job)

                if (job.current_road in self.north_road) and (job.direction is STRAIGHT):
                    self.southToNorthNorthToSouth.sub_task[GROUP_B].append(job)

                # southToWestNorthToEast
                if (job.current_road in self.south_road) and (job.direction is TURN):
                    self.southToWestNorthToEast.sub_task[GROUP_A].append(job)

                if (job.current_road in self.north_road) and (job.direction is TURN):
                    self.southToWestNorthToEast.sub_task[GROUP_B].append(job)

                # westToEastEastToWest
                if (job.current_road in self.west_road) and (job.direction is STRAIGHT):
                    self.westToEastEastToWest.sub_task[GROUP_A].append(job)

                if (job.current_road in self.east_road) and (job.direction is STRAIGHT):
                    self.westToEastEastToWest.sub_task[GROUP_B].append(job)

                # westToNorthEastToSouth
                if (job.current_road in self.west_road) and (job.direction is TURN):
                    self.westToNorthEastToSouth.sub_task[GROUP_A].append(job)

                if (job.current_road in self.east_road) and (job.direction is TURN):
                    self.westToNorthEastToSouth.sub_task[GROUP_B].append(job)
