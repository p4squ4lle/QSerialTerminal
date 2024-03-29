from serial import Serial, SerialException
import serial.tools.list_ports

DEFAULT_SERIAL_TIMEOUT = 1    # [second]
END_OF_LINE = '\r\n'
BEGINNIN_OF_LINE = ''

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
    
    def connect(self, port, baudrate, timeout=DEFAULT_SERIAL_TIMEOUT):
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
        self.available_ports = [k for k in self.port_info.keys()]
        
    def send_string(self, string):
        if self.ser:
            self.last_commands.append(string)
            mgs_to_send = f'{BEGINNIN_OF_LINE}{string}{END_OF_LINE}'
            self.ser.write(bytes(mgs_to_send, 'utf-8'))

    def read_string(self):
        if self.ser:
            msg_from_serport = self.ser.read_until(b'\r\n')
            self.last_messages.append(msg_from_serport.decode('utf-8').strip())

    def get_portinfo(self):
        ports = serial.tools.list_ports.comports()
        port_info = {}
        for i, p in enumerate(ports):
            port_info[p.name] = {'device': p.device,
                                 'description': p.description,
                                 'hwid': p.hwid,
                                 'vid': p.vid,
                                 'pid': p.pid,
                                 'serial_number': p.serial_number,
                                 'location': p.location,
                                 'manufacturer': p.manufacturer,
                                 'product': p.product,
                                 'interface': p.interface}
        return port_info


if __name__ == "__main__":
    ser = SerialConnection()
