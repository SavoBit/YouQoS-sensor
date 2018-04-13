# SELFNET YouQoS sensor
This component offers an interface for the enduser to tell the network about thair flow priority expectations.
For further information see: 
* https://www.youtube.com/watch?v=E_TUhxJxwCU
* https://bscw.selfnet-5g.eu/pub/bscw.cgi/d74996/D3.4-Report%20and%20Prototype%20Implementation%20of%20the%20NFV%20%26%20SDN%20Sensors%20and%20Actuators%20related%20to%20the%20Self-Optimizing%20Use%20Case.pdf
* https://ieeexplore.ieee.org/document/7109502/

## Install and usage:
The sensors core functionality is provided by the script YouQoS/scripts/YouQoS.py which can also used standalone
To generate a SELFNET-kvm image run YouQoS/create.sh
To onboard the created image into SELFNET use the description files proveded in YouQoS/jsondata/
