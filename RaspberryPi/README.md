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
We need to create the hotspot before the PiHole, otherwise there are complications, because both use `dnsmasq`.
```bash
sudo apt install dnsmasq hostapd
```
