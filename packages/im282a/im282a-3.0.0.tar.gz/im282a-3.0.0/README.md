# iM282A WiMOD LR BASE+ HCI Python library
This library allows communicating with iM282A Radio (LoRa/FLRC/FSK) modules using vendor specific HCI messages and the WiMOD LR BASE+ proprietary firmware.

> SensorApp endpoint is not supported (an in-firmware embedded sensor example application)! Feel free to open a PR if it's needed.

> Most length limitations are not enforced or validated - make sure to read the corresponding vendor documentation of the firmware and module.

## Install
```
python -m pip install im282a
```

## Usage Example
```
from im282a import *
from threading import Thread


def receiver(radio: IM282A):
    while True:
        radio.handle()


with IM282A.from_serial("/dev/ttyUSB0", timeout=1) as radio1, IM282A.from_serial("/dev/ttyUSB1", timeout=1) as radio2:
    t1 = Thread(target=receiver, args=(radio1,))
    t2 = Thread(target=receiver, args=(radio2,))
    t1.start()
    t2.start()

    radio1.send(SetRadioConfigReq(SetRadioModeReq.RadioControlNvmFlag_Ram))
    radio2.send(SetRadioConfigReq(SetRadioModeReq.RadioControlNvmFlag_Ram))

    radio1.send(SendConfirmedDataReq(0x10, 0x1234, b"Test message!"))
    
    t1.join()
    t2.join()
```

```
HciMessage:
 Endpoint ID: 3 (radio_link)
 Message ID: 10 (SendConfirmedDataRsp)
 SendConfirmedDataRsp:
  Status: 0 (ok)
HciMessage:
 Endpoint ID: 3 (radio_link)
 Message ID: 14 (ConfirmedDataTXInd)
 ConfirmedDataTXInd:
  Status: 0 (ok)
  TXEventCounter: 21
  RFMessageAirtime: 497 ms
HciMessage:
 Endpoint ID: 3 (radio_link)
 Message ID: 12 (ConfirmedDataRXInd)
 ConfirmedDataRXInd:
  Status:
   Extended: True
   Decrypted: False
   DecryptionError: False
   Encrypted: False
  DstGroupAddress: 0x10
  DstDeviceAddress: 0x1234
  SrcGroupAddress: 0x10
  SrcDeviceAddress: 0x1234
  Payload: 54657374206d65737361676521 (Test message!)
  Rssi: -64 dBm
  Snr: 7 dB
  RXTime: 2021-09-03 12:54:08
HciMessage:
 Endpoint ID: 3 (radio_link)
 Message ID: 20 (AckTXInd)
 AckTXInd:
  Status: 0 (ok)
  TXEventCounter: 3
  RFMessageAirtime: 346 ms
HciMessage:
 Endpoint ID: 3 (radio_link)
 Message ID: 16 (AckRXInd)
 AckRXInd:
  Status:
   Extended: True
   Decrypted: False
   DecryptionError: False
   Encrypted: False
  DstGroupAddress: 0x10
  DstDeviceAddress: 0x1234
  SrcGroupAddress: 0x10
  SrcDeviceAddress: 0x1234
  Payload:  ()
  Rssi: -60 dBm
  Snr: 7 dB
  RXTime: 2021-09-03 03:54:09
```

## How to use (rough overview)
- `IM282A(<serial_device>, [baud_rate], [timeout_s])` will open a serial device using the SLIP protocol. Timeout will affect reading with `instance.handle()`
- `instance.send(<message>)` is used to send messages derived from the `HciMessage` class.
- `instance.register_handler(<endpoint_id>, <message_id>, <function>)` registers a callback function for a specific endpoint/message combination. Multiple functions can be registered per endpoint/message and are called during `instance.receive()` sequentially. The function receives a `data: bytes` argument which has the endpoint and message IDs already stripped and can be consumed by message classes like `ping_response = PingRsp.from_bytes(data)`.
- `instance.default_handler` will handle all messages that are not handled by a callback function (default handler prints the hex bytes on stdout). The function receives two arguments: `head: bytes, data: bytes`. `head` contains the endpoint and message IDs to be consumed by `HciMessage` and data the rest for the resulting message class. See the example above.

## Contribution
Any help is appreciated, especially on documentation, tests or the API itself. Feel free to open issues or PRs.
