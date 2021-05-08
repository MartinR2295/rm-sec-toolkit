from rmsectkf.core.network.port_service_map import *


class Port(object):

    @staticmethod
    def get_service_with_number(port_number):
        if port_number in port_service_map:
            return port_service_map[port_number]
        return None
