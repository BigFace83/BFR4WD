#include <Servo.h> 
#include <math.h> 
#include <Wire.h> //For I2C compass module

#define BUFFERSIZE 64
#define PANCENTRE 1550
#define TILTCENTRE 1550
#define compassaddress 0x60 //defines address of compass

Servo FLwheel;
Servo RLwheel;
Servo FRwheel;
Servo RRwheel;
Servo HeadPan;
Servo HeadTilt;

/**************************************
Global variables
**************************************/
int FLencoder;
int FLencodertotal;
int RLencoder;
int RLencodertotal;
int FRencoder;
int FRencodertotal;
int RRencoder;
int RRencodertotal;

float pulsespercm = 6.94;
float pulsesperdegree = 2.1;
boolean servopoweron = false;


char databuffer[BUFFERSIZE];
int serialcounter = 0;

int WheelSpeed = 3;
int HeadSpeed = 5;

unsigned long previousMilliswheels = 0; //variable for wheel pid loop
unsigned long previousMillishead = 0; //variable for head servo control loop

int HeadPanpos = PANCENTRE;
int HeadTiltpos = TILTCENTRE;
int HeadPanDegrees = 0;
int HeadTiltDegrees = 0;

int SonarThreshold = 20;
int IRThreshold = 2000;

/**************************************
Interrupt handlers for encoders
**************************************/
void incrementFL()
{
  FLencoder ++;
  FLencodertotal ++;
}

void incrementRL()
{
  RLencoder ++;
  RLencodertotal ++;
}

void incrementFR()
{
  FRencoder ++;
  FRencodertotal ++;
}


void incrementRR()
{
  RRencoder ++;
  RRencodertotal ++;
}


void setup() 
{ 
  
  Serial.begin(115200); //start serial communication
  
  Wire.begin(); //connects I2C

  attachInterrupt(0, incrementFL, CHANGE);
  attachInterrupt(1, incrementRL, CHANGE);
  attachInterrupt(4, incrementFR, CHANGE);
  attachInterrupt(5, incrementRR, CHANGE);
  
  pinMode(2, INPUT);
  pinMode(3, INPUT);
  
  FLwheel.attach(4);
  RLwheel.attach(5);
  FRwheel.attach(6);
  RRwheel.attach(7);
  HeadPan.attach(8);
  HeadTilt.attach(9);
  
  FLwheel.writeMicroseconds(1500); //set wheel servos to centre position
  RLwheel.writeMicroseconds(1500);
  FRwheel.writeMicroseconds(1500);
  RRwheel.writeMicroseconds(1500);
  HeadPan.writeMicroseconds(PANCENTRE);
  HeadTilt.writeMicroseconds(TILTCENTRE);

  pinMode(28, OUTPUT); //enable servo power pin

  
}

void loop() 
{ 
  

  while(Serial.available() > 0)  // if something is available from serial port
  { 
      
      char c=Serial.read();      // get it
      databuffer[serialcounter] = c; //add it to the data buffer
      serialcounter++;
      if(c=='\n')  //newline character denotes end of message
      { 
        serialcounter = 0; //reset serialcounter ready for the next message
        
        interpretcommand();

        break;
      }
      
  }
 
}

void interpretcommand()
{
   int Wvalue; //Move wheels
   int Hvalue; //Head move
   int Dvalue; //Data
   int Svalue; //Set
   int Pvalue; //Pan
   int Tvalue; //Tilt
   int Gvalue; //Get
   int Vvalue; //value for set
   int Lvalue; //left wheel encoder count
   int Rvalue; //right wheel encoder count
   boolean validcommand = false;
   
   //Check for any set commands first
   
   Svalue = findchar('S');
   switch(Svalue){
   case(1):{
       Vvalue = findchar('V');
       if(Vvalue == 0)
       {
         digitalWrite(28, LOW); //servo power relay on
         Serial.println("Power Off");
         servopoweron = false;
         validcommand = true;
       }
       if(Vvalue == 1)
       {
         digitalWrite(28, HIGH); //servo power relay on
         Serial.println("Power On");
         servopoweron = true;
         validcommand = true;
       }
       break;}  
     
   case(2):{
       Vvalue = findchar('V');
       if(Vvalue != -1)
       {
         WheelSpeed = Vvalue;
         Serial.print("Wheel speed set to ");
         Serial.println(Vvalue);
         validcommand = true;
       }
       break;}
       
   case(3):{
       Vvalue = findchar('V');
       if(Vvalue != -1)
       {
         if (Vvalue < 0 || Vvalue > 10)
         {
           //Speed value out of range. Change nothing and break.
           //Error code E1 is returned as validcommand is not set to true here 
           break;
         }
         HeadSpeed = Vvalue;
         Serial.print("Head speed set to ");
         Serial.println(Vvalue);
         validcommand = true;
       }
       break;}
     
     }   
   
   //Then check for any wheel move commands and execute
   
   Wvalue = findchar('W');
   if (Wvalue != -1 && servopoweron == false) //don't bother trying to move if servo power is not on
   {
       Serial.println("Servo power is off!");
       return;
   }
   switch(Wvalue){
   case(1):{
       Dvalue = findchar('D');
       if(Dvalue != -1)
       {
         int retval = moverobot(Wvalue, Dvalue*pulsespercm); //convert cm to pulses
         if (retval==0)
             Serial.println("E0");
         else if (retval==1) 
             Serial.println("E2");
         else if (retval==2) 
             Serial.println("E3");
         else if (retval==3) 
             Serial.println("E4");
         validcommand = true;      
       }
       break;}
      
    case(2):{
       Dvalue = findchar('D');
       if(Dvalue != -1)
       {
         int retval = moverobot(Wvalue, Dvalue*pulsespercm); //convert cm to pulses
         if (retval==0)
             Serial.println("E0");
         else if (retval==1) 
             Serial.println("E2");
         else if (retval==2) 
             Serial.println("E3");
         else if (retval==3) 
             Serial.println("E4"); 
         validcommand = true;    
       }
       break;}
       
    case(3):{
       Dvalue = findchar('D');
       if(Dvalue != -1)
       {
         int retval = moverobot(Wvalue, Dvalue*pulsesperdegree); //convert cm to pulses
         if (retval==0)
             Serial.println("E0");
         else if (retval==1) 
             Serial.println("E2");
         else if (retval==2) 
             Serial.println("E3");
         else if (retval==3) 
             Serial.println("E4");
         validcommand = true;    
       }
       break;}
       
    case(4):{
       Dvalue = findchar('D');
       if(Dvalue != -1)
       {
         int retval = moverobot(Wvalue, Dvalue*pulsesperdegree); //convert cm to pulses
         if (retval==0)
             Serial.println("E0");
         else if (retval==1) 
             Serial.println("E2");
         else if (retval==2) 
             Serial.println("E3");
         else if (retval==3) 
             Serial.println("E4"); 
         validcommand = true;    
       }
       break;}
       
    //Move arc forward   
    case(5):{
       Lvalue = findchar('L');
       if(Lvalue != -1)
       {
         Rvalue = findchar('R');
         if(Rvalue != -1)
         {
             int retval = movearc(1, Lvalue*pulsespercm, Rvalue*pulsespercm);
             if (retval==0)
                 Serial.println("E0");
             else if (retval==1) 
                 Serial.println("E2");
             else if (retval==2) 
                 Serial.println("E3");
             else if (retval==3) 
                 Serial.println("E4"); 
             validcommand = true;
         }    
       }
       break;}
       
    //Move arc reverse   
    case(6):{
       Lvalue = findchar('L');
       if(Lvalue != -1)
       {
         Rvalue = findchar('R');
         if(Rvalue != -1)
         {
             int retval = movearc(2, Lvalue*pulsespercm, Rvalue*pulsespercm);
             if (retval==0)
                 Serial.println("E0");
             else if (retval==1) 
                 Serial.println("E2");
             else if (retval==2) 
                 Serial.println("E3");
             else if (retval==3) 
                 Serial.println("E4"); 
             validcommand = true;
         }    
       }
       break;}
       
    // Turn to compass heading clockwise  
    case(7):{
       Vvalue = findchar('V');
       if(Vvalue != -1)
       {
          if(Vvalue < 0 || Vvalue > 358)
          {
            //value is outside of compass range. Ignore command and break.
            //Error code E1 is returned as validcommand is not set to true here
            break;
          }
          int retval = moveheading(Vvalue);
          if (retval==0)
              Serial.println("E0");
          else if (retval==1) 
              Serial.println("E2");
          else if (retval==2) 
              Serial.println("E3");
          else if (retval==3) 
              Serial.println("E4"); 
          validcommand = true;    
       }
       break;}
       
       
   }
       
    //Check for any head move commands and execute
   
   Hvalue = findchar('H'); 
   switch(Hvalue){   
    case(1):{
       Pvalue = findchar('P');
       if(Pvalue != -1)
       {
         HeadPanDegrees = Pvalue;
         validcommand = true;
       }
       Tvalue = findchar('T');
       if(Tvalue != -1)
       {
         HeadTiltDegrees = Tvalue;
         validcommand = true;
       }
       if(Pvalue != -1 || Tvalue != -1) 
       {
           MoveHead(HeadPanDegrees,HeadTiltDegrees);
           Serial.println("E0");
       }
       break;}
       
     }
     
    //Finally check for any get commands and return required data 
     
    Gvalue = findchar('G');
    switch(Gvalue){
    case(1):{
        int encodercm = FLencodertotal/pulsespercm;
        Serial.println(encodercm);
        validcommand = true;
        break;}
    case(2):{
        int encodercm = RLencodertotal/pulsespercm;
        Serial.println(encodercm);
        validcommand = true;
        break;}
    case(3):{
        int encodercm = FRencodertotal/pulsespercm;
        Serial.println(encodercm);
        validcommand = true;
        break;}
    case(4):{
        int encodercm = RRencodertotal/pulsespercm;
        Serial.println(encodercm);
        validcommand = true;
        break;}
    case(5):{
        int sonar = readsonar();
        Serial.println(sonar);
        validcommand = true;
        break;}
    case(6):{
        int IRLeft = readLeftIR();
        Serial.println(IRLeft);
        validcommand = true;
        break;}
    case(7):{
        int IRRight = readRightIR();
        Serial.println(IRRight);
        validcommand = true;
        break;}
    case(8):{
        int Bearing = readcompass();
        Serial.println(Bearing);
        validcommand = true;
        break;}    
        
        
    }
    
    //Do something here if an invalid command is received and return error code E1
    if(validcommand == false)
        Serial.println("E1");
     
     
}


int findchar(char a)
{
  int charindex;
  String value;
  //Find the index of the character being looked for
  for(int i = 0; i<BUFFERSIZE; i++)
  {
    if(databuffer[i] == '\n')
    {
      return -1; //no character found so return -1
    }   
    if(databuffer[i] == a)
    {
      charindex = i;
      break;
    }
  }
  
  //extract characters following character of interest as a string and convert to a value
  for(int i = charindex+1; i<BUFFERSIZE; i++)
  {
    value += (databuffer[i]);
  }
  int data = value.toInt();
  return data;
  
}



int moverobot(int robotdirection, int encodercount)
{

  int pgain = 3;
  int FLwheelspeed = 1500;
  int RLwheelspeed = 1500;
  int FRwheelspeed = 1500;
  int RRwheelspeed = 1500;
  int FLsetpoint;
  int RLsetpoint;
  int FRsetpoint;
  int RRsetpoint;
  boolean FLdone = false;
  boolean RLdone = false;
  boolean FRdone = false;
  boolean RRdone = false;
  
  
  
  switch(robotdirection){
    case(1):
      //Robot forward
      FLsetpoint = -WheelSpeed;
      RLsetpoint = -WheelSpeed;
      FRsetpoint = WheelSpeed;
      RRsetpoint = WheelSpeed;
      break;
    case(2):
      //Robot reverse
      FLsetpoint = WheelSpeed;
      RLsetpoint = WheelSpeed;
      FRsetpoint = -WheelSpeed;
      RRsetpoint = -WheelSpeed;
      break;
    case(3):
      //Turn left on the spot
      FLsetpoint = WheelSpeed;
      RLsetpoint = WheelSpeed;
      FRsetpoint = WheelSpeed;
      RRsetpoint = WheelSpeed;
      break;
    case(4):
      //Turn right on the spot
      FLsetpoint = -WheelSpeed;
      RLsetpoint = -WheelSpeed;
      FRsetpoint = -WheelSpeed;
      RRsetpoint = -WheelSpeed;
      break;
   
  }
    
    
  //initialize all encoder counts to zero before
  //entering pid loop
  FLencodertotal = 0;
  RLencodertotal = 0;
  FRencodertotal = 0;
  RRencodertotal = 0;
  FLencoder = 0;
  RLencoder = 0;
  FRencoder = 0;
  RRencoder = 0;
  
  
  
  while(true){
    
        unsigned long currentMillis = millis();
        
        if(currentMillis - previousMilliswheels > 100) //use this to determine frequency of servo loop
        {
            // save the last time pid loop was called
            previousMilliswheels = currentMillis;
            
            /*******************************************************************************************
            * Control loop for wheels  
            *******************************************************************************************/

           FLwheelspeed = WheelLoop(FLwheelspeed, FLsetpoint, FLencoder, pgain);
           FLencoder = 0;
           
           RLwheelspeed = WheelLoop(RLwheelspeed, RLsetpoint, RLencoder, pgain);
           RLencoder = 0;
           
           FRwheelspeed = WheelLoop(FRwheelspeed, FRsetpoint, FRencoder, pgain);
           FRencoder = 0;
           
           RRwheelspeed = WheelLoop(RRwheelspeed, RRsetpoint, RRencoder, pgain);
           RRencoder = 0;
           
    
          //set new wheel speeds
          FLwheel.writeMicroseconds(FLwheelspeed);
          RLwheel.writeMicroseconds(RLwheelspeed);
          FRwheel.writeMicroseconds(FRwheelspeed);
          RRwheel.writeMicroseconds(RRwheelspeed);
          
        }
        
        /*******************************************************************************************
        * Check to see if encoder setpoints have been reached
        * If they have, stop the wheels and return
        *******************************************************************************************/
        if(FLencodertotal>=encodercount) //if encoder target has been reached
        {
          FLsetpoint = 0; //put setpoint to zero
          FLwheel.writeMicroseconds(1500); //stop the wheels
          FLdone = true;
        }
        if(RLencodertotal>=encodercount) //if encoder target has been reached
        {
          RLsetpoint = 0; //put setpoint to zero
          RLwheel.writeMicroseconds(1500); //stop the wheels
          RLdone = true;
        }
        if(FRencodertotal>=encodercount) //if encoder target has been reached
        {
          FRsetpoint = 0; //put setpoint to zero
          FRwheel.writeMicroseconds(1500); //stop the wheels
          FRdone = true;
        }
        if(RRencodertotal>=encodercount) //if encoder target has been reached
        {
          RRsetpoint = 0; //put setpoint to zero
          RRwheel.writeMicroseconds(1500); //stop the wheels
          RRdone = true;
        }
        
        
        if(FLdone && RLdone && FRdone && RRdone) //if all wheels have reached their target
        {
          FLwheel.writeMicroseconds(1500); //stop the wheels
          RLwheel.writeMicroseconds(1500); //as a double check that wheels are stopped
          FRwheel.writeMicroseconds(1500);
          RRwheel.writeMicroseconds(1500);
          return 0; //return from while loop
        }
         
         
        /*******************************************************************************************
        * Check Sonar sensor and IR sensors to see if threshold has been hit.
        * If it has, stop the wheels and return an error code.
        * Only use when robot is moving forward
        *******************************************************************************************/    
         
        if (robotdirection == 1){
        int sonar = readsonar(); 
        if (sonar<=SonarThreshold)
        {
          FLwheel.writeMicroseconds(1500); //stop the wheels
          RLwheel.writeMicroseconds(1500); //as a double check that wheels are stopped
          FRwheel.writeMicroseconds(1500);
          RRwheel.writeMicroseconds(1500);
          return 1; //return from while loop
        }
        
        int IRLeft = readLeftIR();
        if (IRLeft>=IRThreshold)
        {
          FLwheel.writeMicroseconds(1500); //stop the wheels
          RLwheel.writeMicroseconds(1500); //as a double check that wheels are stopped
          FRwheel.writeMicroseconds(1500);
          RRwheel.writeMicroseconds(1500);
          return 2; //return from while loop
        }
  
        int IRRight = readRightIR();   
        if (IRRight>=IRThreshold)
        {
          FLwheel.writeMicroseconds(1500); //stop the wheels
          RLwheel.writeMicroseconds(1500); //as a double check that wheels are stopped
          FRwheel.writeMicroseconds(1500);
          RRwheel.writeMicroseconds(1500);
          return 3; //return from while loop
        }  
        }
            
            
             
  }   
}






int WheelLoop(int wheelspeed, int setpoint, int encoder, int pgain)
{
    if(setpoint>0)
    {
        double perror = setpoint - encoder;
        wheelspeed = wheelspeed + ((double)pgain*perror);
        return wheelspeed;
    }
    
    else if(setpoint<0)
    {
        double perror = -setpoint - encoder;
        wheelspeed = wheelspeed - ((double)pgain*perror);
        return wheelspeed;
    }
}




int movearc(int robotdirection, int leftencoder, int rightencoder)
{

  int pgain = 3;
  int FLwheelspeed = 1500;
  int RLwheelspeed = 1500;
  int FRwheelspeed = 1500;
  int RRwheelspeed = 1500;
  float FLsetpoint;
  float RLsetpoint;
  float FRsetpoint;
  float RRsetpoint;
  boolean FLdone = false;
  boolean RLdone = false;
  boolean FRdone = false;
  boolean RRdone = false;
  
  
  
  switch(robotdirection){
    case(1):
      //Robot forward arc
      if (leftencoder > rightencoder)
      {
          FLsetpoint = -WheelSpeed;
          RLsetpoint = -WheelSpeed;
          FRsetpoint = WheelSpeed*(float(rightencoder)/float(leftencoder));
          RRsetpoint = WheelSpeed*(float(rightencoder)/float(leftencoder));
          
      }
      else
      {
          FLsetpoint = -WheelSpeed*(float(leftencoder)/float(rightencoder));
          RLsetpoint = -WheelSpeed*(float(leftencoder)/float(rightencoder));
          FRsetpoint = WheelSpeed;
          RRsetpoint = WheelSpeed;
      } 
      break;
    case(2):
      //Robot reverse arc
      if (leftencoder > rightencoder)
      {
          FLsetpoint = WheelSpeed;
          RLsetpoint = WheelSpeed;
          FRsetpoint = -WheelSpeed*(float(rightencoder)/float(leftencoder));
          RRsetpoint = -WheelSpeed*(float(rightencoder)/float(leftencoder));
      }
      else
      {
          FLsetpoint = WheelSpeed*(float(leftencoder)/float(rightencoder));
          RLsetpoint = WheelSpeed*(float(leftencoder)/float(rightencoder));
          FRsetpoint = -WheelSpeed;
          RRsetpoint = -WheelSpeed;
      }
      
      break;
    
   
  }
    
    
  //initialize all encoder counts to zero before
  //entering pid loop
  FLencodertotal = 0;
  RLencodertotal = 0;
  FRencodertotal = 0;
  RRencodertotal = 0;
  FLencoder = 0;
  RLencoder = 0;
  FRencoder = 0;
  RRencoder = 0;
  
  
  
  while(true){
    
        unsigned long currentMillis = millis();
        
        if(currentMillis - previousMilliswheels > 100) //use this to determine frequency of servo loop
        {
            // save the last time pid loop was called
            previousMilliswheels = currentMillis;
            
            /*******************************************************************************************
            * Control loop for wheels  
            *******************************************************************************************/

           FLwheelspeed = WheelLoop(FLwheelspeed, FLsetpoint, FLencoder, pgain);
           FLencoder = 0;
           
           RLwheelspeed = WheelLoop(RLwheelspeed, RLsetpoint, RLencoder, pgain);
           RLencoder = 0;
           
           FRwheelspeed = WheelLoop(FRwheelspeed, FRsetpoint, FRencoder, pgain);
           FRencoder = 0;
           
           RRwheelspeed = WheelLoop(RRwheelspeed, RRsetpoint, RRencoder, pgain);
           RRencoder = 0;
    
          //set new wheel speeds
          FLwheel.writeMicroseconds(FLwheelspeed);
          RLwheel.writeMicroseconds(RLwheelspeed);
          FRwheel.writeMicroseconds(FRwheelspeed);
          RRwheel.writeMicroseconds(RRwheelspeed);
          
        }
        
        /*******************************************************************************************
        * Check to see if encoder setpoints have been reached
        * If they have, stop the wheels and return
        *******************************************************************************************/
        if(FLencodertotal>=leftencoder) //if encoder target has been reached
        {
          FLsetpoint = 0; //put setpoint to zero
          FLwheel.writeMicroseconds(1500); //stop the wheels
          FLdone = true;
        }
        if(RLencodertotal>=leftencoder) //if encoder target has been reached
        {
          RLsetpoint = 0; //put setpoint to zero
          RLwheel.writeMicroseconds(1500); //stop the wheels
          RLdone = true;
        }
        if(FRencodertotal>=rightencoder) //if encoder target has been reached
        {
          FRsetpoint = 0; //put setpoint to zero
          FRwheel.writeMicroseconds(1500); //stop the wheels
          FRdone = true;
        }
        if(RRencodertotal>=rightencoder) //if encoder target has been reached
        {
          RRsetpoint = 0; //put setpoint to zero
          RRwheel.writeMicroseconds(1500); //stop the wheels
          RRdone = true;
        }
        
        
        if(FLdone && RLdone && FRdone && RRdone) //if all wheels have reached their target
        {
          FLwheel.writeMicroseconds(1500); //stop the wheels
          RLwheel.writeMicroseconds(1500); //as a double check that wheels are stopped
          FRwheel.writeMicroseconds(1500);
          RRwheel.writeMicroseconds(1500);
          return 0; //return from while loop
        }
         
         
        /*******************************************************************************************
        * Check Sonar sensor and IR sensors to see if threshold has been hit.
        * If it has, stop the wheels and return an error code.
        * Only use when robot is moving forward
        *******************************************************************************************/    
         
        if (robotdirection == 1){
        int sonar = readsonar(); 
        if (sonar<=SonarThreshold)
        {
          FLwheel.writeMicroseconds(1500); //stop the wheels
          RLwheel.writeMicroseconds(1500); //as a double check that wheels are stopped
          FRwheel.writeMicroseconds(1500);
          RRwheel.writeMicroseconds(1500);
          return 1; //return from while loop
        }
        
        int IRLeft = readLeftIR();
        if (IRLeft>=IRThreshold)
        {
          FLwheel.writeMicroseconds(1500); //stop the wheels
          RLwheel.writeMicroseconds(1500); //as a double check that wheels are stopped
          FRwheel.writeMicroseconds(1500);
          RRwheel.writeMicroseconds(1500);
          return 2; //return from while loop
        }
  
        int IRRight = readRightIR();   
        if (IRRight>=IRThreshold)
        {
          FLwheel.writeMicroseconds(1500); //stop the wheels
          RLwheel.writeMicroseconds(1500); //as a double check that wheels are stopped
          FRwheel.writeMicroseconds(1500);
          RRwheel.writeMicroseconds(1500);
          return 3; //return from while loop
        }  
        }
            
            
             
  }   
}




int moveheading(int compass)
{

  int pgain = 3;
  int FLwheelspeed = 1500;
  int RLwheelspeed = 1500;
  int FRwheelspeed = 1500;
  int RRwheelspeed = 1500;
  int FLsetpoint;
  int RLsetpoint;
  int FRsetpoint;
  int RRsetpoint;
  
  int compassfirst = readcompass(); 
  int difference = compass - compassfirst;
  
  if (difference > 0)
  {
    //Turn right on the spot
      FLsetpoint = -WheelSpeed;
      RLsetpoint = -WheelSpeed;
      FRsetpoint = -WheelSpeed;
      RRsetpoint = -WheelSpeed;
  }
  else
  {
    //Turn left on the spot
      FLsetpoint = WheelSpeed;
      RLsetpoint = WheelSpeed;
      FRsetpoint = WheelSpeed;
      RRsetpoint = WheelSpeed;
  }
    
    
  //initialize all encoder counts to zero before
  //entering pid loop
  FLencodertotal = 0;
  RLencodertotal = 0;
  FRencodertotal = 0;
  RRencodertotal = 0;
  FLencoder = 0;
  RLencoder = 0;
  FRencoder = 0;
  RRencoder = 0;
  
  
  
  while(true){
    
        unsigned long currentMillis = millis();
        
        if(currentMillis - previousMilliswheels > 100) //use this to determine frequency of servo loop
        {
            // save the last time pid loop was called
            previousMilliswheels = currentMillis;
            
            /*******************************************************************************************
            * Control loop for wheels  
            *******************************************************************************************/

           FLwheelspeed = WheelLoop(FLwheelspeed, FLsetpoint, FLencoder, pgain);
           FLencoder = 0;
           
           RLwheelspeed = WheelLoop(RLwheelspeed, RLsetpoint, RLencoder, pgain);
           RLencoder = 0;
           
           FRwheelspeed = WheelLoop(FRwheelspeed, FRsetpoint, FRencoder, pgain);
           FRencoder = 0;
           
           RRwheelspeed = WheelLoop(RRwheelspeed, RRsetpoint, RRencoder, pgain);
           RRencoder = 0;
    
          //set new wheel speeds
          FLwheel.writeMicroseconds(FLwheelspeed);
          RLwheel.writeMicroseconds(RLwheelspeed);
          FRwheel.writeMicroseconds(FRwheelspeed);
          RRwheel.writeMicroseconds(RRwheelspeed);
        
        
        }
        /*******************************************************************************************
        * Check to see if compass heading setpoint has been reached
        * If it has, stop the wheels and return
        *******************************************************************************************/
        
        int compasscurrent = readcompass();

        if(compasscurrent >= (compass-2) && compasscurrent <= (compass+2)) //if compass target has been reached
        {
          FLwheel.writeMicroseconds(1500); //stop the wheels
          RLwheel.writeMicroseconds(1500); //as a double check that wheels are stopped
          FRwheel.writeMicroseconds(1500);
          RRwheel.writeMicroseconds(1500);
          return 0; //return from while loop
        }
        delay(20);
        
             
  }   
}










void MoveHead(int HeadPanTarget, int HeadTiltTarget)
{
  
  HeadPanTarget = map(HeadPanTarget, 90 ,-90 ,PANCENTRE-900 ,PANCENTRE + 900);  
  HeadTiltTarget = map(HeadTiltTarget, 90 ,-90 ,TILTCENTRE-900, TILTCENTRE + 900);
  
  
  while(true){
    
        unsigned long currentMillis = millis();
        
        if(currentMillis - previousMillishead > (10-HeadSpeed)) //use this to determine frequency of servo loop
        {
            // save the last time pid loop was called
            previousMillishead = currentMillis;
            
            if(HeadPanTarget > HeadPanpos)
            { 
              HeadPanpos = HeadPanpos + 3;
              HeadPan.writeMicroseconds(HeadPanpos);
            }
            else if(HeadPanTarget < HeadPanpos)
            {
              HeadPanpos = HeadPanpos - 3;
              HeadPan.writeMicroseconds(HeadPanpos);
            }
                
                
            
            if(HeadTiltTarget > HeadTiltpos)
            { 
              HeadTiltpos = HeadTiltpos + 3;
              HeadTilt.writeMicroseconds(HeadTiltpos);
            }
            else if(HeadTiltTarget < HeadTiltpos)
            {
              HeadTiltpos = HeadTiltpos - 3;
              HeadTilt.writeMicroseconds(HeadTiltpos);
            }     
               
                 
        }
        int differencepan = HeadPanTarget - HeadPanpos; 
        int differencetilt = HeadTiltTarget - HeadTiltpos;
        
        if(abs(differencepan) < 3 && abs(differencetilt) < 3) //if both servo positions have been reached
        {
          break; //exit loop and return
        }
  }
}

int readsonar()
{
  //read head sonar sensor
  pinMode(38, OUTPUT);
  digitalWrite(38, LOW);             // Make sure pin is low before sending a short high to trigger ranging
  delayMicroseconds(2);
  digitalWrite(38, HIGH);            // Send a short 10 microsecond high burst on pin to start ranging
  delayMicroseconds(10);
  digitalWrite(38, LOW);             // Send pin low again before waiting for pulse back in
  pinMode(38, INPUT);
  int duration = pulseIn(38, HIGH);  // Reads echo pulse in from SRF05 in micro seconds
  int sonar = (duration/58);         // Dividing this by 58 gives us a distance in cm
  delay(10);
  return sonar;
}

int readLeftIR()
{
  int LeftIR = analogRead(2);
  return LeftIR;
}

int readRightIR()
{
  int RightIR = analogRead(3);
  return RightIR;
}  
  
  
int readcompass()
{
  byte highByte;
  byte lowByte;
 
  Wire.beginTransmission(compassaddress);      //starts communication with cmps03
  Wire.write(2);                         //Sends the register we wish to read
  Wire.endTransmission();

  Wire.requestFrom(compassaddress, 2);        //requests high byte
  while(Wire.available() < 2);         //while there is a byte to receive
  highByte = Wire.read();           //reads the byte as an integer
  lowByte = Wire.read();
  int bearing = ((highByte*255)+lowByte)/10; 
 
   
  return bearing;
}
