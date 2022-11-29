from instruments import VISAInstrument


class OttimeDelayline(VISAInstrument):
    MINIMUM_POSITION = 0.0
    MAXIMUM_POSITION = 200.0
    
    def __init__(self, name):
        super().__init__(name)
        