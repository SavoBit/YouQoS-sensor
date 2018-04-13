#!/bin/bash
# VM package script, creates SELFNET ready tar including all configuration files
#you have to create the cam befor.. see creat.sh in kvm-folder
#M.Ulbricht InnoRoute.de 2017
VMname="YouQoS"
mkdir package_tmp
virsh dumpxml $VMname > package_tmp/$VMname.xml
image=$(cat package_tmp/$VMname.xml |grep "<source file="| cut -d \' -f2)
cp $image package_tmp
cp -R jsondata/* package_tmp
cd package_tmp 
tar -I pbzip2 -cf $VMname.tar.bz2 $image $VMname.xml
tar cf $VMname.tar metadata.json app-descriptor configuration monitoring $VMname.tar.bz2
cd ..
mv package_tmp/$VMname.tar .
rm package_tmp -R
