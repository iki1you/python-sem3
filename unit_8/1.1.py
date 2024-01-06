import cProfile
from functions_to_profile import load_files, read_database, get_id, get_user_data, generate_words


TASK_FUNCTIONS_ORDER = ['load_files', 'read_database', 'get_id', 'get_user_data', 'generate_words']

profiler = cProfile.Profile()
profiler.enable()
load_files()
read_database()
get_id()
get_user_data()
generate_words()
profiler.create_stats()
profiler.disable()

stats = profiler.stats
time = []
for i in stats:
    if i[2] in TASK_FUNCTIONS_ORDER:
        time.append(stats[i][2])


total_time = sum(time)
for i in time:
    if "{n:.{d}f}".format(n=i, d=4) == 0.0001:
        print(2)
    else:
        print(f'{"{n:.{d}f}".format(n=i, d=4)}: {round((i / total_time if i != 0 else 0 * 100) * 100)}%')
