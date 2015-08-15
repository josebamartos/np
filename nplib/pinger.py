'''
    Pinger class in nplib library for the np (Network Ping)

    Copyright (C) 2015
    Joseba Martos <joseba@otzarri.net>

    This file is part of np (Network Ping)
    Web site: http://otzarri.net/np

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import netaddr
import subprocess
import threading
try:
    import queue
except ImportError:
    import Queue as queue  # lint:ok


class Pinger:
    '''Pinger object'''

    hosts_up = list()
    hosts_down = list()

    def __init__(self, localnetaddr):
        self.localnet = netaddr.IPNetwork(localnetaddr)
        self.pingqueue = queue.Queue()
        self.count = '1'
        self.hosts_up = list()
        self.hosts_down = list()

    def pinger(self,):
        '''Sends ping'''
        while True:
            ip = str(self.pingqueue.get())
            retcode = subprocess.call("ping -c %s %s" % (self.count, ip),
                                      shell=True,
                                      stdout=open('/dev/null', 'w'),
                                      stderr=subprocess.STDOUT)

            if retcode == 0:
                self.hosts_up.append(netaddr.IPAddress(ip))
                Pinger.hosts_up.append(netaddr.IPAddress(ip))
            else:
                self.hosts_down.append(netaddr.IPAddress(ip))
                Pinger.hosts_down.append(netaddr.IPAddress(ip))

            self.pingqueue.task_done()

    def run(self):
        thread_num = self.localnet.size - 2

        for i in range(thread_num):
            worker = threading.Thread(target=self.pinger)
            worker.daemon = True
            worker.start()

        for ip in self.localnet.iter_hosts():
            self.pingqueue.put(ip)

        self.pingqueue.join()
