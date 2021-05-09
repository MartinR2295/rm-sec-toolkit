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
- easy to create custom models

## Install

### pip
```shell
pip install rm-sec-toolkit
```

At the first start, the rm-sec-toolkit script loads the modules from github, so the first start can take a bit longer.

## Docker
You can use rm-sec-toolkit with the provided docker image.
Don't forget to use port mapping, if you want to use server modules.
```shell
docker run -t -i rame22/rm-sec-toolkit
```

### Example with a port scan
```shell
docker run -t -i rame22/rm-sec-toolkit -m remote/gathering/scanner/tcp_syn_scan --rhosts 192.168.0.100 --rports 1-1000 -r
```

### Server example
Expose and map the wished port.
Than map the directory you want to the /app directory.
```shell
docker run -t -i --expose 12345 \
-p 12345:12345 \
-v "$(pwd)":/app rame22/rm-sec-toolkit \
-m local/server/http_file_server --lport 12345 -r
```

## Usage

```shell
Usage
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
rm-sec-toolkit

Required Options
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾

Optional Options
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
--add -a: add a resource {multiple values possible}
--create -c: create a resource {multiple values possible}
--flag -f: add a flag for ctf's {multiple values possible}
--help -h: show usage
--interactive -i: use the interactive mode (default)
--module -m: choose a module {multiple values possible}
--note -n: add a note {multiple values possible}
--version -v: show the current version {multiple values possible}

```

### Examples

#### Run a module directly

Use TCP Scanner module and run it instantly

```shell
rm-sec-toolkit -m remote/gathering/scanner/tcp_syn_scan --rhosts 192.168.0.100 --rports 22-100 -r
```

`-m` use directly a specified module. Every other options behind it, will passed to the module arguments<br>
`-r` run the module instantly instead to print the module menu first

#### Create a project

```shell
rm-sec-toolkit -c project
```

#### Add something to the project notes

```shell
rm-sec-toolkit -n -r
```

`-r` is only used to run it directly, because the add notes option is also a regular module

#### Add a flag for ctf's
```shell
rm-sec-toolkit -a flag -n user_flag -f e3b98a4da31a127d4bde6e43033f66ba274cab0eb7eb1c70ec41402bf6273dd8 -r
```

#### Serve a directory in the local network
Sometimes it's necessary for ctf's to serve some scripts
in the local network to download it on the target machine.
That can easily done with the http_file_server module.
```shell
rm-sec-toolkit -m local/server/http_file_server --lport 12345 -r
```

#### Run a script directly without the rm-sec-toolkit console

```shell
python3 /usr/local/share/rm-sec-toolkit/modules/remote/gathering/scanner/tcp_syn_scan/tcp_syn_scan.py --rhosts 192.168.0.100 -r
```

`/usr/local/share/rm-sec-toolkit` is the default modules location

## Update

You can update rm-sec-toolkit with the update function in the menu.

Start rm-sec-toolkit
```shell
rm-sec-toolkit

Contents
--------------------
(1) - others (C)
(2) - local (C)
(3) - remote (C)
--------------------
(u) - check for new updates
(q) - quit

Please choose one element: 
```

With the `u` option you can check for updates, update the toolkit or only update the modules.

## Advanced Possibilities

### Custom script paths

Add paths to your custom scripts to the `~/.rmsectk_custom_paths` file.

```shell
echo "~/my_custom_scripts_folder" >> ~/.rmsectk_custom_paths
```

You also can add custom script paths per project.
```shell
cd yourProject
echo "/any/path/" >> .rm_sec_proj/.rmsectk_custom_paths
```

Any project contains the `project_scripts` folder. This folder is automatically added to the `.rm_sec_proj/.rmsectk_custom_paths` file. Every module which you put in here, you will find in the rm-sec-toolkit in the root tree under `project_scripts`.

### Write your own script

#### Create a module with the create module command
You can easily create a new module with the toolkit itself.

```shell
rm-sec-toolkit -c module -a Your Name -d Any Description -n fancy_module -sn fmodule
```

You have the following options.
```shell
--author -a: module's author {value needed}
--class-name -c: name of the class {value needed} {default: CustomModule}
--description -d: module description {value needed}
--name -n: module name {value needed}
--short-name -sn: module short name {value needed}
--super-class -s: super class {value needed} {default: BaseModule}
--super-class-path -sp: super class path {value needed} {default: rmsectkf.core.modules.base_module}
```


#### Create a module per hand
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
        if super().run_module() == False:
            return False

        #do some cool stuff here
        your_option_value = self.option_your_option.value

# just return your module here
def get_module():
    return YourScanner()


# start the module if it's executed directly
if __name__ == "__main__":
    module = get_module()
    module.init_module()
    module.start_module()
```

## Example

TCP-Syn-Scanner

```python
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
        self.option_rports.default_value = "1-1000"
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

```



