import os,argparse,logging,time
from multiprocessing import Process
from scapy import *
parser = argparse.ArgumentParser()
parser.add_argument('-o','--option',metavar='',help='Option')
args = parser.parse_args()
class Extract(object):
    def __init__(self,option):
         self.option = option
    @staticmethod 
    def banner(s):
        for c in s + '\n' :
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(10. / 100)
    def main(self):
        banner('''        
        
                ''')
if __name__ == '__main__':
    obj_class = Extract(args.option)
    process = Process(target=obj_class.main)
    process.start()
    process.join()

