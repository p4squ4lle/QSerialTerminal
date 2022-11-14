// defines pins numbers
int stepPinX = 2; 
int dirPinX = 5;
int stepPinY= 3; 
int dirPinY = 6;
int stepPinZ = 4; 
int dirPinZ = 7;

int currentFrequency; // frequency in Hz (max value 1600 Hz for half step mode)
int stepDelay;   // delay for stepper pulse duration
          
long stepsToGo;           // steps to do

int numAccelSteps = 10;

const byte numChars = 64;
char receivedChars[numChars]; // an array to store the received data
char tempChars[numChars];
boolean newData = false;
boolean moveInProgress = false;

char command[2] = {0};   // 1st incoming serial byte
char axis[2] = {0};      // 2nd incomming byte
long steps = 0;

void setup() {
  // Sets the three pins as Outputs
  pinMode(stepPinX,OUTPUT); 
  pinMode(dirPinX,OUTPUT);
  pinMode(stepPinY,OUTPUT); 
  pinMode(dirPinY,OUTPUT);
  pinMode(stepPinZ,OUTPUT); 
  pinMode(dirPinZ,OUTPUT);

  currentFrequency = 250;
  stepDelay = 500000/currentFrequency;
  
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  Serial.println("serial connection successful"); 
}

void loop() {
  recvCommand();
  if (newData == true) {
    strcpy(tempChars, receivedChars);
    parseCommand();
    exeCommand();    
    newData = false;
  }
  
}

void recvCommand() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '#';
    char endMarker = '\n';
    char rc;
 
    while (Serial.available() > 0 && newData == false) {
      rc = Serial.read();

      if (recvInProgress == true) {
        if (rc != endMarker) {
          receivedChars[ndx] = rc;
          ndx++;
          if (ndx >= numChars) {
            ndx = numChars - 1;
          }
        }
        else {
          receivedChars[ndx] = '\0';
          recvInProgress = false;
          ndx = 0;
          newData = true;
        }       
      }
      
      else if (rc == startMarker) {
        recvInProgress = true;
      } 
    }
}

void parseCommand() {
   char * strtokIndx;
  
   strtokIndx = strtok(tempChars, ",");
   strcpy(command, strtokIndx);

   strtokIndx = strtok(NULL, ",");
   strcpy(axis, strtokIndx);

   strtokIndx = strtok(NULL, ",");
   steps = atol(strtokIndx);
  
}

void exeCommand() {
  Serial.print("Command: ");
  Serial.println(command);
  Serial.print("Axis: ");
  Serial.println(axis);
  Serial.print("Number of steps: ");
  Serial.println(steps);

  if (command[0]=='C') {
    moveInProgress = true;
    while (moveInProgress) {
      contMovement();
      delay(1000);
    } 
    
  }
  else if (command[0]=='A') {
    Serial.println("normal movement");
    switch (axis[0]) {
      case 'X':
        Serial.println("x axis");
        break;
      case 'Y':
        Serial.println("y axis");
        break;
      case 'Z':
        Serial.println("z axis");
    }
  }
  else if (command[0]=='X') {
    moveInProgress = false;
    Serial.println("emergency stop");
  }
}

void contMovement() {
  Serial.println("continous movement");
  recvCommand();
  if (newData == true) {
    strcpy(tempChars, receivedChars);
    parseCommand();
    if (command[0]=='X') {
      moveInProgress = false;
      Serial.println("emergency stop");
    }
    newData = false;
  }
}
