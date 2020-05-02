# Feedback for 


## Problem Statement

The high level goal is fairly clear -- to use sensor data to make decisions about how to control traffic lights.   What is less clear is the geographical scale the data would cover and the granularity of the data (at the car, block level ?  how frequent are the updates ? )

I think you might want to focus on a smaller, well defined  geographical area to answer some of the scale questions.  For example, Claremont -- how many cars, lights, etc.  What information would be needed.

Would you need data from other sources -- for example fire trucks or ambulances  ?   What about cyclists and pedestrians ?

## Sensors


### Type

Try to identify the type of sensors (not down to specific parts) and the type of data they will produce.
What communication mechanisms are needed ?

### Number and Data Rate

Estimate for a reasonable scale the number of sensors and their data rates (at various times of the day).  Data rate might play an important role in deciding communciation requirements.

## Data Storage

What data would be stored over what time periods ?  How much and at what rate ?

## Visualization

For a traffic control system what kind a data visualization would be useful both for instantaneous state and for making planning decisions (like where to put bike paths or change road configurations.)

## Other Issues

* Security
* Privacy
* Network requirements
* Providing power for the system