# CryptoGuruPendingNotifier
This is a desktop notifier app that allows you to see what your pending balance is for the CryptoGuru burst pools

If you find value in this app, please consider donating (addresses below)

This was written in Python 3 using PyQt5. 

First, thanks to user spebern for his awesome API that allowed me to build this notifier
https://github.com/spebern/goburstpool-api-example

You can run this directly by calling the CGPN.py 

Requirements:
- GRPC
- goburstpool-api-example files (attached)
- PyQt5
- requests

```
pip3 install grpcio
pip3 install PyQt5
pip3 install requests
```

I have included the icon and image files required for this. If you have the release EXE file, please put the cryptoguru.png file in the same folder as the EXE if you want the CryptoGuru icon to load (a minor change I have yet to make)

On the first close of the app, a settings.ini file will appear. This is holding the settings you had running (Burst Address or Numeric ID, pool selection and custom refresh time).

If you do not select a custom refresh time, it will default to every hour.

Future Edits on the List:
- Integrade png image into exe file
- Add logging feature

If you enjoy this app and feel like donating, that would be greatly appreciated:


BURST: BURST-NN2Q-K695-SVBH-8RV4V

LTC: LQF2fTV42zvQEQZ4CGvVgfr1eTCVfHKedC

BTC: 3CQRAUkBVe6k9fPiYMuu8B5R87HPnEYsex

XTL: Se3GdnGbpQNbnMhDwVQ6Pd2E3FEA2SYBzLqsqRu4NLZmRbwr6MCB9upNrGAetk2iq3gUB8oHa5mA5h2T3sXh4vzf2iV8owuJh

ETN: etnkN25ezb96s7aRbqajd1EYjZCCNhLT47nDHsmyc3uhQABr4RzZ989ahxekNhvCgFKuE3WBtBXXBeWsKB13wLZJ5eEKT3LePp

BitTube: bxc3eVkgTZZ4yiahRkGiqBjDzLC22AN3uWZzLfuhuRoENARFzAxCjrFekkzyEoDsARQUaG9JTLWCFT8L6jF9ngkD2ivDCxovL
