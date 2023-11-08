#!/usr/bin/env python


from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    # pylint: disable=arguments-differ
    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()


class NetworkTopo( Topo ):
    "A simple topology of 3 routers with 3 subnets"

    # pylint: disable=arguments-differ
    def build( self, **_opts ):
        
        # Defining and adding the 3 routers [with different subnets]
        router1 = self.addNode('ra', cls=LinuxRouter, ip='10.0.0.1/24')
        router2 = self.addNode('rb', cls=LinuxRouter, ip='10.100.0.1/24')
        router3 = self.addNode('rc', cls=LinuxRouter, ip='10.200.0.1/24')  

        # Defining and adding the 3 switches
        switch1 = self.addSwitch('s1')
        switch2 = self.addSwitch('s2')
        switch3 = self.addSwitch('s3')

        # Adding links between the routers and the switches [same subnet]
        self.addLink(switch1, router1, intfName2='ra-eth0', params2={'ip' : '10.0.0.1/24'})
        self.addLink(switch2, router2, intfName2='rb-eth0', params2={'ip' : '10.100.0.1/24'})
        self.addLink(switch3, router3, intfName2='rc-eth0', params2={'ip' : '10.200.0.1/24'})

        # Adding links between the routers [with a new subnet]
        self.addLink(router1,
                     router2,
                     intfName1='ra-eth1',
                     intfName2='rb-eth1',
                     params1={'ip': '10.0.50.1/24'},
                     params2={'ip': '10.0.50.2/24'})
        
        self.addLink(router2,
                     router3,
                     intfName1='rb-eth2',
                     intfName2='rc-eth1',
                     params1={'ip': '10.0.100.1/24'},
                     params2={'ip': '10.0.100.2/24'})
        
        self.addLink(router1,
                     router3,
                     intfName1='ra-eth2',
                     intfName2='rc-eth2',
                     params1={'ip': '10.0.150.1/24'},
                     params2={'ip': '10.0.150.2/24'})

        # Adding hosts with the definition of their default routes

        # Hosts connnected to router 1 [ra]
        host1 = self.addHost( 'h1', ip='10.0.0.100/24',
                           defaultRoute='via 10.0.0.1' )
        
        host2 = self.addHost( 'h2', ip='10.0.0.200/24',
                           defaultRoute='via 10.0.0.1' )
        
        # Hosts connnected to router 2 [rb]
        host3 = self.addHost( 'h3', ip='10.100.0.100/24',
                           defaultRoute='via 10.100.0.1' )

        host4 = self.addHost( 'h4', ip='10.100.0.200/24',
                           defaultRoute='via 10.100.0.1' )
        
        # Hosts connnected to router 3 [rc]
        host5 = self.addHost( 'h5', ip='10.200.0.100/24',
                           defaultRoute='via 10.200.0.1' )

        host6 = self.addHost( 'h6', ip='10.200.0.200/24',
                           defaultRoute='via 10.200.0.1' )
        
        # Adding links between the hosts and the switches
        self.addLink(host1, switch1)
        self.addLink(host2, switch1)

        self.addLink(host3, switch2)
        self.addLink(host4, switch2)

        self.addLink(host5, switch3)
        self.addLink(host6, switch3)
        
      
def run():
    "Test linux router"
    topo = NetworkTopo()
    net = Mininet( topo=topo, waitConnected=True) 

    print(info(net['ra'].cmd("ip route add 10.100.0.0/24 via 10.0.50.2 dev ra-eth1")))
    print(info(net['ra'].cmd("ip route add 10.200.0.0/24 via 10.0.150.2 dev ra-eth2")))

    print(info(net['rb'].cmd("ip route add 10.0.0.0/24 via 10.0.50.1 dev rb-eth1")))
    print(info(net['rb'].cmd("ip route add 10.200.0.0/24 via 10.0.100.2 dev rb-eth2")))

    print(info(net['rc'].cmd("ip route add 10.100.0.0/24 via 10.0.100.1 dev rc-eth1")))
    print(info(net['rc'].cmd("ip route add 10.0.0.0/24 via 10.0.150.1 dev rc-eth2")))
    net.start()
    info( '*** Routing Table on Router:\n' )
    info(net[ 'ra' ].cmd( 'route' ))
    info(net[ 'rb' ].cmd( 'route' ))
    info( net[ 'rc' ].cmd( 'route' ) )
    CLI( net )
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
