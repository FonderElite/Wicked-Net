import os,argparse,logging,time,sys,re,subprocess,queue
from threading import Event
from multiprocessing import Process
import scapy.all as scapy
from colorama import Fore,init
from colorama import Back as bg
from wifi import Cell, Scheme
init(autoreset=True)
parser = argparse.ArgumentParser()
parser.add_argument('-ip','--ipaddress',metavar='',help='Local Ip')
parser.add_argument('-s','--subnetrange',metavar='',help='Subnet Range')
parser.add_argument('-t','--timeout',metavar='',help='Timeout')
parser.add_argument('-i','--interface',metavar='',help='Interface to discover Wireless AP')

args = parser.parse_args()
stop_event = Event()
class Extract(object):
    def __init__(self,ip,drange,timeout,iface):
         self.ip = ip
         self.drange = drange
         self.timeout = timeout
         self.iface = iface
    @staticmethod 
    def show_banner(s):
        for c in s + '\n':
            sys.stdout.write(bg.BLACK + Fore.WHITE + c)
            sys.stdout.flush()
            time.sleep(1. / 100)
        print('->Made By FonderElite<-')
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
        arr = []
        localip = os.popen("ifconfig wlan0 | grep -w 'inet'").read()
        if os.path.isfile("local-ip.txt") == False:
            ip_file = open("local-ip.txt","w")
            ip_file_w = ip_file.write(localip)
        elif os.path.isfile("local-ip.txt") == True:
            read_ip_file = open("local-ip.txt","r")
            read_ips = read_ip_file.read()
            ips = re.findall( r'[0-9]+(?:\.[0-9]+){3}',str(read_ips))
            for i in ips[0]:
                arr.append(i)
            arr[10],arr[11],arr[12] = '','',''
            new_local_ip_format = ''.join(arr)
        cmd = f'''
#!/bin/sh
for i in {{1..255}}
do (ping  -c 1  {new_local_ip_format}$i | grep  "bytes from" &) 
done
        '''
        file_open = open('/tmp/ping_device.sh','w')
        file_write = file_open.write(cmd)
        file_open.close()
        if os.path.isfile('/tmp/ping.sh'):
            os.system('sudo chmod 777 /tmp/ping_device.sh')
            time.sleep(1.5)
            os.system('sudo bash /tmp/ping.sh')
        else:
            pass
    def wlan_discovery(self):
        try:
            wlan_discovery = lambda wlan : list(Cell.all(wlan))
            wlan0 = wlan_discovery(self.iface)
            print(f"\n{Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}]Discovering Wireless AP in your area...") 
            time.sleep(1.5)
            for wifi in wlan0:
                print(str(wifi).replace("Cell",""))
            print("Discovered a total of {amount} wifi networks.".format(amount=len(wlan0)))
            print(f'\nMore Detailed Results: ')
            time.sleep(1.5)
            os.system('nmcli device wifi list')
        except Exception as Err:
            print(Err)

if __name__ == '__main__':
    try:
        q = queue.Queue()
        t = time.time()
        obj_class = Extract(args.ipaddress,args.subnetrange,args.timeout,args.interface)
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
        wlan_scan = Process(target=obj_class.wlan_discovery)
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
        wlan_scan.start()
        wlan_scan.join()
        print("Done in: {}".format(time.time()-t) + 's')
    except Exception as Err:
        print(Err)
#Dont Be a Script Kiddie. 
