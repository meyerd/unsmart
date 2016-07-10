UnSmart
=======

Stop Samsung SmartTVs from leaking data to the outside.

Recently, when reconsidering the so called smart functions of my TV set,
I realized, that I do not really need them and could just unplug the TV 
from the network in order to be save, no data leaks out (especially with
all the cameras and microphones built in).

Then I realized, it is no longer possible to watch video files of a USB
disk. This is ridiculous! Watching local files should be possible without
any internet connection. What else do I have a Linux system running in my
TV for, if not doing that?

Ideally, the whole operating system of the TV would be replaced with a full
free and open source version, but this is unfortunately not possible due to
all the signal processing, proprietary chips and no documentation at all.

Well, I still want to watch my video files, but not have a internet connection.

HowTo
-----

Throughout this document the IP address of the TV is assumed to be 192.168.0.31
and the IP address of the linux box (e.g. a RaspberryPI) is 192.168.0.30. In
your setup, you have to replace these numbers of course.

Install `dnsmasq`

    $ sudo apt-get install dnsmasq

Then customize the file `dnsmasq.conf` and put in the IP addresses for
your network. Run the `dnsmasq` daemon via 

    $ sudo dnsmasq -h -d -q -R -C dnsmasq.conf

(if you are happy with your setup, you can run it via `sudo dnsmasq -h -q -R -C dnsmasq.conf`
in order to send it to the background).

Now start the simple TCP server, that will answer all requests on port 80
with the same prerecorded xml file (see below, actually this should really
be improved, especially if you want to run other services in parallel on
you machine including a propoer HTTP server).

    $ sudo python simple_tcp.py 80

You can start this script inside a screen, so you can detach from the
console without exiting the server.

You need to symlink the proper `samsungcom_fake.txt` file, in case you accidentally
"really" connected the tv to the internet and all shit got updated automatically.

Now configure your TV to a fixed IP and put in the IP address of your 
server you just set up as gateway and nameserver. You should now read
the message, that the TV is successfully connected to the internet. The
start page of SmartHub as well as all the other pages will no longer work
properly, but you will be able to watch videos and recordings off the 
local disk. DLNA will also still be working in the local network.

Sniffing the `.xml`
-------------------

You need to sniff the xml file that is regularly requested from Samsung in
order to check for internet connectivity.

First you have to enable ip forwarding via

    sudo sysctl -w net.ipv4.ip_forward=1

Then you have to enable NAT in order to forward the traffic from the 
TV to the internet

    sudo iptables -t nat -F
    sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
    sudo iptables -A FORWARD -i eth0 -o eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT
    sudo iptables -A FORWARD -i eth0 -o eth0 -j ACCEPT

Now all traffic should be forwarded (remember to also adapt your `dnsmasq.conf`
and comment the line `address=/#/192.168.0.30`) and you should be able to 
remotely sniff the traffic via

    ssh <raspberry pi> "sudo tcpdump -U -s0 -w - 'not port 22'" | wireshark -k -i -

Then you should once in a while see a HTTP request to `samsung.com`, downloading
a `.xml` file (`.../us.xml` in my case). Right click in wireshark and choose "follow
TCP stream". Then save this HTTP conversation as raw and delete the request, only
leaving the answer part. This can now be used in the simple Python tcp server.

In my case there were some very suspicious 3 bytes before the xml data starts,
who knows what that is for. Also I wonder why the stocktickers for the US are 
downloaded for a TV model purchased in Germany ...

Working Models
--------------

All this was tested on a Samsung UE40F6400.

Install as Service
------------------

Copy the `.system` files to `/lib/systemd/system`. Adjust the working directory of the 
scripts. Chmod `chmod 0644 /lib/systemd/system/unsmart*`.
Enable the services `systemctl enable unsmart-dns.service`, `systemctl enable unsmart-http.service`.


TODO
====

- Iptables for NAT
- Iptables for selective services (e.g. youtube)
- Run the fake HTTP server on different port and forward via Iptables
- Inspect detailled HTTP traffic
- Inspect SSL traffic example tutorial `http://blog.philippheckel.com/2013/08/04/use-sslsplit-to-transparently-sniff-tls-ssl-connections/`
