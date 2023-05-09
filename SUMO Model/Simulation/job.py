import copy

AVERAGE_CROSS_DURATION = 1


class Job:
    """group of vehicle"""

    def __init__(self, job_id, current_road, direction, clock):
        self.id = job_id
        self.clock = clock
        self.direction = direction
        self.current_road = current_road
        self.vehicle_list = []

        self.duration = None
        self.priority = 0
        self.arrival = None
        self.status = None

        self.t_start = 0
        self.total_delay = 0

    def __setitem__(self, item, data):
        self.vehicle_list[item] = data

    def __getitem__(self, item):
        return self.vehicle_list[item]

    def set_duration(self):
        average_duration_per_vehicle = AVERAGE_CROSS_DURATION
        self.duration = len(self.vehicle_list) * average_duration_per_vehicle

    def set_priority(self):
        for veh_ in self.vehicle_list:
            priority = max(0, veh_.priority)
            self.priority = priority

    def set_arrival(self):
        for veh_ in self.vehicle_list:
            self.arrival = min(40000000, veh_.t_arrival)

    def set_status(self, status):
        self.status = status

    def set_header(self):
        self.header = self.vehicle_list[0].id

    def set_total_delay(self):
        self.total_delay = self.clock[0] - self.arrival

    def set_t_start(self, t_start):
        self.t_start = t_start
