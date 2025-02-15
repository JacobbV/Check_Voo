import requests
from datetime import datetime
from rich.console import Console
import logging
import os
from dotenv import load_dotenv
from pathlib import Path
import time
import folium
from folium import plugins
from geopy.geocoders import Nominatim
import webbrowser
import geocoder

# Inicializa o console do rich
console = Console()

# Caminho absoluto para o diretório de logs
log_dir = os.path.join(os.path.dirname(__file__), "../logs")
os.makedirs(log_dir, exist_ok=True)  # Garante que o diretório logs exista

# Configura o logging com o caminho absoluto
logging.basicConfig(
    filename=os.path.join(log_dir, "erros.log"),
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Caminho para o arquivo .env na raiz do projeto
env_path = Path(__file__).resolve().parent.parent / '.env'

# Verifica se o arquivo .env existe
if not env_path.exists():
    raise FileNotFoundError(f"O arquivo .env não foi encontrado no caminho {env_path}.")

# Carregar o arquivo .env
try:
    load_dotenv(dotenv_path=env_path)
    console.log("[bold green]Arquivo .env carregado com sucesso.[/bold green]")
except Exception as e:
    raise RuntimeError(f"Erro ao carregar o arquivo .env: {e}")

# Configurações da OpenSky API
OPENSKY_HISTORICAL_URL = os.getenv("OPENSKY_HISTORICAL_URL", "https://opensky-network.org/api/flights/{type}?begin={start}&end={end}")
OPENSKY_API_URL = os.getenv("OPENSKY_API_URL", "https://opensky-network.org/api/states/all")
OPENSKY_USERNAME = os.getenv("OPENSKY_USERNAME")
OPENSKY_PASSWORD = os.getenv("OPENSKY_PASSWORD")

# Configurações da ADS-B Exchange API
ADSBEXCHANGE_API_URL = os.getenv("ADSBEXCHANGE_API_URL", "https://adsbexchange.com/api/aircraft")
ADSBEXCHANGE_API_KEY = os.getenv("ADSBEXCHANGE_API_KEY")
ADSBEXCHANGE_HEADERS = {"api-auth": ADSBEXCHANGE_API_KEY}

# Valida as credenciais da OpenSky
if not OPENSKY_USERNAME or not OPENSKY_PASSWORD:
    raise ValueError("Credenciais da OpenSky não encontradas no arquivo .env. Verifique o arquivo .env.")

# Valida a chave da API ADS-B Exchange
if not ADSBEXCHANGE_API_KEY:
    raise ValueError("Chave da API ADS-B Exchange não encontrada no arquivo .env. Verifique o arquivo .env.")

console.log("[bold green]Credenciais carregadas com sucesso.[/bold green]")

def buscar_voos_historicos(tipo, inicio_timestamp, fim_timestamp):
    """
    Busca voos históricos (chegadas ou partidas) dentro de um intervalo de tempo.

    Args:
        tipo (str): Tipo de voo ("arrival" ou "departure").
        inicio_timestamp (int): Timestamp de início do intervalo.
        fim_timestamp (int): Timestamp de fim do intervalo.

    Returns:
        list: Lista de voos históricos ou None em caso de erro.
    """
    try:
        url = OPENSKY_HISTORICAL_URL.format(type=tipo, start=inicio_timestamp, end=fim_timestamp)
        response = requests.get(url, auth=(OPENSKY_USERNAME, OPENSKY_PASSWORD), timeout=10)
        
        if response.status_code == 400:
            console.print("[red]⚠️ Erro 400: Verifique o intervalo de tempo. ⚠️[/red]")
            return None
        response.raise_for_status()

        data = response.json()
        if not isinstance(data, list):
            console.print("[red]⚠️ Resposta da API inválida. ⚠️[/red]")
            return None

        return data
    except requests.exceptions.RequestException as e:
        console.print(f"[red]⚠️ Erro ao buscar voos históricos: {e} ⚠️[/red]")
        logging.error(f"Erro ao buscar voos históricos: {e}")
        return None

def buscar_estados_opensky(timeout=30):
    """
    Busca os estados atuais dos voos usando a OpenSky API.

    Returns:
        list: Lista de estados (voos) ou None em caso de erro.
    """
    try:
        console.print("[yellow]Buscando dados da OpenSky API...[/yellow]")
        response = requests.get(OPENSKY_API_URL, timeout=timeout)
        response.raise_for_status()
        data = response.json()

        if not isinstance(data, dict) or "states" not in data:
            console.print("[red]⚠️ Resposta da API inválida ou sem dados. ⚠️[/red]")
            return None

        return data.get("states", [])
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Erro ao buscar dados da OpenSky API: {e}[/red]")
        logging.error(f"Erro ao buscar dados da OpenSky API: {e}")
        return None

def obter_destino_voo(codigo_icao):
    """
    Busca o destino de um voo com base no código ICAO usando a ADS-B Exchange.

    Args:
        codigo_icao (str): Código ICAO do voo.

    Returns:
        str: Destino do voo ou "Desconhecido" em caso de erro.
    """
    try:
        url = f"{ADSBEXCHANGE_API_URL}/icao/{codigo_icao}/"
        response = requests.get(url, headers=ADSBEXCHANGE_HEADERS, timeout=10)
        response.raise_for_status()

        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            voo = data[0]
            destino = voo.get("estArrivalAirport", "Desconhecido")
            return destino
        else:
            return "Desconhecido"
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Erro ao buscar destino do voo: {e}[/red]")
        logging.error(f"Erro ao buscar destino do voo: {e}")
        return "Desconhecido"

def monitorar_aeronaves_tempo_real(lat, lon, distancia=100, intervalo=10, max_iteracoes=10):
    """
    Monitora aeronaves em tempo real em uma área específica.

    Args:
        lat (float): Latitude do ponto central.
        lon (float): Longitude do ponto central.
        distancia (int): Distância em milhas náuticas.
        intervalo (int): Intervalo entre buscas em segundos.
        max_iteracoes (int): Número máximo de iterações.
    """
    try:
        iteracao = 0
        while iteracao < max_iteracoes:
            console.print("[yellow]Buscando aeronaves próximas...[/yellow]")
            aeronaves = buscar_aeronaves_proximas(lat, lon, distancia)

            if aeronaves:
                console.print("[green]✈️ Dados recebidos da API:[/green]")
                for aeronave in aeronaves:
                    call_sign = aeronave.get('call', 'Desconhecido')
                    altitude = aeronave.get('alt', 'Desconhecido')
                    latitude = aeronave.get('lat', 'Desconhecido')
                    longitude = aeronave.get('lon', 'Desconhecido')
                    velocidade = aeronave.get('spd', 'Desconhecido')
                    direcao = aeronave.get('trak', 'Desconhecido')

                    console.print(f"[cyan]➤ Call Sign: [green]{call_sign}[/green][/cyan]")
                    console.print(f"[cyan]   Altitude: [green]{altitude} ft[/green][/cyan]")
                    console.print(f"[cyan]   Latitude: [green]{latitude}[/green][/cyan]")
                    console.print(f"[cyan]   Longitude: [green]{longitude}[/green][/cyan]")
                    console.print(f"[cyan]   Velocidade: [green]{velocidade} km/h[/green][/cyan]")
                    console.print(f"[cyan]   Direção: [green]{direcao}°[/green][/cyan]")
                    console.print(f"[cyan]-----------------------------[/cyan]")
            else:
                console.print("[yellow]Nenhuma aeronave encontrada.[/yellow]")

            # Pergunta ao usuário se deseja continuar
            continuar = console.input("[cyan]👉 Deseja continuar o monitoramento? (s/n): [/cyan]").strip().lower()
            if continuar != 's':
                console.print("[yellow]🚪 Encerrando monitoramento...[/yellow]")
                break

            time.sleep(intervalo)
            iteracao += 1
    except Exception as e:
        console.print(f"[red]⚠️ Erro ao monitorar aeronaves: {e} ⚠️[/red]")
        logging.error(f"Erro ao monitorar aeronaves: {e}")

def buscar_aeronaves_proximas(lat, lon, distancia=100):
    """
    Busca aeronaves dentro de um raio de X milhas náuticas de um ponto geográfico.

    Args:
        lat (float): Latitude do ponto central.
        lon (float): Longitude do ponto central.
        distancia (int): Distância em milhas náuticas.

    Returns:
        list: Lista de aeronaves ou None em caso de erro.
    """
    try:
        url = f"{ADSBEXCHANGE_API_URL}/lat/{lat}/lon/{lon}/dist/{distancia}/"
        response = requests.get(url, headers=ADSBEXCHANGE_HEADERS, timeout=10)
        response.raise_for_status()
        dados = response.json()

        aeronaves = dados.get("ac", [])
        aeronaves_validas = [a for a in aeronaves if a.get("lat", 0) != 0 and a.get("lon", 0) != 0]
        return aeronaves_validas
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Erro ao buscar aeronaves próximas: {e}[/red]")
        logging.error(f"Erro ao buscar aeronaves próximas: {e}")
        return None

def exibir_aeronaves_no_mapa():
    """
    Exibe as aeronaves em um mapa interativo com base na localização atual ou em uma cidade.
    """
    try:
        console.print("[cyan]👉 Deseja usar sua localização atual ou buscar por uma cidade?[/cyan]")
        console.print("[cyan]1. Usar localização atual[/cyan]")
        console.print("[cyan]2. Buscar por uma cidade[/cyan]")
        opcao = console.input("[cyan]👉 Escolha uma opção (1 ou 2): [/cyan]").strip()

        if opcao == "1":
            g = geocoder.ip('me')
            if g.latlng:
                lat, lon = g.latlng
                console.print(f"[green]✅ Localização atual detectada: Latitude {lat}, Longitude {lon}[/green]")
            else:
                console.print("[red]⚠️ Não foi possível detectar a localização atual. ⚠️[/red]")
                return
        elif opcao == "2":
            cidade = console.input("[cyan]👉 Digite o nome da cidade: [/cyan]").strip()
            geolocator = Nominatim(user_agent="aeronaves_map")
            location = geolocator.geocode(cidade)
            if location:
                lat, lon = location.latitude, location.longitude
                console.print(f"[green]✅ Cidade encontrada: {location.address}[/green]")
            else:
                console.print("[red]⚠️ Cidade não encontrada. ⚠️[/red]")
                return
        else:
            console.print("[red]⚠️ Opção inválida! ⚠️[/red]")
            return

        aeronaves = buscar_aeronaves_proximas(lat, lon, 50)
        if aeronaves:
            mapa = folium.Map(location=[lat, lon], zoom_start=13)

            # Caminho para o arquivo de imagem com os.path.join
            icone_aviao_path = os.path.join(os.path.dirname(__file__), '..', 'img', 'airplane.png')

            # Agora criamos o ícone com o caminho correto
            icone_aviao = folium.features.CustomIcon(
                icon_image=icone_aviao_path,  # Caminho absoluto para a imagem
                icon_size=(20, 20),
            )

            for aeronave in aeronaves:
                if aeronave.get('lat', 0) != 0 and aeronave.get('lon', 0) != 0:
                    folium.Marker(
                        location=[aeronave.get('lat'), aeronave.get('lon')],
                        popup=f"""
                            Call Sign: {aeronave.get('call', 'Desconhecido')}<br>
                            Altitude: {aeronave.get('alt', 'Desconhecido')} ft<br>
                            Velocidade: {aeronave.get('spd', 'Desconhecido')} km/h<br>
                            Direção: {aeronave.get('trak', 'Desconhecido')}°
                        """,
                        icon=icone_aviao,
                    ).add_to(mapa)

            mapa.save("../mapa_aeronaves.html")
            console.print("[green]✅ Mapa gerado com sucesso! Arquivo 'mapa_aeronaves.html' salvo.[/green]")
            webbrowser.open("mapa_aeronaves.html")
        else:
            console.print("[yellow]⚠️ Nenhuma aeronave encontrada para exibir no mapa. ⚠️[/yellow]")
    except Exception as e:
        console.print(f"[red]⚠️ Erro ao exibir aeronaves no mapa: {e} ⚠️[/red]")
        logging.error(f"Erro ao exibir aeronaves no mapa: {e}")