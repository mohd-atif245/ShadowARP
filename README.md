# ShadowARP — Advanced Multi-Threaded MITM & Credential Sniffer Framework

A Python-based Layer 2 **Man-in-the-Middle (MITM)** framework built using **Scapy** to demonstrate **ARP Cache Poisoning**, **HTTP Traffic Interception**, and **Real-Time Credential Harvesting** inside an isolated laboratory environment.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Linux-informational)

⚠️ **This project is intended strictly for educational purposes and authorized security research.**

---

## Project Preview

![Demo](screenshots/demo.png)

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Features](#-features)
- [Technologies Used](#-technologies-used)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Example Output](#-example-output)
- [Defensive Countermeasures](#-defensive-countermeasures)
- [Limitations](#-limitations)
- [Educational Purpose](#-educational-purpose)
- [Disclaimer](#-disclaimer)
- [License](#-license)

---

## 📌 Overview

ShadowARP demonstrates how an attacker positioned inside a local network can manipulate the **Address Resolution Protocol (ARP)** to transparently redirect network traffic through an intermediary machine.

Once traffic is redirected, the framework continuously inspects raw HTTP packets and identifies authentication requests containing potential credentials.

This project is designed to help students and cybersecurity enthusiasts understand why encrypted communication protocols such as **HTTPS** are essential for protecting sensitive information — it is a defensive-awareness tool disguised as an offensive demo.

---

## 🏗 Architecture

```text
                    +----------------------+
                    |      Router          |
                    | 192.168.xxx.x        |
                    +----------+-----------+
                               |
                               |
                     ARP Poisoning
                               |
                               |
      +------------------------+------------------------+
      |                                                 |
+-------------+                               +----------------+
| Victim PC   |<--------Traffic Relay-------->| Kali Linux     |
| Browser     |                               | ShadowARP      |
+-------------+                               +----------------+
```

---

## 🚀 Features

- ✅ Multi-threaded packet sniffing
- ✅ ARP Cache Poisoning
- ✅ Dynamic MAC Address Resolution
- ✅ HTTP Credential Detection
- ✅ Automatic Network Restoration (on exit, ARP tables are restored to prevent lasting disruption)
- ✅ Lightweight Python Implementation
- ✅ Built using Scapy
- ✅ Real-time Packet Monitoring
- ✅ Educational Lab Demonstration

---

## 🛠 Technologies Used

- Python 3
- Scapy
- Linux Networking
- TCP/IP
- ARP Protocol
- Raw Sockets
- Multi-threading

---

## 📂 Project Structure

```text
Advanced_MITM_Framework/
├── mitm_framework.py
├── requirements.txt
├── README.md
├── LICENSE
└── screenshots/
    └── demo.png
```

---

## ⚙ Installation

Clone the repository:

```bash
git clone https://github.com/mohd-atif245/ShadowARP.git
cd Advanced_MITM_Framework
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

`requirements.txt`:
```text
scapy>=2.5.0
```

Enable Linux IP Forwarding (required for traffic to pass through your machine):

```bash
sudo sysctl -w net.ipv4.ip_forward=1
```

> To make this persistent across reboots, add `net.ipv4.ip_forward=1` to `/etc/sysctl.conf`.

---

## ▶ Usage

```bash
sudo python3 mitm_framework.py <Target-IP> <Gateway-IP> <Interface>
```

Example:

```bash
sudo python3 mitm_framework.py 192.168.x.xx 192.168.x.x eth0
```

> The script automatically restores original ARP mappings for both the victim and gateway on exit (Ctrl+C) to avoid leaving the network in a poisoned state.

---

## 🧪 Example Output

```text
[*] Gathering MAC addresses...
[+] Target MAC: XX:XX:XX:XX:XX:XX
[+] Gateway MAC: YY:YY:YY:YY:YY:YY

[*] Sniffer Active...
[*] Starting MITM Pipeline...

[!] Credential fields captured in HTTP POST request
    (Details redacted — see 'Defensive Countermeasures' below for why this matters.)
```

> Note: real captured credential values are intentionally omitted from this README. This tool is for demonstrating *why* the interception is possible, not for showcasing captured data.

---

## 🛡 Defensive Countermeasures

This project demonstrates why organizations should implement:

- HTTPS / TLS everywhere
- HSTS (HTTP Strict Transport Security)
- Dynamic ARP Inspection (DAI) on managed switches
- Static ARP entries for critical hosts
- VPN tunneling for sensitive traffic
- Network segmentation (VLANs)
- IDS / IPS monitoring for ARP anomalies

---

## ⚠ Limitations

- Supports HTTP traffic only — HTTPS traffic is encrypted and cannot be inspected in this demonstration.
- Requires root privileges.
- Victim and attacker must be connected to the same Layer-2 network/broadcast domain.
- Designed exclusively for controlled laboratory environments (e.g. an isolated VM network).
- Does not work against networks with Dynamic ARP Inspection or port security enabled.

---

## 🎓 Educational Purpose

This project was developed to help students and security researchers better understand:

- Address Resolution Protocol (ARP)
- Layer-2 network attacks
- Packet sniffing and traffic analysis
- Offensive security concepts
- Defensive networking principles and mitigations

---

## ⚠ Disclaimer

This software was developed **strictly for educational purposes and authorized security research**.

Do **NOT** use this tool against networks, systems, or devices without **explicit written permission** from the owner. Unauthorized interception of network traffic is illegal in most jurisdictions.

The author assumes **no responsibility** for any misuse or damage resulting from the use of this project.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Muhammad Atif**
- 🎓 Computer Science Student
- 🛡 Aspiring Red Teamer
- 🐧 Linux Enthusiast
- 🐍 Python Developer

GitHub: [github.com/mohd-atif245](https://github.com/mohd-atif245)

---

⭐ If you found this project useful, consider giving it a star!
