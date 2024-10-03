import socket
import json
import random
import time
import threading

def testar_conexao_servidor(host, port):
    try:
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect((host, port))
        cliente_socket.close()
        print(f"Conexão estabelecida com o servidor no endereço {host}:{port}.")
        return True
    except ConnectionRefusedError:
        print("Erro: Não foi possível conectar ao servidor. Certifique-se de que o servidor está em execução.")
        return False

def enviar_transacao(tipo, numero_conta, valor=0):
    try:
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect(("localhost", 12345))
        transacao = {
            "tipo": tipo,
            "numero_conta": numero_conta,
            "valor": valor
        }
        
        cliente_socket.send(json.dumps(transacao).encode())
        resposta = cliente_socket.recv(1024).decode()
        print(f"Resposta do servidor para {numero_conta}: {resposta}")
        cliente_socket.close()
    except ConnectionRefusedError:
        print("Erro: não foi possível conectar ao servidor. Certifique-se de que o servidor está em execução.")

def simular_cliente(numero_cliente, num_operacoes):
    numero_conta = f"conta_{numero_cliente}"
    for _ in range(num_operacoes):
        operacao = random.choice(["deposito", "saque", "consulta"])
        valor = random.randint(10, 1000) if operacao in ["deposito", "saque"] else 0
        enviar_transacao(operacao, numero_conta, valor)
        time.sleep(random.uniform(0.1, 0.3))

def iniciar_clientes(numero_clientes, num_operacoes):
    threads = []
    for i in range(1, numero_clientes + 1):
        thread = threading.Thread(target=simular_cliente, args=(i, num_operacoes))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    host = "localhost"
    port = 12345

    if testar_conexao_servidor(host, port):
        num_clientes = int(input("Digite o número de clientes a serem simulados: "))
        num_operacoes = int(input("Digite o número de operações que cada cliente realizará: "))
        iniciar_clientes(num_clientes, num_operacoes)
    else:
        print("Encerrando o programa porque o servidor não está disponível.")
