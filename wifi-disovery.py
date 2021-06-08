import os,argparse,logging,time,sys,re
from threading import Event
from multiprocessing import Process
import scapy.all as scapy
from colorama import Fore,init
init(autoreset=True)
parser = argparse.ArgumentParser()
parser.add_argument('-ip','--ipaddress',metavar='',help='IP-Address')
parser.add_argument('-r','--devicerange',metavar='',help='Range of Devices')
parser.add_argument('-t','--timeout',metavar='',help='Timeout')

args = parser.parse_args()
stop_event = Event()
class Extract(object):
    def __init__(self,ip,drange,timeout):
         self.ip = ip
         self.drange = drange
         self.timeout = timeout
    @staticmethod 
    def show_banner(s):
        for c in s + '\n':
            sys.stdout.write(Fore.GREEN + c)
            sys.stdout.flush()
            time.sleep(2. / 100)
        print('Made By FonderElite')
        time.sleep(0.5)
        print(f'{Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}]Github:https://github.com/FonderElite')
    def count_down(self):
        stop = abs(int(self.timeout))
        while stop > 0:
            m, s = divmod(stop, 60)
            h, m = divmod(m, 60)
            timeleft = Fore.RED + "Time-out: " + Fore.WHITE + str(h).zfill(2) + ":" + str(m).zfill(2) + ":" + str(s).zfill(2)
            print(f"\r", end=timeleft)
            time.sleep(1)
            stop -= 1
    def main(self):
        try:     
            ip_add_range_pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]*$")
            while True:
                ip_add_range_entered = self.ip + '/' + self.drange
                if ip_add_range_pattern.search(ip_add_range_entered):
                    print(f"{Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}]Discovering LAN devices: {ip_add_range_entered}")
                    break
            arp_result = scapy.arping(ip_add_range_entered)
            print(arp_result)
        except Exception:
           resp = Fore.WHITE + '[' + Fore.RED + '-' + Fore.WHITE + ']' 
           aligned_string = "{:<10}".format(resp)
           print(f'{aligned_string}Invalid Ip-address:{self.ip}')
           print('Use -h for help')
    @staticmethod
    def scan_devices():
        print('Scan Deviced')
if __name__ == '__main__':
    obj_class = Extract(args.ipaddress,args.devicerange,args.timeout)
    banner = Process(target=obj_class.show_banner, args=('''
__        ___      _            _       _   _      _   
\ \      / (_) ___| | _____  __| |     | \ | | ___| |_     
 \ \ /\ / /| |/ __| |/ / _ \/ _` |_____|  \| |/ _ \ __|   
  \ V  V / | | (__|   <  __/ (_| |_____| |\  |  __/ |_  
   \_/\_/  |_|\___|_|\_\___|\__,_|     |_| \_|\___|\__|
        ''',))
    countdown_obj = Process(target=obj_class.count_down,args=(int(args.timeout),))
    process = Process(target=obj_class.main)
    banner.start()
    banner.join()
    process.start()
    process.join(timeout=args.timeout)
    countdown_obj.start()
    countdown_obj.join()
    # We send a signal that the other thread should stop.
    process.terminate()

