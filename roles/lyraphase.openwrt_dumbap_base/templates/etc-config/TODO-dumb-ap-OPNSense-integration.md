<!-- markdownlint-configure-file
{
  "line-length": {
    "line_length": 120
  }
}
-->

# TODO items to integrate with DEC850 OPNSense Firewall + DNS server

- Enable reverse DNS lookup forwarding to `unbound` DNS server running on
  OPNSense
  - Set `DNS forwardings` on
    [DHCP page](http://192.168.1.2/cgi-bin/luci/admin/network/dhcp)
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
  - No `fping` available in LEDE 17.01.4
  - The following commands will do reverse lookups for all ARP hosts

        /bin/sh -c 'arp-scan -qxl -I br-lan | cut -f1 | xargs -n1 nslookup' # slightly faster
        /bin/sh -c 'arp-scan -qxl -I br-lan | cut -f1 | xargs -n1 host'

  - Trying to force ARP ping lookups:

        # Print all hostnames found via reverse IP lookup

        time sh -c 'arp-scan -qxl -I br-lan \
          | cut -f1 | xargs -n1 host \
          | grep ".in-addr.arpa domain name pointer" \
          | sed -e "s/.*\.in-addr\.arpa domain name pointer \(.*\)$/\1/" '

        # Ping all hostnames, forcing a forward DNS lookup
        time sh -c 'arp-scan -qxl -I br-lan \
          | cut -f1 | xargs -n1 host \
          | grep ".in-addr.arpa domain name pointer" \
          | sed -e "s/.*\.in-addr\.arpa domain name pointer \(.*\)$/\1/" \
          | xargs -n1 ping -c 1 -W 1 -q'
        # Unfortunately, this still seems not to work to populate the hostnames in LEDE 17.01.4
        # We will probably have to upgrade to newer OpenWRT version

- Disable option: `Filter private`
  - Help text: `Do not forward reverse lookups for local networks`
  - Result:
    - Removes `dhcp.@dnsmasq[0].boguspriv='1'`
    - Effectively `uci set dhcp.@dnsmasq[0].boguspriv='0'`
    - Removes config line from `dnsmasq.conf.cfg*`:

          bogus-priv
