"""Use ine.py to provision INE CCIE Workbook LAB Routers
Usage:
    python ine.py
    result: prints list of sections and related configs

    python ine.py initial ospf
    result: reboot to clear config and configure all routers according to files
"""

import logging
import nparallel

from sys import argv
from glob import glob

import time
from netmiko import ConnectHandler

logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')

PARAMS = dict(username='cisco', password='cisco',
              device_type='cisco_ios_telnet',
              global_delay_factor=0.2, timeout=12)

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

GLOBAL_SECTIONS = ['mpls', 'eigrp', 'ospf', 'rip', 'bgp', 'multicast', 'lan']

def sections_handling():
    distributed = []
    for section in GLOBAL_SECTIONS:
        print(section.upper())
        for f in glob(CONFIG_FODLER + '*'):
            f = f.split('/')[-1]
            if section in f:
                distributed.append(f)
                print('\t', f)
    print('OTHER')
    for f in glob(CONFIG_FODLER + '*'):
        f = f.split('/')[-1]
        if f not in distributed:
            print('\t', f)

def sleep_and_log(sec):
    logging.info(f'Going sleep for {sec} seconds')
    time.sleep(sec/2)
    logging.info(f'{sec/2} seconds left to sleep')
    time.sleep(sec/2)

class UnlRouter:
    def __init__(self, name, unl_ip, port, param_dict, config_folder):
        self.unl_ip = unl_ip
        self.port = port
        self.params = param_dict.copy()
        self.params.update(dict(ip=self.unl_ip, port=self.port))
        self.conn = None
        self.config_folder = config_folder
        self.name = name

    def connect(self):
        self.conn = ConnectHandler(**self.params)

    def disconnect(self):
        if self.conn:
            self.conn.disconnect()

    def verify_connect(self):
        if self.conn:
            if not self.conn.is_alive():
                self.connect()
        else:
            self.connect()

    def clear_config(self):
        logging.info(f'Trying to reboot {self.name}')
        self.verify_connect()
        self.conn.send_command('end', auto_find_prompt=False, expect_string = '#|>')
        self.conn.send_command('end', auto_find_prompt=False, expect_string = '#|>')
        r = self.conn.send_command('reload', auto_find_prompt=False,
                                   expect_string='.*Save?.*|.*reload.*', delay_factor=0.25)
        if 'Save?' in r:
            self.conn.send_command('no', auto_find_prompt=False,
                                   expect_string='.*Save?.*|.*reload.*', delay_factor=0.25)

        try:
            self.conn.send_command('\n\r', auto_find_prompt=False,
                                   expect_string='.*Save?.*|.*reload.*', delay_factor=0.25, max_loops = 3)
        except OSError:
            logging.info(f'{self.name} gone to reboot')

    def configure(self, section):
        self.verify_connect()
        filename = self.config_folder + section + '/' + self.name + '.txt'
        logging.info(f'Configure {self.name} with {filename}')
        with open(filename, 'r') as f:
           for line in f:
               self.conn.send_command(line, delay_factor=0.05, strip_prompt=False,
                                      expect_string = '#|>', auto_find_prompt=False)
        logging.info(f'Conf{self.name}')
    def __repr__(self):
        return f'{self.name} {self.unl_ip} {self.port}'


# Verify input
if not argv[1:]:
    sections_handling()
    exit()

section = ' '.join(argv[1:]).lower()
available_sections = [folder.split('/')[-1] for folder in glob(CONFIG_FODLER + '*')]

if section not in available_sections:
    print(f'Не найдена указанная секция: {section}')
    exit()

# Get Routers objects
routers = []
for name, port in PORT_TO_R.items():
    routers.append(UnlRouter(name=name, unl_ip=UNL_IP, port=port,
                             param_dict=PARAMS, config_folder=CONFIG_FODLER))

#  Reload to clear config and configure:
nparallel.oprocess('clear_config', routers)

sleep_and_log(56)

nparallel.oprocess('configure', routers, section=section)
nparallel.oprocess('disconnect', routers)

