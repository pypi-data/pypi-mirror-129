"""
UBX Protocol Polling payload definitions

THESE ARE THE PAYLOAD DEFINITIONS FOR _POLL_ MESSAGES _TO_ THE RECEIVER
(e.g. query configuration; request monitoring, receiver management, logging or sensor fusion status)
Response payloads are defined in UBX_PAYLOADS_GET

NB: Attribute names must be unique within each message class/id

Created on 27 Sep 2020

Information sourced from u-blox Interface Specifications © 2013-2021, u-blox AG

:author: semuadmin
"""

from pyubx2.ubxtypes_core import U1, U2, U4

UBX_PAYLOADS_POLL = {
    # AID messages are deprecated in favour of MGA messages in >=Gen8
    "AID-ALM": {},
    "AID-ALM-SV": {"svid": U1},
    "AID-AOP": {},
    "AID-AOP-SV": {"svid": U1},
    "AID-DATA": {},
    "AID-EPH": {},
    "AID-EPH-SV": {"svid": U1},
    "AID-HUI": {},
    "AID-INI": {},
    # *************************************************
    "CFG-ANT": {},
    "CFG-DAT": {},
    "CFG-DOSC": {},
    "CFG-DYNSEED": {},
    "CFG-ESRC": {},
    "CFG-FIXSEED": {},
    "CFG-GEOFENCE": {},
    "CFG-GNSS": {},
    "CFG-INF": {"protocolID": U1},
    "CFG-ITFM": {},
    "CFG-LOGFILTER": {},
    "CFG-MSG": {"msgClass": U1, "msgID": U1},
    "CFG-NAV5": {},
    "CFG-NAVX5": {},
    "CFG-NMEA": {},
    "CFG-ODO": {},
    "CFG-PM2": {},
    # 'CFG-PM': {
    # },
    "CFG-PMS": {},
    "CFG-PRT": {"portID": U1},
    "CFG-PWR": {},
    "CFG-RATE": {},
    "CFG-RINV": {},
    "CFG-RXM": {},
    "CFG-SBAS": {},
    "CFG-TMODE2": {},
    # 'CFG-TMODE': {
    # },
    "CFG-TP5": {},
    "CFG-TP5-TPX": {"tIdx": U1},
    # 'CFG-TP': {
    # },
    "CFG-TXSLOT": {},
    "CFG-USB": {},
    "CFG-VALGET": {
        "version": U1,
        "layer": U1,
        "position": U2,
        "group": ("None", {"keys": U4}),  # repeating group
    },
    # *************************************************
    "ESF-ALG": {},
    "ESF-INS": {},
    "ESF-STATUS": {},
    # *************************************************
    "LOG-BATCH": {},
    "LOG-INFO": {},
    # *************************************************
    "MGA-DBD": {},
    # *************************************************
    "MON-COMMS": {},
    "MON-GNSS": {},
    "MON-HW": {},
    "MON-HW2": {},
    "MON-HW3": {},
    "MON-IO": {},
    "MON-MGSPP": {},
    "MON-PATCH": {},
    "MON-RF": {},
    "MON-RXBUF": {},
    "MON-SMGR": {},
    "MON-SPAN": {},
    "MON-TXBUF": {},
    "MON-VER": {},
    # *************************************************
    "NAV-CLOCK": {},
    "NAV-DOP": {},
    "NAV-GEOFENCE": {},
    "NAV-HPPOSECEF": {},
    "NAV-HPPOSLLH": {},
    "NAV-ODO": {},
    "NAV-ORB": {},
    "NAV-POSECEF": {},
    "NAV-POSLLH": {},
    "NAV-PVT": {},
    "NAV-RELPOSNED": {},
    "NAV-SAT": {},
    "NAV-SBAS": {},
    "NAV-SIG": {},
    "NAV-SLAS": {},
    "NAV-STATUS": {},
    "NAV-SVIN": {},
    "NAV-TIMEBDS": {},
    "NAV-TIMEGAL": {},
    "NAV-TIMEGLO": {},
    "NAV-TIMELS": {},
    "NAV-QZSS": {},
    "NAV-TIMEUTC": {},
    "NAV-VELECEF": {},
    "NAV-VELNED": {},
    # *************************************************
    "RXM-MEASX": {},
    "RXM-IMES": {},
    "RXM-RAW": {},
    "RXM-RAWX": {},
    "RXM-SVSI": {},
    # *************************************************
    "TIM-FCHG": {},
    "TIM-SVIN": {},
    "TIM-TM2": {},
    "TIM-TP": {},
    "TIM-VCOCAL": {},
    "TIM-VRFY": {},
    # *************************************************
    "UPD-SOS": {},
}
