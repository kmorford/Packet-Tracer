# Cisco Packet Tracer Labs

Core Packet Tracer activities used throughout the course.

**Navigation:** [🏠 Home](../index.md) • [🧰 Networking](../Networking/README.md) • [🌐 IoT](../IoT/README.md)

---

## Prerequisites
- Cisco Packet Tracer (current version recommended by instructor)
- Basic CLI familiarity (enable, config t, interface, vlan, ip address)

---

## Lab Index

> Replace `LabN_Name.pkt` with your actual files. Keep the table short and scannable.

| # | Lab Title | Topics / Skills | File |
|---|-----------|------------------|------|
| 1 | Basic Device Setup | Initial config, hostnames, passwords, banner, interface status | [Lab1_BasicSetup.pkt](./Lab1_BasicSetup.pkt) |
| 2 | VLANs & Trunking | Access/trunk ports, VLAN database, verification | [Lab2_VLAN_Trunking.pkt](./Lab2_VLAN_Trunking.pkt) |
| 3 | Inter-VLAN Routing | SVI vs. router-on-a-stick, gateway, connectivity tests | [Lab3_InterVLAN_Routing.pkt](./Lab3_InterVLAN_Routing.pkt) |
| 4 | RIPv2 | Network advertising, no auto-summary, route verification | [Lab4_RIPv2.pkt](./Lab4_RIPv2.pkt) |
| 5 | Single-Area OSPF | OSPF process, network statements, DR/BDR basics | [Lab5_OSPF_SingleArea.pkt](./Lab5_OSPF_SingleArea.pkt) |

---

## Deliverables (Default)
Submit your **`.pkt`** file plus a brief write-up (`PDF`/`MD`) with:
- IP/VLAN plan table and key config snippets
- Verification output (`show ip int br`, `show vlan brief`, `show ip route`, `ping`)
- 2–3 issues encountered and how you resolved them

**File naming:** `LastName_FirstName_LabNN`

---

## Troubleshooting
- Interfaces up? `show ip int br`
- Correct access/trunk modes and VLANs?
- Default gateways on hosts?
- Routes advertised and visible? `show ip route`
- No IP overlaps or ACL blocks?

