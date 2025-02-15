from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
from rich.console import Console
from rich.prompt import Prompt

# Inicializa o console do rich
console = Console()

def buscar_voos_por_pais(estados, pais):
    """
    Filtra os voos pelo país de origem.
    Retorna uma lista de voos que partem do país especificado.
    
    Parâmetros:
    - estados (list): Lista de estados de voo (geralmente retornada pela API OpenSky).
    - pais (str): Nome do país a ser filtrado para verificar de onde os voos estão partindo.
    
    Retorna:
    - list: Lista de voos que partem do país especificado. Se nenhum voo for encontrado, retorna uma lista vazia.
    
    Exemplo:
    >>> buscar_voos_por_pais(voos, "Brasil")
    [{'icao24': 'abc123', 'origem': 'Brasil', ...}]
    """
    # Se a lista de estados estiver vazia, não há voos para filtrar, então retorna uma lista vazia.
    if not estados:
        return []

    # Filtra os estados (voos) onde o valor de 'estado[2]' corresponde ao nome do país.
    voos_filtrados = [estado for estado in estados if estado[2] == pais]

    # Retorna a lista de voos filtrados.
    return voos_filtrados

def buscar_voos_por_horario(estados, horario):
    """
    Filtra os voos com base no horário de partida estimado.
    Retorna uma lista de voos que partem dentro de uma hora do horário especificado.
    
    Parâmetros:
    - estados (list): Lista de estados de voo (geralmente retornada pela API OpenSky).
    - horario (datetime): O horário de partida estimado, usado como base para o filtro.
    
    Retorna:
    - list: Lista de voos que partem dentro de uma hora do horário especificado. Se nenhum voo for encontrado, retorna uma lista vazia.
    
    Exemplo:
    >>> buscar_voos_por_horario(voos, datetime(2025, 2, 14, 15, 0))
    [{'icao24': 'xyz789', 'hora_partida': '2025-02-14 15:30:00', ...}]
    """
    # Se a lista de estados estiver vazia, não há voos para filtrar, então retorna uma lista vazia.
    if not estados:
        return []

    # Inicializa uma lista para armazenar os voos filtrados.
    voos_filtrados = []
    
    # Itera sobre todos os estados (voos) e verifica se o horário de partida está disponível.
    for estado in estados:
        if estado[3]:  # Verifica se o horário de partida (estado[3]) existe.
            # Converte o horário de partida, que está no formato de timestamp, para um objeto datetime.
            hora_partida = datetime.fromtimestamp(estado[3])
            
            # Verifica se o voo está partindo dentro de uma janela de uma hora em relação ao horário fornecido.
            if horario <= hora_partida <= horario + timedelta(hours=1):
                # Se o voo satisfizer a condição, adiciona o voo à lista filtrada.
                voos_filtrados.append(estado)
    
    # Retorna a lista de voos que atendem à condição do horário.
    return voos_filtrados

def obter_endereco(lat, lon):
    """
    Obtém o endereço completo a partir das coordenadas de latitude e longitude.
    
    Parâmetros:
    - lat (float): Latitude das coordenadas.
    - lon (float): Longitude das coordenadas.
    
    Retorna:
    - str: O endereço completo ou uma mensagem de erro caso o endereço não possa ser encontrado.
    """
    # Verifica se as coordenadas são válidas
    if lat is None or lon is None or lat == 0 or lon == 0:
        return "Coordenadas inválidas"

    geolocator = Nominatim(user_agent="meu_app")
    try:
        location = geolocator.reverse((lat, lon), language='pt', timeout=10)
        if location:
            return location.address
        else:
            return "Destino não encontrado"
    except Exception as e:
        console.print(f"[red]⚠️ Erro ao obter endereço: {e} ⚠️[/red]")
        return f"Erro ao obter endereço: {e}"