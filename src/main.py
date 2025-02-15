from rich.console import Console
from menus import exibir_menu_principal_interativo, exibir_menu_ordenacao
from api import buscar_estados_opensky, monitorar_aeronaves_tempo_real, exibir_aeronaves_no_mapa
from utils import exibir_lista_voos, tentar_novamente, ordenar_voos
from filtros import (
    filtrar_por_altitude, filtrar_por_origem, mostrar_voos_com_altitude_conhecida,
    mostrar_voos_com_altitude_desconhecida, filtrar_por_velocidade, filtrar_por_direcao
)
from busca import buscar_voo_especifico
from voos_historicos import exibir_voos_historicos
import logging
import os

# Configura o logging
# Caminho absoluto para o diretório de logs
log_dir = os.path.join(os.path.dirname(__file__), "../logs")
os.makedirs(log_dir, exist_ok=True)  # Garante que o diretório logs exista

# Configura o logging com o caminho absoluto
logging.basicConfig(
    filename=os.path.join(log_dir, "erros.log"),
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Cria uma instância do console
console = Console()

def realizar_consulta():
    """
    Função responsável por realizar a consulta de voos ativos.
    """
    while True:
        estados = buscar_estados_opensky()

        # Verifica se a busca retornou dados válidos
        if estados is None:
            console.print("[red]⚠️ Nenhum dado de voo disponível. ⚠️[/red]")
            if not tentar_novamente():
                return  # Retorna ao menu principal
            else:
                continue  # Tenta novamente

        # Exibe todos os voos encontrados
        console.print("[green]✈️ Exibindo todos os voos encontrados:[/green]")
        exibir_lista_voos(estados)

        # Pergunta ao usuário se deseja realizar outra consulta
        while True:
            resposta = console.input("[cyan]🔁 Realizar outra consulta? (s/n): [/cyan]").strip().lower()
            if resposta in ['s', 'n']:
                break
            else:
                console.print("[red]⚠️ Por favor, insira 's' para sim ou 'n' para não. ⚠️[/red]")

        if resposta == 'n':
            console.print("[yellow]🚪 Retornando ao menu principal...[/yellow]")
            return  # Retorna ao menu principal

def ordenar_voos_menu():
    """
    Função responsável por ordenar a lista de voos.
    """
    while True:
        estados = buscar_estados_opensky()

        # Verifica se a busca retornou dados válidos
        if estados is None:
            console.print("[red]⚠️ Nenhum dado de voo disponível. ⚠️[/red]")
            if not tentar_novamente():
                return  # Retorna ao menu principal
            else:
                continue  # Tenta novamente

        # Exibe o submenu de ordenação
        escolha_ordenacao = exibir_menu_ordenacao()
        if escolha_ordenacao == "1":
            estados = ordenar_voos(estados, "altitude")
        elif escolha_ordenacao == "2":
            estados = ordenar_voos(estados, "velocidade")
        elif escolha_ordenacao == "3":
            estados = ordenar_voos(estados, "callsign")
        elif escolha_ordenacao == "4":
            console.print("[yellow]↩️ Retornando ao menu principal...[/yellow]")
            return  # Retorna ao menu principal
        else:
            console.print("[red]⚠️ Opção inválida! Tente novamente. ⚠️[/red]")
            continue
        
        # Adiciona um espaço antes da pergunta
        console.print()  # Linha em branco
        # Exibe os voos ordenados
        console.print("[green]✈️  Exibindo voos ordenados:[/green]")
        exibir_lista_voos(estados)

def main():
    """
    Função principal que gerencia o fluxo do menu e interage com o usuário.
    """
    while True:
        escolha = exibir_menu_principal_interativo()

        # Lógica para cada opção do menu
        if escolha == "1":
            realizar_consulta()
        elif escolha == "2":
            estados = buscar_estados_opensky()
            if estados:
                filtrar_por_altitude(estados)
            else:
                console.print("[red]⚠️ Nenhum dado de voo disponível. ⚠️[/red]")
        elif escolha == "3":
            filtrar_por_origem()
        elif escolha == "4":
            mostrar_voos_com_altitude_conhecida()
        elif escolha == "5":
            mostrar_voos_com_altitude_desconhecida()
        elif escolha == "6":
            buscar_voo_especifico()
        elif escolha == "7":
            exibir_voos_historicos()
        elif escolha == "8":
            filtrar_por_velocidade()
        elif escolha == "9":
            filtrar_por_direcao()
        elif escolha == "10":
            from filtros import monitorar_aeronaves
            monitorar_aeronaves()
        elif escolha == "11":
            exibir_aeronaves_no_mapa()
        elif escolha == "12":
            ordenar_voos_menu()  # Nova opção de ordenação
        elif escolha == "13":
            console.print("[yellow]🌟 Obrigado por usar o sistema! Até a próxima! 🌟[/yellow]")
            console.print("[cyan]✈️ ============================== ✈️[/cyan]")
            break  # Sai do loop e encerra o programa

# Verifica se o script está sendo executado diretamente (não importado)
if __name__ == "__main__":
    main()