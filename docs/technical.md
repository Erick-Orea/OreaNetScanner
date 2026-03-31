# Manual Técnico — OreaNet Scanner  
## Arquitectura, Diseño Interno y Funcionamiento Técnico

# 1. Introducción
Este documento describe la arquitectura interna, los componentes principales y las decisiones de diseño detrás de **OreaNet Scanner**, una herramienta de reconocimiento activo desarrollada en Python para análisis de red, identificación de puertos abiertos y fingerprinting básico mediante TTL.  
El proyecto está construido con un enfoque modular, mantenible y fácil de extender.

# 2. Arquitectura General
/src  
- oreanet_scanner.py → Punto de entrada y orquestación  
- logger.py → Sistema de logging centralizado  
- exporter.py → Exportación TXT/JSON/CSV  

# 3. Componentes Técnicos

## 3.1. oreanet_scanner.py
Responsabilidades:  
- Menú principal y flujo de ejecución  
- Ping Sweep (ICMP)  
- Escaneo TCP (socket TCP)  
- Escaneo UDP (socket UDP)  
- Fingerprinting básico por TTL  
- Integración con logger y exporter  
- Concurrencia mediante ThreadPoolExecutor  

## 3.2. logger.py
- Registro de eventos con timestamp  
- Formato consistente para auditoría  
- Creación automática del directorio /logs  

## 3.3. exporter.py
- Exportación estructurada en TXT, JSON y CSV  
- Manejo de excepciones  
- Creación automática del directorio /exports  

# 4. Funcionamiento Técnico

## 4.1. Ping Sweep
- Envío de ICMP Echo Request mediante subprocess.run  
- Detección de hosts activos por código de retorno  
- No requiere privilegios elevados  
- No realiza fingerprinting (solo descubrimiento)

## 4.2. Escaneo TCP
- Uso de socket.SOCK_STREAM  
- connect_ex para determinar si el puerto está abierto  
- Banner grabbing automático cuando es posible  
- Manejo de timeouts para evitar bloqueos  

## 4.3. Escaneo UDP
- Envío de datagrama vacío  
- Interpretación de respuestas o timeouts  
- Posibles falsos positivos (característica inherente a UDP)  

## 4.4. Escaneo Híbrido
- Combina fingerprinting por TTL, escaneo TCP y escaneo UDP  
- Exportación consolidada en un solo reporte  

# 5. Concurrencia
El escaneo TCP y UDP utiliza ThreadPoolExecutor(max_workers=100).  
Motivos de diseño:  
- Permite escaneos rápidos sin saturar el sistema  
- Evita bloqueos por timeouts  
- Simplifica el manejo de hilos frente a threading.Thread  
- Alternativa estable frente a asyncio para sockets tradicionales  

# 6. Manejo de Errores
- Timeouts controlados en sockets  
- Excepciones capturadas y registradas en logger.py  
- Validación de formato CIDR en Ping Sweep  
- Manejo de errores en exportación de archivos  

# 7. Limitaciones Técnicas
- El fingerprinting por TTL es aproximado  
- El escaneo UDP puede generar falsos positivos  
- No implementa SYN scan (requiere privilegios elevados)  
- No utiliza raw sockets ni técnicas avanzadas de evasión  

# 8. Conclusión
OreaNet Scanner está diseñado con una arquitectura modular, clara y extensible.  
Su implementación combina sockets de bajo nivel, concurrencia controlada y exportación estructurada, ofreciendo una base sólida para futuras mejoras o integración con herramientas más avanzadas.

