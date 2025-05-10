Next is the explanation of the ARP Spoofing attack. I will be also explaining the ARP proccess because i feel some people misunderstand the correct definition and flow of how thigns works on this networking broadcast process

MITMA(Man In The Middle Attack)

To begin the understanding of the ARP Spoofing MITMA, we need first to understand the ARP (Address Resolution Protocol). I want to give a little background so the later topics will flow thru, so this explanation is meant for myselft and for others that hopeful may find this useful; expect some informal teching stuff since is my way of learn things and so on.

So we need to go straight to the core of this: wehn a device in a LAN needs to "speak" with another device he needs to know its MAC address, but why?

well the thing is, when a IPV4 packet is in the making your device is adding all the info necessary for the correct arriving and after that the correct encapsulation/decapsulaton. What does that means?

we will perform a little example using 2 pcs, 1 switch and 1 router; the most simplest LAN using Packet Tracer

[![arp1.png](https://i.postimg.cc/MpMD728w/arp1.png)](https://postimg.cc/mP4C4nDp)


here PC0 (192.168.0.2) whats to send an ICMP ping to the PC1 (192.168.0.3); as we know PC1 needs to asnwer with a Echo reply of taht ICMP reqeust from PC0. Ok, nothing crazy here. Well, that is in a perfect world. PC0 to organize a sending "letter" to PC1 needs to know its MAC addres because *Switches only understand layer 2*  BUT not only for that, look knowing the ip address of your dest is good enough to know where to look your dest device, but knowing the MAC addres, which is a unique 48 bit hex for each ethernet interface of any device, is to know how to actually knock at the door. Both are a team work to arrive. Ip: Location routing, MAC: place direct

so going back the frame is made...but oh, wait a moment, 
says PC0, "Look i know my destination ip 192.168.0.3, but i need its MAC addres (for the switch and the exact frame dest MAC comunication with the ethernet interface), what do i do?"
"We need to send a ARP broadcast to know the MAC address of that dest ip, so we ask the swtich to broadcast that request ARP  from us and the switch will flood the network. After that the device with the Dest ip we originally wanted to talk will respond a message frame to swtich with its MAC addres for us, so we can update our ARP table"
...
thats how it works

**an ARP is a broadcast which works with packet as a MAC addresses and target ip**


look at the PDU ourbound from PC0 before sending a frame to the swtich, take special note that broadcast dest MAC address with FFFF.FFFF.FFFF is meant to be recevied for the host in a LAN regardless of its unique MAC address. The broadcast MAC address is that important that the resources of a network will be using to its complete extension that every device in the net will recevie you like it or not a ARP reqeust taht was flooded by the swtich

lets see the following images

[![2.png](https://i.postimg.cc/Hx43rw17/2.png)](https://postimg.cc/bDr1M2Jz)


This image we can see that the out layer 3 we use of course the 192.168.0.3 dest



-----------


[![3.png](https://i.postimg.cc/PJS44dxX/3.png)](https://postimg.cc/jnJPq0Pm)
and here the layer 2, see that the broadcast MAC address. But ...wait a moment, why layer 2 has an Ip there? aint switches only MAC MAC MAC...
well yeah, but here is a ARP reqeust, the PDU outbound for an ARP is special becase we are not using neither TCP, UDP transport layers of comunnication, we also even using ICMP wich is a network layer protocol, we using a protocol for "discovery" broadcast and the layer 2. And in this case we dont have a destination IP we have a *TARGET* IP to discover *whatever we are asking for*

look this image


[![1-2.png](https://i.postimg.cc/KvcpgHzc/1-2.png)](https://postimg.cc/Rq8LkGK2)



Is an ARP packet, thats the key

------------


when the frame arrives the switch it will flood all prorts except the incoming reqeust one

[![4.png](https://i.postimg.cc/Fzrp3YhC/4.png)](https://postimg.cc/njWqtcjq)

-------------

we can see here that at the correct target ip the arp packet is recevied( always) but msot important is accepted to reply the arp request with a target ip now change, now the target ip is the original reqest host. Is the same as the network works, but the word "target" is key to understand this packet ARP

[![5.png](https://i.postimg.cc/ZYHVZxLG/5.png)](https://postimg.cc/w3thQJZ2)

-------------



note here taht the router, which is not meant to accet the arp, receives regardless

[![6.png](https://i.postimg.cc/yYNnN3Qk/6.png)](https://postimg.cc/3WP2SNHT)



--------------

After receiving the MAC reply from PC1, the arp table from PC0 will be updated and Look now the PDU outbound format for the PC0 when is sending to the PC1 - is a dest IP not target, we separate here; this is an ICMP, not ARP packet, we have ipv4 packets and Frame for layer 2

[![7.png](https://i.postimg.cc/L60Dg4wv/7.png)](https://postimg.cc/zVKK9NJR)

in all this process the ping echo reply has not even begin


--------

final image where the arp table from pc0 is updated 


[![8.png](https://i.postimg.cc/ydWjPvWq/8.png)](https://postimg.cc/k63WMNxw)



---------------


Sooo why do i take all the effort to explain this process? well, i think is important becasue ppl missunderstood the arp process; some ppl say that arp ask for the router, like what?? that is not correct. Look if you meant to say that all the encapsulation and decapsulation is made thru the home router or a swtich and rotuer setup, thats ok, all the NICs (Network interface cards) needs to send *upstream* the data bits thru there, the only upstream meant; all the electric signals will go up to the either home router or swtich , lets not forget that a home router has a swtich component inside that perform the amc flooding. so, yeah we go to the home router, but two distictions:

1. we dont have as target ip the rotuer(gateway address)
2. we need to remember the layer 2 ,the swtich , from the home router. He just passes the signals trhu the ports, is differetent router component and swtich component


this is key

[![9.png](https://i.postimg.cc/NMXjqvzQ/9.png)](https://postimg.cc/mzbsCJ4n)



because the ARP goes to whomever needs to go, that is, not only the target ip to the rotuer, but, to a pritner, voip, smarphone, another pc etc.

so lets get out of our minds the rotuer thing, yeah it goes thru the rotuer (if it is a home router) but is not meant to the rotuer if our original target is for example a printer, ok?
we can have on our ouwn LAN a FTP server, now youll tell me that the arp is meant for the router?? nooois meant for the ftp, and look taht here we overlook becasue of the missuderstanding of always router, always router, but forget the ARP is meant to whom is meant not always rotuer.

we can have MAITMA between:

-router and pc (most used)
-pc to pc
-pc to printer
-pc to voip
....



we need to secure all. so hence the why of the explanation of the ARP first before going to the ARP Spoofign attack



