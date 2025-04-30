# gps-tracker
GPS Tracker

# Sobre
O projeto simula um servidor que recebe dados de GPS via TCP e expõe a última localização conhecida via API Rest, desenvolvida com FastAPI, baseada no protocolo SFT9001.

Escolhi usar FastAPI por ser mais performático e mais moderno que django e bem menos burocrático que flask. Utilizei uma abordagem com responsabilidades
mais separadas, com um parser isolado e um servidor tcp independente da API, também facilitando os testes.

O projeto é escalável, já que podemos facilmente substituir o server tcp por um websocket, melhorar a autenticação implementando JWT, etc.

# Estrutura de pastas

├── app/
│   ├── main.py             # API REST
│   ├── tcp_server.py       # Servidor TCP
│   ├── parser.py           # Decodificador GPS
│   ├── database.py         # Configuração do banco
│   ├── models.py           # Modelos
│   ├── auth.py             # Autenticação
├── tests/
│   ├── test_parser.py      # Testes unitários do parser
│   ├── test_api.py         # Testes da API
├── requirements.txt        # Dependências
├── pytest.ini              # Configuração de testes
└── README.md               

# Como rodar

1- Instale as dependências com:

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

2- Rode o servidor tcp em um terminal python com o comando:

python -m app.tcp_server

3- Rode a API

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

4- Exemplo de envio de pacote para o servidor TCP

import socket

hex_data = "pacoteseguindoprotocoloSFT9001"
packet = bytes.fromhex(hex_data)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("localhost", 9000))
    s.sendall(packet)

5- Exemplo de requisição para conferência:
curl.exe -H "x-api-key: 3c96b7e2-8e3a-4b10-a821-8d80b259f21e" http://localhost:8000/api/v1/location/0A3F73000000


# Como executar os testes:

pytest -v

# Segurança

A autenticação é feita via x-api-key passada pelo header
A chave padrão válida é "3c96b7e2-8e3a-4b10-a821-8d80b259f21e", setada em auth.py

# Melhorias futuras

Implementação de autenticação com JWT
Histórico de localizações
Aumentar cobertura de testes
