from digi.xbee.devices import XBeeDevice
import time

PORT = "/dev/ttyUSB0"
BAUD_RATE = 57600

device = XBeeDevice(PORT, BAUD_RATE)

try:
    print(f"Abrindo Coordinator em {PORT}...")
    device.open()

    contador = 0

    print("Enviando broadcast...")
    print("Pressione Ctrl+C para sair.\n")

    while True:
        mensagem = f"Broadcast {contador} do Coordinator"
        device.send_data_broadcast(mensagem)

        print("Enviado:", mensagem)

        contador += 1
        time.sleep(1)

except KeyboardInterrupt:
    print("\nEncerrando transmissor.")

except Exception as e:
    print("Erro:", e)

finally:
    if device is not None and device.is_open():
        device.close()
