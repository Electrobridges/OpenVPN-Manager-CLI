# Guía de Configuración

Esta guía detalla todas las opciones de configuración para OpenVPN Manager CLI.

## Configuración de la Aplicación

### Constantes Principales

Edita el archivo `src/ovpn-manager.py`:

```python
# Ruta al archivo de logs de OpenVPN
DEFAULT_LOG_PATH = "/var/log/openvpn/openvpn.log"

# Ruta al archivo de status de OpenVPN
DEFAULT_STATUS_PATH = "/var/log/openvpn/openvpn-status.log"

# Host del management interface
DEFAULT_MGMT_HOST = "localhost"

# Puerto del management interface
DEFAULT_MGMT_PORT = 7505

# Ruta a EasyRSA
EASYRSA_PATH = "/etc/openvpn/easy-rsa"
```

### Descripción de Parámetros

#### DEFAULT_LOG_PATH

- **Descripción**: Ubicación del archivo de logs de OpenVPN
- **Valor por defecto**: `/var/log/openvpn/openvpn.log`
- **Alternativas comunes**:
  - `/var/log/openvpn.log`
  - `/var/log/messages` (algunas distribuciones)

#### DEFAULT_STATUS_PATH

- **Descripción**: Archivo donde OpenVPN escribe el estado de conexiones
- **Valor por defecto**: `/var/log/openvpn/openvpn-status.log`
- **Configuración en OpenVPN**: `status /var/log/openvpn/openvpn-status.log 10`

#### DEFAULT_MGMT_HOST

- **Descripción**: Host donde escucha el management interface
- **Valor por defecto**: `localhost`
- **Nota**: Por seguridad, mantener en localhost a menos que sea necesario

#### DEFAULT_MGMT_PORT

- **Descripción**: Puerto del management interface
- **Valor por defecto**: `7505`
- **Rango recomendado**: 7500-7599
- **Configuración en OpenVPN**: `management localhost 7505`

#### EASYRSA_PATH

- **Descripción**: Directorio donde está instalado EasyRSA
- **Valor por defecto**: `/etc/openvpn/easy-rsa`
- **Alternativas comunes**:
  - `/usr/share/easy-rsa`
  - `/etc/easy-rsa`
  - `~/openvpn-ca`

## Configuración de OpenVPN Server

### Archivo de Configuración Recomendado

Ubicación típica: `/etc/openvpn/server.conf`

```conf
# Puerto y protocolo
port 1194
proto udp
dev tun

# Certificados y claves
ca ca.crt
cert server.crt
key server.key
dh dh2048.pem

# Red VPN
server 10.8.0.0 255.255.255.0
ifconfig-pool-persist ipp.txt

# Rutas
push "redirect-gateway def1 bypass-dhcp"
push "dhcp-option DNS 8.8.8.8"
push "dhcp-option DNS 8.8.4.4"

# Seguridad
keepalive 10 120
cipher AES-256-CBC
user nobody
group nogroup
persist-key
persist-tun

# CRL para certificados revocados
crl-verify crl.pem

# Management interface (REQUERIDO para esta aplicación)
management localhost 7505

# Status file (REQUERIDO para esta aplicación)
status /var/log/openvpn/openvpn-status.log 10

# Logs (RECOMENDADO)
log-append /var/log/openvpn/openvpn.log
verb 3
mute 20
```

### Habilitar Management Interface

El management interface permite controlar OpenVPN remotamente:

```conf
# Formato: management [host] [puerto] [password-file]
management localhost 7505

# Opcional: con archivo de contraseña
# management localhost 7505 /etc/openvpn/mgmt-password
```

**Advertencia de Seguridad**:
- Nunca expongas el management interface a internet
- Usa solo localhost o redes internas confiables
- Considera usar un archivo de contraseña

### Configurar Status File

```conf
status /var/log/openvpn/openvpn-status.log 10
```

El número `10` indica que se actualiza cada 10 segundos.

### Configurar Logging

```conf
# Opción 1: Sobrescribir cada vez
log /var/log/openvpn/openvpn.log

# Opción 2: Añadir al archivo existente (RECOMENDADO)
log-append /var/log/openvpn/openvpn.log

# Nivel de verbosidad (0-11)
verb 3

# Suprimir mensajes duplicados
mute 20
```

Niveles de verbosidad:
- `0`: Sin salida excepto errores fatales
- `3`: Nivel normal (recomendado)
- `5`: Más detallado
- `9`: Debug máximo

### Configurar CRL (Certificate Revocation List)

```conf
crl-verify /etc/openvpn/easy-rsa/pki/crl.pem
```

Esto es **esencial** para que las revocaciones funcionen.

## Configuración de EasyRSA

### Ubicación de Archivos

```
EASYRSA_PATH/
├── easyrsa              # Script principal
├── pki/
│   ├── ca.crt          # Certificado CA
│   ├── issued/         # Certificados emitidos
│   │   ├── server.crt
│   │   └── client1.crt
│   ├── private/        # Claves privadas
│   │   ├── ca.key
│   │   ├── server.key
│   │   └── client1.key
│   ├── revoked/        # Certificados revocados
│   ├── crl.pem         # Lista de revocación
│   └── index.txt       # Índice de certificados
└── vars                # Variables de configuración
```

### Archivo vars

Ubicación: `EASYRSA_PATH/vars`

```bash
# Configuración de EasyRSA
set_var EASYRSA_REQ_COUNTRY    "ES"
set_var EASYRSA_REQ_PROVINCE   "Madrid"
set_var EASYRSA_REQ_CITY       "Madrid"
set_var EASYRSA_REQ_ORG        "Tu Organización"
set_var EASYRSA_REQ_EMAIL      "admin@ejemplo.com"
set_var EASYRSA_REQ_OU         "IT"

# Longitud de claves
set_var EASYRSA_KEY_SIZE       2048

# Validez de certificados (en días)
set_var EASYRSA_CA_EXPIRE      3650
set_var EASYRSA_CERT_EXPIRE    1095
```

## Permisos de Archivos

### Logs

```bash
# Crear directorio de logs si no existe
sudo mkdir -p /var/log/openvpn

# Establecer permisos
sudo chown -R root:adm /var/log/openvpn
sudo chmod 750 /var/log/openvpn
```

### Management Socket

Si usas socket Unix en lugar de TCP:

```bash
sudo chmod 660 /var/run/openvpn/management.sock
```

## Configuración Avanzada

### Múltiples Servidores OpenVPN

Si tienes múltiples instancias de OpenVPN, puedes crear perfiles de configuración:

```python
# En futuras versiones
PROFILES = {
    "server1": {
        "MGMT_PORT": 7505,
        "LOG_PATH": "/var/log/openvpn/server1.log",
        "STATUS_PATH": "/var/log/openvpn/server1-status.log"
    },
    "server2": {
        "MGMT_PORT": 7506,
        "LOG_PATH": "/var/log/openvpn/server2.log",
        "STATUS_PATH": "/var/log/openvpn/server2-status.log"
    }
}
```

### Configuración de Red Segura

Para limitar el acceso al management interface:

```bash
# Firewall (iptables)
sudo iptables -A INPUT -p tcp --dport 7505 -i lo -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 7505 -j DROP

# Firewall (ufw)
sudo ufw deny 7505
```

## Variables de Entorno

En futuras versiones, se podrán usar variables de entorno:

```bash
export OVPN_MGMT_PORT=7505
export OVPN_LOG_PATH=/var/log/openvpn/openvpn.log
```

## Verificación de Configuración

### Script de Verificación

```bash
#!/bin/bash

echo "Verificando configuración..."

# Verificar OpenVPN
systemctl is-active openvpn@server && echo "✓ OpenVPN activo" || echo "✗ OpenVPN no activo"

# Verificar management interface
netstat -tlnp | grep 7505 && echo "✓ Management interface escuchando" || echo "✗ Management interface no disponible"

# Verificar logs
test -f /var/log/openvpn/openvpn.log && echo "✓ Log file existe" || echo "✗ Log file no encontrado"

# Verificar EasyRSA
test -f /etc/openvpn/easy-rsa/easyrsa && echo "✓ EasyRSA encontrado" || echo "✗ EasyRSA no encontrado"

echo "Verificación completa"
```

## Solución de Problemas de Configuración

### Management Interface no Responde

```bash
# Verificar que esté configurado
grep "management" /etc/openvpn/server.conf

# Verificar que el puerto esté escuchando
sudo netstat -tlnp | grep 7505

# Probar conexión manual
telnet localhost 7505
```

### CRL No se Actualiza

```bash
# Regenerar CRL
cd /etc/openvpn/easy-rsa
./easyrsa gen-crl

# Copiar a ubicación correcta
sudo cp pki/crl.pem /etc/openvpn/

# Reiniciar OpenVPN
sudo systemctl restart openvpn@server
```

### Permisos Insuficientes

```bash
# Dar permisos temporales (testing)
sudo chmod 644 /var/log/openvpn/openvpn.log

# Añadir usuario al grupo adm (permanente)
sudo usermod -aG adm $USER
```

## Mejores Prácticas

1. **Seguridad**: Nunca expongas el management interface a internet
2. **Logs**: Usa log rotation para evitar archivos enormes
3. **Backups**: Haz backup regular de tu PKI en EasyRSA
4. **Monitoreo**: Revisa los logs regularmente
5. **Actualizaciones**: Mantén OpenVPN y EasyRSA actualizados

## Referencias

- [Documentación OpenVPN](https://openvpn.net/community-resources/reference-manual-for-openvpn-2-4/)
- [Management Interface](https://openvpn.net/community-resources/management-interface/)
- [EasyRSA Documentation](https://easy-rsa.readthedocs.io/)
