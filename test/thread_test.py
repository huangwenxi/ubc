import threading
from time import sleep,ctime

loops = [4, 2]

def loop(nloop, nsec):
    print 'start loop', nloop, 'at:',ctime()
    sleep(nsec)
    print 'start loop', nloop, 'done at:', ctime()

def main():
    print 'starting at:', ctime()
    threads = []
    nloops = range(len(loops))

    print nloops
    for i in nloops:
        t = threading.Thread(target=loops,
                             args=(i, loops[i]))
        threads.append(t)

    for i in nloops:
        threads[i].start()

    for i in nloops:
        threads[i].join()

    print 'all DONE at:', ctime()

if __name__ == '__main__':
    main()

















