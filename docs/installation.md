# Guía de Instalación

Esta guía te ayudará a instalar y configurar OpenVPN Manager CLI en tu servidor.

## Requisitos del Sistema

### Software Requerido

- **Sistema Operativo**: Linux (Ubuntu 20.04+, Debian 10+, CentOS 8+, o similar)
- **Python**: 3.8 o superior
- **OpenVPN**: 2.4 o superior
- **EasyRSA**: 3.0 o superior

### Permisos

- Acceso root o sudo
- Permisos para ejecutar comandos de OpenVPN
- Acceso a los archivos de configuración de OpenVPN

## Paso 1: Verificar Requisitos Previos

```bash
# Verificar versión de Python
python3 --version

# Verificar OpenVPN
openvpn --version

# Verificar ubicación de EasyRSA
which easyrsa
```

## Paso 2: Instalar Python y Pip

### Ubuntu/Debian

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### CentOS/RHEL

```bash
sudo yum install python3 python3-pip
```

## Paso 3: Clonar el Repositorio

```bash
cd /opt
sudo git clone https://github.com/Electrobridges/OpenVPN-Manager-CLI.git
cd OpenVPN-Manager-CLI
```

## Paso 4: Crear Entorno Virtual (Recomendado)

```bash
python3 -m venv venv
source venv/bin/activate
```

## Paso 5: Instalar Dependencias

```bash
pip install -r requirements.txt
```

## Paso 6: Configurar OpenVPN Management Interface

Edita tu archivo de configuración de OpenVPN:

```bash
sudo nano /etc/openvpn/server.conf
```

Añade o verifica estas líneas:

```conf
# Management interface
management localhost 7505

# Status file
status /var/log/openvpn/openvpn-status.log 10

# Log file
log-append /var/log/openvpn/openvpn.log
verb 3
```

Reinicia OpenVPN:

```bash
sudo systemctl restart openvpn@server
```

## Paso 7: Configurar la Aplicación

Edita el archivo `src/ovpn-manager.py` y ajusta las constantes según tu configuración:

```python
DEFAULT_LOG_PATH = "/var/log/openvpn/openvpn.log"
DEFAULT_STATUS_PATH = "/var/log/openvpn/openvpn-status.log"
DEFAULT_MGMT_HOST = "localhost"
DEFAULT_MGMT_PORT = 7505
EASYRSA_PATH = "/etc/openvpn/easy-rsa"
```

## Paso 8: Verificar Instalación

```bash
sudo python3 src/ovpn-manager.py
```

Si todo está configurado correctamente, deberías ver el menú principal.

## Instalación Alternativa con setup.py

```bash
# Desde el directorio del proyecto
sudo python3 setup.py install
```

## Crear Alias para Ejecución Rápida

Añade al final de tu `~/.bashrc` o `~/.zshrc`:

```bash
alias ovpn-manager='sudo python3 /opt/OpenVPN-Manager-CLI/src/ovpn-manager.py'
```

Luego:

```bash
source ~/.bashrc
```

Ahora puedes ejecutar simplemente:

```bash
ovpn-manager
```

## Solución de Problemas Comunes

### Error: "ModuleNotFoundError: No module named 'rich'"

```bash
pip install rich
```

### Error: "Permission denied" al leer logs

Ejecuta con sudo:

```bash
sudo python3 src/ovpn-manager.py
```

### Error: "Management interface no disponible"

Verifica que OpenVPN esté corriendo:

```bash
sudo systemctl status openvpn@server
```

Verifica que el puerto esté escuchando:

```bash
sudo netstat -tlnp | grep 7505
```

### Error: "No se encontró easy-rsa"

Instala EasyRSA:

```bash
# Ubuntu/Debian
sudo apt install easy-rsa

# CentOS/RHEL
sudo yum install easy-rsa
```

Verifica la ubicación:

```bash
find /etc /usr -name easyrsa 2>/dev/null
```

## Actualización

```bash
cd /opt/OpenVPN-Manager-CLI
git pull
pip install -r requirements.txt --upgrade
```

## Desinstalación

```bash
# Si instalaste con setup.py
sudo pip uninstall openvpn-manager-cli

# Eliminar directorio
sudo rm -rf /opt/OpenVPN-Manager-CLI
```

## Próximos Pasos

- Lee la [Guía de Configuración](configuration.md)
- Revisa el [README](../README.md) para ejemplos de uso
- Consulta [CONTRIBUTING.md](../CONTRIBUTING.md) si quieres contribuir
