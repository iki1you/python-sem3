from multiprocessing import Process, Manager, Pool


def worker(lst, return_list):
    a = worker_function(map(int, lst[1:-1].split()))
    return_list.append(a)


def main():
    array_2d = input()[1:-1].split(',')
    print(array_2d, end=" ")
    manager = Manager()
    return_list = manager.list()

    processes = []
    for lst in array_2d:
        process = Process(target=worker, args=(lst, return_list))
        processes.append(process)
        process.start()
    for p in processes:
        p.join()
    print(processes, end=" ")


if __name__ == "__main__":
    main()