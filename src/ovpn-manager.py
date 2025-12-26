#!/usr/bin/env python3
"""
OpenVPN Manager CLI
Gestión interactiva de servidor OpenVPN
"""

import socket
import subprocess
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.live import Live
from rich.layout import Layout
from rich import box
import re
import time

console = Console()

# Configuración por defecto (ajustar según tu servidor)
DEFAULT_LOG_PATH = "/var/log/openvpn/openvpn.log"
DEFAULT_STATUS_PATH = "/var/log/openvpn/openvpn-status.log"
DEFAULT_MGMT_HOST = "localhost"
DEFAULT_MGMT_PORT = 7505
EASYRSA_PATH = "/etc/openvpn/easy-rsa"

def clear_screen():
    """Limpia la pantalla"""
    console.clear()

def show_header():
    """Muestra el header de la aplicación"""
    header = Panel(
        "[bold cyan]🔐 OpenVPN Manager[/bold cyan]\n"
        "[dim]Gestión de servidor OpenVPN[/dim]",
        border_style="cyan",
        box=box.DOUBLE
    )
    console.print(header)
    console.print()

def show_menu():
    """Muestra el menú principal"""
    menu = Table(show_header=False, show_edge=False, box=None, padding=(0, 2))
    menu.add_column("Opción", style="cyan bold", width=10)
    menu.add_column("Descripción", style="white")
    
    menu.add_row("1", "📋 Ver logs del servidor")
    menu.add_row("2", "👥 Ver conexiones activas")
    menu.add_row("3", "🚫 Revocar acceso de usuario")
    menu.add_row("4", "✅ Restaurar acceso de usuario")
    menu.add_row("5", "👢 Desconectar usuario activo")
    menu.add_row("6", "📊 Estadísticas generales")
    menu.add_row("7", "⚙️  Configuración")
    menu.add_row("0", "❌ Salir")
    
    console.print(Panel(menu, title="[bold]Menú Principal[/bold]", border_style="blue"))
    console.print()

def read_log_file(log_path: str, lines: int = 50):
    """Lee las últimas líneas del log"""
    try:
        with open(log_path, 'r') as f:
            all_lines = f.readlines()
            return all_lines[-lines:]
    except FileNotFoundError:
        console.print(f"[red]❌ No se encontró el archivo de log: {log_path}[/red]")
        return []
    except PermissionError:
        console.print(f"[red]❌ Sin permisos para leer: {log_path}. Usa sudo.[/red]")
        return []

def get_valid_certificates():
    """Obtiene la lista de certificados válidos"""
    easyrsa_dir = Path(EASYRSA_PATH)
    pki_dir = easyrsa_dir / "pki" / "issued"
    
    if not pki_dir.exists():
        return []
    
    valid_certs = []
    for cert_file in pki_dir.glob("*.crt"):
        cert_name = cert_file.stem
        if cert_name != "server":  # Excluir certificado del servidor
            valid_certs.append(cert_name)
    
    return sorted(valid_certs)

def get_revoked_certificates():
    """Obtiene la lista de certificados revocados"""
    easyrsa_dir = Path(EASYRSA_PATH)
    index_file = easyrsa_dir / "pki" / "index.txt"
    
    if not index_file.exists():
        return []
    
    revoked = []
    try:
        with open(index_file, 'r') as f:
            for line in f:
                if line.startswith('R'):  # R = Revoked
                    parts = line.split('\t')
                    if len(parts) >= 6:
                        # Extraer el nombre del Common Name
                        cn_match = re.search(r'/CN=([^/]+)', parts[5])
                        if cn_match:
                            cert_name = cn_match.group(1)
                            if cert_name != "server":
                                revoked.append(cert_name)
    except Exception as e:
        console.print(f"[yellow]⚠️  Error al leer certificados revocados: {e}[/yellow]")
    
    return sorted(list(set(revoked)))

def select_user_from_list(users, title="Selecciona un usuario"):
    """Permite seleccionar un usuario por número o nombre"""
    if not users:
        return None
    
    table = Table(title=title, box=box.ROUNDED)
    table.add_column("#", style="cyan bold", width=5)
    table.add_column("Usuario", style="white")
    
    for i, user in enumerate(users, 1):
        table.add_row(str(i), user)
    
    table.add_row("[dim]0[/dim]", "[dim]← Volver al menú[/dim]")
    
    console.print(table)
    console.print()
    
    selection = Prompt.ask(
        f"Selecciona por [cyan]número (0-{len(users)})[/cyan] o escribe el [cyan]nombre[/cyan]"
    )
    
    # Validar entrada vacía
    if not selection or selection.strip() == "":
        console.print(f"[red]❌ Debes seleccionar una opción[/red]")
        return None
    
    # Intentar convertir a número
    try:
        num = int(selection)
        if num == 0:
            return "CANCEL"  # Señal para cancelar
        elif 1 <= num <= len(users):
            return users[num - 1]
        else:
            console.print(f"[red]❌ Número fuera de rango[/red]")
            return None
    except ValueError:
        # Es un nombre
        if selection in users:
            return selection
        else:
            # Buscar coincidencia parcial
            matches = [u for u in users if selection.lower() in u.lower()]
            if len(matches) == 1:
                console.print(f"[green]✓ Encontrado: {matches[0]}[/green]")
                return matches[0]
            elif len(matches) > 1:
                console.print(f"[yellow]⚠️  Múltiples coincidencias encontradas:[/yellow]")
                for m in matches:
                    console.print(f"  - {m}")
                return None
            else:
                console.print(f"[red]❌ Usuario '{selection}' no encontrado[/red]")
                return None

def view_logs():
    """Opción 1: Ver logs"""
    clear_screen()
    show_header()
    
    console.print(Panel("[bold]📋 Visualización de Logs[/bold]", border_style="green"))
    console.print()
    
    lines = Prompt.ask("¿Cuántas líneas mostrar?", default="50")
    follow = Confirm.ask("¿Seguir logs en tiempo real?", default=False)
    
    try:
        lines = int(lines)
    except:
        lines = 50
    
    console.print()
    
    if follow:
        console.print("[yellow]📡 Siguiendo logs en tiempo real (Ctrl+C para volver)...[/yellow]\n")
        try:
            subprocess.run(["tail", "-f", "-n", str(lines), DEFAULT_LOG_PATH])
        except KeyboardInterrupt:
            console.print("\n[yellow]✋ Detenido[/yellow]")
    else:
        log_lines = read_log_file(DEFAULT_LOG_PATH, lines)
        
        for line in log_lines:
            line = line.strip()
            if "ERROR" in line or "error" in line:
                console.print(f"[red]{line}[/red]")
            elif "WARNING" in line or "warning" in line:
                console.print(f"[yellow]{line}[/yellow]")
            elif "Connected" in line or "connected" in line:
                console.print(f"[green]{line}[/green]")
            else:
                console.print(line)
    
    console.print()
    Prompt.ask("[dim]Presiona Enter para continuar[/dim]")

def get_active_connections_mgmt(host: str, port: int):
    """Obtiene conexiones usando management interface"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    sock.connect((host, port))
    
    sock.recv(1024)
    sock.send(b"status\n")
    data = sock.recv(8192).decode('utf-8')
    sock.close()
    
    connections = []
    lines = data.split('\n')
    
    for line in lines:
        if line.startswith('CLIENT_LIST'):
            parts = line.split(',')
            if len(parts) >= 5:
                connections.append({
                    'user': parts[1],
                    'real_ip': parts[2],
                    'virtual_ip': parts[3],
                    'bytes_recv': int(parts[4]) if parts[4].isdigit() else 0,
                    'bytes_sent': int(parts[5]) if len(parts) > 5 and parts[5].isdigit() else 0,
                    'connected_since': parts[7] if len(parts) > 7 else 'N/A'
                })
    
    return connections

def parse_status_file(status_path: str):
    """Parse del archivo de status"""
    connections = []
    
    try:
        with open(status_path, 'r') as f:
            lines = f.readlines()
        
        in_client_section = False
        for line in lines:
            line = line.strip()
            
            if line.startswith('Common Name,'):
                in_client_section = True
                continue
            
            if in_client_section and line and not line.startswith('ROUTING'):
                parts = line.split(',')
                if len(parts) >= 4:
                    connections.append({
                        'user': parts[0],
                        'real_ip': parts[1],
                        'bytes_recv': int(parts[2]) if parts[2].isdigit() else 0,
                        'bytes_sent': int(parts[3]) if parts[3].isdigit() else 0,
                        'connected_since': parts[4] if len(parts) > 4 else 'N/A',
                        'virtual_ip': 'N/A'
                    })
            
            if line.startswith('ROUTING'):
                break
    except:
        pass
    
    return connections

def format_bytes(bytes_val):
    """Convierte bytes a formato legible"""
    try:
        b = float(bytes_val)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if b < 1024:
                return f"{b:.2f} {unit}"
            b /= 1024
        return f"{b:.2f} TB"
    except:
        return str(bytes_val)

def view_connections():
    """Opción 2: Ver conexiones activas"""
    clear_screen()
    show_header()
    
    console.print(Panel("[bold]👥 Conexiones Activas[/bold]", border_style="green"))
    console.print()
    
    with console.status("[bold green]🔍 Obteniendo conexiones activas..."):
        connections = []
        try:
            connections = get_active_connections_mgmt(DEFAULT_MGMT_HOST, DEFAULT_MGMT_PORT)
        except Exception as e:
            console.print(f"[yellow]⚠️  Management interface no disponible, usando archivo de status...[/yellow]")
            try:
                connections = parse_status_file(DEFAULT_STATUS_PATH)
            except Exception as e2:
                console.print(f"[red]❌ Error: {e2}[/red]")
    
    console.print()
    
    if not connections:
        console.print("[yellow]ℹ️  No hay conexiones activas[/yellow]")
    else:
        table = Table(title=f"✅ {len(connections)} conexión(es) activa(s)", box=box.ROUNDED)
        
        table.add_column("Usuario", style="cyan bold", no_wrap=True)
        table.add_column("IP Real", style="magenta")
        table.add_column("IP Virtual", style="blue")
        table.add_column("Descarga", style="green", justify="right")
        table.add_column("Subida", style="yellow", justify="right")
        table.add_column("Conectado desde", style="dim")
        
        for conn in connections:
            table.add_row(
                conn['user'],
                conn['real_ip'],
                conn.get('virtual_ip', 'N/A'),
                format_bytes(conn.get('bytes_recv', 0)),
                format_bytes(conn.get('bytes_sent', 0)),
                conn.get('connected_since', 'N/A')
            )
        
        console.print(table)
    
    console.print()
    Prompt.ask("[dim]Presiona Enter para continuar[/dim]")

def revoke_user():
    """Opción 3: Revocar usuario"""
    clear_screen()
    show_header()
    
    console.print(Panel("[bold]🚫 Revocar Acceso de Usuario[/bold]", border_style="red"))
    console.print()
    
    with console.status("[bold yellow]🔍 Obteniendo lista de usuarios..."):
        valid_users = get_valid_certificates()
    
    if not valid_users:
        console.print("[yellow]⚠️  No se encontraron certificados válidos[/yellow]")
        console.print("[dim]Verifica que EASYRSA_PATH esté correctamente configurado[/dim]")
        console.print()
        Prompt.ask("[dim]Presiona Enter para continuar[/dim]")
        return
    
    console.print(f"[green]✓ {len(valid_users)} usuario(s) con acceso activo[/green]\n")
    
    username = select_user_from_list(valid_users, "📋 Usuarios con acceso activo")
    
    if username == "CANCEL":
        console.print("\n[yellow]← Volviendo al menú principal...[/yellow]")
        time.sleep(1)
        return
    
    if not username:
        console.print("\n[red]❌ Selección inválida[/red]")
        Prompt.ask("[dim]Presiona Enter para continuar[/dim]")
        return
    
    console.print()
    confirm = Confirm.ask(f"[bold red]⚠️  ¿Estás seguro de revocar el acceso a '{username}'?[/bold red]")
    
    if not confirm:
        console.print("[yellow]❌ Operación cancelada[/yellow]")
        Prompt.ask("[dim]Presiona Enter para continuar[/dim]")
        return
    
    console.print()
    with console.status(f"[bold yellow]🔒 Revocando certificado de '{username}'..."):
        easyrsa_dir = Path(EASYRSA_PATH)
        if not easyrsa_dir.exists():
            console.print(f"[red]❌ No se encontró easy-rsa en: {EASYRSA_PATH}[/red]")
            console.print("[yellow]💡 Edita EASYRSA_PATH en el script[/yellow]")
            Prompt.ask("[dim]Presiona Enter para continuar[/dim]")
            return
        
        try:
            result = subprocess.run(
                ["./easyrsa", "revoke", username],
                cwd=easyrsa_dir,
                capture_output=True,
                text=True,
                input="yes\n"
            )
            
            if result.returncode == 0:
                console.print(f"[green]✅ Certificado de '{username}' revocado[/green]")
                
                console.print("\n[yellow]📝 Generando nueva CRL...[/yellow]")
                crl_result = subprocess.run(
                    ["./easyrsa", "gen-crl"],
                    cwd=easyrsa_dir,
                    capture_output=True,
                    text=True
                )
                
                if crl_result.returncode == 0:
                    console.print("[green]✅ CRL actualizada[/green]")
                    console.print("\n[yellow]⚠️  Recuerda reiniciar el servicio OpenVPN:[/yellow]")
                    console.print("[cyan]   sudo systemctl restart openvpn@server[/cyan]")
                else:
                    console.print(f"[red]⚠️  Error al generar CRL: {crl_result.stderr}[/red]")
            else:
                console.print(f"[red]❌ Error al revocar: {result.stderr}[/red]")
                
        except Exception as e:
            console.print(f"[red]❌ Error: {e}[/red]")
    
    console.print()
    Prompt.ask("[dim]Presiona Enter para continuar[/dim]")

def restore_user():
    """Opción 4: Restaurar acceso de usuario"""
    clear_screen()
    show_header()
    
    console.print(Panel("[bold]✅ Restaurar Acceso de Usuario[/bold]", border_style="green"))
    console.print()
    
    with console.status("[bold yellow]🔍 Obteniendo lista de usuarios revocados..."):
        revoked_users = get_revoked_certificates()
    
    if not revoked_users:
        console.print("[yellow]ℹ️  No hay usuarios revocados[/yellow]")
        console.print()
        Prompt.ask("[dim]Presiona Enter para continuar[/dim]")
        return
    
    console.print(f"[yellow]⚠️  {len(revoked_users)} usuario(s) revocado(s)[/yellow]\n")
    
    username = select_user_from_list(revoked_users, "📋 Usuarios revocados")
    
    if username == "CANCEL":
        console.print("\n[yellow]← Volviendo al menú principal...[/yellow]")
        time.sleep(1)
        return
    
    if not username:
        console.print("\n[red]❌ Selección inválida[/red]")
        Prompt.ask("[dim]Presiona Enter para continuar[/dim]")
        return
    
    console.print()
    console.print(f"[bold yellow]⚠️  IMPORTANTE:[/bold yellow]")
    console.print("Para restaurar el acceso, necesitas:")
    console.print("1. Eliminar el certificado revocado")
    console.print("2. Generar un nuevo certificado con el mismo nombre")
    console.print()
    
    confirm = Confirm.ask(f"[bold green]¿Generar nuevo certificado para '{username}'?[/bold green]")
    
    if not confirm:
        console.print("[yellow]❌ Operación cancelada[/yellow]")
        Prompt.ask("[dim]Presiona Enter para continuar[/dim]")
        return
    
    console.print()
    with console.status(f"[bold yellow]🔓 Restaurando acceso de '{username}'..."):
        easyrsa_dir = Path(EASYRSA_PATH)
        
        try:
            # Remover del índice (esto permite regenerar el certificado)
            index_file = easyrsa_dir / "pki" / "index.txt"
            if index_file.exists():
                with open(index_file, 'r') as f:
                    lines = f.readlines()
                
                with open(index_file, 'w') as f:
                    for line in lines:
                        if f'/CN={username}' not in line:
                            f.write(line)
                
                console.print(f"[green]✓ Entrada eliminada del índice[/green]")
            
            # Generar nuevo certificado sin contraseña
            result = subprocess.run(
                ["./easyrsa", "build-client-full", username, "nopass"],
                cwd=easyrsa_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                console.print(f"[green]✅ Nuevo certificado generado para '{username}'[/green]")
                
                # Regenerar CRL
                console.print("\n[yellow]📝 Actualizando CRL...[/yellow]")
                crl_result = subprocess.run(
                    ["./easyrsa", "gen-crl"],
                    cwd=easyrsa_dir,
                    capture_output=True,
                    text=True
                )
                
                if crl_result.returncode == 0:
                    console.print("[green]✅ CRL actualizada[/green]")
                    console.print(f"\n[green]🎉 Acceso restaurado para '{username}'[/green]")
                    console.print("\n[cyan]📁 Archivos generados:[/cyan]")
                    console.print(f"   Certificado: {easyrsa_dir}/pki/issued/{username}.crt")
                    console.print(f"   Llave: {easyrsa_dir}/pki/private/{username}.key")
                    console.print("\n[yellow]⚠️  Recuerda reiniciar el servicio OpenVPN:[/yellow]")
                    console.print("[cyan]   sudo systemctl restart openvpn@server[/cyan]")
                else:
                    console.print(f"[red]⚠️  Error al generar CRL: {crl_result.stderr}[/red]")
            else:
                console.print(f"[red]❌ Error al generar certificado: {result.stderr}[/red]")
                
        except Exception as e:
            console.print(f"[red]❌ Error: {e}[/red]")
    
    console.print()
    Prompt.ask("[dim]Presiona Enter para continuar[/dim]")

def kick_user():
    """Opción 5: Desconectar usuario"""
    clear_screen()
    show_header()
    
    console.print(Panel("[bold]👢 Desconectar Usuario Activo[/bold]", border_style="yellow"))
    console.print()
    
    # Obtener usuarios conectados
    with console.status("[bold yellow]🔍 Obteniendo usuarios conectados..."):
        try:
            connections = get_active_connections_mgmt(DEFAULT_MGMT_HOST, DEFAULT_MGMT_PORT)
        except:
            try:
                connections = parse_status_file(DEFAULT_STATUS_PATH)
            except:
                connections = []
    
    if not connections:
        console.print("[yellow]ℹ️  No hay usuarios conectados actualmente[/yellow]")
        console.print()
        Prompt.ask("[dim]Presiona Enter para continuar[/dim]")
        return
    
    console.print(f"[green]✓ {len(connections)} usuario(s) conectado(s)[/green]\n")
    
    connected_users = [conn['user'] for conn in connections]
    username = select_user_from_list(connected_users, "📋 Usuarios conectados")
    
    if username == "CANCEL":
        console.print("\n[yellow]← Volviendo al menú principal...[/yellow]")
        time.sleep(1)
        return
    
    if not username:
        console.print("\n[red]❌ Selección inválida[/red]")
        Prompt.ask("[dim]Presiona Enter para continuar[/dim]")
        return
    
    console.print()
    with console.status(f"[bold yellow]👢 Desconectando a '{username}'..."):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((DEFAULT_MGMT_HOST, DEFAULT_MGMT_PORT))
            
            sock.recv(1024)
            command = f"kill {username}\n"
            sock.send(command.encode())
            response = sock.recv(1024).decode('utf-8')
            sock.close()
            
            if "SUCCESS" in response:
                console.print(f"[green]✅ Usuario '{username}' desconectado[/green]")
            else:
                console.print(f"[yellow]⚠️  Respuesta: {response}[/yellow]")
                
        except Exception as e:
            console.print(f"[red]❌ Error: {e}[/red]")
            console.print("[yellow]💡 Asegúrate de que el management interface esté habilitado[/yellow]")
    
    console.print()
    Prompt.ask("[dim]Presiona Enter para continuar[/dim]")

def show_stats():
    """Opción 6: Estadísticas"""
    clear_screen()
    show_header()
    
    console.print(Panel("[bold]📊 Estadísticas Generales[/bold]", border_style="green"))
    console.print()
    
    with console.status("[bold green]📊 Calculando estadísticas..."):
        try:
            connections = get_active_connections_mgmt(DEFAULT_MGMT_HOST, DEFAULT_MGMT_PORT)
        except:
            try:
                connections = parse_status_file(DEFAULT_STATUS_PATH)
            except:
                connections = []
        
        valid_users = get_valid_certificates()
        revoked_users = get_revoked_certificates()
        
        total_users = len(connections)
        total_recv = sum(conn.get('bytes_recv', 0) for conn in connections)
        total_sent = sum(conn.get('bytes_sent', 0) for conn in connections)
        total_traffic = total_recv + total_sent
    
    stats_table = Table(box=box.SIMPLE, show_header=False)
    stats_table.add_column("Métrica", style="cyan bold")
    stats_table.add_column("Valor", style="green bold")
    
    stats_table.add_row("👥 Usuarios conectados", str(total_users))
    stats_table.add_row("✅ Certificados activos", str(len(valid_users)))
    stats_table.add_row("🚫 Certificados revocados", str(len(revoked_users)))
    stats_table.add_row("📥 Tráfico descargado", format_bytes(total_recv))
    stats_table.add_row("📤 Tráfico subido", format_bytes(total_sent))
    stats_table.add_row("📊 Tráfico total", format_bytes(total_traffic))
    
    console.print(stats_table)
    
    if connections:
        console.print("\n[bold cyan]Top usuarios por tráfico:[/bold cyan]\n")
        
        sorted_conns = sorted(connections, 
                            key=lambda x: x.get('bytes_recv', 0) + x.get('bytes_sent', 0), 
                            reverse=True)[:5]
        
        top_table = Table(box=box.ROUNDED)
        top_table.add_column("#", style="dim", width=3)
        top_table.add_column("Usuario", style="cyan bold")
        top_table.add_column("Tráfico Total", style="green", justify="right")
        
        for i, conn in enumerate(sorted_conns, 1):
            total = conn.get('bytes_recv', 0) + conn.get('bytes_sent', 0)
            top_table.add_row(str(i), conn['user'], format_bytes(total))
        
        console.print(top_table)
    
    console.print()
    Prompt.ask("[dim]Presiona Enter para continuar[/dim]")

def show_config():
    """Opción 7: Configuración"""
    clear_screen()
    show_header()
    
    console.print(Panel("[bold]⚙️  Configuración Actual[/bold]", border_style="blue"))
    console.print()
    
    config_table = Table(box=box.SIMPLE, show_header=False)
    config_table.add_column("Parámetro", style="cyan bold")
    config_table.add_column("Valor", style="white")
    
    config_table.add_row("📋 Log path", DEFAULT_LOG_PATH)
    config_table.add_row("📊 Status path", DEFAULT_STATUS_PATH)
    config_table.add_row("🔌 Management host", DEFAULT_MGMT_HOST)
    config_table.add_row("🔌 Management port", str(DEFAULT_MGMT_PORT))
    config_table.add_row("🔐 Easy-RSA path", EASYRSA_PATH)
    
    console.print(config_table)
    
    console.print("\n[yellow]💡 Para cambiar estos valores, edita las constantes al inicio del script[/yellow]")
    
    console.print()
    Prompt.ask("[dim]Presiona Enter para continuar[/dim]")

def main():
    """Función principal con menú interactivo"""
    while True:
        clear_screen()
        show_header()
        show_menu()
        
        choice = Prompt.ask("Selecciona una opción", choices=["0", "1", "2", "3", "4", "5", "6", "7"], default="0")
        
        if choice == "0":
            console.print("\n[yellow]👋 ¡Hasta luego![/yellow]\n")
            break
        elif choice == "1":
            view_logs()
        elif choice == "2":
            view_connections()
        elif choice == "3":
            revoke_user()
        elif choice == "4":
            restore_user()
        elif choice == "5":
            kick_user()
        elif choice == "6":
            show_stats()
        elif choice == "7":
            show_config()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]👋 Interrumpido por el usuario. ¡Hasta luego![/yellow]\n")
    except Exception as e:
        console.print(f"\n[red]❌ Error inesperado: {e}[/red]\n")