"""Example code for using the Maqueen Plus V1.0 infrared receiver

Necessary code is provided as a library by Peter Hinch at https://github.com/peterhinch/micropython_ir.

To use the library, copy the 'ir_rx' folder to the root folder of the Pico:ed.
E.g. in Thonny right-click on the folder and select 'Upload to /'.
"""

from ir_rx.test import test

test(8)  # Example for testing with the Samsung protocol
