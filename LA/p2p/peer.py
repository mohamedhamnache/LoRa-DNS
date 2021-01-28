import threading

from clients.chs_client import Chs_client
from clients.ma_client import La_client

chs_client = Chs_client()
ma_client = La_client()
thread = threading.Thread(
    target=chs_client.startFrameHandler,
    args=("3235313214003900", chs_client.uplinkHandler),
)
thread.start()

qsize = chs_client.frames.qsize()
frames = chs_client.frames
while True:
    if frames.qsize() - qsize > 0:
        frame = frames.get()
        if frame.mType == "JoinRequest":
            print(frame.joinEUI)
            joinEUI = frame.joinEUI
            ma_client.dns_resolver(joinEUI)
        qsize = chs_client.frames.qsize()
        print(qsize)
