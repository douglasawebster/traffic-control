# Final Project Draft: Traffic Control

### Defining The Problem
According to the [National Association of City Transportation Officials](https://nacto.org/publication/urban-street-design-guide/intersection-design-elements/traffic-signals/signal-cycle-lengths/), the perfect amount of time for a light to remain red it between 60 and 90 seconds.  Taking into account that approximately twenty percent of all driving time is spent at red lights, that can certainly add up.  Furthermore, according to [AAA](http://newsroom.aaa.com/2016/09/americans-spend-average-17600-minutes-driving-year/), the average American spends 17,600 minutes driving each year.  Thus, 3,520 minutes, or 58.6 hours, are spent waiting at red lights each year.

Not only is waiting at red lights frustrating, it is also harmful to the environment and to our health.  Being stopped at a red light increases travel time.  This increase in travel time results in an increase in emitted pollution.  Also, while at a red light many drivers are surrounded by idling engines creating pollution hot-spots.  A study conducted in the United Kingdom monitored drivers' exposure to air pollutants at various points of a journey.  It was found that traffic intersections produced pollution hot-spots.  With drivers decelerating and stopping at lights, idling for a period of time, and then revving up to move quickly when lights turn green, peak particle concentration was found to be twenty-nine times higher than that during free-flowing traffic conditions.    

As cities continue to become more dense and the number of cars on the street increases, traffic congestion and traffic light waiting times will only become more problematic.  While many of the traffic lights in our cities are able to adapt to changes in demand (i.e. the number of cars currently at a light) they can only adjust to cars which are already at the light.  Thus, they fail to foresee changes in demand that will occur a short period of time into future.  In order to combat these problems I am building a system that gathers current traffic information and then uses the information to make global traffic flow decisions.  Thus, my final project will focus on building an IoT network for traffic control.

At a high level this project asks two questions.  First, how do we collect the information needed to make global traffic flow decisions?  Second, once the information is gathered how do traffic signals make global traffic flow decisions?  

In order to answer these questions I begin by stating the goals and reviewing the terminology that will be used throughout the report.  The next section focuses on data collection which includes geographic scale, sensor types and quantities, data transport, data rates, and data storage.  After a thorough discussion on data collection the following section will detail how this information will be used to make global traffic flow decisions.  Once this has been done I will discuss the architecture linking the data collection system and decision making system together.  Lastly, I will review an elementary prototype of this system using various live traffic API's, the MQTT message protocol, traffic optimization algorithms, and data visualizations for human monitoring. 

### Goals
- Optimize current global traffic flow 
- Optimize future global traffic flow
- Do not over optimize current traffic flow at the expense of future traffic flow and vice versa

### Terminology
- **Streetlight:** A light on the side of the road used to illuminate the road surface 
- **Traffic light:** A light at an intersection directing traffic
- **Current:** The immediate time frame and lasts for ten seconds, thus it refers to the current state of traffic within about five-hundred feet
- **Future:** The time frame between ten seconds to two minutes after the current time frame which is between five-hundred feet and one mile
- **Global:** A ___ radius emanating from a traffic control light
- **Optimum traffic flow:** A function of motor vehicle speed, density, and wait time

### Geographic Scale
Traffic control is a broadly scoped project.  To consolidate the implementation of the project I will be focusing on traffic control in La Jolla, California.  The map included below showcases the high-level road structure of La Jolla.  This cross-section covers about three miles horizontally and two miles vertically.  Additionally, special attention will be focused on La Jolla Parkway, Torrey Pines Road, La Jolla Boulevard, Pearl Street, and Nautilus Street.  These roads handle much of the traffic in La Jolla and are known to get congested during rush hour, school drop-off/pickup, and the summer months.

![Alt text](img/la-jolla-street-map.png)

This geographical working space will be filled with sensors to monitor road activity.  The sensors for the traffic control system will be placed at streetlights and traffic lights.  The use of streetlights and traffic lights for sensors is crucial for this system because both of them provide the necessary electricity needed to run the sensors during the day an night, removing the need for additional power lines to be laid.  

Using a database provided by the City of San Diego I was able to find all of the streetlights in La Jolla. The data was stored via csv with the following format `ID, Model, Type, Wattage, Voltage, Longitude, Latitude, Description`.  To determine if the streetlight was in La Jolla it was necessary to do some prescreening because there were over 60,000 entries.  I first pruned the data by picking a rough boarder around La Jolla.  These coordinates were `max_latitude_north = 32.889147`, `min_latitude_south = 32.802140`, `max_longitude_west = -117.289555`, and `min_longitude_east = -117.235660`.  Then I checked to see if the streetlight was within these coordinates.  If it was outside of the range the entry was ignored because it was outside of La Jolla.  However, if the coordinates were within the rough boundary, closer inspection was needed.  To definitively determine if the streetlight was in La Jolla I made use of a python library to query the coordinates.  The returned result from the query contain a postal code field which I used to determine if the streetlight was in La Jolla.  For each streetlight in La Jolla I added it to a JSON with the key field being the streetlights identification number and values being filled with the rest of the data from the csv. The files pertaining to the streetlight locations can be found in the following directory `final-project/data/streetlight-data/`.  Within this directory the following files are present:

`streetlight-locations.csv`: contains the raw csv data with information for every streetlight in San Diego (provided by City of San Diego website)

`streetlight-dictionary.csv`: contains explanations of each of the abbreviations used in streetlight-locations.csv (provided by City of San Diego website)

`streetlight-parser.py`: script to parse through csv data, returns JSON of all streetlights in La Jolla with appropriate key value pairs

`streetlight-mapping.py`: script to read through JSON and extract coordinates of each streetlight (this information was used for the map below)

`streetlight-json.json`: JSON database of all streetlights in La Jolla.  The key is the unique streetlight identification number and the value is the associated data with the streetlight

`geopy-query-raw-data-example.json`: an example result from querying geopy library

Using an online [mapping software](http://www.copypastemap.com/) I was able to plot all of the coordinates of the streetlights in La Jolla.

![Alt Text](img/la-jolla-streetlights.png)

From the data provided by the City of San Diego there are about 1000 streetlights in La Jolla which can be used to mount and power the various sensors.  There are two reasons for using streetlights as docking points instead of placing them in the road.  First, in-road sensors have high installation, maintenance, and repair costs.  Second, streetlight sensors are much easier to fix or update because they do not require road construction. 

The capabilities of the sensors placed on the streetlights must include: speed detection, vehicle density, lane detection, and vehicle classification.  There are many sensors that can be used to accomplish these goals.  Thus, to come to a conclusion on the best sensors to use it is important to review each of the sensors capabilities and its advantages/disadvantages.  The sensors that will be reviewed in this report include: video cameras, radar sensors, infrared sensors, ultrasonic sensors, and acoustic array sensors. 

Video cameras can be placed along the road to collect and analyze video to determine traffic flow and vehicle occupancy.  However, using video cameras requires heavy image processing and sophisticated algorithm-based software for interpreting the images and translating them into traffic data.  This is likely to be resource intensive and impractical for high data rates because images possess large amounts of data.  Additionally, video cameras are highly susceptible to bad weather conditions.   

Radar sensors transmit low-energy microwave radiation that is reflected by all objects within the detection zone.  There are different types of radar sensor system.  The Doppler systems use the frequency shift of the return signal to track the number of vehicles, and determine speed very accurately.  Another systems uses frequency-modulated continuous wave radar which radiates continuous transmission power and is used to measure flow volume, speed, and presence.  The advantage to using radar sensors is that they are easy to install, support multiple detection zones, and can operate during the day or night.  Their main disadvantage is that they are susceptible to electromagnetic interference.

Infrared sensors detect the energy generated by vehicles, road surfaces, or other objects.  These sensors convert the reflected energy into electrical signals that are sent to the processing unit.  Infrared sensors are divided into two categories, passive infrared and active infrared.  Passive infrared detects vehicles based on emission or reflection of infrared radiation and are used to collect data on flow volume, vehicle presence, and vehicle occupancy.  Active infrared sensors use light emitting diodes or laser diodes to measure the reflection time and collect data on flow volume, speed, vehicle classification, vehicle presence, and traffic density.  

Ultrasonic sensors calculate the distance between two objects based on the elapsed time between a sound waves initial transmission and the sensors receiving of the transmission after being reflected by an object.  These sensors are used to collect data about vehicle flow and vehicle speed.  The main disadvantage to ultrasonic sensor is its high sensitivity to environmental effects.

Acoustic array sensors are formed by a set of microphones that are used to detect an increase in sound energy produced by an approaching vehicle.  These sensors are used to calculate traffic volume, vehicle occupancy, and average speed of vehicles.

Given this information I have chosen to use radar and infrared sensors.  Together these sensor are capable of meeting all of the required capabilities, speed detection, vehicle density, lane detection, and vehicle classification.  The radar sensors will be used for tracking vehicle speed and determining the number of vehicles in each lane.  The appeal of radar sensors is the ability to easily install these sensors along with support for multiple detection zones and the ability operate at day or night.  To fulfill the remaining data collection requirements active infrared sensors will be used because they can measure flow volume and classify vehicles.         


<img src="img/vehicle-speed.png" width="425"/> <img src="img/vehicle-lane.png" width="425"/> 

<img src="img/vehicle-density.png" width="425"/> <img src="img/vehicle-classification.png" width="425"/>

 








https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5948625/


