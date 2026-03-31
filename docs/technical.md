# Manual Técnico — OreaNet Scanner  
### Arquitectura, Diseño Interno y Funcionamiento Técnico

---

## 1. Introducción

Este documento describe la arquitectura interna, los componentes principales y las decisiones técnicas detrás de **OreaNet Scanner**, una herramienta de reconocimiento activo y análisis de puertos desarrollada en Python.

---

## 2. Arquitectura General

```
/src
    oreanet_scanner.py
    logger.py
    exporter.py
```

---

## 3. Componentes Técnicos

### 3.1. oreanet_scanner.py
- Control principal
- Menú
- Escaneos TCP/UDP
- Ping Sweep
- Fingerprinting por TTL

### 3.2. logger.py
- Registro de eventos
- Timestamps
- Auditoría

### 3.3. exporter.py
- Exportación TXT/JSON/CSV
- Estructura de datos limpia

---

## 4. Funcionamiento Técnico

### Ping Sweep
- ICMP Echo Request
- TTL para inferir SO

### Escaneo TCP
- Conexión `socket.SOCK_STREAM`
- Banner grabbing

### Escaneo UDP
- Datagrama vacío
- Interpretación ICMP

### Escaneo Híbrido
- Combina todo lo anterior

---

## 5. Concurrencia

Uso de:

```
ThreadPoolExecutor(max_workers=100)
```

Evita saturación del sistema y mejora rendimiento.

---

## 6. Limitaciones Técnicas

- UDP puede generar falsos positivos  
- TTL no es 100% exacto  
- Escaneo SYN requiere privilegios  

---

## 7. Conclusión

OreaNet Scanner es modular, estable y profesional, diseñado con buenas prácticas de arquitectura y concurrencia.

