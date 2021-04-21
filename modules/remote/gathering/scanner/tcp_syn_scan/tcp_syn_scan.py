from ..scanner_module import ScannerModule

class TCPSynScan(ScannerModule):

    def show_usage(self):
        print("Scan a target :)")

def get_module():
    return TCPSynScan()