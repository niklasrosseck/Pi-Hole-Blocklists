# Documentation for the Raspberry Pi configuration
There are two ways to recreate the Raspberry Pi setup that I used. 
The first is to download the image provided here and use Raspberry Pi Imager to load the image onto the 
Raspberry Pi. 
The second is to recreate all the steps manually. The manual setup is explained in the following:
# Manual Setup 
The Raspberry Pi Version used was the 64-bit version and the used Pi was a Raspberry Pi 4 Model B. 
By following this setup step-by-step you should get a Pi which provides a Hotspot with hostapd,
provides filtering via PiHole and can host a website with a Django framework. 
So let`s get started.
The first step is to update the Pi. 
```bash
sudo apt update
```
Then the Pi should be upgraded fully.
```bash
sudo apt full-upgrade
```
After this we can install the needed packages for the hotspot. 
We need to create the hotspot before the PiHole, otherwise there are complications, because PiHole overwrites `dnsmasq`.
```bash
sudo apt install dnsmasq hostapd dhcpcd5
```
# Static IP Address
We need a static IP address for the wireless port and for the ethernet port. The static IP address for the wireless port is
required, because our Pi should act as a router, and the static ethernet IP address is needed for PiHole. 
For this we need to edit the configuration file of dhcpcd.
```bash
sudo nano /etc/dhcpcd.conf
```
At the end of the file insert the following:
```bash
interface eth0
    static ip_address=192.168.2.135/24

interface wlan0
    static ip_address=192.168.5.1/24
    nohook wpa_supplicant
```
The IP-addresses can be adjusted to your liking. This is just an example, but keep in mind that the IP-address for eth0 is the one
you need if you want to ssh into your Pi. 
After this restart the service.
```bash
sudo systemctl restart dhcpcd
```
# Configure DHCP Server
For configuring the DHCP server and handing out the correct IP-addresses to the clients we need to adjust the configuration of dnsmasq.
```bash
sudo nano /etc/dnsmasq.conf
```
Search for `#interface=` and input:
```bash
interface=wlan0
```
Then a bit further down you will find `#dhcp-range=`. Change this to your desired DHCP range.
```bash
dhcp-range=192.168.5.50,192.168.5.150,255.255.255.0,12h
```
This is again just an example. You can choose a different range or different lease time. 
Restart the service for the changes to take effect.
```bash
sudo systemctl restart dnsmasq
```
# Creating the hotspot
For the hotspot we are using hostapd. Create a configuration file for hostapd.
```bash
sudo nano /etc/hostapd/hostapd.conf
```
Then input the following:
```bash
# Name of the interface
interface=wlan0
# Name of the Access Point
ssid=YOURSSID
wpa=2
# Passphrase
wpa_passphrase=YOURPASSPHRASE
country_code=DE
channel=7
auth_algs=1
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP CCMP
rsn_pairwise=CCMP
```
Make sure to input your own SSID and your own passphrase. The passphrase needs to be atleast 8 characters long.
Now we add this configuration file as the default hostapd configuration.
```bash
sudo nano /etc/default/hostapd
```
Here find `#DAEMON_CONF` and replace it with:
```bash
DAEMON_CONF="/etc/hostapd/hostapd.conf"
```
Now we can start our hotspot. 
```bash
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd
```
Now we have a hotspot and it should show up as a viable access point, but we have no internet access.
This is because we are missing a few routing rules.
# Routing rules
First we need to enable routing. For this we edit the `sysctl.conf`.
```bash
sudo nano /etc/sysctl.conf
```
Here we need to uncomment the following:
```bash
net.ipv4.ip_forward=1
```
Now we just need one more rule, but for this we need to install `iptables`.
```bash
sudo apt install iptables
```
We could now add our iptables rule, but then it would not get saved and after a reboot it would be lost. I tried `netfilter-persistent` but it did not work for me.
That is why I found another way using `rc.local`.
For this we create a script which `rc.local` executes when booting. 
```bash
sudo nano /etc/iptables-rules.sh
```
In this script we add the following:
```bash
#!/bin/sh
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```
Then we make the script executable.
```bash
sudo chmod +x /etc/iptables-rules.sh
```
There is another script we need to add to `rc.local`, which restarts the hostapd service after every boot. Without this script the hostapd service would need to be restarted
manually after every reboot or shutdown. So we create a script for this too.
```bash
sudo nano /etc/hostapd-rules.sh
```
Add the following:
```bash
#!/bin/bash
systemctl restart hostapd
```
Make the script executable.
```bash
sudo chmod +x /etc/hostapd-rules.sh
```
Now we can add both scripts to `rc.local`. Add them before `exit 0`.
```bash
/etc/iptables-rules.sh
/etc/hostapd-rules.sh
```
Make the `rc.local` script executable.
```bash
sudo chmod +x rc.local
```
We are now finished and can reboot.
```bash
sudo reboot
```
After the reboot you should see the SSID of your hotspot and it should be working as intented. 
Now that we have a working hotspot we can add PiHole. If you are using a desktop environment it might not be working after a reboot, because the light display manager failed.
To fix this you can adjust the configuration for the light display manager.
```bash
sudo nano /etc/lightdm/lightdm.conf
```
Search for the uncommentated `greeter-session` and replace it with:
```bash
greeter-session=lightdm-gtk-greeter
```
# PiHole
For adding PiHole we can download it from PiHole directly with:
```bash
curl -sSL https://install.pi-hole.net | bash
```
This will run for a bit and then open an installation wizard. 
[!alt text](https://github.com/niklasrosseck/Pi-Hole-Blocklists/blob/main/RaspberryPi/Images/first_step.png)
Just press ENTER(OK) and proceed.
The second screen will tell you that PiHole is free, but you can support by donating. Here everyone can decide for themselves if they wanna donate.
[![No G](https://raw.githubusercontent.com/niklasrosseck/Pi-Hole-Blocklists/main/RaspberryPi/Images/pihole_second step.png)](https://github.com/niklasrosseck/Pi-Hole-Blocklists)
Press ENTER(OK) to proceed. 
