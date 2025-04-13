#!/usr/bin/python3

# node and Network confi
# please change 

braodcast_ip = "192.168.20.255"
nodes = []
log_path = "/var/www/html/pow-log/refoss_"

#EM06 node 1
uuid = "241xxxxxxx204740701c4e7xxxxxxxx"
ip = "192.168.20.82"
_node = {"ip":ip,"uuid":uuid,"name":"OG"}
nodes.append(_node)

#EM06 node 2 # option
uuid = "241cccccccc7740701c4e7yyyyyyy"
ip = "192.168.20.81"
_node = {"ip":ip,"uuid":uuid,"name":"EG"}
nodes.append(_node)

#EM06 node 3 # option
