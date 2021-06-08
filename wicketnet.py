import os,argparse,logging,time,sys,re,subprocess,queue
from threading import Event
from multiprocessing import Process
import scapy.all as scapy
from colorama import Fore,init
from colorama import Back as bg
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
            sys.stdout.write(bg.BLACK + Fore.WHITE + c)
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
            print("\r", end=timeleft)
            time.sleep(1)
            stop -= 1
    def main(self):
        try:     
            ip_add_range_pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]*$")
            logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
            logging.info('Wicked-Net is running.')
            time.sleep(2)
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
        print(f"\n{Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}]Devices' IP in your Local Area Network(LAN): ")
        cmd = '''
#!/bin/sh
for i in {1..255}
do (ping  -c 1 192.168.1.${i} | grep  "bytes from" &) 
done
        '''
        file_open = open('/tmp/ping.sh','w')
        file_write = file_open.write(cmd)
        file_open.close()
        if os.path.isfile('/tmp/ping.sh'):
            os.system('sudo chmod 777 ping.sh')
            time.sleep(1.5)
            os.system('sudo bash ping.sh')
        else:
            pass
if __name__ == '__main__':
    try:
        q = queue.Queue()
        t = time.time()
        obj_class = Extract(args.ipaddress,args.devicerange,args.timeout)
        banner = Process(target=obj_class.show_banner, args=('''
 _         ___      _            _       _   _      _       *  .  . *       *    .        .        .   *    ..
 \ \      / (_) ___| | _____  __| |     | \ | | ___| |_      .   __      *        .        .      .        .            *
  \ \ /\ / /| |/ __| |/ / _ \/ _` |_____|  \| |/ _ \ __| *   ___( o)> '   *     *.   *       .     *      *        *    .
   \ V  V / | | (__|   <  __/ (_| |_____| |\  |  __/ |_      \ <_. )     *     *      ' *       * '     *  ' '      * '
    \_/\_/  |_|\___|_|\_\___|\__,_|     |_| \_|\___|\__|       ---'  
''',))
        countdown_obj = Process(target=obj_class.count_down)
        scan_obj = Process(target=obj_class.scan_devices)
        process = Process(target=obj_class.main)
        banner.start()
        banner.join()
        process.start()
        process.join(timeout=int(args.timeout))
        countdown_obj.start()
        process.terminate()
        countdown_obj.join()
        # We send a signal that the other thread should stop.
        scan_obj.start()
        scan_obj.join()
        print("Done in: {}".format(time.time()-t) + 's')
    except Exception as Err:
        print(Err)
