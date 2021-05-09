#!/usr/bin/env python3
from rmsectkf.core.modules.remote.remote_module import RemoteModule
import http.server
import socketserver

'''
HttpFileServerModule
'''


class HttpFileServerModule(RemoteModule):

    def __init__(self):
        super().__init__()

    def lpart_exists(self):
        return True

    def init_module(self):
        super().init_module()
        self.option_rhosts.required = False
        self.option_lport.default_value = 8888
        self.option_lport.required = True

    def run_module(self):
        if super().run_module() == False:
            return False

        print("start server on port {}".format(self.option_lport.value))
        with socketserver.TCPServer(("0.0.0.0", self.option_lport.value),
                                    http.server.SimpleHTTPRequestHandler) as server:
            print("use curl http://your-ip:{}/file to get the file you want on the target.".format(
                self.option_lport.value))
            server.serve_forever()


def get_module():
    return HttpFileServerModule()


# start the module if it's executed directly
if __name__ == "__main__":
    module = get_module()
    module.init_module()
    module.start_module()
