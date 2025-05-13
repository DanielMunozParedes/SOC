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
                print(f" + ARP REPLY SUCCESS FROM {pkt[ARP].psrc}  and updated in the ARP table of this host with the ip: {MyIp}") 

    arp_packet = Ether(src = MyMac , dst = "FF:FF:FF:FF:FF:FF")/ARP(op=1, pdst = requested , psrc = MyIp, hwsrc = MyMac)
    sendp(arp_packet, iface=iface, count = 1, inter = 1.0) 
    print(f" + ARP REQUEST was sended to {requested} from this host with the ip: {MyIp}")    




sniff(filter="arp", prn = packet_handler, count = 10)





#sudo apr -d ip we want to delete from the table








