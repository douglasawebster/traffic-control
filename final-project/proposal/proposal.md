# Final Project Proposal: Traffic Control

For my final project I am proposing to build an IoT network for traffic control.  As cities become more dense the number of cars on the street increases leading to congestion at traffic lights.  While many of the traffic lights in our cities are able to adapt to changes in demand (i.e. the number of cars currently at a light) they can only adjust to cars which are already at the light.  Thus, they fail to foresee changes in demand that will occur a short period of time into future.  I would like to build a system that gathers current traffic information and then uses the information to make global traffic flow decisions.

At a high level this project asks two questions.  First, how do we collect the information needed to make global traffic flow decisions?  Second, once the information is gathered how do traffic signals make global traffic flow decisions?  In order to answer these questions we begin by stating the goals.  

**Goal:** Optimize current global traffic flow 

**Goal:** Optimize future global traffic flow

**Goal:** Do not over optimize current traffic flow at the expense of future traffic flow and vice versa.  

To understand what these goals mean I will define current, future, global, and optimum traffic flow.  Current refers to the immediate time frame and lasts for ten seconds, thus it refers to the current state of traffic within about five-hundred feet.  Future is defined as the time frame between ten seconds to two minutes after the current time frame which is between five-hundred feet and a mile.  Next, global refers to a currently undefined radius emanating from a traffic control light.  Lastly, optimum traffic flow is also currently undefined but will be some function of motor vehicle speed, density, and wait time.

Now that the goals have been clearly defined we can begin to answer the previously proposed questions.  With regard to collecting adequate information the system would rely on sensors placed on street lights.  The use of street lights is crucial for this system because they provide the electricity needed to run the sensors during the day and night, removing the need for additional power lines to be laid.  The capabilities of the sensors placed on the street lights must include: speed, number of vehicles, the lane the vehicle is currently in, and the type of vehicle.  

The speed of vehicles is important because it gives us a measure for current traffic flow as well as an estimation of how long it will take for a car to travel to a particular traffic signal.  The number of vehicles is also important because the current flow of traffic is not solely explainable by speed.  For example, on some roads there may be five cars traveling at thirty miles per hour, but at some later point there maybe one-hundred cars on that road traveling at thirty miles per hour.  These situations need to be handled differently if we are to optimize traffic flow.  Additionally, knowing the lane of the vehicle can be used to determine if the driver is going to go straight at a traffic signal or making a turn.  Therefore, we can determine how many drivers are on the road and how many will soon leave a road and join another.  Lastly, the sensors must be able to detect different types of vehicles.  Detecting the type of vehicle is crucial for optimizing turn lanes.  Semi-trucks make turns very slowly so it may be necessary to keep the light on longer to allow a sufficient number of vehicles to turn. 

Data that is collected by the sensors will be transmitted to a central server that is responsible for making the decisions.  The most difficult part of this system is settling on an optimization criteria.  Currently, the optimization criteria includes the average speed in a local and global area, density in local and global area, waiting time at a traffic signal, and a maximum flow threshold.  Each of these factors will be feed into a function which scales the weights of each of the criteria in hopes of returning traffic signal decisions that maximize the average speed of all vehicles in a global area.

In order to send data from the sensor to the server and then from the server to traffic signals the MQTT message protocol will be used.  Its compact message format will allow relatively low powered sensors to send many messages at a high rate.  

At this point the general types of data the sensors will collect has been defined as well as how the data will be optimized and relayed as decisions to traffic signals.  Now it is important to detail more precisely the data that will be collected and transmitted to the server and then the decisions sent to the traffic signals.  The following examples will outline how data is collected and transmitted using the MQTT message protocol.  

Collecting data from sensors
Speed data:  The speed that a sensor transmits to the sever will be the average speed of the vehicles it can measure over two seconds.  Thus, eliminating the possibility of choosing a vehicle that is traveling much higher or lower than other vehicles.  The speed measurements will be taken every few seconds as to provide real time speed data to the server.

`publish: united-states/california/san-diego/la-jolla/SENSOR-NUMBER/speed AVERAGE-SPEED`

Number of vehicles data:  The number of vehicles that a sensor transmits to the sever will be the number of vehicles that pass by over two seconds.  This measurement will be taken every few seconds.

`publish: united-states/california/san-diego/la-jolla/SENSOR-NUMBER/num-vehicles NUM-VEHICLES`

Number of vehicles in lanes:  The number of vehicles that a sensor transmits to the sever will be the number of vehicles that pass by over two seconds in the respective lanes.

`publish: united-states/california/san-diego/la-jolla/SENSOR-NUMBER/lane-X NUM-VEHICLES-LANE-X`

Types of vehicles: The vehicle types that a sensor transmits to the server will be broadly categorized.  Such categories will include: passenger vehicle, truck, emergency vehicle, and Semi-trucks.

`publish: united-states/california/san-diego/la-jolla/SENSOR-NUMBER/VEHICLE-TYPE NUM-VEHICLES`

Sending data to traffic signals
`publish: united-states/california/san-diego/la-jolla/INTERSECTION/TRAFFIC-SIGNAL/value VALUE-TIME`

Most of the proposed system will be theoretical.  However, some things that can be implemented include: using Flespi and MQTT to send sensor data to the server and traffic signals, a node-red flow to handle message topics, and a dashboard that displays various metrics (metrics to be decided later).

As far as issues for this project it will be difficult to scope this project appropriately.  This project can get complicated quickly and require more work than can be done in the remaining few weeks of class. 

Success for this project would be a clear description of the IoT system, a node-red flow utilizing Flespi and MQTT messages, and a dashboard that displays the data in the messages.

Here is a short video I found online that captures a few of the ideas I am trying to incorporate in my final project.
[Traffic Control System](https://www.youtube.com/watch?v=YJukLN-gLy4)