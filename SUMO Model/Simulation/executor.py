import copy
import traci
from global_ import *

class Executor:
    """send instruction to veh"""

    def __init__(self, clock, job_list):
        self.clock = clock
        self.job_list = job_list
        self.executing_jobs = []

    def execute_jobs(self, jobs):
        done = False
        remaining_vehicle = 0
        print(f"in loop: executing jobs {self.executing_jobs}")
        ################################## update executing jobs #####################################
        if jobs is not self.executing_jobs:
            self.executing_jobs = copy.deepcopy(jobs)
            print(f"executing jobs {self.executing_jobs}")

        ################################### set the job to cross #####################################
        for job in self.job_list:
            # only execute jobs that are in executing jobs list
            if job.id in self.executing_jobs:
                # if there is vehicle in job
                if len(job.vehicle_list) > 0:
                    print(f"currently executed job: {job.current_road}")
                    print(f"current job road: {job.current_road}")
                    print(f"there is {len(job.vehicle_list)} vehicle need to be executed in job {job.id}")
                    print(f"The vehicles are {job.vehicle_list} ")
                    # the vehicle is still exist
                    if job.vehicle_list[0].id in traci.vehicle.getIDList():

                        # resume the vehicle from stop
                        job.total_delay = traci.vehicle.getWaitingTime(job.vehicle_list[0].id)
                        print(f"{job.vehicle_list[0].id} is still exist, its current road: {job.vehicle_list[0].road}")

                        # execute the vehicle
                        print(f"resuming {job.vehicle_list[0].id}")
                        if traci.vehicle.isStopped(job.vehicle_list[0].id):
                            print(f"{job.vehicle_list[0].id} is currently stop and executor try to resume it")
                            print(f"set job {job.vehicle_list[0].id} t_start")
                            job.t_start = copy.deepcopy(self.clock[0])

                            traci.vehicle.resume(job.vehicle_list[0].id)
                            traci.vehicle.setSpeed(job.vehicle_list[0].id, START_SPEED)

                        # set car to red, shows that they are about to move
                        for _veh in job.vehicle_list:
                            if _veh.id in traci.vehicle.getIDList():
                                traci.vehicle.setSpeed(job.vehicle_list[0].id, START_SPEED)
                                traci.vehicle.setColor(_veh.id, [255, 0, 0, 255])
                else:
                    # remove the jobs from executing job list if there is no vehicle in the jobs
                    # self.job_list.remove(job) # will be removed by scheduler
                    pass

                # remove car from job list if it is already cross
                for veh in job.vehicle_list:
                    # the vehicle is still exist
                    if veh.id in traci.vehicle.getIDList():
                        print(f"{job.vehicle_list[0].id} is still exist, it current road: {job.vehicle_list[0].road}")
                        # the vehicle already cross the junction
                        if traci.vehicle.getRoadID(veh.id) != job.current_road:
                            print(f"{veh.id} already cross")
                            print(f"removing {veh.id} from list because it already cross")
                            # remove vehicle from job list if it is already cross
                            job.vehicle_list.remove(veh)

                remaining_vehicle += len(job.vehicle_list)

            print(f"remaining vehicle in job {job.id}: {remaining_vehicle}")

        ################################### if the job is finished #####################################
        if remaining_vehicle <= 0:
            done = True

        return done
