# Check_Voo

Check_Voo é uma aplicação que consulta dados em tempo real sobre os estados de voos comerciais utilizando a OpenSky API e a ADS-B Exchange API. Ele permite filtrar voos com base em informações como origem, altitude, velocidade, direção, e exibir aeronaves em um mapa interativo.

## Funcionalidades

- **Consulta de voos em tempo real**: Busca dados de voos ativos usando a OpenSky API.
- **Filtros avançados**:
  - Por altitude.
  - Por origem (nacional ou internacional).
  - Por velocidade.
  - Por direção (norte, sul, leste, oeste).
- **Busca de voos específicos**: Permite buscar um voo pelo código ICAO.
- **Monitoramento de aeronaves em tempo real**: Exibe aeronaves próximas a uma localização específica.
- **Mapa interativo**: Exibe aeronaves em um mapa usando a biblioteca Folium.
- **Histórico de voos**: Consulta voos históricos com base em um intervalo de tempo.

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/JacobbV/Check_Voo.git

2. Navegue até o diretório do projeto:
    ```bash
    cd Check_Voo
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Crie um arquivo .env na raiz do projeto e adicione suas credenciais:
    ```bash
    # Credenciais da OpenSky Network
    OPENSKY_USERNAME=seu_usuario
    OPENSKY_PASSWORD=sua_senha

    # Chave da API ADS-B Exchange
    ADSBEXCHANGE_API_KEY=sua_chave_aqui
    ```

5. Execute o script principal:
    ```bash
    python main.py
    ```

## Como Usar

Ao executar o script main.py, você verá um menu interativo com as seguintes opções:

- **Exibir todos os voos**: Mostra todos os voos ativos.
- **Filtrar por Altitude**: Filtra voos com base na altitude mínima.
- **Filtrar por Origem**: Filtra voos nacionais ou internacionais.
- **Mostrar voos com altitude conhecida**: Exibe voos com altitude registrada.
- **Mostrar voos com altitude desconhecida**: Exibe voos sem altitude registrada.
- **Buscar voo específico**: Busca um voo pelo código ICAO.
- **Exibir voos históricos**: Consulta voos históricos em um intervalo de tempo.
- **Filtrar por Velocidade**: Filtra voos com base na velocidade mínima ou máxima.
- **Filtrar por Direção**: Filtra voos com base na direção (norte, sul, leste, oeste).
- **Monitorar aeronaves em tempo real**: Monitora aeronaves próximas a uma localização específica.
- **Exibir aeronaves no mapa**: Exibe aeronaves em um mapa interativo.
- **Ordenar voos**: Ordena voos por altitude, velocidade ou código de voo.
- **Sair**: Encerra o programa.

## Estrutura do Projeto

**Check_Voo/**
# ├── src/
# │   ├── main.py
# │   ├── api.py
# │   ├── busca.py
# │   ├── consultas.py
# │   ├── filtros.py
# │   ├── menus.py
# │   ├── utils.py
# │   ├── voos_historicos.py
# ├── img/
# │   ├── airplane.png
# ├── logs/
# │   ├── erros.log
# ├── output/
# │   ├── mapa_aeronaves.html
# ├── .env
# ├── README.md
# ├── requirements.txt
# ├── LICENSE.md

## Tecnologias Usadas

- **Python:** Linguagem principal do projeto.
- **Requests:** Para fazer requisições HTTP às APIs.
- **Rich**: Para interfaces de console interativas e coloridas.
- **Folium**: Para exibir aeronaves em um mapa interativo.
- **Geopy**: Para geolocalização e obtenção de endereços.
- **Dotenv:** Para gerenciar variáveis de ambiente.

## Contribuição

1. Faça um fork deste repositório.
2. Crie uma branch com a sua feature (`git checkout -b feature/nome-da-feature`).
3. Faça as alterações necessárias.
4. Envie um pull request com as alterações.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE.md](LICENSE.md) para mais detalhes.

## Autor

Feito por Rameson Jacó Gomes da Fonseca 
- [GitHub](https://github.com/JacobbV) 
- [LinkedIn](https://www.linkedin.com/in/rameson-jacó-772547120/)

## Observações

- Certifique-se de que o arquivo *.env* está configurado corretamente com suas credenciais.
- O projeto foi projetado para ser modular e fácil de expandir. Sinta-se à vontade para adicionar novas funcionalidades!
