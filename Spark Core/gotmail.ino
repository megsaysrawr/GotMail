//// VARIABLE DEFINITIONS ////
int led = D7;   // This one is the built-in tiny one to the right of the USB jack
int sensors[] = {A0, A1, A2, A3, A4}; // List of sensor pins {Sensor1, Sensor2, Sensor3, ... }
int sens_to_check;  // Number of sensor that will be checked (1, 2, 3, ...)
int sensor_val;     // The analog input read from the sensor.

void setup()
{
    pinMode(led, OUTPUT);   // The blinky light is an output pin
    //// SENSOR ALLOCATION ////
    pinMode(A0, INPUT);     // The sensor is an input pin
    // ...
    //// SPARK API EXPOSURE ////
    Spark.function("analogRead", analogread); // Make our analogread() function (defined below) callable through Spark API
}

void loop()
{
    digitalWrite(led, Time.second()%2); // A blinky light to show that the program is running.
}

int analogread(String sensornum)
{
    sens_to_check = int(sensornum.charAt(0))-49;    // Turn '1' into 0, '2' into 1, '3' into 2, etc. 
    sensor_val = analogRead(sensors[sens_to_check]);// Read the desired sensor.
    return sensor_val;
}
