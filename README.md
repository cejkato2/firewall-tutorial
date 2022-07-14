# firewall-tutorial

The aim of this repo is to support explanation of firewall using
firewalld and OpenVSwitch (OVS) for remote blocking of the network traffic (Remotely Triggered BlackHole - RTBH).

This repo contains files to create and install a set of virtual machines using vagrant and VirtualBox:

## Server:

contains Apache server (default Fedora page only) listening on 80/TCP,
and Flask web application with login (with a web page with a template from
"Free Html Templates") listening on 8080/TCP started by systemd service.

## OVS:

Contains OpenVSwitch and a simple Flask web application to insert entries into Flow table via web browser.
Flask application is started by systemd server (rtbh)
It contains:
1) management NIC
2) hostonly interface to connect host OS into the infrastructure
3) interface connected to Server (there is a configured QoS - to rate limit cca 100Kb/s connectivity of this port)
4) interface connected to Attacker

## Attacker:

Contains simple Flask web application to start a) bruteforce attack to iterate password into login page on the Server (http://172.16.10.2:8080/login/),
b) simple flood of UDP packets with spoofed source IP targetted against Server to exhaust Server's connectivity.

Using http://172.16.10.123/ it can be started and stopped.

# Setup

To prepare the host OS, use `./ovs-init-host.sh`, which:

1. creates vboxnet0 (hostonly interface for VirtualBox)
2. creates veth interface pairs to interconnect OVS - Server, OVS - Attacker
3. runs `vagrant up` to start everything

Presentation slides (in Czech language) are included: [presentation-slides-cs.pdf](presentation-slides-cs.pdf)

