from PythonApplication1 import classify_new
from io import BytesIO
import socket


soc = socket.socket()
soc.bind(("", 8000))
soc.listen(5)
while True:
    sock, adrr_info = soc.accept()
    recv_bytes = -1
    file = BytesIO()
    buffer = bytearray(4096)
    total_bytes = 0
    while recv_bytes != 0:
        recv_bytes = sock.recv_into(buffer)
        file.write(buffer[:recv_bytes])
        total_bytes += recv_bytes
    print("{0} bytes written to memory".format(total_bytes))
    sock.close()
    file.seek(0)
    classify_new(file.read())


soc.close()