# ine-provision
Provision of UNL devices for INE CCIE R&S workbook configs with one command

Prerequisite:
1) UNL host accessible from host where script is launched
2) LAB uses Cisco IOL L3 images
3) Configs are compatible with IOL, there is in configs you have Eth0/* instead Gi0/* (it easy to do with all files replacement)
4) nparallel module (you can find it in my profile on github) 

Preconfiguration:
Open ine.py and insert values from your own environment for next variables:

    UNL_IP = '10.0.0.1'

    PORT_TO_R = {'R1': '33281',
                 'R2': '33282',
                 'R3': '33283',
                 'R4': '33284',
                 'R5': '33285',
                 'R6': '33286',
                 'R7': '33287',
                 'R8': '33288',
                 'R9': '33289',
                 'R10': '33290'}

    CONFIG_FODLER = '/root/dev/files/ine_wb_configs/'

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
    result: reboot routers to clear config and configure all routers according to files
