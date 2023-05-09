# Communication-based-Intersection-Management-Using-Adaptive-Scheduling

# System model

This repository contains two simulation model that with diffrent purpose
1. UPPAL Model that used to verify the puoposed and safety of the proposed system
2. SUMO Model to validate and visualize the merging of job proposed 

## UPPAL Model
This model run on UPPAAL platform. There are the mode to run the model
### 1) Using fix scheduling algorithm
To run on this mode:
1. in system declaration, the "scheduler_" value should be set to "classic()"
2. in declaration file, set the  select_scheduler = 0 and interrupt_mode = 0

### 2) Using Adaptive scheduling algorithm
To run on this mode:
1. in system declaration, the "scheduler_" value should be set to "scheduler()"
2. in declaration file, set the  select_scheduler = 1 and interrupt_mode = 0

### 3) Using Adaptive scheduling algorithm with interrupt (to handle high prioroty job)
To run on this mode:
1. in system declaration, the "scheduler_" value should be set to "scheduler()"
2. in declaration file, set the  select_scheduler = 1 and interrupt_mode = 1

## SUMO Model
This model run on SUMO and python enviroment (Traci Library needed). To run this simulation, execute simulation.py file.


# Evaluation
 for the uppal model, the waiting time can be observed on the value of max_delay_low_p (for low priority job) and max_delay_high_p (for high priority job) during the simulation. The  verification can be done automatically in verifier tab. For the Sumo model, the result of merging process can be seen by observing the served group of vehicle(have the same colour, red and the other colour shows that the vehicle are still waiting)
