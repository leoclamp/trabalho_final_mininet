# Projeto final Mininet

# Questão 1

## Criar uma topologia linear com oito hosts no Mininet

1. O comando a seguir cria uma topologia linear com oito hosts no Mininet:

- `--topo linear,8`: cria uma topologia linear com 8 hosts.
- `--mac`: atribui endereços MAC padronizados automaticamente aos hosts.
- `--link tc,bw=30`: define a largura de banda dos links entre os hosts como 30 Mbps.

```sh
    sudo mn --topo linear,8 --mac --link tc,bw=30
```

![Criar_topologia_mininet](./imagens/topologia_linear.png)

## Inspecionar informações das interfaces, endereços MAC, IP e portas

```sh
    h1 ifconfig
    h2 ifconfig
    ...
    h8 ifconfig
```

![info_host_1](./imagens/h1_ifconfig.png)
![info_host_2](./imagens/h2_ifconfig.png)
![info_host_3](./imagens/h3_ifconfig.png)
![info_host_4](./imagens/h4_ifconfig.png)
![info_host_5](./imagens/h5_ifconfig.png)
![info_host_6](./imagens/h6_ifconfig.png)
![info_host_7](./imagens/h7_ifconfig.png)
![info_host_8](./imagens/h8_ifconfig.png)

```sh
    nodes
```

![nodes](./imagens/nodes.png)

```sh
    net
```

![net](./imagens/net.png)

```sh
    dump
```

![dump](./imagens/dump.png)

## Desenho ilustrativo da topologia

![desenho_ilustrativo_da_topologia_1](./imagens/desenho_ilustrativo_da_topologia_1.png)

## Testar Conectividade com Ping e tcpdump

3. testando a conectividade entre Host 1 e Host 8.

```sh
    h1 ping h8
```

![ping_host_1_e_host_8](./imagens/h1_ping_h8.png)

```sh
    h1 tcpdump -n -i h1-eth0
```

![tcpdump_h1_h8](./imagens/tcpdump_h1_h8.png)

## Configuração do servidor e cliente TCP com iperf

```sh
    h1 iperf -s -p 5555 -i 1
```
```sh
    h2 iperf -c 10.0.0.1 -p 5555 -i 1 -t 15
```

![iperf_30mb](./imagens/iperf_30mb.png)

4. Repetindo o teste para diferentes valores de largura de banda:

- largura de banda = 1 Mbps
```sh
    sudo mn --topo linear,8 --mac --link tc,bw=1
    h1 iperf -s -p 5555 -i 1
    h2 iperf -c 10.0.0.1 -p 5555 -i 1 -t 15
```

![iperf_1mb](./imagens/iperf_1mb.png)

- largura de banda = 5 Mbps
```sh
    sudo mn --topo linear,8 --mac --link tc,bw=5
    h1 iperf -s -p 5555 -i 1
    h2 iperf -c 10.0.0.1 -p 5555 -i 1 -t 15
```

![iperf_5mb](./imagens/iperf_5mb.png)

- largura de banda = 10 Mbps
```sh
    sudo mn --topo linear,8 --mac --link tc,bw=10
    h1 iperf -s -p 5555 -i 1
    h2 iperf -c 10.0.0.1 -p 5555 -i 1 -t 15
```

![iperf_10mb](./imagens/iperf_10mb.png)

- largura de banda = 15 Mbps
```sh
    sudo mn --topo linear,8 --mac --link tc,bw=15
    h1 iperf -s -p 5555 -i 1
    h2 iperf -c 10.0.0.1 -p 5555 -i 1 -t 15
```

![iperf_15mb](./imagens/iperf_15mb.png)

- largura de banda = 20 Mbps
```sh
    sudo mn --topo linear,8 --mac --link tc,bw=20
    h1 iperf -s -p 5555 -i 1
    h2 iperf -c 10.0.0.1 -p 5555 -i 1 -t 15
```

![iperf_20mb](./imagens/iperf_20mb.png)

- largura de banda = 25 Mbps
```sh
    sudo mn --topo linear,8 --mac --link tc,bw=25
    h1 iperf -s -p 5555 -i 1
    h2 iperf -c 10.0.0.1 -p 5555 -i 1 -t 15
```

![iperf_25mb](./imagens/iperf_25mb.png)

# Questão 2

### Arquivo:
  - `topologia_customizada`

## Desenho ilustrativo da topologia

![desenho_ilustrativo_da_topologia_2](./imagens/desenho_ilustrativo_da_topologia_2.png)

### Colaboradores
- Leonardo Matias
- Raissa Beatriz

