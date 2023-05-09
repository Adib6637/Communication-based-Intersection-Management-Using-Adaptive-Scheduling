import traci

from vehicle import *
from global_ import *


class RequestHandler:
    """receive request from incoming vehicle and put them in vehicle queue"""

    def __init__(self, com_queue, veh_queue, get_direction, clock):
        self.com_queue = com_queue
        self.veh_queue = veh_queue
        self.get_direction = get_direction
        self.clock = clock

    def listen_to_request(self):
        for veh in self.com_queue:
            if veh is not None:
                self.add_vehicle_to_queue(veh)
                self.com_queue.remove(veh)

    def add_vehicle_to_queue(self, veh):
        self.veh_queue.append(Vehicle(veh, self.get_vehicle_priority(veh), self.get_vehicle_road(veh), self.get_vehicle_next_road(veh), self.get_vehicle_t_arrival(veh), self.get_direction(self.get_vehicle_road(veh), self.get_vehicle_next_road(veh))))

    @staticmethod
    def get_vehicle_road(veh):
        return traci.vehicle.getRoadID(veh)

    @staticmethod
    def get_vehicle_next_road(veh):
        return traci.vehicle.getRoute(veh)[1]

    @staticmethod
    def get_vehicle_priority(veh):
        if traci.vehicle.getTypeID(veh) in high_priority_list:
            return 1
        else:
            return 0

    def get_vehicle_t_arrival(self, veh):
        t_arrival = self.clock[0] + (traci.vehicle.getLanePosition(veh)-traci.lane.getLength(f"{self.get_vehicle_road(veh)}_0"))/10  # traci.vehicle.getSpeed(veh)
        return t_arrival
