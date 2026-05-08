from digi.xbee.devices import XBeeDevice
import time

PORT = "/dev/ttyUSB1"
BAUD_RATE = 57600


def data_receive_callback(xbee_message):
    data = xbee_message.data.decode(errors="ignore")
    remote_addr = xbee_message.remote_device.get_64bit_addr()

    print(f"Recebido de {remote_addr}: {data}")


def main():
    device = XBeeDevice(PORT, BAUD_RATE)

    try:
        print(f"Abrindo Router em {PORT}...")
        device.open()

        print("Endereço local deste módulo:")
        print(device.get_64bit_addr())

        device.add_data_received_callback(data_receive_callback)

        print("\nRouter escutando...")
        print("Pressione Ctrl+C para sair.\n")

        while True:
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nEncerrando receptor.")

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == "__main__":
    main()
