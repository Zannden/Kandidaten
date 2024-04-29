import RPi.GPIO as IO
import time
IO.setwarnings(False)
IO.setmode(IO.BCM)

#left leds
IO.setup(26,IO.IN); #GDPIO -> led 1
IO.setup(19,IO.IN); #GDPIO -> led 2
IO.setup(13,IO.IN); #GDPIO -> led 3
IO.setup(6,IO.IN); #GDPIO -> led 4


#right leds
IO.setup(5,IO.IN); #GDPIO -> led 5
IO.setup(11,IO.IN); #GDPIO -> led 6
IO.setup(9,IO.IN); #GDPIO -> led 7
IO.setup(10,IO.IN); #GDPIO -> led 8

state = "Nothing";

#led class id and state
class LED:
	def __init__(self, ID, state):
		self.ID = ID;
		self.state = state;
	def __str__(self):
		return f"Led: {self.ID} ({self.state})"
		
#addresing all leds
led1 = LED(1,"Low")
led2 = LED(2,"Low")
led3 = LED(3,"Low")
led4 = LED(4,"Low")
led5 = LED(5,"Low")
led6 = LED(6,"Low")
led7 = LED(7,"Low")
led8 = LED(8,"Low")

#arayy off IDs
IDs = [led1, led2, led3 ,led4 ,led5, led6 ,led7, led8]

n = 0;
while 1:
	print("Start");
#LED 1
	if(IO.input(26)==True):
		led1.state = "Hig"
	if(IO.input(26)==False):
		led1.state = "Low"
			
#LED 2		
	if(IO.input(19)==True):
		led2.state = "Hig"
	if(IO.input(19)==False):
		led2.state = "Low"
		
#LED 3
	if(IO.input(13)==True):
		led3.state = "Hig"
	if(IO.input(19)==False):
		led3.state = "Low"
		
#LED 4	
	if(IO.input(6)==True):
		led4.state = "Hig"
	if(IO.input(6)==False):
		led4.state = "Low"
			
#LED 5
	if(IO.input(5)==True):
		led5.state = "Hig"
	if(IO.input(5)==False):
		led5.state = "Low"
			
#LED 6
	if(IO.input(11)==True):
		led6.state = "Hig"
	if(IO.input(11)==False):
		led6.state = "Low"
			
#LED 7
	if(IO.input(9)==True):
		led7.state = "Hig"
	if(IO.input(9)==False):
		led7.state = "Low"
			
#LED 8
	if(IO.input(10)==True):
		led8.state = "Hig"
	if(IO.input(10)==False):
		led8.state = "Low"
	
	
	"""
	#fram
	if(IO.input(13)==True and IO.input(9)==True): 
		state = "Forward";
	#fram
	if(IO.input(13)==False and IO.input(9)==False): 
		state = "All low";
		
	#right
	if(IO.input(13)==True and IO.input(9)==False):
		state = "Turning Right";
		
	#left
	if(IO.input(13)==False and IO.input(9)==True):
		state = "Turning Left";
		
	#still
	#else:
		#state = "error";
	print(state);
	"""
	
	#skriver ut Ledsens states i consolen
	print(IDs[0],IDs[1],IDs[2],IDs[3],IDs[4],IDs[5],IDs[6],IDs[7]);
	#for x in IDs:
	#	print(x);
	n+1;	
	time.sleep(1);

