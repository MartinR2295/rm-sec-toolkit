from ..base_module import BaseModule
from ...mappers.port_mapper import PortMapper


class RemoteModule(BaseModule):
    def __init__(self):
        BaseModule.__init__(self)
        self.option_rhosts = self.option_handler.create_option("rhosts", "target hosts",
                                                               multiple_values=True,
                                                               required=True,
                                                               needs_value=True)
        self.option_rports = self.option_handler.create_option("rports", "target ports",
                                                               multiple_values=True,
                                                               needs_value=True,
                                                               mapper=PortMapper)
        if self.lpart_exists():
            self.option_lhost = self.option_handler.create_option("lhost", "attacker host",
                                                                  default_value=None,
                                                                  needs_value=True)
            self.option_lport = self.option_handler.create_option("lport", "attacker port",
                                                                  default_value=None,
                                                                  needs_value=True,
                                                                  mapper=PortMapper)

    def run_module(self):
        if super().run_module() == False:
            return False

        if self.option_rports.has_value():
            self.option_rports.value = self.normalize_and_sort_ports_array(self.option_rports.value)

        return True

    # normalize and sort port list
    def normalize_and_sort_ports_array(self, ports):
        port_list = []
        for port in ports:
            if type(port) is list:
                port_list += port
            elif type(port) is int:
                port_list.append(port)
        # remove duplicates and sort the list
        return list(set(sorted(port_list)))

    '''
    Defines if the module needs a left part (lport, lhost)
    '''

    def lpart_exists(self):
        return False

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
