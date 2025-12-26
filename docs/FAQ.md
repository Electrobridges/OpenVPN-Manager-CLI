# Preguntas Frecuentes (FAQ)

## General

### ¿Qué es OpenVPN Manager CLI?

OpenVPN Manager CLI es una aplicación de línea de comandos que te permite gestionar tu servidor OpenVPN de manera interactiva, con una interfaz visual moderna usando Rich.

### ¿Es gratuito?

Sí, es completamente gratuito y de código abierto bajo licencia MIT.

### ¿Funciona en Windows?

Actualmente está diseñado para sistemas Linux donde típicamente se ejecutan servidores OpenVPN. Sin embargo, con WSL (Windows Subsystem for Linux) podría funcionar.

## Instalación

### ¿Necesito Python?

Sí, necesitas Python 3.8 o superior.

### ¿Puedo instalar sin sudo?

Puedes instalar las dependencias sin sudo usando un entorno virtual, pero para ejecutar la aplicación necesitarás permisos de root ya que accede a archivos de sistema de OpenVPN.

### ¿Funciona con pip?

En la versión 1.0.0 puedes clonar el repositorio e instalar con `pip install -r requirements.txt`. Una versión en PyPI está planeada.

## Configuración

### ¿Cómo configuro los paths de OpenVPN?

Edita las constantes al inicio del archivo `src/ovpn-manager.py`:

```python
DEFAULT_LOG_PATH = "/var/log/openvpn/openvpn.log"
DEFAULT_STATUS_PATH = "/var/log/openvpn/openvpn-status.log"
DEFAULT_MGMT_PORT = 7505
EASYRSA_PATH = "/etc/openvpn/easy-rsa"
```

### ¿Qué es el management interface?

Es una característica de OpenVPN que permite controlarlo mediante comandos. Añade estas líneas a tu `server.conf`:

```conf
management localhost 7505
```

### ¿Es seguro habilitar el management interface?

Sí, siempre y cuando:
- Solo escuche en localhost (no en 0.0.0.0)
- No expongas el puerto a internet
- Opcionalmente uses un archivo de contraseña

## Uso

### ¿Por qué necesito sudo?

La aplicación necesita:
- Leer logs de OpenVPN
- Acceder a certificados en EasyRSA
- Conectarse al management interface
- Ejecutar comandos easyrsa

### ¿Puedo revocar múltiples usuarios a la vez?

Actualmente no, pero es una característica planeada para futuras versiones.

### ¿Cómo veo logs en tiempo real?

Opción 1 del menú, luego cuando pregunta "¿Seguir logs en tiempo real?" responde "y" (yes).

### ¿Puedo exportar las estadísticas?

No en la versión actual, pero está en el roadmap para futuras versiones (exportar a CSV/JSON).

## Troubleshooting

### Error: "Management interface no disponible"

**Causas comunes**:
1. OpenVPN no está corriendo
2. Management interface no está configurado
3. Puerto incorrecto en la configuración

**Solución**:
```bash
# Verificar que OpenVPN está corriendo
sudo systemctl status openvpn@server

# Verificar configuración
grep "management" /etc/openvpn/server.conf

# Verificar puerto
sudo netstat -tlnp | grep 7505
```

### Error: "No se encontró easy-rsa"

**Solución**:
```bash
# Encontrar easy-rsa
sudo find / -name easyrsa 2>/dev/null

# Actualizar EASYRSA_PATH en el script
```

### Error: "Permission denied"

**Solución**:
```bash
# Ejecutar con sudo
sudo python3 src/ovpn-manager.py

# O dar permisos temporales (para testing)
sudo chmod 644 /var/log/openvpn/*.log
```

### Los certificados revocados siguen conectándose

**Causas**:
1. No regeneraste la CRL
2. OpenVPN no tiene `crl-verify` configurado
3. No reiniciaste OpenVPN

**Solución**:
```bash
# Regenerar CRL
cd /etc/openvpn/easy-rsa
./easyrsa gen-crl

# Copiar CRL
sudo cp pki/crl.pem /etc/openvpn/

# Verificar configuración
grep "crl-verify" /etc/openvpn/server.conf

# Añadir si no existe
echo "crl-verify crl.pem" | sudo tee -a /etc/openvpn/server.conf

# Reiniciar OpenVPN
sudo systemctl restart openvpn@server
```

### Las estadísticas de tráfico muestran 0

El archivo de status se resetea cuando reinicias OpenVPN. Las estadísticas son desde el último reinicio del servicio.

### No veo colores en la terminal

Tu terminal podría no soportar colores ANSI. Intenta:
```bash
export TERM=xterm-256color
```

## Características

### ¿Puedo gestionar múltiples servidores OpenVPN?

No en la versión actual, pero está planeado para v2.0.

### ¿Hay una interfaz web?

No, es puramente CLI. Una interfaz web opcional está en el roadmap.

### ¿Puedo crear nuevos usuarios con esta herramienta?

No en v1.0, solo gestionar existentes (revocar/restaurar). La creación de usuarios requiere generar archivos .ovpn completos, lo cual está planeado para futuras versiones.

### ¿Soporta notificaciones?

No actualmente, pero está en el roadmap (email/Slack/Discord cuando usuarios se conectan/desconectan).

## Desarrollo

### ¿Puedo contribuir?

¡Absolutamente! Lee [CONTRIBUTING.md](../CONTRIBUTING.md) para empezar.

### ¿Cómo reporto un bug?

Abre un issue en GitHub usando la plantilla de bug report.

### ¿Hay tests?

No en v1.0, pero es una prioridad alta para v1.1.

### ¿Qué tecnologías usa?

- Python 3.8+
- [Rich](https://github.com/Textualize/rich) para la UI
- Sockets para comunicación con OpenVPN
- Subprocess para comandos easyrsa

## Seguridad

### ¿Es seguro usar esta aplicación?

Sí, pero recuerda:
- Siempre revisa el código antes de ejecutar con sudo
- No expongas el management interface a internet
- Mantén backups de tu PKI
- Revisa los logs regularmente

### ¿Almacena contraseñas?

No almacena ninguna contraseña. Se comunica con OpenVPN mediante el management interface local.

### ¿Puedo usarlo en producción?

Sí, pero siempre:
- Prueba primero en un entorno de desarrollo
- Mantén backups
- Revisa el código
- Reporta cualquier problema de seguridad responsablemente

### Encontré una vulnerabilidad de seguridad

Por favor NO abras un issue público. Envía un email a [Contact@Electrobridges.com].

## Licencia

### ¿Puedo usar esto comercialmente?

Sí, la licencia MIT permite uso comercial.

### ¿Puedo modificar el código?

Sí, puedes modificarlo libremente. Si haces mejoras, considera contribuir de vuelta.

### ¿Debo dar crédito?

Es apreciado pero no requerido por la licencia MIT.

## Soporte

### ¿Dónde obtengo ayuda?

1. Revisa esta FAQ
2. Lee la [documentación](installation.md)
3. Busca en [issues cerrados](https://github.com/Electrobridges/OpenVPN-Manager-CLI/issues?q=is%3Aissue+is%3Aclosed)
4. Abre un nuevo issue

### ¿Hay un canal de chat?

No actualmente, pero puedes usar GitHub Discussions.

### ¿Ofrecen soporte pagado?

Este es un proyecto de código abierto sin soporte pagado oficial.

---

¿No encontraste tu pregunta? [Abre un issue](https://github.com/Electrobridges/OpenVPN-Manager-CLI/issues/new) o revisa la [documentación completa](installation.md).
