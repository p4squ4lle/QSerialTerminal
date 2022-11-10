from serial import Serial, SerialException
import serial.tools.list_ports

class SerialConnection():
    """
    establish a serial connection to a device and receive/send serial data.
    """

    def __init__(self):
        self.ser = None
        self.port = None
        self.baudrate = None
        self.timeout = None

        self.connected = False
        self.last_commands = []
        self.last_messages = []

        self.refresh_portlist()
    
    def connect(self, port, baudrate, timeout):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = Serial(self.port, self.baudrate, timeout=self.timeout)
        self.connected = True

    def close(self):
        if self.ser:
            self.ser.close()
        self.__init__()

    def refresh_portlist(self):
        self.port_info = self.get_portinfo()
        self.num_ports = len(self.port_info.keys())
        self.available_ports = [self.port_info[i]['name']
                                for i in range(self.num_ports)]

    def send_string(self, string):
        if self.ser:
            self.ser.write(string)

    def read_string(self):
        if self.ser:
            self.last_message = self.ser.read()

    def get_portinfo(self):
        ports = serial.tools.list_ports.comports()
        port_info = {}
        for i, p in enumerate(ports):
            port_info[i] = {'device': p.device,
                            'name': p.name,
                            'description': p.description,
                            'hwid': p.hwid,
                            'vid': p.vid,
                            'pid': p.pid,
                            'serial_number': p.serial_number,
                            'location': p.location,
                            'manufacturer': p.manufacturer,
                            'product': p.product,
                            'interface': p.interface
                            }
        return port_info


if __name__ == "__main__":
    ser = SerialConnection()
