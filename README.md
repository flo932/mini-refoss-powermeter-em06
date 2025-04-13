```
request energy data from refoss powermeter 6channel  
no cloud

SPDX GPL-2.0-only m.rathfelder 2025

some code snipet from  (MIT)
origin	https://github.com/Refoss/refoss-homeassistant.git 

1.chang ip in search.py
x.send(ip="192.168.20.255") # broadcast
to your LAN broadcast ip
x.send(ip="192.168.1.255") # broadcast

2. start 
python3 search.py
- your EM06 responses with some data ...

3. copy default_config.py to config.py
# edit your node's
uuid = "24101ccc6957740701xxxxxxx"
ip = "192.168.20.81"

4. change log path in config.py log_path
log_path = "/var/www/html/pow-log/refoss_"

apendix
- Network

block dns port for refoss powermeter EM06 on the local dns-lxc-container
iptables -A INPUT -i eth0 -s 192.168.20.81 -j DROP -m comment --comment "block-dns refoss powermeter"
iptables -A INPUT -i eth0 -s 192.168.20.82 -j DROP -m comment --comment "block-dns refoss powermeter"


- crontab
 */10    *    *   *   *    python3 /root/refoss/get_power.py
```
