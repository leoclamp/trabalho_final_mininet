from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI

class CustomTopo(Topo):
    def build(self):
        # Adicionar switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')
        s6 = self.addSwitch('s6')
        s7 = self.addSwitch('s7')

        # Adicionar hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        h5 = self.addHost('h5')
        h6 = self.addHost('h6')
        h7 = self.addHost('h7')

        # Conectar hosts aos switches
        self.addLink(h1, s2)
        self.addLink(h2, s6)
        self.addLink(h3, s6)
        self.addLink(h4, s5)
        self.addLink(h5, s4)
        self.addLink(h6, s3)
        self.addLink(h7, s7)

        # Conectar switches entre si
        self.addLink(s1, s2)
        self.addLink(s2, s4)
        self.addLink(s3, s4)
        self.addLink(s3, s7)
        self.addLink(s4, s5)
        self.addLink(s5, s6)

def run():
    # Configurar o log
    setLogLevel('info')

    # a) Criar topologia customizada
    topo = CustomTopo()
    net = Mininet(topo=topo, controller=None)
    net.start()

    # b) Inspecionar informações das interfaces
    for host in net.hosts:
        print(f"Informações do host {host.name}:")
        print("IP:", host.IP())
        print("MAC:", host.MAC())
        print("Porta:", host.defaultIntf())

    # d) Fazer um ping para cada host e verificar a conectividade
    print("Executando teste de ping geral entre todos os hosts...")
    print(net.pingAll())

    # e) Apagar regras anteriores
    print("Apagando regras anteriores nos switches...")
    for switch in net.switches:
        switch.cmd('ovs-ofctl del-flows', switch.name)

    # Adicionar regras baseadas em MAC para comunicação entre hosts
    print("Configurando regras baseadas em endereços MAC...")
    s2, s4, s6 = net.get('s2', 's4', 's6')
    h1, h3, h5 = net.get('h1', 'h3', 'h5')

    # Regras de exemplo para permitir comunicação baseada em MAC entre alguns hosts
    print(s2.cmd(f'ovs-ofctl add-flow {s2} dl_src={h1.MAC()},dl_dst={h5.MAC()},actions=output:1'))
    print(s4.cmd(f'ovs-ofctl add-flow {s4} dl_src={h5.MAC()},dl_dst={h3.MAC()},actions=output:2'))
    print(s6.cmd(f'ovs-ofctl add-flow {s6} dl_src={h3.MAC()},dl_dst={h1.MAC()},actions=output:1'))

    # e) Testar ping entre hosts para verificar regras de MAC
    print("Executando teste de ping entre hosts com regras de MAC...")
    print(net.ping([h1, h5]))
    print(net.ping([h5, h3]))
    print(net.ping([h3, h1]))

    # Abrir CLI para exploração interativa
    CLI(net)

    # Encerrar a rede
    net.stop()

if __name__ == '__main__':
    run()