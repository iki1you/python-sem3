import cProfile
import pstats

def slow_code():
    iterator = 0
    for i in range(10000001):
        iterator += i

def slow_code2():
    iterator = 0
    for i in range(100000):
        iterator += i

def slow_code3():
    iterator = 0
    for i in range(100000):
        iterator += i

def slow_code4():
    iterator = 0
    for i in range(1000001):
        iterator += i

def slow_code5():
    iterator = 0
    for i in range(1000011):
        iterator += i


TASK_FUNCTIONS_ORDER = ['slow_code', 'slow_code2', 'slow_code3', 'slow_code4', 'slow_code5']

profiler = cProfile.Profile()
for i in TASK_FUNCTIONS_ORDER:
    profiler.run(i + '()')

stats = pstats.Stats(profiler).sort_stats('name').get_stats_profile()
total_time = stats.total_tt
for i in stats.func_profiles:
    time = stats.func_profiles[i].cumtime
    print(f'{round(time, 4)}: {round(time / total_time * 100)}%')

