#explanation coming soon


from scapy.all import Ether,conf,get_if_hwaddr,sendp,Raw
iface =  conf.iface
frame = Ether(src = get_if_hwaddr(iface) , dst = "FF:FF:FF:FF:FF:FF" , type = 0x0800)/Raw(load="hello carlos")
sendp(frame, iface=iface, count= 3)
