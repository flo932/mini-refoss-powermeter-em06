```
request energy data from refoss powermeter 6channel  
no cloud

SPDX GPL-2.0-only m.rathfelder 2025

some code snipet from  (MIT)
origin	https://github.com/Refoss/refoss-homeassistant.git 

0. copy default_config.py to config.py

1.change broadcast ip in config.py
  braodcast_ip = "192.168.20.255"
  to your LAN broadcast ip
  braodcast_ip = "192.168.1.255"

2. execute >> python3 search.py
  - your EM06 responses with some data ...
  - append result from search.py in config.py
     # append in your config.py 
     _node = {'ip': '192.168.20.xx', 'uuid': 'xxxxxxxxxxxxxxx', 'name': 'floor1'}
     nodes.append(_node)

3. test get_power.py
  - shoud return powerdata from your EM06 nodes
    0 {'stamp': '2025-04-13 12:33:11', 'name': 'OG', 'CH': 1, 'A': 0.0, 'V': 229.46, 'W': 0.0, 'kWh': 0.76, 'fa': 0}
    ....
    ....

4. change log path in config.py log_path
  log_path = "/var/www/html/pow-log/refoss_"

5. add cronjob like every 10minute
    */10    *    *   *   *    python3 /root/refoss/get_power.py





apendix / option - Network

#block dns port for refoss powermeter EM06 on the local dns-lxc-container
iptables -A INPUT -i eth0 -s 192.168.20.81 -j DROP -m comment --comment "block-dns refoss powermeter"
iptables -A INPUT -i eth0 -s 192.168.20.82 -j DROP -m comment --comment "block-dns refoss powermeter"
```
