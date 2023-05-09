from __future__ import print_function
from __future__ import absolute_import
import os
import sys
import optparse
from intersection import *
from global_ import *

if "SUMO_HOME" in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
import traci  # noqa
from sumolib import checkBinary  # noqa


def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                          default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options


binary = 'sumo-gui'
if 'nogui' in sys.argv:
    binary = 'sumo'

################################################ simulation ###########################################################

################## communication ###############

history = []
com_queue = []


def request_simulation():
    for veh in traci.vehicle.getIDList():
        if veh not in history:
            history.append(veh)
            com_queue.append(veh)


################## object ######################

clock = [0, 0]
intersection = Intersection(south_road, north_road, east_road, west_road, com_queue, clock)

################## real time ###################

NUMBER_OF_ROUTE = 8
NUMBER_OF_VEHICLE_ADDED_PER_ROUTE_EVERY_STEP = 2


def run():
    step = 0
    while step < max_simulation_step:
        traci.simulationStep()

        for veh in traci.vehicle.getIDList():
            #print(f"list veh {traci.vehicle.getIDList()}")
            traci.vehicle.setLaneChangeMode(veh, 512)

        step += 1
        clock[0] = traci.simulation.getTime()
        request_simulation()
        intersection.run()

    print(f"Total job: {intersection.calculate_total_serviced_job()}")

    print(f"Total vehicle: {len(history)}")
    print(f"Average waiting time: {intersection.calculate_average_delay()}")
    print(f"Minimum waiting time: {intersection.calculate_min_delay()}")
    print(f"Maximum waiting time: {intersection.calculate_max_delay()}")
    """
    print(f"Total job (high priority): {intersection.calculate_total_serviced_job_p()}")
    print(f"Average waiting time (high priority): {intersection.calculate_average_delay_p()}")
    print(f"Minimum waiting time (high priority): {intersection.calculate_min_delay_p()}")
    print(f"Maximum waiting time (high priority): {intersection.calculate_max_delay_p()}")"""
    traci.close()
    sys.stdout.flush()


################################################ execution ############################################################
# Main entry point
if __name__ == "__main__":
    options = get_options()

    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # traci starts sumo as subprocess and then this script connects and runs

    traci.start([sumoBinary, "-c", "ims.sumocfg",
                 "--tripinfo-output", "tripinfo.xml"])
    run()

# traci.vehicle.add(str(vehID), str(routeID), depart=0+1000*step, pos=0, speed=-1, lane=0, typeID="type1")





""""route = 0
        if False:
            while route < NUMBER_OF_ROUTE:
                veh = 0
                while veh < NUMBER_OF_VEHICLE_ADDED_PER_ROUTE_EVERY_STEP:
                    if route in route_turn_list:
                        pass  # traci.vehicle.add(f"car{vehicle_counter_id}", f"route{route}", departLane=1, typeID="car")
                    else:
                        traci.vehicle.add(f"car{vehicle_counter_id}", f"route{route}", departLane=0, typeID="car")
                    vehicle_counter_id += 1
                    veh += 1
                route += 1
                
                
            traci.route.add("route0", ("E0", "E3"))  # north to south
    traci.route.add("route1", ("E0", "E2"))  # north to west (turn)
    traci.route.add("route2", ("-E1", "E2"))  # east to west
    traci.route.add("route3", ("-E1", "E3"))  # east to north (turn)
    traci.route.add("route4", ("-E3", "-E0"))  # south to north
    traci.route.add("route5", ("-E3", "E2"))  # south to west (turn)
    traci.route.add("route6", ("-E2", "E1"))  # west to east
    traci.route.add("route7", ("-E2", "-E0"))  # west to north (turn)

    vehicle_counter_id = 0
    route_turn_list = [1, 3, 5, 7]"""