from scapy.all import conf,ARP,get_if_addr,get_if_hwaddr , sniff
from rich import print
from datetime import datetime



iface = conf.iface
MyMAC= get_if_hwaddr(iface)
MyIP = get_if_addr(iface)

router = "192.168.1.1"
router_mac= "08:00:27:aa:e9:50"

arp_table = {MyIP:MyMAC, router:router_mac}

def checking_Arp(ip,mac,type):
    flag = 0
    for key,value in arp_table.items():
        if key == ip:
            if type == 2:
            
                if value != mac:
                    print (f"[bold red] ALERT : THIS DEVICE {ip}, HAS A DIFFERENT MAC FROM THE ORIGINAL (TABLE,NEW): {value} != {mac} [/bold red]" )
                else:
                    print (f"[bold blue]NORMAL : THIS DEVICE {ip}, HAS THE MAC FROM THE ORIGINAL (TABLE,NEW): {value} == {mac} --- SAFE [/bold blue]" )
            flag = 1
    return flag 



def packet_handler(pkt):
    aux = 0
    if ARP in pkt:
        if pkt[ARP].op == 1:
            print("\n")
            current_time = datetime.now()
            print(f"REQUEST FROM {pkt[ARP].psrc} TO {pkt[ARP].pdst} AT {current_time.strftime("%H:%M:%S")}")
            aux = checking_Arp( pkt[ARP].psrc ,pkt[ARP].hwsrc, pkt[ARP].op)
            if aux == 0:
                print(f"[bold yellow]NEW DEVICE DETECTED: {pkt[ARP].psrc} WITH THIS MAC ADDRESS {pkt[ARP].hwsrc} --- UPDATING ARP TABLE [/bold yellow]")
                arp_table [pkt[ARP].psrc] = pkt[ARP].hwsrc
        if pkt[ARP].op == 2:
            print("\n")
            current_time = datetime.now()
            print(f"REPLY FROM {pkt[ARP].psrc}   TO {pkt[ARP].pdst} AT {current_time.strftime("%H:%M:%S")}...CHECKING ARP TABLE")
            print("\n")
            aux = checking_Arp( pkt[ARP].psrc ,pkt[ARP].hwsrc , pkt[ARP].op)
    #print("ARP TABLE SO FAR")
    #print(arp_table)


sniff( filter = "arp", prn=packet_handler)

 
