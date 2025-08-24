# Packet Tracer — FA 2025

Welcome to the Packet Tracer repository for Fall 2025. This site hosts curated labs, templates, and reference materials used in class and for independent practice with Cisco Packet Tracer.

> **Target audience:** Community college networking students building practical skills in routing/switching, basic IoT scenarios, and multi-subnet design.

---

## Quick Start

1. **Install Cisco Packet Tracer** (current version recommended by instructor).
2. Clone or download this repo:
   ```bash
   git clone https://github.com/kmorford/Packet-Tracer.git
Open .pkt files from the sections below and follow the embedded instructions.

Repository Map

Cisco Packet Tracer

Core Packet Tracer activities, device configuration walkthroughs, and assessment-style practice.

Networking

Subnetting, VLANs, trunking, inter-VLAN routing, static/dynamic routing (RIPv2/OSPF), DHCP/DNS, and standard troubleshooting playbooks.

IoT

Introductory IoT topologies in Packet Tracer, simple sensor/actuator networks, and event-driven scenarios.

Tip: Each folder contains numbered labs. Start with the lowest number unless your instructor directs otherwise.


How to Use These Labs

Before you start: Read the lab’s Objectives and Deliverables in the first page or lab README.

During the lab: Take configuration notes (commands used, verification output). Screenshots are acceptable for evidence but do not replace required configuration text.

After the lab: Save your .pkt and export a brief write-up (see rubric) summarizing design choices and verification steps.

Submission Format (default)

Unless your instructor specifies otherwise, submit:

The completed .pkt file.

A short write-up (PDF or MD) including:

IP/VLAN plan table,

Key config snippets (e.g., show run | sec vlan, show ip route),

Verification output (ping, tracert, show ip int br),

2–3 problems encountered and fixes.

File naming: LastName_FirstName_LabNN.
Academic honesty: Your configs must be your own work. Sharing finished .pkt files is prohibited.

Troubleshooting Checklist

Interfaces up? (show ip int br, show int status)

Correct VLANs and access/trunk modes?

Default gateway set on end hosts?

Routing protocol enabled and networks advertised?

ACLs or security settings blocking traffic?

IP addressing overlaps or gateway mismatches?

Notes & Attribution

This repository is maintained for instructional use. Materials may be updated during the term—pull frequently.

Cisco Packet Tracer is a Cisco tool; use according to your program’s license terms.
