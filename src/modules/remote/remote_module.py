from ..base_module import BaseModule


class RemoteModule(BaseModule):
    def __init__(self):
        BaseModule.__init__(self)
        self.option_rhosts = self.option_handler.create_option("rhosts", "target hosts",
                                                               multiple_values=True,
                                                               default_value=[])
        self.option_lhost = self.option_handler.create_option("lhost", "attacker host",
                                                              default_value=None)
        self.option_rports = self.option_handler.create_option("rports", "target ports",
                                                               multiple_values=True,
                                                               default_value=[])
        self.option_lport = self.option_handler.create_option("lport", "attacker port",
                                                              default_value=None)


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

