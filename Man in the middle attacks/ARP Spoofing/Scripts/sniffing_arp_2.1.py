from scapy.all import ARP,sniff,conf

iface = conf.iface

def pkt_handler(pkt):
    if ARP in pkt:
        if pkt[ARP].op == 1:
            #request
            print(f"REQUEST from: {pkt[ARP].psrc} with MAC {pkt[ARP].hwsrc} is asking to {pkt[ARP].pdst} for ARP reply"  )

        elif pkt[ARP].op == 2:
            #reply
            print(f"REPLY from: {pkt[ARP].psrc} with MAC {pkt[ARP].hwsrc} to the asker {pkt[ARP].pdst}")



sniff(filter="arp",prn=pkt_handler, iface=iface,count = 10)
