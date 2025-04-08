Auditoría DNS con Shodan
========================

Este proyecto permite auditar servidores DNS expuestos en Internet utilizando la API de Shodan, junto con funcionalidades de resolución de dominios, detección de IPs en lista negra y generación de reportes.

REQUISITOS
----------
- Python 3.8 o superior
- Librerías necesarias:
    Ejecutar: pip install -r requisitos_previos.txt

CONFIGURACIÓN INICIAL
----------------------
1. Abrir el archivo config.py.
2. Reemplazar la clave de API con tu propia API Key de Shodan:
   SHODAN_API_KEY = "TU_API_KEY"
3. Opcional: crear el archivo blacklist.txt con IPs que deseas bloquear (una por línea).

EJECUCIÓN
---------
Ejecutar desde consola:
    python guiAvanzado.py

FUNCIONALIDADES
---------------
- Buscar servidores DNS públicos.
- Verificar si responden correctamente a resoluciones DNS.
- Consultar coincidencias con la lista negra.
- Revisar errores registrados automáticamente.
- Mostrar declaración ética desde la interfaz.

ÉTICA Y USO RESPONSABLE
-----------------------
Este script ha sido desarrollado exclusivamente con fines educativos y defensivos. Hace uso legítimo de la API pública de Shodan para analizar información accesible públicamente en Internet.

No realiza ningún tipo de explotación, intrusión o escaneo no autorizado. El usuario final es responsable del uso que le dé a la herramienta.

Fuente de datos: https://www.shodan.io
