========================
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

PASO A PASO PARA EJECUTAR DESDE CERO
------------------------------------
1. Clonar el repositorio:

   git clone https://github.com/JuanCa1505/ProyectoDNSconIA.git
   cd ProyectoDNSconIA

2. Crear un entorno virtual (opcional pero recomendado):

   python3 -m venv venv
   source venv/bin/activate      (En Windows: venv\Scripts\activate)

3. Instalar las dependencias:

   pip install -r requisitos_previos.txt

4. Configurar la clave de API de Shodan:

   - Editar el archivo config.py
   - Reemplazar: SHODAN_API_KEY = "TU_API_KEY"

5. (Opcional) Crear archivo blacklist.txt con IPs bloqueadas

6. Ejecutar la interfaz gráfica:

   python guiAvanzado.py

7. Usar la herramienta desde la GUI para realizar auditorías, ver resultados, errores y declaración ética.