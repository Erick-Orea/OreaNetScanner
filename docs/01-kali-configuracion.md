# Kali Linux – Configuración Base

## 1. Datos generales
- SO: Kali Linux Rolling
- RAM: 4 GB
- CPU: 2 cores
- Disco: 40 GB
- Fecha de creación: (tu fecha)

## 2. Configuración de red
- Adaptador 1: NAT
- Adaptador 2: Host‑Only #7
- Rango Host‑Only: 192.168.215.0/24
- IP asignada: 192.168.215.10
- Gateway: 192.168.215.1
- DNS: 8.8.8.8

## 3. Comandos de verificación
### ip a

┌──(kali㉿kali)-[~]
└─$ ip a           
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute 
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:58:9b:8c brd ff:ff:ff:ff:ff:ff
    inet 10.0.2.15/24 brd 10.0.2.255 scope global dynamic noprefixroute eth0
       valid_lft 85874sec preferred_lft 85874sec
    inet6 fd17:625c:f037:2:92d8:9068:5960:5216/64 scope global dynamic noprefixroute 
       valid_lft 86216sec preferred_lft 14216sec
    inet6 fe80::a692:d7a7:fe0b:d28e/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:d7:05:40 brd ff:ff:ff:ff:ff:ff
    inet 192.168.215.10/24 brd 192.168.215.255 scope global eth1
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fed7:540/64 scope link proto kernel_ll 
       valid_lft forever preferred_lft forever
                                                  

## 4. Pruebas de conectividad
- Ping a Ubuntu: `ping 192.168.215.20` (OK)

## 5. Snapshot asociado
- Nombre: kali-base-red-configurada
- Fecha: 23 Mar. 2026