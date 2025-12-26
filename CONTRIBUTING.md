# Guía de Contribución

¡Gracias por tu interés en contribuir a OpenVPN Manager CLI! Esta guía te ayudará a empezar.

## Código de Conducta

Este proyecto se adhiere a un código de conducta. Al participar, se espera que mantengas un ambiente respetuoso y profesional.

## Cómo Contribuir

### Reportar Bugs

Si encuentras un bug, por favor crea un issue con:

1. **Título descriptivo**: Resume el problema en una línea
2. **Descripción detallada**: Explica qué esperabas vs qué sucedió
3. **Pasos para reproducir**:
   ```
   1. Ejecutar comando X
   2. Seleccionar opción Y
   3. Ver error Z
   ```
4. **Entorno**:
   - SO y versión (ej: Ubuntu 22.04)
   - Versión de Python
   - Versión de OpenVPN
   - Versión de la aplicación
5. **Logs relevantes**: Incluye mensajes de error

### Solicitar Nuevas Características

Para proponer nuevas características:

1. **Verifica** que no exista ya un issue similar
2. **Describe** el caso de uso y el problema que resuelve
3. **Propón** una solución si tienes una idea
4. **Discute** con los mantenedores antes de implementar

### Pull Requests

#### Antes de Empezar

1. **Busca** issues abiertos o crea uno nuevo
2. **Comenta** en el issue que trabajarás en él
3. **Espera** confirmación de un mantenedor

#### Proceso de Desarrollo

1. **Fork** el repositorio
2. **Crea** una rama desde `main`:
   ```bash
   git checkout -b feature/nombre-descriptivo
   ```
3. **Configura** tu entorno:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
4. **Desarrolla** tu característica:
   - Escribe código limpio y documentado
   - Sigue las convenciones de estilo
   - Añade comentarios donde sea necesario
5. **Prueba** tu código:
   ```bash
   # Ejecuta la aplicación
   sudo python3 src/ovpn-manager.py

   # Verifica todas las funcionalidades afectadas
   ```
6. **Commit** tus cambios:
   ```bash
   git add .
   git commit -m "feat: añade funcionalidad X"
   ```
7. **Push** a tu fork:
   ```bash
   git push origin feature/nombre-descriptivo
   ```
8. **Crea** un Pull Request

#### Convenciones de Commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

```
tipo(alcance): descripción corta

[cuerpo opcional]

[footer opcional]
```

**Tipos**:
- `feat`: Nueva característica
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `style`: Formato, puntos y comas faltantes, etc
- `refactor`: Refactorización de código
- `test`: Añadir tests
- `chore`: Tareas de mantenimiento

**Ejemplos**:
```
feat(connections): añade filtro de búsqueda de usuarios
fix(revoke): corrige error al revocar certificados con espacios
docs(readme): actualiza guía de instalación
```

## Guías de Estilo

### Python

Seguimos [PEP 8](https://pep8.org/) con algunas excepciones:

```python
# Bueno ✓
def get_active_connections(host: str, port: int) -> list:
    """
    Obtiene las conexiones activas del servidor OpenVPN.

    Args:
        host: Dirección del management interface
        port: Puerto del management interface

    Returns:
        Lista de diccionarios con datos de conexión
    """
    connections = []
    # Implementación...
    return connections

# Malo ✗
def get_connections(h, p):
    conn = []
    # Sin documentación
    return conn
```

### Documentación

- **Funciones**: Docstrings con descripción, parámetros y retorno
- **Clases**: Docstring describiendo propósito y uso
- **Módulos**: Docstring al inicio del archivo
- **Comentarios**: Explica el "por qué", no el "qué"

```python
# Bueno ✓
# Usamos timeout corto porque el management interface es local
sock.settimeout(5)

# Malo ✗
# Establecer timeout a 5
sock.settimeout(5)
```

### Rich UI

Cuando uses la librería Rich:

```python
# Bueno ✓
console.print("[green]✅ Operación exitosa[/green]")

# Consistencia en iconos
# ✅ - Éxito
# ❌ - Error
# ⚠️  - Advertencia
# ℹ️  - Información
# 🔍 - Buscando
# 📋 - Lista
```

## Estructura del Código

### Organización de Funciones

```python
# 1. Imports
import socket
from rich.console import Console

# 2. Constantes
DEFAULT_PORT = 7505

# 3. Utilidades generales
def format_bytes(b):
    pass

# 4. Funciones de core
def get_connections():
    pass

# 5. Funciones de UI
def show_menu():
    pass

# 6. Main
def main():
    pass

if __name__ == "__main__":
    main()
```

### Manejo de Errores

```python
# Bueno ✓
try:
    result = risky_operation()
except SpecificException as e:
    console.print(f"[red]❌ Error: {e}[/red]")
    console.print("[yellow]💡 Intenta: solución sugerida[/yellow]")
    return None

# Malo ✗
try:
    result = risky_operation()
except:
    print("Error")
```

## Testing

Aunque actualmente no tenemos tests automatizados, por favor prueba manualmente:

### Checklist de Testing

- [ ] Opción 1: Ver logs
  - [ ] Con logs existentes
  - [ ] Sin logs
  - [ ] Seguir logs en tiempo real (Ctrl+C para salir)

- [ ] Opción 2: Ver conexiones
  - [ ] Con conexiones activas
  - [ ] Sin conexiones
  - [ ] Con management interface caído

- [ ] Opción 3: Revocar usuario
  - [ ] Selección por número
  - [ ] Selección por nombre
  - [ ] Cancelar operación
  - [ ] Sin usuarios disponibles

- [ ] Opción 4: Restaurar usuario
  - [ ] Usuario revocado válido
  - [ ] Sin usuarios revocados

- [ ] Opción 5: Desconectar usuario
  - [ ] Usuario conectado
  - [ ] Sin usuarios conectados

- [ ] Opción 6: Estadísticas
  - [ ] Con datos
  - [ ] Sin datos

- [ ] Opción 7: Configuración
  - [ ] Visualización correcta

## Roadmap de Desarrollo

Áreas donde necesitamos ayuda:

### Prioridad Alta
- [ ] Tests unitarios y de integración
- [ ] Validación de configuración al inicio
- [ ] Mejor manejo de errores de conexión

### Prioridad Media
- [ ] Soporte para múltiples servidores
- [ ] Exportación de datos (CSV, JSON)
- [ ] Configuración mediante archivo config

### Prioridad Baja
- [ ] Panel web opcional
- [ ] Notificaciones push
- [ ] Integración con Prometheus/Grafana

## Preguntas Frecuentes

### ¿Cómo pruebo cambios en OpenVPN sin romper mi servidor?

Usa una máquina virtual o contenedor Docker:

```bash
docker run -it --rm --cap-add=NET_ADMIN \
  -v $(pwd):/app \
  ubuntu:22.04 /bin/bash
```

### ¿Necesito saber sobre OpenVPN para contribuir?

No necesariamente. Hay muchas áreas donde puedes ayudar:
- Documentación
- UI/UX mejoras
- Manejo de errores
- Tests
- Traducciones

### ¿Cuánto tiempo tarda en revisarse un PR?

Intentamos revisar PRs en 3-5 días hábiles.

## Recursos Útiles

- [Documentación de Rich](https://rich.readthedocs.io/)
- [OpenVPN Management Interface](https://openvpn.net/community-resources/management-interface/)
- [EasyRSA Docs](https://easy-rsa.readthedocs.io/)
- [PEP 8 Style Guide](https://pep8.org/)

## Contacto

- **Issues**: [GitHub Issues](https://github.com/Electrobridges/OpenVPN-Manager-CLI/issues)
- **Discusiones**: [GitHub Discussions](https://github.com/Electrobridges/OpenVPN-Manager-CLI/discussions)
- **Email**: Contact@Electrobridges.com

## Reconocimientos

Todos los contribuidores serán añadidos a la sección de agradecimientos del README.

¡Gracias por contribuir! 🎉
