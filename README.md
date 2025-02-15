# Check_Voo

Check_Voo é uma aplicação que consulta dados em tempo real sobre os estados de voos comerciais utilizando a OpenSky API. Ele permite filtrar voos com base em informações como origem, altitude, velocidade e direção.

## Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/JacobbV/Check_Voo.git
    ```

2. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

3. Execute o script principal:
    ```bash
    python main.py
    ```

## Como Usar

O script `main.py` realiza uma consulta dos voos atuais e os exibe filtrados pela origem (Brasil). Basta rodar o script e ele buscará os dados automaticamente.

## Tecnologias Usadas

- Python
- Requests
- datetime
- Colorama
- Folium (para mapas interativos)

## Contribuição

1. Faça um fork deste repositório.
2. Crie uma branch com a sua feature (`git checkout -b feature/nome-da-feature`).
3. Faça as alterações necessárias.
4. Envie um pull request com as alterações.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE.md](LICENSE.md) para mais detalhes.

## Autor

Feito por Rameson Jacó Gomes da Fonseca  
[LinkedIn](https://www.linkedin.com/in/rameson-jacó-772547120/)