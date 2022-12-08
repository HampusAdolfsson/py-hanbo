# py-hanbo

A command line utility for controlling the brightness and colors of the Razer Hanbo AIO cooler.
Uses reverse-engineered HID packets, and thus works without Razer Synapse. Tested on windows, but should work on linux as well.

The Hanbo does not seem to support hardware effects; it only allows direct control of the LED colors. Thus, to achieve anything other than
static colors you'd need some software on your computer driving the effects (e.g. [Artemis](https://artemis-rgb.com/)).

## Usage
See:
```sh
python3 src/main.py --help
```
