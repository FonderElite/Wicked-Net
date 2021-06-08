import os,argparse,logging,time,sys,re
from multiprocessing import Process
import scapy.all as scapy
from colorama import Fore,init
init(autoreset=True)
parser = argparse.ArgumentParser()
parser.add_argument('-ip','--ipaddress',metavar='',help='IP-Address')
parser.add_argument('-r','--devicerange',metavar='',help='Range of Devices')
args = parser.parse_args()
class Extract(object):
    def __init__(self,ip,drange):
         self.ip = ip
         self.drange = drange
    @staticmethod 
    def show_banner(s):
        for c in s + '\n':
            sys.stdout.write(Fore.GREEN + c)
            sys.stdout.flush()
            time.sleep(2. / 100)
        print('Made By FonderElite')
        time.sleep(0.5)
        print(f'{Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}]Github:https://github.com/FonderElite')
    def main(self):
        try:
            ip_add_range_pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]*$")
            while True:
                ip_add_range_entered = self.ip + '/' + self.drange
                if ip_add_range_pattern.search(ip_add_range_entered):
                    print(f"{ip_add_range_entered} is a valid ip address range")
                    break
                arp_result = scapy.arping(ip_add_range_entered)
        except OSError:
            print(f'{Fore.WHITE} [{Fore.RED}-{Fore.WHITE}]Unknown Ip argument: {self.ip}')
if __name__ == '__main__':
    obj_class = Extract(args.ipaddress,args.devicerange)
    banner = Process(target=obj_class.show_banner, args=('''
        __        ___ ___          ____ ___ ___ ____       ___      ____ ____
|  | | /  ` |__/ |__  |  \ __ |\ | |__   |   |  |__)  /\  /  ` |__/ |__  |__) 
|/\| | \__, |  \ |___ |__/    | \| |___  |   |  |  \ /~~\ \__, |  \ |___ |  \ 
        ''',))
    process = Process(target=obj_class.main)
    banner.start()
    banner.join()
    process.start()
