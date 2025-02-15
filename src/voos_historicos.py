from datetime import datetime, timedelta
from api import buscar_voos_historicos
from utils import exibir_lista_voos, tentar_novamente
from rich.console import Console
from rich.prompt import Prompt
from geopy.geocoders import Nominatim
from consultas import obter_endereco  # Importando a função de obter o endereço
import requests


# Inicializa o console do rich
console = Console()

def obter_localizacao():
    """
    Obtém a localização do usuário, tentando primeiro uma abordagem automática via API IPinfo,
    e, caso não seja possível, solicita que o usuário insira manualmente sua latitude e longitude.

    Retorna:
        tuple: Latitude e longitude da localização do usuário.
    
    Exceções:
        Caso a API IPinfo falhe ou o usuário forneça informações incorretas, solicita que ele forneça a localização manualmente.
    """
    try:
        # Obtemos a localização automaticamente pela API IPinfo
        resposta = requests.get('https://ipinfo.io')
        dados = resposta.json()
        localizacao = dados['loc'].split(',')
        latitude = float(localizacao[0])
        longitude = float(localizacao[1])

        console.print(f"Localização detectada automaticamente: Latitude = {latitude}, Longitude = {longitude}", style="bold green")
        
        # Usar Geopy para melhorar a precisão e obter o nome da cidade, por exemplo
        geolocator = Nominatim(user_agent="localizador")
        local = geolocator.reverse((latitude, longitude), language='pt', timeout=10)
        
        console.print(f"Localização detalhada (cidade): {local}", style="bold green")
        return latitude, longitude
    
    except Exception as e:
        console.print(f"Erro ao obter localização automaticamente: {e}", style="bold red")
        console.print("Por favor, insira sua localização manualmente.", style="bold yellow")
        
        latitude = float(Prompt.ask("Digite sua latitude manualmente"))
        longitude = float(Prompt.ask("Digite sua longitude manualmente"))
        return latitude, longitude

def exibir_voos_historicos():
    """
    Exibe uma lista de voos históricos com base no tipo de voo (chegadas ou partidas) e em um intervalo de tempo fornecido.

    Processo:
        - Solicita ao usuário o tipo de voo (chegada ou partida).
        - Solicita um intervalo de tempo com as datas e horas de início e fim.
        - Realiza a busca de voos históricos dentro do intervalo de tempo fornecido.
        - Exibe os voos encontrados ou uma mensagem informando que não há voos no intervalo.

    Exceções:
        - Se o tipo de voo não for válido, exibe um aviso.
        - Se o intervalo de tempo for inválido, também exibe um aviso.
        - Se a API de voos históricos não retornar dados válidos, solicita ao usuário tentar novamente.
    """
    while True:
        try:
            # Solicita ao usuário o tipo de voo (chegadas ou partidas)
            tipo_voo = Prompt.ask("👉 Digite o tipo de voo (arrival para chegadas, departure para partidas)", choices=["arrival", "departure"]).strip().lower()
            
            # Solicita ao usuário o intervalo de tempo
            inicio = Prompt.ask("👉 Digite a data e hora de início (formato: DD/MM/AAAA HH:MM)")
            fim = Prompt.ask("👉 Digite a data e hora de fim (formato: DD/MM/AAAA HH:MM)")

            # Converte as strings de data/hora para objetos datetime
            inicio_dt = datetime.strptime(inicio, "%d/%m/%Y %H:%M")
            fim_dt = datetime.strptime(fim, "%d/%m/%Y %H:%M")

            # Verifica se a data de início é no futuro
            if inicio_dt > datetime.now():
                console.print("⚠️ A data de início não pode ser no futuro. Tente novamente.", style="bold red")
                continue

            # Verifica se a data de fim é posterior à data de início
            if fim_dt <= inicio_dt:
                console.print("⚠️ A data de fim deve ser posterior à data de início.", style="bold red")
                continue

            # Verifica se o intervalo de tempo é maior que 2 horas
            if (fim_dt - inicio_dt) > timedelta(hours=2):
                console.print("⚠️ O intervalo de tempo não pode ser maior que 2 horas.", style="bold red")
                continue

            # Converte as datas para timestamps Unix
            inicio_timestamp = int(inicio_dt.timestamp())
            fim_timestamp = int(fim_dt.timestamp())

            # Busca os voos históricos
            voos_historicos = buscar_voos_historicos(tipo_voo, inicio_timestamp, fim_timestamp)

            # Verifica se a busca retornou dados válidos
            if voos_historicos is None:
                console.print("⚠️ Nenhum dado de voo histórico disponível para o intervalo especificado.", style="bold yellow")
                
                # Pergunta ao usuário se deseja tentar novamente
                if not tentar_novamente():
                    return
                else:
                    continue

            # Prepara e exibe os dados
            voos_formatados = [
                [
                    None,
                    voo.get("callsign", "N/A"),
                    voo.get("origin_country", "Desconhecido"),
                    # Usando as coordenadas para obter o endereço
                    obter_endereco(voo.get("latitude", 0), voo.get("longitude", 0)),
                    None,
                    None,
                    None,
                    voo.get("altitude", "Desconhecida"),
                    voo.get("velocity", "Desconhecida"),
                    voo.get("heading", "Desconhecida")
                ]
                for voo in voos_historicos
            ]

            console.print(f"✈️ Exibindo voos históricos ({tipo_voo}) de {inicio_dt.strftime('%d/%m/%Y %H:%M')} a {fim_dt.strftime('%d/%m/%Y %H:%M')}:", style="bold green")
            exibir_lista_voos(voos_formatados)

            # Pergunta ao usuário se deseja realizar outra consulta
            if not tentar_novamente():
                return

        except ValueError:
            console.print("⚠️ Erro ao processar a data/hora. Certifique-se de usar o formato DD/MM/AAAA HH:MM.", style="bold red")
            continue

        except Exception as e:
            console.print(f"⚠️ Erro ao buscar voos históricos: {e}", style="bold red")
            if not tentar_novamente():
                return