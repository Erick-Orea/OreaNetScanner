# 01 - Configuración de Kali Linux  
## Entorno base para el laboratorio de ciberseguridad

---

# 🖥️ Información del sistema

- **Versión:** Kali GNU/Linux Rolling (2026.1)  
- **Origen:** Imagen oficial de Offensive Security  
- **Recursos asignados:**  
  - RAM: 6144 MB  
  - CPU: 2 vCPUs  
  - Disco: 40 GB  

---

# 🌐 Configuración de red

La máquina Kali utiliza una configuración de red dual para permitir acceso a internet y comunicación interna con el servidor Ubuntu.

- **Modo de red:** NAT + Host-Only  

## Interfaz NAT (eth0)
- IP: 10.0.2.15  
- Uso: Acceso a internet desde la VM  

## Interfaz Host-Only (eth1)
- IP: 192.168.215.10/24  
- Uso: Comunicación directa con el servidor Ubuntu  

## Conectividad con Ubuntu
- Comunicación verificada mediante ping a **192.168.215.11**  
- Conectividad estable y bidireccional  

---

# 🔧 Herramientas base instaladas

Kali incluye múltiples herramientas preinstaladas.  
Para este laboratorio se consideran esenciales:

- Nmap  
- Net-tools  
- Git  
- Curl  
- Wget  

*(Herramientas adicionales se documentarán en este archivo.)*

---

# 📸 Evidencias

## Salida de `ip a`
screenshots/configuracionVMs/kali/Salida_ip.png  

## Salida de `cat /etc/os-release`
screenshots/configuracionVMs/kali/Salida_cat.png  

## Prueba de ping hacia Ubuntu
screenshots/configuracionVMs/kali/Ping.png  

---

# 📝 Notas adicionales

- Kali funciona como estación principal de pentesting dentro del laboratorio.  
- Conectividad SSH hacia Ubuntu verificada.  
- Configuración estable y lista para prácticas de análisis de red y seguridad.
