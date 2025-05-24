Ok, going to make an explanation of what is an ARP Spoofing attack,and why is called a man in the middle attack as well.

this guide builds upon the previous explanation of the ARP Process whihc is [here](https://github.com/DanielMunozParedes/SOC/blob/main/Man%20in%20the%20middle%20attacks/ARP%20Spoofing/ARP-PROCESS.md)
this guide,also, initially will be based on the lab environment diagram in [victualbox](https://github.com/DanielMunozParedes/SOC/blob/main/lab-diagrams/1.md)

## so what is spoofing ?

basically , spoofing "something" is to fake , to lie, to disguise as something or someone else; and becasue the ARP Process is sooo, and i reapeat soo blindly-trustful, some ppl take advantage of this.


![ops](https://static.scientificamerican.com/sciam/cache/file/17EF5FC0-20B4-4F03-A6620074C5751260_source.jpg)

*yeah, taht is your OS and NIC trustung every ARP reply and request*


## what consist an ARP Spoofing attack?

a threat actor/atacker will aim to send multiple, constantly, ARP replies to the victim. Those replies contain a lie where the attacker is saying "Hey, hey my answer bro, this 192.168.1.1(rotuer's) is (at) this address (Interface) (00:11:22:33:44:55)

that address is the MAC address, and is important to knwo this becase that in fact is not the real mac address of the 192.168.1.1(router's). Here the attacker sends replies, that are not fake, i mean those replies are real, and because are real both on the crafting and building of those, your (and others) NIC will accept it as it is. The lie is on the MAC address. Your machine will accept it and save that mac address (which is not the reouter's) and map it to the 192.168.1.1, 
and you would say? bor but the routers ip is still there, why bothering?
well because ip, and most importantly , local ip addresses are intercahngable (unless is static), what i mean by that is those can change, 
ips are permanent, depending on a number of factors host A can have a certain ip address but the moment host A leaves that network another host B will be optaining that ip address if needed. 

MAC address o nthe other hand... well as i have explained on the ARP Process MAC address are a layer 2; belong to the switch realm and are unique. It is attached to your NI(Network Interface) and because of this fact when a packet leaves your pc, or most strictly a frame leaves your pc and goes trhu your NI it arrives to the home router and to the port (the switch component part in most home routers) and depending of each port interface you are attached it will save and send your frames to the correct destination port. So if your frame is to be on the port destination of host C which has a mac address of aa:bb:cc:dd:ee:ff your Switch will see is COM table and (like a ARP table) will send the frame based on previous maping of the port.

That is the core of this, the attack will say to the victim the rotuers(or anyone we try to impersonate) MAC is to this address (the attacker's), when the victim sends a frame (taht could be a request for a https website or smt else) the switch won't care that the MAC address the frame has aas destination for the router's ip is different as i said swtiches don't care about ips, so waht will the swicth does?

exactly, 
it will send (based on the CAM TABLE)  to the whatever destination mac addr is attached to the frame, so in this attack it will go right to the attaacker's, simply as that.


But why your victim, or let's call it better, why all the NIC have to be so blidly-trust to any ARP reply? That is the way it is. That is the mechanism ARP works as today. and that is a vulnerability that is and has been exploited. another thing that, at least is like a double edge sword about ARP, is that ARP has a terrible memory, like really bad (lol). so for devices to be "speaking" and comunicating they need to send each x amount of time constant replies so their partners know where to find them. why i said "double edge sword"? because we can detect an ARP spoofing attack by looking at the amount of replies coming from and to a single device.



---------------

next i will show some simple image examples of a kali machie(attacker) sending ARP replies to an Ubuntu Desktop (Victim) and the rotuers as well

[![1.png](https://i.postimg.cc/wBy90ZFb/1.png)](https://postimg.cc/qtrf7mP8)


we can see here the arp table that the Ubuntu has originally before the attack (dont mind the incomplete 192.168.1.116 is SOC machine because there is a wazuh agent on the ubuntu is constantly sending arps the meaning of this is the soc machien is turned off). take nothe of the mac address

---------



[![2.png](https://i.postimg.cc/KY6xVfHc/2.png)](https://postimg.cc/Y4z5L67T)

this again, arp table of the pfsense router/firewall of this lab. take nothe of the mac address

---------


[![3.png](https://i.postimg.cc/63CtNZkr/3.png)](https://postimg.cc/474r6YNy)

on the wireshark, from the POV of the ubuntu everithing seems normal


----------


[![4.png](https://i.postimg.cc/02kxLbcS/4.png)](https://postimg.cc/4nSrcNC4)

now from the kali attacker machine we will lauch the attack, impersonating the router and sending replies to the victim(ubuntu) to our mac address


---------

[![5.png](https://i.postimg.cc/T1GG2wxZ/5.png)](https://postimg.cc/wyWn097V)

look!!! the arp table of the ubuntu now has 2 same mac address, the 100% indicator that there is an ARP spoofing attack. one fro mthe attackers kali ip .112 and the other the rotuers whom initially has a different mac address


---------


[![6.png](https://i.postimg.cc/hthntNFP/6.png)](https://postimg.cc/w1KZWfTS)

a "tip" is that attackers will do a full duplex attack. 

what is that? well to be called a MITM attack you have to be in the middle of somthing, and here we need to do the saem spoofing attack but to the routers, we need to make sure everione implicated is spoofed. router also got its spoof so we send like we are the ubuntu machine sendign replies and changing the arp table of the pfsense rotuer.

attackers also will do ip_forwarding ,which is basically, forward all the reqeust and replies: "give me that ubuntu i will pass it for you..." not touching anything inside yet, but passing it. and becase is "not injecting or touching" tools like wireshark or suricata will not see the kali ip address

-------------



[![7.png](https://i.postimg.cc/d3BFhYtD/7.png)](https://postimg.cc/LgnwWGPM)

now look the pfsense arp table

--------------

[![8.png](https://i.postimg.cc/bNm88pBB/8.png)](https://postimg.cc/zVH4FZ5C)

bro, look all the suspicious traffic now coming (this is fro mthe POV fo the ubuntu), a lot of ARP replies...hmmm i wonder who could it be...


----------


[![9.png](https://i.postimg.cc/zGMrbp5w/9.png)](https://postimg.cc/3kg6zXkW)


in this image above is the virtual machine kali filtering with wireshark dns packages
below is the ubuntu machine before going to the league of legends website

--------

[![10.png](https://i.postimg.cc/3wvHgpJs/10.png)](https://postimg.cc/jWt9TDfc)


all the traffic passing trhu the kali, look for the keywords "riotgames" or "league of legends"

-----------



[![11.png](https://i.postimg.cc/KzhhQz1R/11.png)](https://postimg.cc/p9CSLPYH)

this last image is to be the certain problem of the ARP replies, wehre the lie it is soo strong that the replies are built upon fake , 192.168.1.1 (pfsense) never sent one, but here we are seeing one legit ARP reply suposedly sended but .1 from that mac address...


--------------

this guide builds upon the previous explanation of the ARP Process whihc is [here](https://github.com/DanielMunozParedes/SOC/blob/main/Man%20in%20the%20middle%20attacks/ARP%20Spoofing/ARP-PROCESS.md)


if you are interested on more on deep analysis on this topic i have here sections, like POVs, divided based on [RED TEAM](https://github.com/DanielMunozParedes/SOC/blob/main/Man%20in%20the%20middle%20attacks/ARP%20Spoofing/ATTACKER/README.md
)
, [BLUE TEAM specifically SOC](https://github.com/DanielMunozParedes/SOC/blob/main/Man%20in%20the%20middle%20attacks/ARP%20Spoofing/DEFENDER/SOC/README.md)  and [Network Security](https://github.com/DanielMunozParedes/SOC/blob/main/Man%20in%20the%20middle%20attacks/ARP%20Spoofing/DEFENDER/NETSEC/README.md
)


