
from scapy.all import ARP, Ether ,sendp ,conf , get_if_hwaddr, get_if_addr, subprocess , sniff

iface = conf.iface
MyIp = get_if_addr(iface)
MyMac= get_if_hwaddr(iface)

requested = "192.168.0.5"

def packet_handler(pkt):

    if ARP in pkt:
        if pkt[ARP].op == 2:
            #REPLY
            if pkt[ARP].pdst == MyIp and pkt[ARP].psrc == requested:
                subprocess.run(["sudo", "arp", "-s", pkt[ARP].psrc, pkt[ARP].hwsrc ])


    arp_packet = Ether(src = MyMac , dst = "FF:FF:FF:FF:FF:FF")/ARP(op=1, pdst = requested , psrc = MyIp, hwsrc = MyMac)
    sendp(arp_packet, iface=iface, count = 1, inter = 1.0)     




sniff(filter="arp", prn = packet_handler, count = 10)








