STRAIGHT = 0
TURN = 1

STOP = 0
MOVE = 1

MAX_JOB_DURATION = 16
JOB_GAP_DURATION = 1

PRIORITY_USE_CASE = False

START_SPEED = 20
high_priority_list = ["ev"]

max_simulation_step = 1000

north_road = ['E0', '-E0']
south_road = ['-E3', 'E3']
east_road = ['E1', '-E1']
west_road = ['E2', '-E2']

# used by the system to stop scheduler in order to handle interrupt. Should not be changed
interrupt = False
select_task = None