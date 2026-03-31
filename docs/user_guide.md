# Manual de Usuario — OreaNet Scanner  
## Guía práctica para instalación, uso y exportación de resultados

# 1. Introducción
Este documento explica cómo instalar, ejecutar y utilizar **OreaNet Scanner**, una herramienta de reconocimiento activo diseñada para análisis de red, identificación de puertos abiertos y obtención de banners de servicios.

# 2. Requisitos
- Python 3.10 o superior  
- Sistema operativo Linux (Kali recomendado)  
- Permisos para ejecutar ping  
- Conexión a una red local para pruebas  

# 3. Instalación

## 3.1. Clonar el repositorio
git clone https://github.com/Erick-Orea/OreaNetScanner.git  
cd OreaNetScanner  

## 3.2. Ejecución
python3 src/oreanet_scanner.py  

# 4. Menú Principal
El menú principal ofrece las siguientes opciones:

1. Ping Sweep  
2. Escaneo TCP  
3. Escaneo UDP  
4. Escaneo híbrido (TCP + UDP + OS)  
5. Salir  

# 5. Funciones de la Herramienta

## 5.1. Ping Sweep
Descubre hosts activos dentro de una red en formato CIDR.  
Ejemplo:  
- Ingresar red: 192.168.1.0/24  

Imagen de referencia:  
screenshots/ping_sweep.png  

## 5.2. Escaneo TCP
Identifica puertos TCP abiertos y realiza banner grabbing cuando es posible.  
Ejemplo:  
- IP objetivo: 192.168.1.10  
- Rango: 1–1024  

Imagen de referencia:  
screenshots/tcp_scan.png  

## 5.3. Escaneo UDP
Envía datagramas UDP y detecta puertos abiertos o filtrados.  
Ejemplo:  
- IP objetivo: 192.168.1.10  
- Rango: 1–1024  

Imagen de referencia:  
screenshots/udp_scan.png  

## 5.4. Escaneo Híbrido
Combina:  
- Fingerprinting por TTL  
- Escaneo TCP  
- Escaneo UDP  

Ejemplo:  
- IP objetivo: 192.168.1.10  
- Rango: 1–1024  

Imagen de referencia:  
screenshots/hybrid_scan.png  

# 6. Exportación de Resultados
Los resultados pueden exportarse en los formatos:  
- TXT  
- JSON  
- CSV  

Los archivos se guardan automáticamente en la carpeta:  
/exports  

Imagen de referencia:  
screenshots/exports.png  

# 7. Logs del Sistema
Todos los eventos se registran en:  
/logs/oreanetscanner.log  

Imagen de referencia:  
screenshots/logs.png  

# 8. Estructura de Carpetas
/src  
/docs  
/logs  
/exports  

# 9. Contacto
**Erick de Jesús Hernández Orea**  
TI & Cybersecurity  
Desarrollo de herramientas de seguridad y automatización.



