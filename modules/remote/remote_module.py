from ..base_module import BaseModule


class RemoteModule(BaseModule):
    rhosts = []
    lhost = None
    rports = []
    lport = None

    '''
    Defines if the module can handle multiple targets
    '''
    def multiple_rhosts(self):
        return False

    '''
    Defines if the module can handle multiple hosts
    '''
    def multiple_rports(self):
        return False

