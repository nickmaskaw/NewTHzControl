from instruments import VISAInstrument


class OttimeDelayline(VISAInstrument):
    MINIMUM_POSITION = 0.0
    MAXIMUM_POSITION = 200.0
    
    def __init__(self, name="Ottime Delay-line"):
        super().__init__(name)
        
        self._velocity = 100
        
    @property
    def velocity(self): return self._velocity
        
    def setVelocity(self, velocity):
        self._velocity = velocity
        
    def moveTo(self, position):
        self.device.query('@0M{position}{self.velocity}')
        
    def returnTo(self, position):
        self.setVelocity(100)
        self.moveTo(position)
        
    def home(self):
        self.device.query('@0R1')