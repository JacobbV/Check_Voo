from rich.console import Console
from api import buscar_estados_opensky, monitorar_aeronaves_tempo_real, buscar_aeronaves_proximas
from consultas import buscar_voos_por_pais
from utils import exibir_lista_voos, tentar_novamente, filtrar_voos
from menus import exibir_menu_origem
import time

# Cria uma instância do console
console = Console()

def filtrar_por_altitude(estados=None):
    """
    Filtra os voos com base na altitude mínima fornecida pelo usuário.
    """
    while True:
        if estados is None:
            estados = buscar_estados_opensky()

        if estados is None:
            console.print("[red]⚠️ Nenhum dado de voo disponível. ⚠️[/red]")
            if not tentar_novamente():
                return
            else:
                continue

        try:
            altitude_minima = float(console.input("[cyan]👉 Digite a altitude mínima para filtrar os voos (em metros, ex: 10000): [/cyan]"))
            if altitude_minima <= 0:
                console.print("[red]⚠️ Por favor, insira uma altitude maior que zero. ⚠️[/red]")
                continue

            # Filtra os voos com base na altitude
            voos_filtrados = filtrar_voos(estados, lambda voo: voo[7] and voo[7] >= altitude_minima)

            if not voos_filtrados:
                console.print("[yellow]⚠️ Nenhum voo encontrado com a altitude solicitada. ⚠️[/yellow]")
            else:
                console.print(f"[green]✈️ Exibindo voos com altitude mínima de {altitude_minima} metros:[/green]")
                exibir_lista_voos(voos_filtrados)

            # Pergunta ao usuário se deseja realizar outra consulta
            if not tentar_novamente():
                return

        except ValueError:
            console.print("[red]⚠️ Por favor, insira um número válido para a altitude. ⚠️[/red]")

def filtrar_por_origem():
    """
    Filtra os voos por origem (nacional ou internacional).
    """
    while True:
        estados = buscar_estados_opensky()

        if estados is None:
            console.print("[red]⚠️ Nenhum dado de voo disponível. ⚠️[/red]")
            return

        exibir_menu_origem()
        opcao = console.input("[cyan]👉 Escolha uma opção (1 a 3): [/cyan]").strip()

        if opcao == "1":
            voos_internacionais = [voo for voo in estados if voo[2] != 'Brazil']
            if voos_internacionais:
                console.print("[green]✈️ Exibindo voos internacionais:[/green]")
                exibir_lista_voos(voos_internacionais)
            else:
                console.print("[yellow]⚠️ Nenhum voo internacional encontrado. ⚠️[/yellow]")

        elif opcao == "2":
            voos_nacionais = buscar_voos_por_pais(estados, "Brazil")
            if voos_nacionais:
                console.print("[green]✈️ Exibindo voos nacionais (do Brasil):[/green]")
                exibir_lista_voos(voos_nacionais)
            else:
                console.print("[yellow]⚠️ Nenhum voo encontrado para o Brasil. ⚠️[/yellow]")

        elif opcao == "3":
            console.print("[yellow]🚪 Retornando ao menu principal...[/yellow]")
            return

        else:
            console.print("[red]⚠️ Opção inválida! Tente novamente. ⚠️[/red]")

        if not tentar_novamente():
            return

def mostrar_voos_com_altitude_conhecida():
    """
    Filtra e exibe apenas os voos que possuem uma altitude conhecida.
    """
    while True:
        estados = buscar_estados_opensky()

        if estados is None:
            console.print("[red]⚠️ Nenhum dado de voo disponível. ⚠️[/red]")
            if not tentar_novamente():
                return
            else:
                continue

        voos_com_altitude_conhecida = filtrar_voos(estados, lambda voo: voo[7] is not None)

        if not voos_com_altitude_conhecida:
            console.print("[yellow]⚠️ Nenhum voo com altitude conhecida encontrado. ⚠️[/yellow]")
        else:
            console.print("[green]✈️ Exibindo voos com altitude conhecida:[/green]")
            exibir_lista_voos(voos_com_altitude_conhecida)

        if not tentar_novamente():
            return

def mostrar_voos_com_altitude_desconhecida():
    """
    Filtra e exibe apenas os voos que possuem uma altitude desconhecida.
    """
    while True:
        estados = buscar_estados_opensky()

        if estados is None:
            console.print("[red]⚠️ Nenhum dado de voo disponível. ⚠️[/red]")
            return

        voos_com_altitude_desconhecida = filtrar_voos(estados, lambda voo: voo[7] is None)

        if not voos_com_altitude_desconhecida:
            console.print("[yellow]⚠️ Nenhum voo com altitude desconhecida encontrado. ⚠️[/yellow]")
        else:
            console.print("[green]✈️ Exibindo voos com altitude desconhecida:[/green]")
            exibir_lista_voos(voos_com_altitude_desconhecida)

        if not tentar_novamente():
            return

def filtrar_por_velocidade():
    """
    Filtra os voos com base na velocidade mínima ou máxima fornecida pelo usuário.
    """
    while True:
        estados = buscar_estados_opensky()

        if estados is None:
            console.print("[red]⚠️ Nenhum dado de voo disponível. ⚠️[/red]")
            if not tentar_novamente():
                return
            else:
                continue

        try:
            tipo_velocidade = console.input("[cyan]👉 Deseja filtrar por velocidade mínima ou máxima? (min/max): [/cyan]").strip().lower()
            if tipo_velocidade not in ["min", "max"]:
                console.print("[red]⚠️ Por favor, insira 'min' para velocidade mínima ou 'max' para velocidade máxima. ⚠️[/red]")
                continue

            velocidade = float(console.input(f"[cyan]👉 Digite a velocidade {'mínima' if tipo_velocidade == 'min' else 'máxima'} (em km/h): [/cyan]"))
            if velocidade < 0:
                console.print("[red]⚠️ Por favor, insira uma velocidade maior ou igual a zero. ⚠️[/red]")
                continue

            if tipo_velocidade == "min":
                voos_filtrados = filtrar_voos(estados, lambda voo: voo[9] and voo[9] >= velocidade)
            else:
                voos_filtrados = filtrar_voos(estados, lambda voo: voo[9] and voo[9] <= velocidade)

            if not voos_filtrados:
                console.print("[yellow]⚠️ Nenhum voo encontrado com a velocidade solicitada. ⚠️[/yellow]")
            else:
                console.print(f"[green]✈️ Exibindo voos com velocidade {'mínima' if tipo_velocidade == 'min' else 'máxima'} de {velocidade} km/h:[/green]")
                exibir_lista_voos(voos_filtrados)

            if not tentar_novamente():
                return

        except ValueError:
            console.print("[red]⚠️ Por favor, insira um número válido para a velocidade. ⚠️[/red]")

def filtrar_por_direcao():
    """
    Filtra os voos com base na direção (norte, sul, leste, oeste).
    """
    while True:
        estados = buscar_estados_opensky()

        if estados is None:
            console.print("[red]⚠️ Nenhum dado de voo disponível. ⚠️[/red]")
            if not tentar_novamente():
                return
            else:
                continue

        try:
            direcao = console.input("[cyan]👉 Digite a direção desejada (norte, sul, leste, oeste): [/cyan]").strip().lower()
            if direcao not in ["norte", "sul", "leste", "oeste"]:
                console.print("[red]⚠️ Por favor, insira uma direção válida (norte, sul, leste, oeste). ⚠️[/red]")
                continue

            if direcao == "norte":
                condicao = lambda voo: voo[10] is not None and (0 <= voo[10] < 45 or 315 <= voo[10] < 360)
            elif direcao == "sul":
                condicao = lambda voo: voo[10] is not None and (135 <= voo[10] < 225)
            elif direcao == "leste":
                condicao = lambda voo: voo[10] is not None and (45 <= voo[10] < 135)
            elif direcao == "oeste":
                condicao = lambda voo: voo[10] is not None and (225 <= voo[10] < 315)

            voos_filtrados = [voo for voo in estados if condicao(voo)]

            if not voos_filtrados:
                console.print(f"[yellow]⚠️ Nenhum voo encontrado na direção {direcao}. ⚠️[/yellow]")
            else:
                console.print(f"[green]✈️ Exibindo voos na direção {direcao}:[/green]")
                exibir_lista_voos(voos_filtrados)

            if not tentar_novamente():
                return

        except ValueError:
            console.print("[red]⚠️ Erro ao processar a direção. Tente novamente. ⚠️[/red]")

def monitorar_aeronaves():
    """
    Coleta os dados do usuário e inicia o monitoramento de aeronaves em tempo real.
    """
    try:
        lat = float(console.input("[cyan]👉 Digite a latitude (ex: -23.5505 para São Paulo): [/cyan]").strip().replace(",", "."))
        lon = float(console.input("[cyan]👉 Digite a longitude (ex: -46.6333 para São Paulo): [/cyan]").strip().replace(",", "."))
        distancia = int(console.input("[cyan]👉 Digite a distância em milhas náuticas (máximo 100, ex: 20): [/cyan]").strip())
        intervalo = float(console.input("[cyan]👉 Digite o intervalo de atualização em segundos (ex: 5): [/cyan]").strip().replace(",", "."))

        # Verifica se a distância é válida
        if distancia < 0 or distancia > 100:
            console.print("[red]⚠️ A distância deve estar entre 0 e 100 milhas náuticas. ⚠️[/red]")
            return

        # Verifica se o intervalo é válido
        if intervalo <= 0:
            console.print("[red]⚠️ O intervalo de atualização deve ser maior que zero. ⚠️[/red]")
            return

        # Inicia o monitoramento
        console.print("[yellow]Iniciando monitoramento de aeronaves...[/yellow]")
        console.print(f"[cyan]Latitude: {lat}, Longitude: {lon}, Distância: {distancia} NM, Intervalo: {intervalo} segundos[/cyan]")

        while True:
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
                break  # Sai do loop

            time.sleep(intervalo)  # Pausa o loop pelo intervalo especificado

    except ValueError:
        console.print("[red]⚠️ Entrada inválida! Certifique-se de digitar números. ⚠️[/red]")