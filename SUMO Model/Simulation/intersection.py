from requestHandler import *
from job import *
from task import *
from vehicle import *
from jobManager import *
from taskManager import *
from executor import *
from scheduler import *
from global_ import *


class Intersection:
    def __init__(self, south_road, north_road, east_road, west_road, com_queue, clock):
        self.south_road = south_road
        self.north_road = north_road
        self.east_road = east_road
        self.west_road = west_road
        self.road_set = [south_road, north_road, east_road, west_road]

        self.vehicle_list = []
        self.job_list = []

        self.delay_data = []
        self.delay_data_high_priority = []

        self.clock = clock

        self.southToNorthNorthToSouth = Task()
        self.southToWestNorthToEast = Task()
        self.westToEastEastToWest = Task()
        self.westToNorthEastToSouth = Task()

        self.executor = Executor(clock, self.job_list)
        self.executor2 = Executor(clock, self.job_list)

        self.request_handler = RequestHandler(com_queue, self.vehicle_list, self.get_direction, self.clock)
        self.job_manager = JobManager(self.job_list, self.clock, self.get_direction, self.executor, self.delay_data, self.delay_data_high_priority)
        self.task_manager = TaskManager(self.job_list, self.road_set, self.southToNorthNorthToSouth,
                                        self.southToWestNorthToEast, self.westToEastEastToWest,
                                        self.westToNorthEastToSouth)
        self.scheduler = Scheduler(self.job_list, self.southToNorthNorthToSouth, self.southToWestNorthToEast,
                                   self.westToEastEastToWest,
                                   self.westToNorthEastToSouth, self.executor, clock, self.delay_data, self.delay_data_high_priority)

    def get_direction(self, current_road, next_road) -> int:
        if ((current_road in self.south_road) and (next_road in self.north_road)) or (
                (current_road in self.north_road) and (next_road in self.south_road)) or (
                (current_road in self.west_road) and (next_road in self.east_road)) or (
                (current_road in self.east_road) and (next_road in self.west_road)):
            return STRAIGHT

        else:
            return TURN

    def run(self):
        self.request_handler.listen_to_request()
        self.job_manager.update_job_list(self.vehicle_list)
        self.task_manager.update_task()
        self.scheduler.activate()

    def get_current_vehicle_number(self):
        total_veh = 0
        for job in self.job_list:
            for veh in job.vehicle_list:
                total_veh += 1
        print(f"Total vehicle in sumo: {len(traci.vehicle.getIDList())}, total vehicle in jobs: {total_veh}")

    def calculate_total_serviced_job(self):
        return len(self.delay_data)
    def calculate_average_delay(self):
        average_delay = 0
        for delay in self.delay_data:
            average_delay += delay
        return average_delay/len(self.delay_data)

    def calculate_min_delay(self):
        min_delay = None
        for delay in self.delay_data:
            # initialize
            if min_delay is None:
                min_delay = delay
            else:
                min_delay = min(min_delay, delay)
        return min_delay

    def calculate_max_delay(self):
        max_delay = 0
        for delay in self.delay_data:
            max_delay = max(max_delay, delay)
        return max_delay

    def calculate_average_delay_p(self):
        average_delay = 0
        for delay in self.delay_data_high_priority:
            average_delay += delay
        return average_delay/len(self.delay_data)

    def calculate_min_delay_p(self):
        min_delay = None
        for delay in self.delay_data_high_priority:
            # initialize
            if min_delay is None:
                min_delay = delay
            else:
                min_delay = min(min_delay, delay)
        return min_delay

    def calculate_max_delay_p(self):
        max_delay = 0
        for delay in self.delay_data_high_priority:
            max_delay = max(max_delay, delay)
        return max_delay

    def calculate_total_serviced_job_p(self):
        return len(self.delay_data_high_priority)
