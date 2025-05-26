I was trying to understand the  arpspoof form the dsniff toolkit. Certanly i got caught on the ,shoudl we say,nuts and bolts of this. As i dive more dsniff has a lot of resources and among those arpsoof. 

doing my research i need to try this, having acces to a certain network the only thing i want to do and study was the consequeces of this vulnerability: arp spoofing

so this is waht happenend: i wanted to create my own arp spoofer. nothing crazy since i suposse a lot of cybersec researchers have done of at least know how to. So i wanted to make my shoot. 
After understanding the [ARP processs] i went to understand the [ARP Spoofing tactics], and one of the most important things i learned was "the revert part". Bear with me as i am noob on this, but trying to hide your tracks or at least less amount of noise is something i want to embed on my learning joruney (and also as i understand is an essential part of pentesting)

if you are interested to learn about my journey, please go to the next post(s)!

1 - building an raw frame
2 - sniffing the network (see what out NIC sees)
3 - building an ARP request and saving it on our arp table
4 - sending request and reply and sniffing to capture the mac address of the victim
5 - complete arp spoofing loop and revert
