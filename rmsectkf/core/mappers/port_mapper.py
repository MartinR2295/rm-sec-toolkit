from rmoptions.mapper import BaseMapper
import re


class PortMapper(BaseMapper):

    def __init__(self):
        BaseMapper.__init__(self)

    def get_target_type_name(self):
        return "int"

    def get_expected_input_format(self):
        return "from/to or p1 p2 p3 or all"

    def map(self, value):
        if value == "all":
            return [p for p in range(1, 65535+1)]
        # parse if it's a range (from-to)
        port_range = re.search("^([0-9]+)\-([0-9]+)$", value)

        if port_range:
            return [p for p in range(int(port_range.group(1)), int(port_range.group(2)) + 1)]

        # parse single port number
        if value.isdigit():
            return int(value)
