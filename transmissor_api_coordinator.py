from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress
import time

PORT = "/dev/ttyUSB0"
BAUD_RATE = 57600

ROUTER_64BIT_ADDR = "0013A20041839DCA"

INTERVALO_SEGUNDOS = 1.0


def main():
    device = XBeeDevice(PORT, BAUD_RATE)

    try:
        print(f"Abrindo Coordinator em {PORT}...")
        device.open()

        remote_router = RemoteXBeeDevice(
            device,
            XBee64BitAddress.from_hex_string(ROUTER_64BIT_ADDR)
        )

        print(f"Enviando para Router: {ROUTER_64BIT_ADDR}")
        print("Pressione Ctrl+C para sair.\n")

        contador = 0

        while True:
            mensagem = f"Pacote {contador} do Coordinator"

            device.send_data(remote_router, mensagem)

            print("Enviado:", mensagem)

            contador += 1
            time.sleep(INTERVALO_SEGUNDOS)

    except KeyboardInterrupt:
        print("\nEncerrando transmissor.")

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == "__main__":
    main()
