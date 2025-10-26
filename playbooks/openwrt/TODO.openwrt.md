# TODO Items

- Turn off odhcpcd / DHCPv6 server on lan

      uci del dhcp.lan.ra_slaac
      uci del dhcp.lan.dhcpv6
      uci set dhcp.lan.ra='hybrid'

- Turn on IGMP snooping on br-lan, but disable querier (Let Cisco switches do it)

      uci set network.cfg030f15.igmp_snooping='1'
      uci set network.cfg030f15.multicast_querier='0'
