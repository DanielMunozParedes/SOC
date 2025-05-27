level 1 dectection.

---------------------------

show setup image 1 here

setup of the soc machine . custom built upon xubuntu with SIEM wazuh,wiresahrk and suricata IDS and evebox to visualize. promiscous mode. Not that realistic, since for example tools like suricata or zeek are to be deployed behind the firewall. I must say i have suricata isntalled on the pfsense direclty, but for practical uses i will focus on the promiscous mode for the learning on hwo to use the suricata tool
also for context this machine, that works as a wazuh server, has a wazuh agent on ubuntu desktop target machine already

-------------------------

image 2

setup o nthe machine ubuntu desktop, using syslog with arpwatch filtering the word arpwatch, arp table on view and my custom script to detect changes o nthe arp table

everithing normal so far

-------------------------


image 3

image to show the agent ubuntu

-----------------------

image 4

attack begins


--------------------

image 5

inmediatly alerts start to be triggered on the agent. we can distinguish ,among obvious things thanks for the alerts, the arp has 2 ip addresses with the  same mac address

arpwatch detected the change and the flip flop was registered on the syslog  at 2025 - 05 - 26  23:08:30.3444

-----------------

image 6

pfsense arp table is changed too, the attack is full duplex host to attacker, attacker to gateway

---------------

image 7

wireshark shows suspicious behavior. multiple arp replies in a short time window
all coming to say the gateway ip is at different mac addres
08:00:27:71:ad:82

routers lan mac is : 08:00:27:aa:e9:50

-------------

image 8

looks like the victim(192.168.1.101) is accessing to the wikipedia website. suricate catch those request. but not trace for the attacker
msut be using ip forwarding and not injecting any packet

--------------


image 8 netdiscover

using netdiscover to track the mac address wit hthe ip address
192.168.1.112 ---> 08:00:27:71:ad:82

---------------

image 9

comfirms , target ubuntu machine was reqeusting the wikipedia website, having internet connection means the attacker enabled ip forwarding


-----------

image 10

checking on evebox the reqeust DNS for the wikipedia, again no traces for the attacker 192.168.1.112

--------

image 12

wazuh dashboard, filtering rule groups arpwatch we can see the two flip flips
one for the router and the other for the target machine
full duplex attack

------------
image 13

target machine now showing "normal" logs, the attacker revert the arp spoofing
but we catch the correct data

------------------

image 14

pfsense arp table now normal again

