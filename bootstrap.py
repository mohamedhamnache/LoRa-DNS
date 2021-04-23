import uuid

id = uuid.uuid1()

id = id.hex[:8]
print(id)

import coloredlogs, logging

# Create a logger object.
logger = logging.getLogger("LA")

# By default the install() function installs a handler on the root logger,
# this means that log messages from your code and log messages from the
# libraries that you use will all show up on the terminal.
# coloredlogs.install(level='DEBUG')

# If you don't want to see log messages from libraries, you can pass a
# specific logger object to the install() function. In this case only log
# messages originating from that logger will show up on the terminal.
coloredlogs.install(level="DEBUG", logger=logger)

# Some examples.
logger.debug("this is a debugging message")
logger.info("this is an informational message")
logger.warning("this is a warning message")
logger.error("this is an error message")
logger.critical("this is a critical message")
# Device
"""
{
  "device": {
    "devEUI": "beefdead0009deaa",
    "name": "RN2483",
    "applicationID": "5",
    "description": "RN2483",
    "deviceProfileID": "a4207855-19cc-40c4-b33b-0e7bb3546e79",
    "skipFCntCheck": false,
    "referenceAltitude": 0,
    "variables": {},
    "tags": {},
    "isDisabled": false
  }
}

#context
{
  "deviceActivation": {
    "devEUI": "beefdead0009deaa",
    "devAddr": "002cffad",
    "appSKey": "3e3792dc977691557e6735b927350eee",
    "nwkSEncKey": "e4d43b262fed1315b771eefb680d0e48",
    "sNwkSIntKey": "e4d43b262fed1315b771eefb680d0e48",
    "fNwkSIntKey": "e4d43b262fed1315b771eefb680d0e48",
    "fCntUp": 1,
    "nFCntDown": 1,
    "aFCntDown": 0
  }
}
 
 #keys
 {
  "deviceKeys": {
    "devEUI": "beefdead0009deaa",
    "nwkKey": "beef456789abcdef0123456789abcdef",
    "appKey": "00000000000000000000000000000000",
    "genAppKey": ""
  }
}
"""
