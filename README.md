# rm-sec-toolkit

[![PyPI version](https://badge.fury.io/py/rm-sec-toolkit.svg)](https://badge.fury.io/py/rm-sec-toolkit)
[![Docker Image Version (latest by date)](https://img.shields.io/docker/v/rame22/rm-sec-toolkit?label=dockerhub)](https://hub.docker.com/repository/docker/rame22/rm-sec-toolkit)
[![Docker Pulls](https://img.shields.io/docker/pulls/rame22/rm-sec-toolkit)](https://hub.docker.com/repository/docker/rame22/rm-sec-toolkit)
[![GitHub last commit](https://img.shields.io/github/last-commit/MartinR2295/rm-sec-toolkit)](https://github.com/MartinR2295/rm-sec-toolkit)


A toolkit and a framework for python security scripts.

## Features

- module based security framework
- console script rm-sec-toolkit
- project handling
- notes handling in the project
- custom scripts location
- ctf flag function for projects

## Install

```shell
pip install rm-sec-toolkit
```

At the first start, the rm-sec-toolkit script load the modules from github, so the first start can take a bit longer.

## Usage

```shell
Usage
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
rm-sec-toolkit

Required Options
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾

Optional Options
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
--create -c: create a resource {multiple values possible}
--flag -f: add a flag for ctf's {multiple values possible}
--help -h: show usage
--module -m: choose a module {multiple values possible}
--note -n: add a note {multiple values possible}
```

### Examples

#### Run a module directly

Use TCP Scanner module and run it instantly

```shell
rm-sec-toolkit -m remote/gathering/scanner/tcp_syn_scan --rhosts 192.168.0.100 --rports 22-100 -r
```

`-m` use directly a specified module. Every other options behind it, will passed to the module arguments
`-r` run the module instantly instead to print the module menu first

#### Create a project

```shell
rm-sec-toolkit -c project
```

#### Add something to the project notes

```shell
rm-sec-toolkit -n -r
```

`-r` is only used to run it directly, because the add notes is also a regular module

#### Run a script directly without the rm-sec-toolkit console

```shell
python3 /usr/local/share/rm-sec-toolkit/modules/remote/gathering/scanner/tcp_syn_scan/tcp_syn_scan.py --rhosts 192.168.0.100 -r
```

`/usr/local/share/rm-sec-toolkit` is the default modules location

## Advanced Possibilities

### custom script paths

Add paths to your custom scripts to the `~/.rmsectk_custom_paths` file.

```shell
echo "~/my_custom_scripts_folder" >> ~/.rmsectk_custom_paths
```

### Write your own script

Create a folder with the following contents.

- __init__.py (just to mark it as package)
- rm_module.json
- your_module.py

#### rm_module.json

```json
{
    "name": "Your Module Name",
    "description": "Description",
    "version": 1.0,
    "author": "Your Name",
    "module": "your_module.py"
}
```

#### your_module.py

```python
#!/usr/bin/env python3
from rmsectkf.core.modules.remote.gathering.scanner.scanner_module import ScannerModule

'''
Your super cool scanner
'''


class YourScanner(ScannerModule):
    def __init__(self):
        ScannerModule.__init__(self)

    # do init stuff here like define the options you need
    def init_module(self):
        #define the options you need (rm-options package)
        self.option_your_option = self.option_handler.create_option("your-option", "your super cool option", needs_value=True, required=True)
        pass

    # this is the part where you put your code
    def run_module(self):
        super().run_module()

        #do some cool stuff here
        your_option_value = self.option_your_option.value

# just return your module here
def get_module():
    return YourScanner()


# start the module if it's executed directly
if __name__ == "__main__":
    get_module().init_module()
    get_module().start_module()
```

## Example

TCP-Syn-Scanner

```python
#!/usr/bin/env python3
from rmsectkf.core.modules.remote.gathering.scanner.scanner_module import ScannerModule
from scapy.all import *

'''
TCP Syn Port Scanner
'''


class TCPSynScan(ScannerModule):
    def __init__(self):
        ScannerModule.__init__(self)

    def init_module(self):
        self.option_rhosts.needs_value = True
        self.option_rhosts.required = True
        self.option_rhosts.value = []
        pass

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


# start the module if it's executed directly
if __name__ == "__main__":
    get_module().init_module()
    get_module().start_module()
```



