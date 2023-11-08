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


        host4 = self.addHost( 'h4' )

        
        # Adding links between the hosts and the switches
        self.addLink(host1, switch1)


        self.addLink(host4, switch2)

        # Adding links between the switches
        self.addLink(switch1, switch2, bw=100, delay='5ms')

        
      
def run():
    "Test linux router"
    topo = NetworkTopo()
    net = Mininet( topo=topo, link=TCLink ) 

    net.start()
    net['h4'].cmd("python -m http.server 80 &")
    CLI( net )
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
