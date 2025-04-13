#!/usr/bin/python3

# node and Network confi
# please change 

log_path = "/var/www/html/pow-log/refoss_"



nodes = []

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
