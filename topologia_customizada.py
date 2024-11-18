from mininet.topo import Topo

class MyTopo( Topo ):
    "7 host, 7 switch"

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        h1 = self.addHost('h1', mac="00:00:00:00:00:01", ip="10.0.0.1/24")
        h2 = self.addHost('h2', mac="00:00:00:00:00:02", ip="10.0.0.2/24")
        h3 = self.addHost('h3', mac="00:00:00:00:00:03", ip="10.0.0.3/24")
        h4 = self.addHost('h4', mac="00:00:00:00:00:04", ip="10.0.0.4/24")
        h5 = self.addHost('h5', mac="00:00:00:00:00:05", ip="10.0.0.5/24")
        h6 = self.addHost('h6', mac="00:00:00:00:00:06", ip="10.0.0.6/24")
        h7 = self.addHost('h7', mac="00:00:00:00:00:07", ip="10.0.0.7/24")

        s1 = self.addSwitch( 's1' )
        s2 = self.addSwitch( 's2' )
        s3 = self.addSwitch( 's3' )
        s4 = self.addSwitch( 's4' )
        s5 = self.addSwitch( 's5' )
        s6 = self.addSwitch( 's6' )
        s7 = self.addSwitch( 's7' )
        

        # Add links
        self.addLink(s1,s2)
        self.addLink(s2,h1)
        self.addLink(s2,s4)
        self.addLink(s4,h5)
        self.addLink(s4,s3)
        self.addLink(s3,h6)
        self.addLink(s3,s7)
        self.addLink(s7,h7)
        self.addLink(s4,s5)
        self.addLink(s5,h4)
        self.addLink(s5,s6)
        self.addLink(s6,h2)
        self.addLink(s6,h3)
        


topos = { 'mytopo': ( lambda: MyTopo() ) }


def setup_network():
    topo = MyTopo()
    # Inicializa a rede Mininet usando a topologia `topo`, com switches OVS e um controlador remoto.
    net = Mininet(topo=topo, switch=OVSSwitch, controller=RemoteController)
    net.start()

    # B) Inspecionar interfaces e endereços MAC/IP
    print("\nNetwork Interfaces and MAC/IP Addresses:")
    # Imprime o nome do host, seu endereço MAC e IP.
    for host in net.hosts:
        # Imprime o nome do host, seu endereço MAC e IP.
        print(f"{host.name} - MAC: {host.MAC()} - IP: {host.IP()}")

    # Loop através de cada switch na rede.
    for switch in net.switches:
        print(f"\nSwitch {switch.name} interfaces:")
        
        # Executa o comando "ovs-ofctl show" para mostrar as interfaces do switch e detalhes de suas portas.
        print(switch.cmd("ovs-ofctl show", switch.name))
        
        # Executa o comando "ovs-ofctl dump-flows" para exibir as regras de fluxo atuais do switch.
        print(switch.cmd("ovs-ofctl dump-flows", switch.name))

    # D) Teste de ping entre alguns hosts
    print("\nTesting connectivity with ping between selected hosts:")
    # Realiza um teste de ping entre h1 e h2...
    net.ping([net.get('h1'), net.get('h2')])
    net.ping([net.get('h1'), net.get('h7')])
    net.ping([net.get('h3'), net.get('h5')])
    net.ping([net.get('h4'), net.get('h6')])
    net.ping([net.get('h2'), net.get('h3')])


    # E) Remover regras anteriores e criar regras baseadas em endereços MAC
    print("\nDeleting previous rules and setting up MAC-based flows:")
    # Loop através de cada switch na rede.
    for switch in net.switches:
        # Remove todas as regras de fluxo do switch usando "ovs-ofctl del-flows".
        switch.cmd("ovs-ofctl del-flows", switch.name)

    # Regras para comunicação baseada em MAC
    # Adiciona uma regra no switch s6 para encaminhar pacotes de h3 para h2 na porta 4.
    net.get('s6').cmd("ovs-ofctl add-flow s6 'dl_src=00:00:00:00:00:03,dl_dst=00:00:00:00:00:02,actions=output:4'")

    # Adiciona uma regra no switch s6 para encaminhar pacotes de h2 para h3 na porta 1.
    net.get('s6').cmd("ovs-ofctl add-flow s6 'dl_src=00:00:00:00:00:02,dl_dst=00:00:00:00:00:03,actions=output:1'")
    
    # Adiciona uma regra no switch s6 para encaminhar pacotes de h3 para h4 na porta 9.
    net.get('s6').cmd("ovs-ofctl add-flow s6 'dl_src=00:00:00:00:00:03,dl_dst=00:00:00:00:00:04,actions=output:9'")
    
    # Adiciona uma regra no switch s5 para encaminhar pacotes de h4 para h3 na porta 1.
    net.get('s5').cmd("ovs-ofctl add-flow s5 'dl_src=00:00:00:00:00:04,dl_dst=00:00:00:00:00:03,actions=output:1'")

    # Adiciona uma regra no switch s6 para encaminhar pacotes de h3 para h5 na porta 12.
    net.get('s6').cmd("ovs-ofctl add-flow s6 'dl_src=00:00:00:00:00:03,dl_dst=00:00:00:00:00:05,actions=output:12'")
    
    # Adiciona uma regra no switch s4 para encaminhar pacotes de h5 para h3 na porta 1.
    net.get('s4').cmd("ovs-ofctl add-flow s4 'dl_src=00:00:00:00:00:05,dl_dst=00:00:00:00:00:03,actions=output:1'")

    # Adiciona uma regra no switch s6 para encaminhar pacotes de h2 para h4 na porta 9.
    net.get('s6').cmd("ovs-ofctl add-flow s6 'dl_src=00:00:00:00:00:02,dl_dst=00:00:00:00:00:04,actions=output:9'")
    
    # Adiciona uma regra no switch s4 para encaminhar pacotes de h4 para h2 na porta 4.
    net.get('s5').cmd("ovs-ofctl add-flow s5 'dl_src=00:00:00:00:00:04,dl_dst=00:00:00:00:00:02,actions=output:4'")

    # F) Testando conectividade após configuração de regras
    print("\nTesting connectivity with ping after setting MAC-based flows:")


    net.ping([net.get('h3'), net.get('h2')])
    net.ping([net.get('h3'), net.get('h4')])
    net.ping([net.get('h3'), net.get('h5')])
    net.ping([net.get('h2'), net.get('h4')])


    # Abre o CLI do Mininet para permitir a interação manual com a rede.
    CLI(net)

    # Para a rede após o término da configuração e testes.
    net.stop()


if __name__ == '__main__':
    # Define o nível de log para "info" para fornecer mais detalhes durante a execução.
    setLogLevel('info')

    # Executa a função `setup_network` para configurar e testar a rede.
    setup_network()



# Comandos no mininet:
# A)
# sudo mn --custom mytopo.py --topo mytopo --mac --controller=remote,ip=127.0.0.1,port=6633

# B)
# nodes
# h1 ifconfig
# h1 ping -c 4 h2
# sh ovs-ofctl show s1 // Verifica as portas e conexão de um switch especifico
# sh ovs-ofctl dump-flows s1 // Verificar as rotas dos switches

# C) - Foto

# D)
# h1 ping -c 4 h2
# h1 ping -c 4 h7
# h3 ping -c 4 h5
# h4 ping -c 4 h6
# h2 ping -c 4 h3

# E) Usar ovs-ofctl para cada switch, removendo as regras
# sh ovs-ofctl del-flows s1
# sh ovs-ofctl del-flows s2
# sh ovs-ofctl del-flows s3
# sh ovs-ofctl del-flows s4
# sh ovs-ofctl del-flows s5
# sh ovs-ofctl del-flows s6
# sh ovs-ofctl del-flows s7

# Criando novas regras:

# F) Testando as regras
# h1 ping -c 4 h5
# h2 ping -c 4 h6





