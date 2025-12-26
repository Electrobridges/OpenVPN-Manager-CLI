# OpenVPN Manager CLI

Una aplicación CLI moderna e interactiva para gestionar servidores OpenVPN con una interfaz visual elegante.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)

## Características

- **Gestión de Conexiones**: Visualiza usuarios conectados en tiempo real con estadísticas de tráfico
- **Administración de Certificados**: Revoca y restaura certificados de usuario fácilmente
- **Visualización de Logs**: Monitorea logs del servidor en tiempo real o históricos
- **Desconexión de Usuarios**: Desconecta usuarios activos desde la interfaz
- **Estadísticas Detalladas**: Visualiza métricas de uso y tráfico de red
- **Interfaz Moderna**: UI basada en Rich con tablas, paneles y colores

## Capturas de Pantalla

### Menú Principal
![Menú Principal](screenshots/Screenshot%202025-12-26%20215936.png)

## Requisitos Previos

- Python 3.8 o superior
- Servidor OpenVPN configurado y funcionando
- EasyRSA para gestión de certificados
- Acceso root o sudo en el servidor

## Instalación

### Instalación Rápida

```bash
# Clonar el repositorio
git clone https://github.com/Electrobridges/OpenVPN-Manager-CLI.git
cd OpenVPN-Manager-CLI

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
sudo python src/ovpn-manager.py
```

### Instalación desde pip (próximamente)

```bash
pip install openvpn-manager-cli
```

## Configuración

Antes de usar la aplicación, edita las constantes al inicio del archivo `src/ovpn-manager.py`:

```python
DEFAULT_LOG_PATH = "/var/log/openvpn/openvpn.log"
DEFAULT_STATUS_PATH = "/var/log/openvpn/openvpn-status.log"
DEFAULT_MGMT_HOST = "localhost"
DEFAULT_MGMT_PORT = 7505
EASYRSA_PATH = "/etc/openvpn/easy-rsa"
```

### Habilitar Management Interface

Asegúrate de que tu configuración de OpenVPN incluya:

```conf
management localhost 7505
status /var/log/openvpn/openvpn-status.log 10
```

## Uso

### Ejecutar la aplicación

```bash
sudo python src/ovpn-manager.py
```

### Menú Principal

1. **Ver logs del servidor** - Visualiza logs históricos o en tiempo real
2. **Ver conexiones activas** - Lista usuarios conectados con estadísticas
3. **Revocar acceso de usuario** - Revoca certificados de cliente
4. **Restaurar acceso de usuario** - Regenera certificados revocados
5. **Desconectar usuario activo** - Expulsa usuarios conectados
6. **Estadísticas generales** - Métricas y top usuarios por tráfico
7. **Configuración** - Visualiza configuración actual

### Ejemplos de Uso

#### Ver conexiones activas
```bash
# Opción 2 en el menú
# Muestra tabla con:
# - Nombre de usuario
# - IP real del cliente
# - IP virtual asignada
# - Tráfico de descarga/subida
# - Tiempo de conexión
```

#### Revocar un certificado
```bash
# Opción 3 en el menú
# 1. Selecciona usuario de la lista
# 2. Confirma la revocación
# 3. Reinicia OpenVPN: sudo systemctl restart openvpn@server
```

## Estructura del Proyecto

```
OpenVPN-Manager-CLI/
├── src/
│   └── ovpn-manager.py      # Aplicación principal
├── docs/
│   ├── installation.md      # Guía de instalación detallada
│   └── configuration.md     # Guía de configuración
├── screenshots/             # Capturas de pantalla
├── tests/                   # Tests (próximamente)
├── README.md               # Este archivo
├── requirements.txt        # Dependencias Python
├── setup.py               # Instalación con pip
├── LICENSE                # Licencia MIT
└── .gitignore            # Archivos ignorados por git
```

## Dependencias

- [rich](https://github.com/Textualize/rich) - Terminal UI con formato avanzado
- Python standard library (socket, subprocess, pathlib, etc.)

## Permisos Requeridos

La aplicación requiere permisos elevados (root/sudo) para:
- Leer logs de OpenVPN
- Acceder a certificados en EasyRSA
- Conectarse al management interface
- Ejecutar comandos de revocación/generación de certificados

## Solución de Problemas

### Error: "Management interface no disponible"

Verifica que:
1. OpenVPN esté configurado con `management localhost 7505`
2. El puerto sea accesible: `netstat -tlnp | grep 7505`
3. No haya firewall bloqueando el puerto

### Error: "No se encontró easy-rsa"

Actualiza la ruta de EasyRSA en la configuración:
```python
EASYRSA_PATH = "/ruta/a/tu/easy-rsa"
```

### Error: "Sin permisos para leer logs"

Ejecuta con sudo:
```bash
sudo python src/ovpn-manager.py
```

## Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Añade nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

Lee [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles.

## Roadmap

- [ ] Tests unitarios
- [ ] Soporte para múltiples servidores
- [ ] Exportación de estadísticas a CSV/JSON
- [ ] Panel web opcional
- [ ] Notificaciones de eventos
- [ ] Integración con sistemas de monitoring

## Seguridad

Si encuentras una vulnerabilidad de seguridad, por favor NO abras un issue público. Envía un email a [Contact@Electrobridges.com].

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## Autor

**Daniel Puentes** - [GitHub](https://github.com/Electrobridges)

## Agradecimientos

- [Rich](https://github.com/Textualize/rich) - Por la increíble librería de terminal UI
- Comunidad OpenVPN
- Todos los contribuidores

## Enlaces

- [Documentación de OpenVPN](https://openvpn.net/community-resources/)
- [EasyRSA en GitHub](https://github.com/OpenVPN/easy-rsa)
- [Reportar un Bug](https://github.com/Electrobridges/OpenVPN-Manager-CLI/issues)

---

Hecho con ❤️ para la comunidad OpenVPN
