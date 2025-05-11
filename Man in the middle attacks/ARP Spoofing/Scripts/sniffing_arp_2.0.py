from scapy.all import sniff

sniff( filter="arp" , prn = lambda pkt: pkt.summary()   )
