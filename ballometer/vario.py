class Vario:
    def __init__(self):
        self.qnh_pa = 101325.0  # Pa
        self.pressure = 101325.0  # Pa

    @property
    def altitude(self):
        return 44330.0 * (1.0 - (self.pressure / self.qnh_pa) ** 0.1903)  # m
