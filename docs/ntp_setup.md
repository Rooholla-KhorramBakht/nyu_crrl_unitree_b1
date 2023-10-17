# Time synchronization between machines

chrony is used to perform synchronization. It conflicts with `systemd-timesyncd` service. On all computers, run:
```bash
  systemctl disable --now systemd-timesyncd.service
  sudo apt install chrony
```

On unitree, modify `/etc/chrony/chrony.conf` to add (right after all pools):
```
local stratum 10
allow 192.168.123.0/24
```

Then run:
```bash
  systemctl restart chrony.service
```

This enables the use of unitree machine as an NTP server for jetsons.

On each jetson, modify `/etc/chrony/chrony.conf`, comment out all pool links, then
add (again, right after pools):
```
server 192.168.123.1 minpoll -1 maxpoll -1
```
The `minpoll` and `maxpoll` options determine the minimum and maximum polling rate to negotiate the time with the server. The value is powers of two so -1 means 0.5 seconds. 
Then run
```
  systemctl restart chrony.service
```

Verify using `timedatectl` that the time stamps are synchronized between different machines.

*NOTE*: What we really care is that the computers on Unitree are synchronized between
each other, even if they may be slightly off globally. However, global synchronization
becomes important when we need to perform package updates
