#!/usr/bin/env python3
from rmsectkf.core.modules.remote.gathering.scanner.scanner_module import ScannerModule
from rmsectkf.core.network.port import Port
from scapy.all import *

'''
TCP Syn Port Scanner
'''


class TCPSynScan(ScannerModule):
    def __init__(self):
        ScannerModule.__init__(self)

    def init_module(self):
        super().init_module()
        self.option_rhosts.required = True
        self.option_rports.default_value = ["1-1000"]
        self.option_rports.required = True

    def run_module(self):
        if super().run_module() == False:
            return False

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
                        print(
                            "\tport {} is open (possible service: {})".format(port, Port.get_service_with_number(port)))


def get_module():
    return TCPSynScan()


# start the module if it's executed directly
if __name__ == "__main__":
    module = get_module()
    module.init_module()
    module.start_module()
