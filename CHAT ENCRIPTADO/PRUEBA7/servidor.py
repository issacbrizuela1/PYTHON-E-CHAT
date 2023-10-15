import socket
import threading
import cryptography.fernet

# llave para la encriptacion
key = cryptography.fernet.Fernet.generate_key()
f = cryptography.fernet.Fernet(b"r5BkBHhmTScN2ioU6hZ93LfO0qm2KaleMarCHep2X_c=")
# Configuración del servidor
HOST = '0.0.0.0'
PORT = 55555

# Lista de clientes conectados
clientes = []

# Función para manejar la comunicación con un cliente


def handle_client1(client_socket, clientes, addr):
    try:
        while True:
            # Recibir mensaje del cliente
            data = client_socket.recv(4096).decode('utf-8')
            if not data:
                break
            print(f'Mensaje recibido: {f.decrypt(data)}')

            # Reenviar el mensaje a todos los clientes conectados
            for client in clientes:
                if client[1] != addr:
                    data_bytes = bytes(f.decrypt(data))
                    client_1_bytes = bytes(f"{client[1][0]} : {client[1][1]}", encoding="utf-8")

                    # Realiza la concatenación de datos
                    mensaje = client_1_bytes + b" : " + data_bytes

                    # Cifra el mensaje y envíalo
                    mensaje_cifrado = f.encrypt(mensaje)
                    client[0].send(mensaje_cifrado)
    except Exception as e:
        print(f"Error: {e}")
        clientes=[]
        client_socket.close()


# Configurar el servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print(f'Servidor escuchando en {HOST}:{PORT}')

# Esperar conexiones de clientes
while True:
    client_socket, addr = server.accept()
    clientes.append([client_socket, addr])
    print(f'Conexión establecida desde {addr[0]}:{addr[1]}')
    # Iniciar un hilo para manejar la comunicación con el cliente
    client_thread = threading.Thread(
        target=handle_client1, args=(client_socket, clientes, addr))
    client_thread.start()
