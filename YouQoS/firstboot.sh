#!/bin/bash
pip install --upgrade Flask
update-rc.d youqos_init.sh defaults
/etc/init.d/youqos_init.sh &
#echo "" >> /etc/network/interfaces
#echo "auto eth1" >> /etc/network/interfaces
#echo "iface eth1 inet dhcp" >> /etc/network/interfaces
#echo "" >> /etc/network/interfaces
#echo "auto eth2" >> /etc/network/interfaces
#echo "iface eth2 inet dhcp" >> /etc/network/interfaces
#crontab -l | { cat; echo "@reboot python /home/selfnet/YouQoS.py &"; } | crontab -
#sleep 60
#reboot
