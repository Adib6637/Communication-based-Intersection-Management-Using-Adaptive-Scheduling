import traci


class Vehicle:
    """representation of vehicle in sumo"""

    def __init__(self, veh_id, priority, road, next_road, t_arrival, direction):
        print(f"request from vehicle {veh_id}")
        self.id = veh_id
        self.priority = priority
        self.road = road
        self.next_road = next_road
        self.direction = direction
        self.t_arrival = t_arrival
        self.waiting_time = None

    def set_stop(self):
        print(f"{self.id} stopping with direction {self.direction}")
        traci.vehicle.setStop(self.id, self.road, traci.lane.getLength(f"{self.road}_0") - 5)
