#!/bin/bash -x
echo "$MASTERIP master" >> /etc/hosts
echo "$SLAVE1IP slave1" >> /etc/hosts
echo "$SLAVE2IP slave2" >> /etc/hosts

yum -y -q install nfs-utils nfs-utils-lib 
#java-1.8.0-openjdk java-1.8.0-openjdk-devel
mkfs.ext4 /dev/vdb
mkdir $DIRECTORYNAME
echo "/dev/vdb $DIRECTORYNAME ext4 user,rw,auto 0 0" >> /etc/fstab
mount /dev/vdb
chkconfig rpcbind on
chkconfig nfs on
echo "$DIRECTORYNAME $CIDRADDRESS(rw,sync,crossmnt,no_root_squash,no_subtree_check)" >> /etc/exports
exportfs -a
rpcbind
chmod 777 $DIRECTORYNAME
service nfs start

# PYTHON 2.7
yum install numpy.x86_64
wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm
rpm -Uhv epel-release-latest-6.noarch.rpm
wget https://centos6.iuscommunity.org/ius-release.rpm
rpm -Uhv ius-release.rpm

yum -y install python27 python27-devel python27-pip python27-setuptools python27-virtualenv --enablerepo=ius

# CONDOR INSTALLATION

wget http://research.cs.wisc.edu/htcondor/yum/repo.d/htcondor-stable-rhel6.repo
cp htcondor-stable-rhel6.repo /etc/yum.repos.d/
wget http://htcondor.org/yum/RPM-GPG-KEY-HTCondor
rpm --import RPM-GPG-KEY-HTCondor
yum -y -q install condor-all
CONFIGURATION_FILE=/etc/condor/condor_config 
CONFIGURATION_FILE_LOCAL=/etc/condor/condor_config.local
echo "CONDOR_HOST = $MASTERIP" >> $CONFIGURATION_FILE 
echo "CONDOR_HOST = $MASTERIP" >> $CONFIGURATION_FILE_LOCAL
echo "HOSTALLOW_READ = *" >> $CONFIGURATION_FILE 
echo "HOSTALLOW_WRITE = *" >> $CONFIGURATION_FILE 
echo "#HOSTDENY_WRITE = *" >> $CONFIGURATION_FILE 
echo "HOSTALLOW_ADMINISTRATOR = *" >> $CONFIGURATION_FILE 
echo "#HOSTALLOW_OWNER = *" >> $CONFIGURATION_FILE
/etc/init.d/condor start 