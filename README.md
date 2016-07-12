|B|I|G| |F|A|C|E| |R|O|B|O|T|I|C|S|

Author : Peter Neal

BFR4WD
Software for BFR4WD mobile robot.

Contains arduino code and python scripts to run on the onboard Raspberry pi.

BFR4WD.ino

Arduino code. Will wait until data is received and act depending on the instruction sent. Functions include control loops for the two head servos and the 4 continuous rotation servos used for the drive wheels. Encoders on the wheels provide feedback for the control loop. Uses a command set that I have named BFRCode to receive commands from a connected PC.


|            |Command | Description| Parameters|Description|
|---|--------|--------|------------|-----------|-----------|         
|Wheel Move|	 W1|	          Move forward|	          D|	            Encoder counts|
|          |    	W2|	          Move reverse	 |         D|	            Encoder counts|
|	   |           W3|	          Turn left on spot|	      D	|            Encoder counts|
|	   |           W4 |         	Turn right on spot|	    D	 |           Encoder counts|
|	    |          W5|	          Forward Arc	   |       L and R| Left encoder count and right encoder count|
|	    |          W6|	          Reverse Arc	  |        L and R|Left encoder count and right encoder count|
|Head Move  |   	H1|		                    |       P and T/ P or T|	|
|Set     |      	S1	 |         Wheel speed	   |         V	  |          Speed|
|	   |           S2|	          Head speed|	            V	|            Speed (0-10)|
|	   |           S3|	          Sonar threshold|	        V| cm value to trigger obstacle detected|
|	    |          S4 |         	IR threshold	|          V|	 IR value (0-400) to trigger obstacle detected|
|Get	  |          G1	   |       FL Encoder		|
|	  |            G2|	          RL Encoder	|	
|	  |            G3|	          FR Encoder	|	
|        |     	G4  |        	RR Encoder	|	
|	  |            G5|	          Sonar		|
|	  |            G6  |       	Left IR	|	
|	 |            G7   |         Right IR	|	
|Error	 |         E0	   |       No error – command complete|		
|	 |             E1|	          Invalid command|		
|	 |             E2|	          Obstacle sonar|		
|	 |             E3|	          Obstacle Left IR|		
|	 |             E4|	          Obstacle Right IR|		
|	 |             E5|	          Wheel move timeout|		
|Image	 |       IMGDIS	    |    Capture and display image|		
|	 |           IMGSAVE|	        Capture image and save|		


