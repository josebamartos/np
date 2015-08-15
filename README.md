# np (Network Ping)
np (Network Ping) is a tool for quick discovery of alive hosts in the network. Automatically detects the networks where our machine is connected and sends pings simultaneously to each existing IP address in the selected networks. Returns a list of alive hosts.

Project home: http://otzarri.net/np

| Technical        | Specs              |
| ---------------- | ------------------ |
| Language         | Python 2.7         |
| Operating system | GNU/Linux          |
| Tested distros   | Debian, Ubuntu     |
| Required modules | netaddr, netifaces |

## Installation

Dependency installation via pip:

```
# pip install netifaces netaddr
```

Dependency installation via apt in Debian/Ubuntu:

```
# apt-get install python-netifaces python-netaddr
```

Cloning np from GitHub:

```
$ git clone https://github.com/josebamartos/np.git
```

Running np:

```
$ cd np
$ ./np

The following interfaces are connected to a network:
eth0
wlan0

Select one of them or type All: wlan0

Hosts alive (all):
192.168.1.1
192.168.1.48
192.168.1.51
```

## Benchmarking

| Command                       | Seconds | Comments                    |
| ----------------------------- | -------:| --------------------------- |
| np                            |   4.102 | Automatic address detection |
| nmap -sP 192.168.1.1-255      |   6.591 | Range must be set manually  |
| fping -a -q -g 192.168.1.0/24 |  26.946 | Range must be set manually  |
