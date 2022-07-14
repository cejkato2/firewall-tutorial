# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # config.vm.network "forwarded_port", guest: 80, host: 8080
  # config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"
  # config.vm.network "private_network", ip: "192.168.33.10"
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  config.vm.define "ovs" do |ovs|
    ovs.vm.box = "generic/fedora35"

    ovs.vm.provider "virtualbox" do |v|
      v.customize ["modifyvm", :id, "--nic2", "hostonly", "--hostonlyadapter2", "vboxnet0", "--nicpromisc2", "allow-all"]
      v.customize ["modifyvm", :id, "--nic3", "bridged", "--bridgeadapter3", "veth-ovs", "--nicpromisc3", "allow-all"]
      v.customize ["modifyvm", :id, "--nic4", "bridged", "--bridgeadapter4", "veth-oa", "--nicpromisc4", "allow-all"]
    end

    ovs.vm.synced_folder "ovs", "/vagrant/", type: "rsync"

    ovs.vm.provision "shell", inline: <<-SHELL
      hostnamectl set-hostname ovs
      dnf -y install openvswitch openvswitch-test tcpdump nc python3-pip
      pip install flask
      systemctl enable --now openvswitch
      ovs-vsctl add-br br0
      ovs-vsctl add-port br0 eth1
      ovs-vsctl add-port br0 eth2
      ovs-vsctl add-port br0 eth3
      ovs-vsctl add-port br0 int0 -- set Interface int0 type=internal
      ip a a 172.16.10.254/24 b + dev int0
      ip l set int0 up

      ovs-vsctl -- set Bridge br0 ipfix=@i -- --id=@i create IPFIX targets='"172.16.10.1:4739"' obs_domain_id=123 obs_point_id=456 cache_active_timeout=30
      ovs-vsctl -- set port eth2 qos=@newqos -- --id=@newqos create qos type=linux-htb other-config:max-rate=100000 queues:123=@eth10queue -- --id=@eth10queue create queue other-config:max-rate=100000

      ovs-ofctl del-flows br0
      ovs-ofctl add-flow br0 priority=5,in_port=2,actions=set_queue:123,normal
      ovs-ofctl add-flow br0 priority=1,actions=normal

      cp /vagrant/rtbh.service /usr/lib/systemd/system/
      systemctl enable --now rtbh.service
      firewall-cmd --add-port 8080/tcp

      # ONOS SDN controller:
      #  dnf install -y podman
      #  podman pull docker.io/onosproject/onos:latest
      #  podman run --name onos -p 6653:6653 -p 8101:8101 -p 8181:8181 -d onos
      #  ovs-vsctl set bridge br0 protocols=OpenFlow10,OpenFlow11,OpenFlow12,OpenFlow13
      #  ovs-vsctl set-controller br0 tcp:172.16.10.254:6653

    SHELL
  end

  config.vm.define "server" do |server|
    server.vm.box = "generic/fedora35"
    server.vm.provider "virtualbox" do |v|
      v.customize ["modifyvm", :id, "--nic2", "bridged", "--bridgeadapter2", "veth-srv", "--nicpromisc2", "allow-all"]
    end
    server.vm.synced_folder "server", "/vagrant/", type: "rsync"
    server.vm.provision "shell", inline: <<-SHELL
      hostnamectl set-hostname server
      dnf -y install httpd tcpdump python3-pip
      pip install flask Flask-Session
      systemctl enable --now httpd.service
      nmcli c modify "Wired connection 1" ipv4.addresses '172.16.10.2/24' ipv4.gateway 172.16.10.254 ipv4.method manual
      nmcli d disconnect eth1
      nmcli d connect eth1
      cp /vagrant/webapp.service /lib/systemd/system/
      systemctl enable --now webapp.service
      firewall-cmd --add-port 8080/tcp
    SHELL
  end

  config.vm.define "attacker" do |attacker|
    attacker.vm.box = "generic/alpine316"
    attacker.vm.provider "virtualbox" do |v|
      v.customize ["modifyvm", :id, "--nic2", "bridged", "--bridgeadapter2", "veth-at", "--nicpromisc2", "allow-all"]
    end

    attacker.vm.synced_folder "attacker", "/vagrant/", type: "rsync"

    attacker.vm.provision "shell", inline: <<-SHELL
      apk update
      apk add python3 py3-pip
      pip install flask requests scapy
      ip a a 172.16.10.123/24 dev eth1
      ip l set up dev eth1
      cp /vagrant/attackerwebapp /etc/init.d/
      chmod +x /etc/init.d/attackerwebapp
      rc-update add attackerwebapp
      rc-service  attackerwebapp start
    SHELL
  end
end
