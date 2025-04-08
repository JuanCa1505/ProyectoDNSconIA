# main.py

import shodan
import socket
from config import SHODAN_API_KEY, QUERY_BASE, LIMITE_RESULTADOS

def buscar_dns_expuestos():
    api = shodan.Shodan(SHODAN_API_KEY)
    resultados_formateados = []

    try:
        resultados = api.search(QUERY_BASE, limit=LIMITE_RESULTADOS)
        print(f"[+] {resultados['total']} resultados encontrados.")

        for result in resultados['matches']:
            ip = result.get('ip_str', 'N/A')
            org = result.get('org', 'Desconocida')
            pais = result.get('location', {}).get('country_name', 'Desconocido')

            resultados_formateados.append((ip, org, pais))

        return resultados_formateados

    except Exception as e:
        print(f"[!] Error al buscar en Shodan: {e}")
        return []

def verificar_resolucion_dns(ip, dominio='www.google.com'):
    try:
        respuesta = socket.gethostbyname_ex(dominio)
        print(f"[+] {ip} resolvió {dominio} a {respuesta[2]}")
        return True, respuesta[2]
    except Exception as e:
        print(f"[!] {ip} no pudo resolver {dominio}: {e}")
        return False, []

if __name__ == "__main__":
    resultados = buscar_dns_expuestos()
    for ip, org, pais in resultados:
        print(f"IP: {ip} | Organización: {org} | País: {pais}")
        verificar_resolucion_dns(ip)
