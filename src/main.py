import argparse
from enum import Enum
import hid
import re

RAZER_VID = 0x1532
HANBO_PID = 0x0F35

def main():
    parser = argparse.ArgumentParser(prog = "py-hanbo", description="Controls the ARGB lighting of a Razer Hanbo Cooler")
    parser.add_argument("--channel",
        help="The target of the command",
        type=str,
        default="both",
        choices=["all", "pump", "fan1", "fan2", "fan3", "fans"])
    parser.add_argument("-b", "--brightness", help="Sets the brightness of the channel. NOTE: the fan1 channel controls the brightness of all fans. It is not possible to control the brightness of each individual fan.", type=int)
    parser.add_argument("--fill", help="Sets all LEDs for the selected channel(s) to the given color (hex format, e.g. #FF0000)", type=str)
    args = parser.parse_args()

    channels = {
        "all": ["pump", "fan1", "fan2", "fan3"],
        "fans": ["fan1", "fan2", "fan3"],
    }.get(args.channel) or [args.channel]

    with hid.Device(RAZER_VID, HANBO_PID) as device:
        print(f"Found device: {device.product}")

        if args.brightness is not None:
            if args.brightness < 0 or args.brightness > 100:
                raise ValueError("Brightness must be in the range [0, 100]")
            set_brightness(device, channels, args.brightness)

        if args.fill is not None:
            color = parse_color(args.fill)
            set_color_fill(device, channels, color)


def set_brightness(device, channels, brightness) -> None:
    for channel in channels:
        print(f"Setting brightness for '{channel}' to: {brightness}")
        payload = [0] # report number
        payload.extend([0x70, 1]) # command id?
        payload.append(channel_id(channel))
        payload.append(brightness)
        device.write(bytes(payload))

def set_color_fill(device, channels, color):
    for channel in channels:
        print(f"Setting color for '{channel}' to: {color}")
        payload = [0] # report number
        payload.append(color_command(channel))
        payload.extend([0x01, 0x07, 0, 0, 0, 0]) # not sure what these mean
        payload.append(channel_id(channel))
        payload.extend([color[1], color[0], color[2]] * channel_size(channel)) # colors are GRB
        device.write(bytes(payload))

def parse_color(hex):
    """Parses a hex string to an RGB tuple"""
    match = re.match(r"#([a-fA-F\d]{6})", hex)
    if match is None:
        raise ValueError(f"Invalid color '{hex}'. It must be a hex string (e.g. #ff0000)")
    color_str = match.group(1)
    return (int(color_str[0:2], 16), int(color_str[2:4], 16), int(color_str[4:6], 16))

def channel_id(channel):
    id = {
        "pump": 0,
        "fan1": 1,
        "fan2": 2,
        "fan3": 3,
    }.get(channel)
    if id is None:
        raise ValueError(F"Invalid channel: {channel}")
    return id

def channel_size(channel):
    """Gives the number of LEDs in the channel"""
    size = {
        "pump": 16,
        "fan1": 18,
        "fan2": 18,
        "fan3": 18,
    }.get(channel)
    if size is None:
        raise ValueError(F"Invalid channel: {channel}")
    return size

def color_command(channel):
    """Gets the first byte used to set colors for the channel. This is *probably* some sort of command id."""
    command = {
        "pump": 0x32,
        "fan1": 0x40,
        "fan2": 0x40,
        "fan3": 0x40,
    }.get(channel)
    if command is None:
        raise ValueError(F"Invalid channel: {channel}")
    return command


if __name__ == "__main__":
    main()