Ok, going to make an explanation of what is an ARP Spoofing attack,and why is called a man in the middle attack as well.

this guide builds upon the previous explanation of the ARP Process whihc is [here](https://github.com/DanielMunozParedes/SOC/blob/main/Man%20in%20the%20middle%20attacks/ARP%20Spoofing/ARP-PROCESS.md)


so what is spoofing ??

basically , spoofing "something" is to fake , to lie, to disguise as something or someone else; and becasue the ARP Process is sooo, and i reapeat soo blindly-trustful, some ppl take advantage of this.

what consist an ARP Spoofing attack?

a threat actor/atacker will aim to send multiple, constantly, ARP replies to the victim. Those replies contain a lie where the attacker is saying "Hey, hey my answer bro, this 192.168.1.1(rotuer's) is (at) this address (Interface) (00:11:22:33:44:55)

that address is the MAC address, and is important to knwo this becase that in fact is not the real mac address of the 192.168.1.1(router's). Here the attacker sends replies, that are not fake, i mean those replies are real, and because are real both on the crafting and building of those, your (and others) NIC will accept it as it is. The lie is on the MAC address. Your machine will accept it and save that mac address (which is not the reouter's) and map it to the 192.168.1.1, 
and you would say? bor but the routers ip is still there, why bothering?
well because ip, and most importantly , local ip addresses are intercahngable (unless is static), what i mean by that is those can change, 
ips are permanent, depending on a number of factors host A can have a certain ip address but the moment host A leaves that network another host B will be optaining that ip address if needed. 

MAC address o nthe other hand... well as i have explained on the ARP Process MAC address are a layer 2; belong to the switch realm and are unique. It is attached to your NI(Network Interface) and because of this fact when a packet leaves your pc, or most strictly a frame leaves your pc and goes trhu your NI it arrives to the home router and to the port (the switch component part in most home routers) and depending of each port interface you are attached it will save and send your frames to the correct destination port. So if your frame is to be on the port destination of host C which has a mac address of aa:bb:cc:dd:ee:ff your Switch will see is COM table and (like a ARP table) will send the frame based on previous maping of the port.

That is the core of this, the attack will say to the victim the rotuers(or anyone we try to impersonate) MAC is to this address (the attacker's), when the victim sends a frame (taht could be a request for a https website or smt else) the switch won't care that the MAC address the frame has aas destination for the router's ip is different as i said swtiches don't care about ips, so waht will the swicth does?

exactly, it will send (based on the CAM TABLE)  to the whatever destination mac addr is attached to the frame, so in this attack it will go right to the attaacker's, simply as that.


and here is the thing: those replies are the attack. You see, those replies ,when sended thru your NIC, will go to the network whenenver the architecture and send a frame to be "readble" to the switch and the majority of tools will use this process because 
