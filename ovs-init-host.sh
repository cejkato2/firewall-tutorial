#!/bin/bash

for i in "veth-ovs veth-srv" "veth-oc veth-cl" "veth-oa veth-at"; do
   names=($i)
   if ! ip l show dev "${names[0]}" 2> /dev/null; then
      echo -ne "Creating ${names[0]}@${names[1]} veth...\t"
      sudo ip l a "${names[0]}" type veth peer name "${names[1]}"
      sudo ip l set up dev "${names[0]}"
      sudo ip l set up dev "${names[1]}"
      echo "done"
   else
      echo -e "\tSkipping creation of the existing ${names[0]}@${names[1]}."
   fi
done

if ! vboxmanage list hostonlyifs | grep -q '\<vboxnet0\>'; then
   echo -ne "Creating vboxnet0...\t"
   vboxmanage hostonlyif create
   echo "done"
else
   echo -e "\tSkipping creation of the existing vboxnet0 (virtualbox hostonlyif)."
fi

echo "Starting vagrant up..."
vagrant up

echo "Set up vboxnet0 local IP"
sudo ip a a 172.16.10.1/24 b + dev vboxnet0

echo "done.

