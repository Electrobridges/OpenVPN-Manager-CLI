# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [No Publicado]

### Planeado
- Tests unitarios
- Soporte para múltiples servidores
- Exportación de datos a CSV/JSON
- Panel web opcional
- Sistema de notificaciones

## [1.0.0] - 2025-12-23

### Añadido
- Visualización de logs del servidor OpenVPN
  - Modo histórico con número configurable de líneas
  - Modo tiempo real (tail -f)
  - Colores según tipo de mensaje (error, warning, info)
- Gestión de conexiones activas
  - Listado de usuarios conectados
  - Estadísticas de tráfico (descarga/subida)
  - Información de IP real y virtual
  - Tiempo de conexión
- Administración de certificados
  - Revocación de acceso de usuarios
  - Restauración de acceso (regeneración de certificados)
  - Lista de certificados válidos y revocados
- Funcionalidades de gestión
  - Desconexión forzada de usuarios activos
  - Estadísticas generales del servidor
  - Top usuarios por tráfico
  - Visualización de configuración
- Interfaz de usuario
  - Menú interactivo con Rich
  - Tablas formateadas con estadísticas
  - Paneles con información clara
  - Selección de usuarios por número o nombre
  - Confirmaciones para operaciones críticas
- Documentación completa
  - README detallado con ejemplos
  - Guía de instalación paso a paso
  - Guía de configuración avanzada
  - Guía de contribución
  - Licencia MIT

### Características Técnicas
- Comunicación con OpenVPN Management Interface
- Parsing de archivos de status y logs
- Integración con EasyRSA para gestión de certificados
- Manejo robusto de errores
- Soporte para Python 3.8+

## Tipos de Cambios

- `Añadido` para nuevas características
- `Cambiado` para cambios en funcionalidades existentes
- `Obsoleto` para características que serán removidas
- `Removido` para características removidas
- `Corregido` para corrección de bugs
- `Seguridad` para vulnerabilidades

## Versionado

- **MAJOR** (1.x.x): Cambios incompatibles con versiones anteriores
- **MINOR** (x.1.x): Nueva funcionalidad compatible con versiones anteriores
- **PATCH** (x.x.1): Corrección de bugs compatible con versiones anteriores

---

[No Publicado]: https://github.com/Electrobridges/OpenVPN-Manager-CLI/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Electrobridges/OpenVPN-Manager-CLI/releases/tag/v1.0.0
