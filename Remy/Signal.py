

class Signal(object):
    def __init__(self, signal):
        self.signal = signal

    @property
    def header(self):
        return self.signal[:9]

    @property
    def footer(self):
        return self.signal[-5:]

    @property
    def body(self):
        return self.signal[9:-5]

    @property
    def length(self):
        return self.header[1:4]
