# Ubuntu Server – Configuración Base

## 1. Datos generales
- SO: Ubuntu Server 22.04
- RAM: 4 GB
- CPU: 2 cores
- Disco: 40 GB
- Fecha de creación: 22 Mar. 2026

## 2. Configuración de red
- Adaptador 1: NAT
- Adaptador 2: Host‑Only #7
- Rango Host‑Only: 192.168.215.0/24
- IP asignada: 192.168.215.20
- Gateway: 192.168.215.1
- DNS: 8.8.8.8

## 3. Archivo de configuración (Netplan)
/etc/netplan/01-netcfg.yaml

network:
  version: 2
  ethernets:
    enp0s3:
      addresses:
        - 192.168.215.20/24
      gateway4: 192.168.215.1
      nameservers:
        addresses:
          - 8.8.8.8

## 4. Comandos de verificación
### ip a
(agrega captura o salida)

## 5. Pruebas de conectividad
- Ping a Kali: `ping 192.168.215.10` (OK)

## 6. Snapshot asociado
- Nombre: ubuntu-base-red-configurada
- Fecha: (23 Mar. 2025)