# Overview

This directory provides a template for a node-red "project".  By default, node-red has poor support 
for separate projects.  Thus, you will use a separate data directory for each Lab experiment

To use this template, copy the entire directory to a new directory -- at the same level.  
For example, from within this template

```
cd ..
cp -r node-red-template lab-n
```

You may then execute node red from within that directory 

```
cd lab-n
./start-node-red
```

This will create an instance of node-red running on the localhost ip address (127.0.0.1).  Any flows
that you create will be saved within lab-n
