#!/usr/bin/python

from mininet.log import setLogLevel, info
from subprocess import call

from topologies.simple_topology import SimpleTopology
from topologies.cpu_limited import CpuLimitedTopology

import sdnlb_conf

if __name__ == '__main__':
    setLogLevel( 'info' )

    switchIp = sdnlb_conf.switch_ip
    switchMac = sdnlb_conf.switch_mac

    while 1:
        cmd = raw_input("topology:")

        if(cmd == "help"):
            print "Available topologies:"
            print "For simple topology: type in 'simple'"
            print "For cpu limited topology: type in 'cpu'"
            print "For delayed links topology: type in 'link'"
            continue


        elif(cmd == "quit"):
	    call(["sudo", "mn","-c"]) # clean up mininet
            break
            
        elif(cmd == "simple"):
            SimpleTopology(switchIp,switchMac)

        elif(cmd == "cpu"):
            CpuLimitedTopology(switchIp,switchMac)
        else:
            print "unknown command:%s"%cmd

        call(["sudo", "mn","-c"]) # clean up mininet
        
        


