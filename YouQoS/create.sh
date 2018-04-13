#!/bin/bash
#build script for SELFNET YouQoS-sensor
#Ulbricht@InnoRoute.de 2017
distri="trusty"
objectname="YouQoS"
BASEDIR=$(dirname "$(readlink -f "$0")")
#sudo apt-get install qemu-kvm 
#sudo adduser $USER kvm
cd "$BASEDIR" ##change dir
echo "change to $BASEDIR"
echo "Try to delete old YouQoS versions"
sudo virsh destroy $objectname
sudo virsh undefine $objectname
echo "Downloading and building Image...grap a coffe..."
sudo ubuntu-vm-builder kvm $distri \
									-o \
									--templates $BASEDIR/vmtemplates/ \
									--flavour virtual \
                  --domain $objectname \
                  --dest $objectname \
                  --arch i386 \
                  --hostname $objectname \
                  --mem 2048 \
									--firstboot=$BASEDIR/firstboot.sh \
		 						  --rootsize 1024 \
                  --user selfnet \
                  --pass selfnet \
                  --components main,universe \
                  --addpkg=acpid \
									--addpkg=sqlite3 \
									--addpkg=python-pip \
                  --addpkg=nano \
                  --addpkg=curl \
									--addpkg=python \
                  --addpkg=cron \
									--addpkg=python-requests \
									--addpkg=python-flask \
                  --addpkg=openssh-server \
                  --addpkg=avahi-daemon \
									-c vmbuilder.cfg \
                  --libvirt qemu:///system ;
#									--install-mirror=http://192.168.1.117:3142/de.archive.ubuntu.com/ubuntu \
virsh  attach-interface --domain $objectname --type network --source SELFNETmmnt --model virtio --config --persistent
virsh  attach-interface --domain $objectname --type network --source net5 --model virtio --config --persistent

#                  --ip 192.168.122.66 \
#                  --mask 255.255.255.0 \
#                  --net 192.168.122.0 \
#                  --bcast 192.168.122.255 \
#                  --gw 192.168.122.1 \
#                  --dns 192.168.122.1 \
