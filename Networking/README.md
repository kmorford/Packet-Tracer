# Networking Labs

Layer-2/Layer-3 fundamentals: addressing, VLANs, routing, and services.

**Navigation:** [🏠 Home](../index.md) • [🧪 Cisco PT Labs](../Cisco%20Packet%20Tracer/README.md) • [🌐 IoT](../IoT/README.md)

---

## Focus Areas
- IPv4 addressing & VLSM
- VLAN segmentation, trunking, inter-VLAN routing
- RIPv2 / OSPF single-area
- Core services: DHCP, DNS

---

## Lab Index

| # | Lab Title | Topics / Skills | File |
|---|-----------|------------------|------|
| 1 | Addressing & VLSM | Subnet design, addressing plan, gateway assignment | [Lab1_VLSM_Design.pkt](./Lab1_VLSM_Design.pkt) |
| 2 | DHCP & DNS | DHCP pools, exclusions, DNS records, client tests | [Lab2_DHCP_DNS.pkt](./Lab2_DHCP_DNS.pkt) |
| 3 | VLAN Topology | Access/trunk config, port mapping, endpoint tests | [Lab3_VLAN_Topology.pkt](./Lab3_VLAN_Topology.pkt) |
| 4 | Inter-VLAN Routing | SVIs, R-on-a-S, helper addresses | [Lab4_InterVLAN.pkt](./Lab4_InterVLAN.pkt) |
| 5 | OSPF Fundamentals | OSPF process/area, neighbors, route verification | [Lab5_OSPF_Fundamentals.pkt](./Lab5_OSPF_Fundamentals.pkt) |

---

## Submission Checklist
- `.pkt` file opens and runs without errors
- Documentation includes:
  - Address plan table (net, mask/prefix, gateway, VLAN)
  - Command snippets (e.g., `show vlan brief`, `show ip route`)
  - Connectivity proof (`ping`, `tracert`/`traceroute`)

**File naming:** `LastName_FirstName_LabNN`

---

## Quick Commands
- Port mode: `switchport mode access|trunk`
- VLAN verify: `show vlan brief`
- Trunk verify: `show interfaces trunk`
- Routing verify: `show ip route`, `show ip ospf neighbor`

## Lab Index

<!-- AUTO-LIST:START -->
_(No .pkt files found yet.)_
<!-- AUTO-LIST:END -->
