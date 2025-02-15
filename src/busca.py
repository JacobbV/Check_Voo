from rich.console import Console
from rich.prompt import Prompt
from api import buscar_estados_opensky
from utils import exibir_lista_voos
import re

# Inicializa o console do rich
console = Console()

def buscar_voo_especifico():
    """
    Permite ao usuário buscar um voo específico pelo código ICAO.

    A função executa em loop até que o usuário decida parar, validando o código ICAO
    e exibindo os detalhes do voo encontrado. Caso o voo não seja encontrado ou 
    o código ICAO seja inválido, o sistema fornecerá feedback adequado.

    Processos da função:
    - Solicita ao usuário um código ICAO válido.
    - Valida o código para garantir que ele contenha entre 4 e 7 caracteres alfanuméricos.
    - Realiza uma busca utilizando a função 'buscar_estados_opensky()'.
    - Exibe os detalhes do voo, se encontrado, ou uma mensagem informando que o voo não foi localizado.
    - Permite ao usuário realizar outra busca ou retornar ao menu principal.

    Parâmetros:
    - Nenhum parâmetro é necessário para esta função.

    Retorna:
    - None: A função executa em loop até que o usuário decida parar.
    
    Exemplo de uso:
    >>> buscar_voo_especifico()
    Digite o código do voo (ICAO, ex: SWA3220): SWA3220
    Detalhes do voo SWA3220:
    [Detalhes do voo aqui]
    🔁 Realizar outra busca? (s/n): n
    🚪 Retornando ao menu principal...
    """
    while True:  # Loop principal para permitir múltiplas buscas
        # Solicita o código ICAO ao usuário e faz a validação
        codigo_voo = Prompt.ask("👉 Digite o código do voo (ICAO, ex: SWA3220)").strip().upper()
        
        # Validação do código ICAO (4 a 7 caracteres alfanuméricos)
        if not re.match(r"^[A-Z0-9]{3,8}$", codigo_voo):
            console.print("⚠️ Código ICAO inválido. Deve conter entre 3 e 8 caracteres alfanuméricos.", style="bold red")
            continue  # Volta ao início do loop para pedir o código novamente

        # Busca os estados dos voos na API OpenSky
        estados = buscar_estados_opensky()

        # Verifica se a busca retornou dados válidos
        if estados is None:
            console.print("⚠️ Não foi possível buscar os dados dos voos. Tente novamente mais tarde.", style="bold red")
            return  # Retorna ao menu principal

        # Procura o voo pelo código ICAO fornecido
        voo_encontrado = next((voo for voo in estados if voo[1] and voo[1].strip().upper() == codigo_voo), None)

        # Exibe o resultado da busca
        if voo_encontrado:
            console.print(f"✅ Detalhes do voo {codigo_voo}:", style="bold green")
            exibir_lista_voos([voo_encontrado])
        else:
            console.print(f"⚠️ Nenhum voo encontrado com o código {codigo_voo}.", style="bold yellow")

        # Pergunta ao usuário se deseja realizar outra busca
        resposta = Prompt.ask("🔁 Deseja realizar outra busca?", choices=["s", "n"], default="n").strip().lower()
        if resposta == 'n':
            console.print("🚪 Retornando ao menu principal...", style="bold yellow")
            return  # Sai da função e retorna ao menu principal