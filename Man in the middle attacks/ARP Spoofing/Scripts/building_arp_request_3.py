from scapy.all import ARP, Ether ,sendp ,conf , get_if_hwaddr, get_if_addr 



iface = conf.iface
MyIp = get_if_addr(iface)
MyMac= get_if_hwaddr(iface)

requested = "192.168.0.8"
#should return .8 with 0c:9a:3c:2c:78:56

 
arp_packet = Ether(src = MyMac , dst = "FF:FF:FF:FF:FF:FF")/ARP(op=1, pdst = requested , psrc = MyIp, hwsrc = MyMac)
#arp_packet = Ether(dst = "FF:FF:FF:FF:FF:FF")/ARP(op=1, pdst = requested , psrc = MyIp, hwsrc = MyMac)

sendp(arp_packet, iface=iface, count = 10, inter = 2.0)





