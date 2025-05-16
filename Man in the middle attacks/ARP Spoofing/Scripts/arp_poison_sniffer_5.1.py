from scapy.all import sniff, ARP,conf,get_if_hwaddr

iface = conf.iface
MyMAC = get_if_hwaddr(iface)

ip_victim = "192.168.1.101"
fake_ip = "192.168.1.45"


def packet_handler(pkt):
    victim_mac = ""
    if ARP in pkt:
        if pkt[ARP].op == 2:
            if pkt[ARP].psrc == ip_victim and pkt[ARP].pdst == fake_ip:
                victim_mac = pkt[ARP].hwsrc
                print(f"we got it guys {victim_mac}")


sniff(filter = "arp", prn = packet_handler)