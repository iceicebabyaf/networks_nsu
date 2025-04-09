# Settings:
**making a docker network:**
```
docker network create --ipv6 --subnet=2001:db8:1::/64 ipv6net
```
**creating 2 docker containers (node1, node2) with ubuntu:**
```
docker run -dit --name node1 --network ipv6net --sysctl net.ipv6.conf.all.disable_ipv6=0 ubuntu
docker run -dit --name node2 --network ipv6net --sysctl net.ipv6.conf.all.disable_ipv6=0 ubuntu
```
installing tcpdump & ip into containers:
```
apt update
apt install tcpdump
# additional to node2 container:
apt install iputils-ping
```

# IPv4
searching for address:
```
xd@MacBook-Pro---x-2 ~ % docker inspect node2 | grep "IPAddress"
            "SecondaryIPAddresses": null,
            "IPAddress": "",
                    "IPAddress": "172.21.0.3",
```
so IPv4 == 172.21.0.3

now we turning on "sniffing" in node2 by IPv4:
```
tcpdump -i eth0 ip
```
and turning on sending packages from node1:
```
ping 172.21.0.3
```
so, on node2 we have:
```
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), snapshot length 262144 bytes
16:05:48.958247 IP node1.ipv6net > 6cef6c7f2f3d: ICMP echo request, id 1, seq 1, length 64
16:05:48.958330 IP 6cef6c7f2f3d > node1.ipv6net: ICMP echo reply, id 1, seq 1, length 64
```

# IPv6
searching for address:
```
root@6cef6c7f2f3d:/# ip -6 addr show dev eth0
11: eth0@if22: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default  link-netnsid 0
    inet6 2001:db8:1::3/64 scope global nodad 
       valid_lft forever preferred_lft forever
    inet6 fe80::ec71:c5ff:fede:5ae3/64 scope link 
       valid_lft forever preferred_lft forever
```
so IPv6 == 2001:db8:1::3
also we have link local adress == fe80::ec71:c5ff:fede:5ae3 (it'll be usefull for neighbor discovery)

now we turning on "sniffing" in node2 by IPv6:
```
tcpdump -i eth0 ip6
```
and turning on sending packages from node1:
```
ping6 2001:db8:1::3
```
so, on node2 we have:
```
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), snapshot length 262144 bytes
16:10:30.253783 IP6 node1.ipv6net > ff02::1:ff00:3: ICMP6, neighbor solicitation, who has 6cef6c7f2f3d, length 32
16:10:30.253946 IP6 6cef6c7f2f3d > node1.ipv6net: ICMP6, neighbor advertisement, tgt is 6cef6c7f2f3d, length 32
16:10:30.254053 IP6 node1.ipv6net > 6cef6c7f2f3d: ICMP6, echo request, id 2, seq 1, length 64
16:10:30.254072 IP6 6cef6c7f2f3d > node1.ipv6net: ICMP6, echo reply, id 2, seq 1, length 64
```


