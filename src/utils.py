from rich.console import Console
from rich.table import Table
import logging
import os

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

def formatar_numero(numero, casas_decimais=2):
    """
    Formata um número para exibição, com um número específico de casas decimais.
    """
    try:
        return f"{numero:,.{casas_decimais}f}"
    except (ValueError, TypeError):
        return "Desconhecido"

def ordenar_voos(voos, criterio):
    """
    Ordena a lista de voos com base no critério especificado.
    
    Parâmetros:
    - voos (list): Lista de voos.
    - criterio (str): Critério de ordenação (ex: "altitude", "velocidade", "callsign").
    
    Retorna:
    - list: Lista de voos ordenada.
    """
    if not voos:
        return voos

    # Define a chave de ordenação com base no critério
    if criterio == "altitude":
        chave = lambda voo: voo[7] if voo[7] is not None else float('-inf')
    elif criterio == "velocidade":
        chave = lambda voo: voo[9] if voo[9] is not None else float('-inf')
    elif criterio == "callsign":
        chave = lambda voo: voo[1] if voo[1] is not None else ""
    else:
        return voos  # Retorna a lista original se o critério for inválido

    # Ordena a lista de voos
    return sorted(voos, key=chave, reverse=(criterio in ["altitude", "velocidade"]))

def exibir_lista_voos(voos):
    """
    Exibe uma lista de voos em formato de tabela usando rich.
    """
    if not voos:
        console.print("⚠️ Nenhum voo encontrado.", style="bold yellow")
        return

    # Adiciona um espaço antes da tabela
    console.print()  # Linha em branco

    # Cria uma tabela para exibir os voos
    table = Table(title="✈️ Lista de Voos", show_header=True, header_style="bold magenta")
    table.add_column("Código de Voo", style="cyan")
    table.add_column("País de Origem", style="green")
    table.add_column("Destino", style="blue")
    table.add_column("Altitude (m)", style="yellow")
    table.add_column("Velocidade (km/h)", style="red")
    table.add_column("Direção (°)", style="purple")

    # Adiciona os voos à tabela
    for voo in voos:
        callsign = str(voo[1]) if voo[1] else "N/A"
        pais_origem = str(voo[2]) if voo[2] else "Desconhecido"
        endereco = str(voo[3]) if voo[3] else "Desconhecido"
        altitude = str(voo[7]) if voo[7] is not None else "Desconhecida"
        
        # Verifica se a velocidade está presente e é um número
        if len(voo) > 9 and isinstance(voo[9], (int, float)):
            velocidade = str(voo[9])  # Exibe a velocidade em km/h
        else:
            velocidade = "Desconhecida"
        
        # Converte a direção para uma descrição textual
        direcao = converter_grau_para_direcao(voo[10]) if voo[10] is not None else "Desconhecida"

        table.add_row(callsign, pais_origem, endereco, altitude, velocidade, direcao)

    # Exibe a tabela
    console.print(table)

    # Adiciona um espaço após a tabela
    console.print()  # Linha em branco

    # Exibe o total de voos encontrados
    console.print(f"✅ Total de voos encontrados: {len(voos)}", style="bold green")

    # Adiciona um espaço após o total de voos
    console.print()  # Linha em branco

def tentar_novamente():
    """
    Pergunta ao usuário se deseja tentar novamente.
    """
    # Adiciona um espaço antes da pergunta
    console.print()  # Linha em branco
    resposta = console.input("👉 Deseja tentar novamente? (s/n): ").strip().lower()
    return resposta == 's'

def filtrar_voos(estados, condicao):
    """
    Filtra uma lista de voos com base em uma condição fornecida.
    """
    try:
        return [voo for voo in estados if condicao(voo)]
    except Exception as e:
        console.print(f"[red]⚠️ Erro ao filtrar voos: {e} ⚠️[/red]")
        logging.error(f"Erro ao filtrar voos: {e}")
        return []

def converter_grau_para_direcao(grau):
    """
    Converte um valor em graus (0 a 360) em uma direção (cardeal ou intercardeal).
    """
    try:
        if grau is None:
            return "Desconhecida"
        if 0 <= grau < 22.5 or 337.5 <= grau < 360:
            return f"{grau}° (norte)"
        elif 22.5 <= grau < 67.5:
            return f"{grau}° (nordeste)"
        elif 67.5 <= grau < 112.5:
            return f"{grau}° (leste)"
        elif 112.5 <= grau < 157.5:
            return f"{grau}° (sudeste)"
        elif 157.5 <= grau < 202.5:
            return f"{grau}° (sul)"
        elif 202.5 <= grau < 247.5:
            return f"{grau}° (sudoeste)"
        elif 247.5 <= grau < 292.5:
            return f"{grau}° (oeste)"
        elif 292.5 <= grau < 337.5:
            return f"{grau}° (noroeste)"
        else:
            return f"{grau}° (desconhecida)"
    except Exception as e:
        console.print(f"[red]⚠️ Erro ao converter grau para direção: {e} ⚠️[/red]")
        logging.error(f"Erro ao converter grau para direção: {e}")
        return "Desconhecida"