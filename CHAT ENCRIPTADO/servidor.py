import socket

from cryptography.fernet import Fernet

#PROCESO DE ENCRIPTACION DE LOS MENSAGES

def encriptar(texto, clave):
    # Generar una clave de encriptación a partir de la clave proporcionada
    clave_bytes = clave.encode()
    clave_encriptacion = Fernet.generate_key()
    f = Fernet(clave_encriptacion)

    # Encriptar el texto
    texto_encriptado = f.encrypt(texto.encode())

    return texto_encriptado, clave_encriptacion

def desencriptar(texto_encriptado, clave_encriptacion):
    f = Fernet(clave_encriptacion)

    # Desencriptar el texto
    texto_desencriptado = f.decrypt(texto_encriptado).decode()

    return texto_desencriptado
import socket
mensajes=[]
def main():
    # Crea un socket TCP/IP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Asocia el socket a un puerto
    server_address = ('localhost', 12345)
    sock.bind(server_address)

    # Escucha conexiones entrantes
    sock.listen(1)
    print("Servidor en espera de conexiones...")

    while True:
        # Espera una conexión
        connection, client_address = sock.accept()
        print("Conexión establecida desde:", client_address)

        try:
            while True:
                # Recibe los datos del cliente
                data = connection.recv(1024)
                if data:
                    mensajes.append(data)
                    # Devuelve los datos al cliente
                    connection.sendall()
                    print("Mensaje recibido y devuelto:", data.decode())

                    # Verifica si se recibió el mensaje de salida
                    if data.decode() == "exit":
                        break
                else:
                    break
        finally:
            # Cierra la conexión
            connection.close()

            # Verifica si se recibió el mensaje de salida para terminar el programa
            if data.decode() == "exit":
                break

    # Cierra el socket principal
    sock.close()

if __name__ == '__main__':
    main()
