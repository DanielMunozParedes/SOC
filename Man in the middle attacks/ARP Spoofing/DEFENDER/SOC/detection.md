level 1 dectection.

---------------------------

[![1.png](https://i.postimg.cc/gJCLDNmS/1.png)](https://postimg.cc/qhG7Bcty)

setup of the soc machine . custom built upon xubuntu with SIEM wazuh,wiresahrk and suricata IDS and evebox to visualize. promiscous mode. Not that realistic, since for example tools like suricata or zeek are to be deployed behind the firewall. I must say i have suricata isntalled on the pfsense direclty, but for practical uses i will focus on the promiscous mode for the learning on hwo to use the suricata tool
also for context this machine, that works as a wazuh server, has a wazuh agent on ubuntu desktop target machine already

-------------------------

[![2.png](https://i.postimg.cc/sfWhXd4t/2.png)](https://postimg.cc/XXVJHPh8)

setup o nthe machine ubuntu desktop, using syslog with arpwatch filtering the word arpwatch, arp table on view and my custom script to detect changes o nthe arp table

everithing normal so far

-------------------------


[![3.png](https://i.postimg.cc/hvVz3TGS/3.png)](https://postimg.cc/JH4zsyJg)

image to show the agent ubuntu

-----------------------

[![4-attack.png](https://i.postimg.cc/28FLQQJG/4-attack.png)](https://postimg.cc/SJRKqMmY)

attack begins


--------------------

[![5.png](https://i.postimg.cc/Hk6JKpT7/5.png)](https://postimg.cc/gx6kLbXY)

inmediatly alerts start to be triggered on the agent. we can distinguish ,among obvious things thanks for the alerts, the arp has 2 ip addresses with the  same mac address

arpwatch detected the change and the flip flop was registered on the syslog  at 2025 - 05 - 26  23:08:30.3444

-----------------

[![6-pfsense.png](https://i.postimg.cc/9fz4Hvfg/6-pfsense.png)](https://postimg.cc/v1F8W2f5)

pfsense arp table is changed too, the attack is full duplex host to attacker, attacker to gateway

---------------

[![7-wireshark.png](https://i.postimg.cc/cJjvxXgx/7-wireshark.png)](https://postimg.cc/FfyrGbV8)

wireshark shows suspicious behavior. multiple arp replies in a short time window
all coming to say the gateway ip is at different mac addres
08:00:27:71:ad:82

routers lan mac is : 08:00:27:aa:e9:50

-------------

[![8-evebox-wiki.png](https://i.postimg.cc/Hn1j5n9F/8-evebox-wiki.png)](https://postimg.cc/ft5wQwFv)

looks like the victim(192.168.1.101) is accessing to the wikipedia website. suricate catch those request. but not trace for the attacker
msut be using ip forwarding and not injecting any packet

--------------


[![8-netdiscover.png](https://i.postimg.cc/gJZnn88v/8-netdiscover.png)](https://postimg.cc/MMzWLcsT)

using netdiscover to track the mac address wit hthe ip address
192.168.1.112 ---> 08:00:27:71:ad:82

---------------

[![9-ubuntu-wiki.png](https://i.postimg.cc/J4mGzynk/9-ubuntu-wiki.png)](https://postimg.cc/t7SXr4Fq)

comfirms , target ubuntu machine was reqeusting the wikipedia website, having internet connection means the attacker enabled ip forwarding


-----------

[![10-evebox.png](https://i.postimg.cc/hPrhzSz3/10-evebox.png)](https://postimg.cc/0bz9h1Cp)

checking on evebox the reqeust DNS for the wikipedia, again no traces for the attacker 192.168.1.112

--------

[![12-wazuh.png](https://i.postimg.cc/dVV3GzGQ/12-wazuh.png)](https://postimg.cc/YhTtHDXT)

wazuh dashboard, filtering rule groups arpwatch we can see the two flip flips
one for the router and the other for the target machine
full duplex attack

------------

[![13.png](https://i.postimg.cc/W4D4Hg9Q/13.png)](https://postimg.cc/kVm9V6Pc)

target machine now showing "normal" logs, the attacker revert the arp spoofing
but we catch the correct data

------------------

[![14.png](https://i.postimg.cc/pLcTCqBf/14.png)](https://postimg.cc/xXHnTGh8)


pfsense arp table now normal again

