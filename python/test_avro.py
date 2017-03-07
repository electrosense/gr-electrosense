import io
import avro.schema
import avro.io
import socket
import sys
import struct
import numpy as np

schema = avro.schema.parse(open("rtl-spec.avsc").read())



writer = avro.io.DatumWriter(schema)

bytes_writer = io.BytesIO()
encoder = avro.io.BinaryEncoder(bytes_writer)

writer.write({"SenId": 123456, "SenConf":{"HoppingStrategy":0, "WindowingFunction":0, "FFTSize": 256, "AveragingFactor": 5, "FrequencyOverlap": 0.5, "FrequencyResolution": 50, "Gain":-1 }, "SenTime":{"TimeSecs":1262306000, "TimeMicrosecs":np.random.randint(500)}, "SenData":{"CenterFreq":2345, "SquaredMag": [1]*256}}, encoder)

raw_bytes = bytes_writer.getvalue()
print(len(raw_bytes))
print(type(raw_bytes))

bytes_reader = io.BytesIO(raw_bytes)
decoder = avro.io.BinaryDecoder(bytes_reader)
reader = avro.io.DatumReader(schema)
data1 = reader.read(decoder)

print(data1)



def get_constants(prefix):
    """Create a dictionary mapping socket module constants to their names."""
    return dict( (getattr(socket, n), n)
                 for n in dir(socket)
                 if n.startswith(prefix)
                 )

families = get_constants('AF_')
types = get_constants('SOCK_')
protocols = get_constants('IPPROTO_')

# Create a TCP/IP socket
sock = socket.create_connection(('localhost', 5000))

print >>sys.stderr, 'Family  :', families[sock.family]
print >>sys.stderr, 'Type    :', types[sock.type]
print >>sys.stderr, 'Protocol:', protocols[sock.proto]
print >>sys.stderr

try:
    # Send data
    for j in range(4):
        pktlen=int(len(raw_bytes))
        fftsize=int((1-0.5)*(512))
        extra = pktlen%4
        if extra: 
            pktlen=pktlen+extra
            raw_bytes=raw_bytes+struct.pack('!I', 0)[0:extra]
        message = struct.pack('!I', pktlen)+struct.pack('!I', fftsize)+raw_bytes 
        print(len(message))
        sock.sendall(message)

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
