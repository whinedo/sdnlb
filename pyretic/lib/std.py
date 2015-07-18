################################################################################
# The Pyretic Project                                                          #
# frenetic-lang.org/pyretic                                                    #
# author: Joshua Reich (jreich@cs.princeton.edu)                               #
################################################################################
# Licensed to the Pyretic Project by one or more contributors. See the         #
# NOTICES file distributed with this work for additional information           #
# regarding copyright and ownership. The Pyretic Project licenses this         #
# file to you under the following license.                                     #
#                                                                              #
# Redistribution and use in source and binary forms, with or without           #
# modification, are permitted provided the following conditions are met:       #
# - Redistributions of source code must retain the above copyright             #
#   notice, this list of conditions and the following disclaimer.              #
# - Redistributions in binary form must reproduce the above copyright          #
#   notice, this list of conditions and the following disclaimer in            #
#   the documentation or other materials provided with the distribution.       #
# - The names of the copyright holds and contributors may not be used to       #
#   endorse or promote products derived from this work without specific        #
#   prior written permission.                                                  #
#                                                                              #
# Unless required by applicable law or agreed to in writing, software          #
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT    #
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the     #
# LICENSE file distributed with this work for specific language governing      #
# permissions and limitations under the License.                               #
################################################################################

"""Pyretic Standard Library"""
from pyretic.core.language import StaticPolicy, DerivedPolicy, identity, all_packets, passthrough, no_packets, match, parallel
import pyretic.core.util as util
from datetime import datetime

### DEFINITIONS
ARP_TYPE = 2054


### BREAKPOINT policy

class breakpoint(DerivedPolicy):
    def eval(self, pkt):
        if self.policy.eval(pkt):
            try:
                import ipdb as debugger
            except:
                import pdb as debugger
            debugger.set_trace()
        return {pkt}

    def __repr__(self):
        return "***breakpoint on %s***" % util.repr_plus([self.policy])


### CONVENIENCE policies

class _in(DerivedPolicy):
    def __init__(self,field,group):
        self.group = group
        self.field = field
        super(_in,self).__init__(parallel([match({field : i}) 
                                for i in group]))
    def __repr__(self):
        return "_in: %s" % self.group


class switch_in(_in):
    def __init__(self,switches):
        super(switch_in,self).__init__('switch',switches)

    def __repr__(self):
        return "switch%s" % super(switch_in,self).__repr__()


class dstip_in(_in):
    def __init__(self,dstips):
        super(dstip_in,self).__init__('dstip',dstips)

    def __repr__(self):
        return "dstip%s" % super(dstip_in,self).__repr__()


### PRINTING policies

class _print(StaticPolicy):
    def __init__(self,s=''):
        self.s = s
        super(_print,self).__init__()

    def __repr__(self):
        return "[%s %s]" % (self.name(),self.s)


class str_print(_print):
    def eval(self, pkt):
        print str(datetime.now()),
        print " | ",
        print self.s
        return set()


class pkt_print(_print):
    def eval(self, pkt):
        if self.s != '':
            print "---- %s -------" % self.s
        print str(datetime.now())
        print pkt
        if self.s != '':
            print "-------------------------------"
        return set()


class topo_print(_print):
    def print_fn(self, pkt):
        if self.s != '':
            print "---- %s -------" % self.s
        print str(datetime.now())
        print self.network.topology
        if self.s != '':
            print "-------------------------------"
        return set()
