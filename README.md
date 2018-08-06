# ine-provision
Provision of UNL devices for INE CCIE R&S workbook configs with one command

Prerequisite:
1) UNL host accessible from host where script is launched
2) LAB uses Cisco IOL L3 images
3) Configs are compatible with IOL, there is in configs you have Eth0/* instead Gi0/* (it easy to do with all files replacement)
4) nparallel module (you can find it in my profile on github) 

Preconfiguration:
Open ine.py and insert values from your own environment for next constants:

    UNL_IP
    PORT_TO_R
    CONFIG_FODLER


Usage:

    >> python ine.py
    result: prints list of sections and related configs
    EIGRP
         eigrpv6 basic
         initial eigrp
         mpls eigrp site of origin
         mpls pe ce routing with eigrp
         basic eigrp routing
         eigrpv6 initial
    OSPF
         initial ospf
         ...(output omitted)
         
    
         
    >> python ine.py initial ospf
    result: reboot to clear config and configure all routers according to files
