#!/usr/bin/env python


from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink


class NetworkTopo( Topo ):
    "A simple topology of 3 routers with 3 subnets"

    # pylint: disable=arguments-differ
    def build( self, **_opts ):
        
        # Defining and adding the 2 switches
        switch1 = self.addSwitch('s1')
        switch2 = self.addSwitch('s2')

        # Defining the 2 hosts 
        host1 = self.addHost( 'h1' )
        host2 = self.addHost('h2')
        host3 = self.addHost('h3')
        host4 = self.addHost( 'h4' )

        
        # Adding links between the hosts and the switches
        self.addLink(host1, switch1)
        self.addLink(host2, switch1)

        self.addLink(host3, switch2)
        self.addLink(host4, switch2)

        # Adding links between the switches
        self.addLink(switch1, switch2, delay='5ms')

        
def run():
    "Test linux router"
    topo = NetworkTopo()
    net = Mininet( topo=topo, link=TCLink) 

    net.start()

    net['h4'].cmd("iperf -s -p 5201 -D")
    net['h4'].cmd("iperf -s -p 5202 -D")
    net['h4'].cmd("iperf -s -p 5203 -D")

    net['h4'].cmd("timeout 10000 tcpdump -i h4-eth0 -w capture4.pcap &")
    net['h1'].cmd("timeout 7000 tcpdump -i h1-eth0 -w capture1.pcap & iperf -c 10.0.0.4 -p 5201 -t 5 &")
    net['h2'].cmd("timeout 7000 tcpdump -i h2-eth0 -w capture2.pcap & iperf -c 10.0.0.4 -p 5202 -t 5 &")
    net['h3'].cmd("timeout 7000 tcpdump -i h3-eth0 -w capture3.pcap & iperf -c 10.0.0.4 -p 5203 -t 5")

    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()