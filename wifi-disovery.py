import os,argparse,logging,time,sys
from multiprocessing import Process
from scapy import *
from colorama import Fore,init
init(autoreset=True)
parser = argparse.ArgumentParser()
parser.add_argument('-ip','--ipaddress',metavar='',help='IP-Address')
parser.add_argument('-r','--devicerange',metavar='',help='Range of Devices')
args = parser.parse_args()
BBLK = "033[1;30m"
BRED = "033[1;31m"
BGRN = "033[1;32m"
BYEL = "033[1;33m"
BBLU = "033[1;34m"
BMAG = "033[1;35m"
BCYN = "033[1;36m"
BWHT = "033[1;37m"
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
        print(Fore.WHITE + '[' + Fore.GREEN + '+' + Fore.WHITE + ']' + 'Github:https://github.com/FonderElite')
    def main(self):
     print('Start')
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
    obj_class.main()
    
