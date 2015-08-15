'''
    NetDiscover class in nplib library for the np (Network Ping)

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
import netifaces
import sys


class NetDiscover():

    ifaces = list()
    ifaces_excluded = ['lo']  # Excluding loopback interface
    networks = list()

    @staticmethod
    def iface_discover():
        '''If the interface list self.ifaces is empty, it discovers the
        network interfaces in the host and adds them to the list'''
        if len(NetDiscover.ifaces) < 1:
            NetDiscover.ifaces = netifaces.interfaces()
            for iface in NetDiscover.ifaces_excluded:
                if iface in NetDiscover.ifaces:
                    NetDiscover.ifaces.remove(iface)

    @staticmethod
    def link_checker():
        '''Checks if the interfaces listed in NetDiscover.ifaces are linked and
        returns the linked ones.'''
        NetDiscover.iface_discover()

        for iface in NetDiscover.ifaces:
            carrier_path = '/sys/class/net/' + iface + '/carrier'
            carrier_file = open(carrier_path, 'r')
            try:
                carrier_status = carrier_file.read().strip()
            except IOError:
                carrier_status = '0'
            if carrier_status == '0':
                NetDiscover.ifaces.remove(iface)

    @staticmethod
    def ip_checker():
        '''Checks if the interfaces listed in NetDiscover.ifaces have an IP
        address assigned on a network and deletes from list the interfaces that
        do not have assigned an IP address.'''
        NetDiscover.iface_discover()

        for iface in NetDiscover.ifaces:
            if 2 not in netifaces.ifaddresses(iface):
                NetDiscover.ifaces.remove(iface)

    @staticmethod
    def discover_working_ifaces():
        '''Calls NetDiscover.link_checker and NetDiscover.ip_checker to set in
        the interface list NetDiscover.ifaces only the interfaces that are
        working in a network. When detects more than one interface, asks if the
        user wants to use only one of them or all for pinging the networks'''

        NetDiscover.link_checker()
        NetDiscover.ip_checker()

        if len(NetDiscover.ifaces) < 1:
            print('No interface connected to any network')
            sys.exit(1)

        if len(NetDiscover.ifaces) > 1:
            iface = None
            while iface != 'All' and iface not in NetDiscover.ifaces:
                print('\nThe following interfaces are connected to a network:')
                print(('\n'.join(NetDiscover.ifaces)))
                iface = raw_input("\nSelect one of them or type All: ")
                if iface != 'All':
                    del NetDiscover.ifaces[:]
                    NetDiscover.ifaces.append(iface)

    @staticmethod
    def discover_working_networks():
        '''Calls NetDiscover.get_working_ifaces() for setting in the interface
        list NetDiscover.ifaces only the working interfaces and adds the
        working networks to the network list NetDiscover.networks'''

        NetDiscover.discover_working_ifaces()

        for iface in NetDiscover.ifaces:
            address = netifaces.ifaddresses(iface)[2][0]['addr']
            netmask = netifaces.ifaddresses(iface)[2][0]['netmask']
            NetDiscover.networks.append(
                str(netaddr.IPNetwork(address, netmask)))
