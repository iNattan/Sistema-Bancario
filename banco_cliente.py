import socket
import json
import random
import time
import threading

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
        print(f"Resposta do servidor: {resposta}")
        cliente_socket.close()
    except ConnectionRefusedError:
        print("Erro: não foi possível conectar ao servidor. Certifique-se de que o servidor está em execução.")

def simular_cliente(numero_cliente):
    numero_conta = f"conta_{numero_cliente}"
    for _ in range(5):
        operacao = random.choice(["deposito", "saque", "consulta"])
        valor = random.randint(10, 1000) if operacao in ["deposito", "saque"] else 0
        enviar_transacao(operacao, numero_conta, valor)
        time.sleep(random.uniform(2, 3)) 

def iniciar_clientes(numero_clientes):
    threads = []
    for i in range(1, numero_clientes + 1):
        thread = threading.Thread(target=simular_cliente, args=(i,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    num_clientes = int(input("Digite o número de clientes a serem simulados: "))
    iniciar_clientes(num_clientes)
