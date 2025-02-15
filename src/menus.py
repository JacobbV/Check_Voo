from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Cria uma instância do console
console = Console()

def exibir_menu_principal_interativo():
    """
    Exibe o menu principal de forma interativa usando rich.
    """
    opcoes = {
        "1": "🛫 Exibir todos os voos",
        "2": "📏 Filtrar por Altitude",
        "3": "🌍 Filtrar por Origem",
        "4": "✅ Mostrar voos com altitude conhecida",
        "5": "❌ Mostrar voos com altitude desconhecida",
        "6": "🔍 Buscar voo específico",
        "7": "🕰️  Exibir voos históricos",
        "8": "🚀 Filtrar por Velocidade",
        "9": "🧭 Filtrar por Direção",
        "10": "🛰️  Monitorar aeronaves em tempo real",
        "11": "🗺️  Exibir aeronaves no mapa",
        "12": "📊 Ordenar voos",  # Nova opção de ordenação
        "13": "🚪 Sair",
    }

    while True:
        # Cabeçalho do menu
        console.print(Panel("🌟 MENU PRINCIPAL 🌟", style="bold cyan"))

        # Exibe as opções do menu
        table = Table(show_header=False, box=None)
        for key, value in opcoes.items():
            table.add_row(f"[green]{key}[/green]", value)

        console.print(table)

        # Solicita a escolha do usuário
        escolha = console.input("[cyan]👉 Escolha uma opção (1 a 13): [/cyan]").strip()

        if escolha in opcoes:
            return escolha
        else:
            console.print("[red]⚠️ Opção inválida! Tente novamente. ⚠️[/red]")

def exibir_menu_ordenacao():
    """
    Exibe o submenu de ordenação de voos.
    """
    console.print(Panel("📊 MENU DE ORDENAÇÃO 📊", style="bold cyan"))
    console.print("[green]1. 🛫 Ordenar por Altitude (maior para menor)[/green]")
    console.print("[yellow]2. 🚀 Ordenar por Velocidade (maior para menor)[/yellow]")
    console.print("[blue]3. 🔤 Ordenar por Código de Voo (A-Z)[/blue]")
    console.print("[red]4. ↩️  Voltar ao menu principal[/red]")
    
    escolha = console.input("[cyan]👉 Escolha uma opção (1 a 4): [/cyan]").strip()
    return escolha

def exibir_menu_origem():
    """
    Exibe o menu de filtro por origem.
    """
    console.print(Panel("🌍 MENU DE ORIGEM 🌍", style="bold yellow"))
    console.print("[yellow]1. 🌐 Voos Internacionais[/yellow]")
    console.print("[blue]2. 🇧🇷 Voos Nacionais[/blue]")
    console.print("[green]3. 🚪 Voltar ao menu principal[/green]")