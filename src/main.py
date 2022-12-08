import argparse
from enum import Enum
import hid

RAZER_VID = 0x1532
HANBO_PID = 0x0F35

EXPECTED_USAGE      = 1
EXPECTED_USAGE_PAGE = 0xFF00

class Channel(Enum):
    PUMP = "pump",
    FANS = "fans",
    BOTH = "both",

def main():
    parser = argparse.ArgumentParser(prog = "py-hanbo", description="Controls the ARGB lighting of a Razer Hanbo Cooler")
    parser.add_argument("--channel",
        help="The target of the command: 0 for the pump head -- 1 for the fans -- 2 for both",
        type=str,
        default=Channel.BOTH,
        choices=["pump", "fans", "both"])
    parser.add_argument("-b", "--brightness", help="Sets the brightness of the channel", type=int)
    args = parser.parse_args()

    channels = [Channel.PUMP, Channel.FANS] if args.channel == Channel.BOTH else [args.channel]

    with hid.Device(RAZER_VID, HANBO_PID) as device:
        print(f"Found device: {device.product}")

        if args.brightness is not None:
            if args.brightness < 0 or args.brightness > 100:
                raise ValueError("Brightness must be in the range [0, 100]")
            set_brightness(device, channels, args.brightness)


def set_brightness(device, channels, brightness) -> None:
    for channel in channels:
        print(f"Setting brightness for '{channel}' to: {brightness}")
        payload = [0] # report number
        payload.extend([0x70, 1]) # command id?
        payload.append(channel_id(channel))
        payload.append(brightness)
        device.write(bytes(payload))

def channel_id(channel):
    if channel == Channel.PUMP:
        return 0
    elif channel == Channel.FANS:
        return 1
    raise ValueError(f"Invalid channel: {channel}")


if __name__ == "__main__":
    main()