#!/bin/sh

if [ ! -e "/tmp/etc/ethers" ]; then
	if [ -L "/etc/ethers" ]; then
		touch /tmp/etc/ethers
	else
		mv /etc/ethers /tmp/etc/ethers
	fi
	ln -s /tmp/etc/ethers /etc/ethers
fi

if [ ! -e "/tmp/etc/hosts" ]; then
	if [ -L "/etc/hosts" ]; then
		touch /tmp/etc/hosts
	else
		mv /etc/hosts /tmp/etc/hosts
	fi
	ln -s /tmp/etc/hosts /etc/hosts
fi

# Any custom hosts need to be added here
cat > /etc/hosts <<- EOM
# NOTE: THIS HOSTS FILE WILL BE OVERWRITTEN BY $(readlink -f $0)
127.0.0.1 localhost

::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters

# Automatically added adresses will be added below:
EOM

LANST=$(ifstatus lan)
LANADDR=`echo "$LANST" |  jsonfilter -e '@["ipv4-address"][0].address'`
INTERFACE=`echo "$LANST" |  jsonfilter -e '@.device'`
LANNET=`ip r | grep "link\s\+src $LANIP" | awk -F ' ' '{print $1}'`
DNSSERVER=`echo "$LANST" |  jsonfilter -e '@["dns-server"][0]'`

arp-scan -q -x -I $INTERFACE $LANNET | awk -F' ' '{print $2 " " $1}' > /etc/ethers

for IPADDR in `cat /etc/ethers | awk -F' ' '{print $2}'`; do

	FQDN=`nslookup $IPADDR $DNSSERVER | grep -m 1 arpa | awk -F' ' '{print $4}'`
	if [ $FQDN != "find" ]; then
		echo "$IPADDR	$FQDN" >> /etc/hosts
	fi

done

