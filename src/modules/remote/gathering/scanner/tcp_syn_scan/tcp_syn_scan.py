from ..scanner_module import ScannerModule
from scapy.all import *

'''
new idea:
make a module for a man in the middle device.
So two Ethernet inputs, and almost all traffic go through them. 
Now we can send Ethernet and IP Packages with fake mac and ip addresses (or also random for each request).
The responses to this request we block, and send a rst back.
With this approach all requests come from another device, and IDS and IPS are not able to detect it.
'''


class TCPSynScan(ScannerModule):
    def __init__(self):
        ScannerModule.__init__(self)

    def init_module(self):
        self.option_rhosts.needs_value = True
        self.option_rhosts.required = True
        self.option_rhosts.value = []
        pass

    def show_usage(self):
        print("tcp scanning usage")

    def run_module(self):
        super().run_module()

        # ask for rports if no one is specified
        while len(self.option_rhosts.value) < 1:
            print("Please specify the host which should be scanned!")
            ip = input("IP-Address of target: ")
            self.option_rhosts.value.append(ip)

        # set the most common ports if no one is specified
        if not self.option_rports.in_use or len(self.option_rports.value) < 1:
            self.option_rports.value = [x for x in range(1, 1001)]

        # do the scan for each host
        for host in self.option_rhosts.value:
            print("\nresults for {}:".format(host))
            for port in self.option_rports.value:
                ip = IP(dst=host)  # host ip
                tcp = TCP(dport=port, flags='S')  # specify port and the SYN flag

                # do the request, and get the response
                for request, response in sr(ip / tcp, verbose=0, timeout=0.1)[0]:
                    # check if the response has a tcp layer and check if the flag is a (SYN, ACK) flag.
                    # in that case the port is open
                    if response.haslayer(TCP) and response.getlayer(TCP).flags == 0x12:
                        print("\tport {} is open".format(port))


def get_module():
    return TCPSynScan()