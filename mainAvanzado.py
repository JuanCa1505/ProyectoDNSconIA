import shodan
import dns.resolver
from config import SHODAN_API_KEY, QUERY_BASE

# Iniciar cliente de Shodan
api = shodan.Shodan(SHODAN_API_KEY)

# Cargar blacklist desde archivo
def cargar_blacklist(ruta="blacklist.txt"):
    try:
        with open(ruta, "r") as f:
            return set(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        return set()

BLACKLIST = cargar_blacklist()

# Lista de IPs detectadas en blacklist durante ejecución
ips_en_blacklist = []

# Lista de errores encontrados
errores_encontrados = []

def buscar_dns_expuestos(query=QUERY_BASE, pagina=1):
    """
    Realiza búsqueda en Shodan por página (paginación).
    Filtra IPs que estén en blacklist y guarda coincidencias.
    """
    resultados_formateados = []
    try:
        resultados = api.search(query, page=pagina)
        for servicio in resultados['matches']:
            ip = servicio['ip_str']
            org = servicio.get('org', 'Desconocida')
            pais = servicio.get('location', {}).get('country_name', 'Desconocido')
            if ip in BLACKLIST:
                ips_en_blacklist.append(ip)
                continue
            resultados_formateados.append((ip, org, pais))
    except shodan.APIError as e:
        error_msg = f"[Shodan API] Error al buscar DNS expuestos: {e}"
        errores_encontrados.append(error_msg)
        resultados_formateados.append((error_msg, "", ""))

    guardar_ips_en_blacklist()
    guardar_errores()
    return resultados_formateados

def guardar_ips_en_blacklist(ruta="coincidencias_blacklist.txt"):
    if not ips_en_blacklist:
        return
    try:
        with open(ruta, "w") as f:
            f.write("IPs encontradas en la blacklist:\n")
            for ip in ips_en_blacklist:
                f.write(ip + "\n")
    except Exception as e:
        errores_encontrados.append(f"[Archivo] No se pudo guardar la blacklist: {e}")

def guardar_errores(ruta="errores_detectados.txt"):
    if not errores_encontrados:
        return
    try:
        with open(ruta, "w") as f:
            f.write("Registro de errores durante la ejecución:\n\n")
            for err in errores_encontrados:
                f.write(f"- {err}\n")
    except Exception as e:
        print(f"[!] Error al guardar el archivo de errores: {e}")

def verificar_ip(ip):
    try:
        info = api.host(ip)
        for servicio in info['data']:
            if servicio['port'] == 53:
                return f"✔️ La IP {ip} tiene el puerto 53 ({servicio['transport']}) abierto."
        return f"❌ La IP {ip} no tiene el puerto 53 abierto."
    except shodan.APIError as e:
        error_msg = f"[Shodan API] Error al consultar IP {ip}: {e}"
        errores_encontrados.append(error_msg)
        guardar_errores()
        return f"❌ {error_msg}"

def resolver_con_ip(personal_dns_ip, dominios="www.google.com"):
    """
    Recibe una IP y una cadena con múltiples dominios separados por coma.
    Intenta resolver cada uno desde esa IP.
    """
    resultados = []
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [personal_dns_ip]
    resolver.timeout = 2
    resolver.lifetime = 3

    for dominio in [d.strip() for d in dominios.split(",") if d.strip()]:
        try:
            respuesta = resolver.resolve(dominio, 'A')
            ips_resueltas = [r.address for r in respuesta]
            resultados.append(f"✔️ {dominio} → {', '.join(ips_resueltas)}")
        except dns.resolver.NXDOMAIN:
            resultados.append(f"❌ {dominio}: No existe (NXDOMAIN).")
        except dns.resolver.Timeout:
            resultados.append(f"❌ {dominio}: Tiempo de espera agotado.")
        except dns.resolver.NoNameservers:
            resultados.append(f"❌ {dominio}: No hay servidores válidos.")
        except Exception as e:
            error_msg = f"[DNS Resolver] {dominio}: {str(e)}"
            errores_encontrados.append(error_msg)
            resultados.append(f"❌ {dominio}: Error → {str(e)}")

    guardar_errores()
    return "\n".join(resultados)
