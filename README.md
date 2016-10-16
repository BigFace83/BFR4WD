|B|I|G| |F|A|C|E| |R|O|B|O|T|I|C|S|

Author : Peter Neal

BFR4WD
Software for BFR4WD mobile robot.

Contains arduino code and python scripts to run on the onboard Raspberry pi.

BFR4WD.ino

Arduino code. Will wait until data is received and act depending on the instruction sent. Functions include control loops for the two head servos and the 4 continuous rotation servos used for the drive wheels. Encoders on the wheels provide feedback for the control loop. Uses a command set that I have named BFRCode to receive commands from a connected PC.

Be Aware: Most of this is work in progress and experimentation. Use as reference but not all functions are complete.
