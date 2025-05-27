# ARP Spoofing Attack Detected on Internal Network

## Summary

On **2025-05-27 at *23:08:30.3444***, a possible ARP spoofing attack was detected affecting host `192.168.1.101`. The attack originated from a device impersonating the default gateway.

---

## Timeline

| Time           | Event                                                                 |
|----------------|-----------------------------------------------------------------------|
| 23:08:30.3444  | arpwatch and custom script detect from target machine                |
| 23:08:31       | (approx) pfSense LAN ARP table was affected                          |
| 23:09:15       | SOC started the investigation (reviewing Wireshark, Wazuh and Suricata) |
| 23:20:33.36    | The attack was restarted, looks like a test on 23:08:30.3444         |
| 23:38:08.083   | Attack was stopped by the threat actor                               |

---

## Indicators of Compromise (IOCs)

- **Attacker IP:** `192.168.1.112`  
- **Victim IP:** `192.168.1.101`  
- **Duplicate MAC:** `08:00:27:71:ad:82`

---

## Tools Used

- Wazuh (with arpwatch integration and custom script built)  
- Wireshark (promiscuous mode)  
- Manual inspection of ARP tables  
- pfSense ARP diagnostics

---

## Impact

- Potential MITM attack  
- Risk of credential theft, session hijack, traffic manipulation  
- Passive sniffing (no injection)

---

## Action Taken / Recommendation

- Blocking the attacker IP is a temporary solution  
- Isolated attacker  
- Create an easy victim target machine so the attacker is baited  
- Static entries on ARP table on critical devices like the gateway  
- Monitor for recurring ARP anomalies — looks like this attacker tends to make tests at the same time
