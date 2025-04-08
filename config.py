# config.py

# Clave de API de Shodan
SHODAN_API_KEY = 'ylDwTurnigxLMIqvyQELiovHFQNPKkA8'

# País a buscar (ISO 2 letras)
PAIS = 'CO'

# Cantidad máxima de resultados por búsqueda
LIMITE_RESULTADOS = 10

# Query base de búsqueda
QUERY_BASE = f'dns port:53 country:"{PAIS}"'
