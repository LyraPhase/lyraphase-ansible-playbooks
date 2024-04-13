# TODO items to integrate with DEC850 OPNSense Firewall + DNS server


- Enable reverse DNS lookup forwarding to `unbound` DNS server running on OPNSense
  - Set `DNS forwardings` on [DHCP page](http://192.168.1.2/cgi-bin/luci/admin/network/dhcp)
  - Add DNS forwarder lines: `/*.in-addr.arpa/192.168.1.1`, `192.168.1.1`
  - Results in `/tmp/etc/dnsmasq.conf.cfg02411c` with contents:

        server=/local/
        server=/cluster.local/10.96.0.10
        server=/*.in-addr.arpa/192.168.1.1
        server=192.168.1.1
    
  - And in `uci show`:

        uci show  | grep -i cluster.local
        dhcp.@dnsmasq[0].server='/cluster.local/10.96.0.10' '/*.in-addr.arpa/192.168.1.1'

- [x] Install package: `arp-scan`
- [x] Install crontab
  - Fix no `-d` option in LEDE 17.01.4
- Disable option: `Filter private`
  - Help text: `Do not forward reverse lookups for local networks`
  - Result:
    - Removes `dhcp.@dnsmasq[0].boguspriv='1'`
    - Effectively `uci set dhcp.@dnsmasq[0].boguspriv='0'`
    - Removes config line from `dnsmasq.conf.cfg*`:

        bogus-priv

