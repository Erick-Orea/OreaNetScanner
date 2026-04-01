

#!/usr/bin/env python3

# ============================================================
# OreaNet Scanner - Network Scanner Profesional
# Autor: Erick de Jesús Hernández Orea
# Descripción:
#   Herramienta de reconocimiento activo para análisis de red,
#   desarrollada con arquitectura modular y soporte para TCP, UDP
#   y fingerprinting básico de sistema operativo.
# ============================================================

import socket
import subprocess
import threading
import ipaddress
import re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from logger import info, found, warning, error
from exporter import export_txt, export_json, export_csv


def show_banner():

    BLUE = "\033[1;94m"
    RESET = "\033[0m"

    print(r"""
=====================================================================================
                                OreaNet-Scanner
=====================================================================================
""")
    print(BLUE + r"""
                           ___   ____  _____    _    
                          / _ \ |  _ \| ____|  / \   
                         | | | || |_) |  _|   / _ \  
                         | |_| ||  _ <| |___ / ___ \ 
                          \___/ |_| \_\_____/_/   \_\
                              _   _ _____ _____ 
                             | \ | | ____|_   _|
                             |  \| |  _|   | |  
                             | |\  | |___  | |  
                             |_| \_|_____| |_|  
                          ____   ____    _    _   _ 
                         / ___| / ___|  / \  | \ | |
                         \___ \| |     / _ \ |  \| |
                          ___) | |___ / ___ \| |\  |
                         |____/ \____/_/   \_\_| \_|
""" + RESET)

    print(r"""
=====================================================================================
                                OreaNet-Scanner
=====================================================================================

          Herramienta de Reconocimiento Activo y Análisis de Puertos

                  Desarrollado por Erick de Jesús Hernández Orea

""")


# -----------------------------
# 1. Detección de SO (OS Fingerprinting)
# -----------------------------

def detect_os(ip):
    """
    Detecta el sistema operativo probable basado en el TTL del ping.
    """
    try:
        result = subprocess.run(
            ["ping", "-c", "1", ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        ttl_match = re.search(r"ttl=(\d+)", result.stdout.lower())
        if not ttl_match:
            warning(f"No se pudo obtener TTL para {ip}")
            return "Desconocido"

        ttl = int(ttl_match.group(1))

        if ttl <= 64:
            os_name = "Linux/Unix"
        elif ttl <= 128:
            os_name = "Windows"
        else:
            os_name = "Cisco/BSD/Solaris"

        found(f"Sistema operativo probable para {ip}: {os_name} (TTL={ttl})")
        return f"{os_name} (TTL={ttl})"

    except Exception as e:
        error(f"Error detectando SO en {ip}: {e}")
        return "Desconocido"


# -----------------------------
# 2. Descubrimiento de hosts (Ping Sweep)
# -----------------------------

def discover_hosts(network):

    info(f"Ping Sweep iniciando en {network}")
    print(f"\n[+] Iniciando descubrimiento de hosts en la red {network}...\n")
    active_hosts = []

    try:
        net = ipaddress.ip_network(network, strict=False)
    except ValueError:
        print("[-] Error: formato de red inválido. Usa algo como 192.168.56.0/24")
        error(f"Formato de red inválido: {network}")
        return active_hosts

    for ip in net.hosts():
        ip = str(ip)
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "1", ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        if result.returncode == 0:
            print(f"[+] Host activo: {ip}")
            found(f"Host activo detectado: {ip}")
            active_hosts.append(ip)

    print("\n[+] Descubrimiento completado.")
    info("Ping Sweep completado")
    return active_hosts


# -----------------------------
# 3. Escaneo de puertos TCP
# -----------------------------

def grab_banner(ip, port):
    try:
        sock = socket.socket()
        sock.settimeout(1)
        sock.connect((ip, port))
        banner = sock.recv(1024).decode(errors="ignore")
        sock.close()

        if banner:
            found(f"Banner detectado en {ip}:{port} → {banner.strip()}")

        return banner.strip()

    except Exception as e:
        warning(f"No se pudo obtener banner en {ip}:{port} | {e}")
        return None


def scan_single_port(target_ip, port, open_ports):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((target_ip, port))

        if result == 0:
            banner = grab_banner(target_ip, port)
            if banner:
                print(f"[+] Puerto {port} abierto | Banner: {banner}")
                found(f"Puerto {port} abierto en {target_ip} | Banner: {banner}")
            else:
                print(f"[+] Puerto {port} abierto | Banner no disponible")
                found(f"Puerto {port} abierto en {target_ip} | Banner no disponible")

            open_ports.append(port)

        sock.close()

    except Exception as e:
        error(f"Error escaneando puerto {port} en {target_ip}: {e}")


def scan_ports(target_ip, ports, export_results=True):

    info(f"Escaneo de puertos TCP iniciado en {target_ip}")

    print(f"\n[+] Escaneando puertos TCP en {target_ip} con multithreading (pool=100)...\n")
    open_ports = []

    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(scan_single_port, target_ip, port, open_ports) for port in ports]
        for f in futures:
            # Forzamos a que se propaguen excepciones si las hubiera
            f.result()

    print("\n[+] Escaneo TCP completado.")
    print(f"[+] Puertos TCP abiertos encontrados: {open_ports}")

    info(f"Escaneo de puertos TCP completado en {target_ip}")

    if export_results:
        export = input("¿Deseas exportar los resultados TCP? (s/n): ")
        if export.lower() == "s":
            filename = input("Nombre del archivo (sin extensión): ")

            data = {
                "tipo_escaneo": "TCP",
                "objetivo": target_ip,
                "puertos_tcp_abiertos": open_ports
            }

            export_txt(filename, data)
            export_json(filename, data)
            export_csv(filename, data)

    return open_ports


# -----------------------------
# 4. Escaneo de puertos UDP
# -----------------------------

def scan_single_udp(ip, port, open_udp, udp_banners):
    """
    Escanea un puerto UDP individual con timeout de 1 segundo.
    """
    sock = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)

        # Enviar datagrama vacío
        sock.sendto(b"", (ip, port))

        try:
            data, _ = sock.recvfrom(1024)
            banner = data.decode(errors="ignore").strip()

            found(f"UDP {port} abierto | Banner: {banner}")
            print(f"[+] UDP {port} abierto | Banner: {banner}")
            open_udp.append(port)
            udp_banners[port] = banner

        except socket.timeout:
            # UDP abierto/filtrado (sin respuesta)
            found(f"UDP {port} abierto/filtrado (sin respuesta)")
            print(f"[+] UDP {port} abierto/filtrado (sin respuesta)")
            open_udp.append(port)

        except Exception as e:
            warning(f"UDP {port} respuesta inesperada: {e}")

    except Exception as e:
        error(f"Error escaneando UDP {port} en {ip}: {e}")

    finally:
        if sock:
            sock.close()


def scan_udp_ports(ip, ports, export_results=True):
    print(f"\n[+] Escaneando puertos UDP en {ip} con multithreading (pool=100)...\n")
    info(f"Escaneo UDP iniciado en {ip}")

    open_udp = []
    udp_banners = {}

    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(scan_single_udp, ip, port, open_udp, udp_banners) for port in ports]
        for f in futures:
            f.result()

    print(f"\n[+] Escaneo UDP completado. Puertos UDP abiertos: {open_udp}")
    info(f"Escaneo UDP completado en {ip}")

    if export_results:
        export = input("¿Deseas exportar los resultados UDP? (s/n): ")
        if export.lower() == "s":
            filename = input("Nombre del archivo (sin extensión): ")

            data = {
                "tipo_escaneo": "UDP",
                "objetivo": ip,
                "puertos_udp_abiertos": open_udp,
                "banners_udp": udp_banners
            }

            export_txt(filename, data)
            export_json(filename, data)
            export_csv(filename, data)

    return open_udp, udp_banners


# -----------------------------
# 5. Escaneo híbrido (TCP + UDP + SO)
# -----------------------------

def scan_hybrid(ip, ports):
    print(f"\n[+] Iniciando escaneo híbrido en {ip}...\n")
    info(f"Escaneo híbrido iniciado en {ip}")

    os_detected = detect_os(ip)

    tcp_open = scan_ports(ip, ports, export_results=False)
    udp_open, udp_banners = scan_udp_ports(ip, ports, export_results=False)

    print("\n=== RESULTADOS HÍBRIDOS ===")
    print(f"Sistema operativo probable: {os_detected}")
    print(f"Puertos TCP abiertos: {tcp_open}")
    print(f"Puertos UDP abiertos: {udp_open}")

    info(f"Escaneo híbrido completado en {ip}")

    export = input("¿Deseas exportar los resultados híbridos? (s/n): ")
    if export.lower() == "s":
        filename = input("Nombre del archivo (sin extensión): ")

        data = {
            "tipo_escaneo": "Híbrido (TCP + UDP)",
            "objetivo": ip,
            "sistema_operativo": os_detected,
            "puertos_tcp_abiertos": tcp_open,
            "puertos_udp_abiertos": udp_open,
            "banners_udp": udp_banners
        }

        export_txt(filename, data)
        export_json(filename, data)
        export_csv(filename, data)


# -----------------------------
# 6. Menú principal
# -----------------------------

def main():
    show_banner()

    info("OreaNet Scanner iniciado")

    print("\n=======================================================================")
    print("                      OreaNet Scanner - Menú Principal     ")
    print("=========================================================================")
    print("1. Ping Sweep")
    print("2. Escaneo TCP")
    print("3. Escaneo UDP")
    print("4. Escaneo híbrido (TCP + UDP)")
    print("5. Salir")
    print("============================================")

    opcion = input("Selecciona una opción: ")
    info(f"Opcion seleccionada: {opcion}")

    if opcion == "1":
        network = input("Ingresa la red en formato CIDR (ej: 192.168.56.0/24): ")
        discover_hosts(network)

    elif opcion == "2":
        target = input("Ingresa la IP objetivo: ")
        start_port = int(input("Puerto inicial: "))
        end_port = int(input("Puerto final: "))
        ports = range(start_port, end_port + 1)
        scan_ports(target, ports)

    elif opcion == "3":
        target = input("Ingresa la IP objetivo: ")
        start_port = int(input("Puerto inicial: "))
        end_port = int(input("Puerto final: "))
        ports = range(start_port, end_port + 1)
        scan_udp_ports(target, ports)

    elif opcion == "4":
        target = input("Ingresa la IP objetivo: ")
        start_port = int(input("Puerto inicial: "))
        end_port = int(input("Puerto final: "))
        ports = range(start_port, end_port + 1)
        scan_hybrid(target, ports)

    elif opcion == "5":
        print("Saliendo...")
        info("OreaNet Scanner finalizado por el usuario")

    else:
        print("Opción inválida.")
        warning(f"Opcion invalida ingresada: {opcion}")


if __name__ == "__main__":
    main()
