from subprocess import Popen, PIPE, STDOUT,call
from multiprocessing import Pool


def telnet(port):
	#cmd = "timeout %d telnet localhost %d"%(timeout,port)
        timeout = 60
        p = call(["telnet","localhost","%d"%port])
        print "SHIT"
        return p



if __name__ == '__main__':
        pool = Pool(processes=10)
        port = 10000
        r = [pool.apply_async(telnet,args=(port,)) for x in range(1,10)]
        # print pool.map(f, range(10))
        output = [p.get() for p in r]
        #pool.close()
        #pool.join()
        #pool.wait()
        #print(output)
