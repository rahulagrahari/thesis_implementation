class DriverModel:
    """
        this saves the information about the vehicle
    """
    def __init__(self):
        self.acceleration = None
        self.retardation = None
        self.speed = []
        self.position = []
        self.lane = None
        self.direction = None
        self.requestedSpeed = []
        self.neighbour_info = []
        self.flag = False

    def __str__(self):
        return "Control Object" + str(self)

    @property
    def self_obj(self):
        return self

    @property
    def vehicle_info(self):
        return [self.acceleration,
                self.retardation,
                self.speed,
                self.position,
                self.lane,
                self.direction,
                self.neighbour_info,
                self.requestedSpeed,
                self.flag]
