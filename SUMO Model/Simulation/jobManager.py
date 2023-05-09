from intersection import *
import traci
import random
from global_ import interrupt as interrupt_
import global_
class JobManager:
    """create job (vehicle grouping) and merged jobs if needed"""

    def __init__(self, job_list, clock, get_direction, executor, delay_data,delay_data_high_priority):
        self.job_list = job_list
        self.get_direction = get_direction
        self.clock = clock
        self.executor = executor

        self.counter = 0
        self.executing_job = []
        self.working_job_id = None

        self.job_p = None
        self.done_interrupt = False

        self.delay_data = delay_data
        self.delay_data_high_priority = delay_data_high_priority

    def update_job_list(self, vehicle_list):
        "if there is new vehicle in queue, it will put it in a job and merge with previous suitable job if possible"
        # print(f"initial veh {vehicle_list}")
        merging = False
        gap = 100000
        print(f"vehicle_list {vehicle_list}")
        for veh in vehicle_list:
            if veh is not None:
                print(f"taking veh: {veh.id}")
                ################################## create job buffer #####################################
                current_road = veh.road
                next_road = veh.next_road
                direction = self.get_direction(current_road, next_road)
                veh.direction = direction
                job = Job(self.counter, current_road, direction, self.clock)
                self.working_job_id = job.id
                ####################################  initialize ##########################################
                self.counter += 1
                # transfer from global vehicle queue to vehicle list in job
                job.vehicle_list.append(copy.deepcopy(veh))
                vehicle_list.remove(veh)
                job.set_duration()
                job.set_priority()
                job.set_arrival()
                job.set_status(STOP)

                ################################ try to merge with previous job ###########################
                print(f"buffer job id {self.counter} with vehicle list: {job.vehicle_list}, current road: {job.current_road}, direction: {job.direction}")
                for job_ in self.job_list:
                    print(f"examine job {job_.id}. current road: {job_.current_road}, current direction: {job_.direction}, status {job_.status}")
                    # condition to merge: (1) same current road (2) same direction (3) only merge with stopped job (4) total duration is acceptable (5) small gap
                    if job.current_road == job_.current_road:
                        if job.direction == job_.direction:
                            if job_.status == STOP:
                                print(f"try to merge job {job.id} and {job_.id}")

                                if (job_.duration + job.duration + JOB_GAP_DURATION) < MAX_JOB_DURATION:
                                    self.working_job_id = job_.id
                                    for veh_b in job_.vehicle_list:
                                        distance = traci.vehicle.getLanePosition(job.vehicle_list[0].id) - traci.vehicle.getLanePosition(veh_b.id)
                                        gap = min(gap, distance)

                                    if gap < 5:  # no vehicle in between
                                        print(f"small gap detected")
                                        merging = True

                                        # if merge is possible, reset all value
                                        job_.vehicle_list.extend(copy.deepcopy(job.vehicle_list))
                                        job_.set_duration()
                                        job_.set_priority()
                                        job_.set_arrival()
                                        # traci.vehicle.setColor(job_.vehicle_list[0].id, [0, 255, 255, 0])
                                    else:
                                        print(
                                            f"merging process failed. gap is {gap}")
                                else:
                                    print(
                                        f"merging process failed. Total duration if merge: {job_.duration + job.duration}")
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass

                if not merging:
                    print(f"merging is not possible. new job created with id {self.counter}")
                    # set to stop the first vehicle
                    job.vehicle_list[0].set_stop()
                    # unified job colour
                    for veh_ in job.vehicle_list:
                        traci.vehicle.setColor(veh_.id, [random.randrange(256), random.randrange(256), random.randrange(256), 255])
                        print(f"colouring vehicle {veh_}")
                    # add job to job list
                    self.job_list.append(job)
                else:
                    pass

        if global_.PRIORITY_USE_CASE:
            self.priority_check(interrupt_)

##################################### PRIORITY_USE_CASE ################################
    def priority_check(self, interrupt):
        working_job = None
        job_buffer = []
        # no interrupt is cunrrently running
        if not interrupt:
            print("jdgbjdfgbjdfhgjdfhgkjdfg")
            # get new job id
            print(f"PRIORITY_USE_CASE: working job id {self.working_job_id}")
            for j in self.job_list:
                if j.id == self.working_job_id:
                    working_job = j
                else:
                    pass

        if working_job is not None:
            if working_job.priority > 0:
                print("#################################################################################  handling interrupt")
                interrupt = 1
                working_current_road = working_job.current_road
                working_direction = working_job.direction
                print(f"Job with priority {working_job.priority} detected")
                # collect all job with the same lane and direction

                for _job in self.job_list:
                    if _job.current_road == working_job.current_road:
                        if _job.direction == working_job.direction:
                            job_buffer.append(copy.deepcopy(_job))

                            # remove the job from job list
                            self.job_list.remove(_job)
                            # _job.vehicle_list.clear()

                # merge the job
                print(f"forced merging jobs {job_buffer}")
                self.job_p = Job(self.counter, working_current_road, working_direction, self.clock)
                status = STOP

                for _job in job_buffer:
                    self.job_p.vehicle_list.extend(copy.deepcopy(_job.vehicle_list))
                    self.job_p.set_duration()
                    self.job_p.set_priority()
                    self.job_p.set_arrival()
                    if self.job_p.arrival is None:
                        self.job_p.arrival = 0
                    print(f"####################################################################################################################################  {self.job_p.arrival}")
                    # continue moving if one of the job is currently moving
                    if _job.status == MOVE:
                        status = MOVE
                        self.job_p.t_start = self.clock[0]
                    # this id is currently used by the scheduler. choose the minimum one (the earliest)
                    self.job_p.id = min(self.job_p.id, _job.id)

                self.job_p.status = status
                print(f"status of job {self.job_p.id} with priority 1: {status}")

                # put the job in job list
                self.job_list.append(self.job_p)

                # add job to execute list
                self.executing_job.append(self.job_p.id)

                # executing the job pair
                if self.job_p.current_road in north_road:
                    for j in self.job_list:
                        if j.current_road in south_road:
                            if j.status != MOVE:
                                j.t_start = self.clock[0]
                                self.executing_job.append(j.id)
                elif self.job_p.current_road in south_road:
                    for j in self.job_list:
                        if j.current_road in north_road:
                            if j.status != MOVE:
                                j.t_start = self.clock[0]
                                self.executing_job.append(j.id)
                elif self.job_p.current_road in east_road:
                    for j in self.job_list:
                        if j.current_road in west_road:
                            if j.status != MOVE:
                                j.t_start = self.clock[0]
                                self.executing_job.append(j.id)
                elif self.job_p.current_road in west_road:
                    for j in self.job_list:
                        if j.current_road in west_road:
                            if j.status != MOVE:
                                j.t_start = self.clock[0]
                                self.executing_job.append(j.id)
            else:
                pass
        else:
            pass

        if interrupt:
            self.done_interrupt = self.executor.execute_jobs(self.executing_job)
            if self.done_interrupt:
                self.done_interrupt = False
                interrupt = False
                print(f"job list ({len(self.job_list)}) before removing job: {self.job_list}")
                for j in self.job_list:
                    if j.id in self.executing_job:
                        j.total_delay = j.t_start - j.arrival
                        self.delay_data.append(copy.deepcopy(j.total_delay))
                        if j.priority > 0:
                            self.delay_data_high_priority.append(j.total_delay)
                        print(f"removing job {j.id} with {len(j.vehicle_list)} vehicles")
                        self.job_list.remove(j)
                        self.executing_job.remove(j.id)
                print(f"job list ({len(self.job_list)}) after removing job: {self.job_list}")
                self.executing_job = []

                print("#################################################################################  finish interrupt")


