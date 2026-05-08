from digi.xbee.devices import XBeeDevice
import time

PORT = "/dev/ttyUSB0"
BAUD_RATE = 57600


def main():
    device = XBeeDevice(PORT, BAUD_RATE)

    try:
        print(f"Abrindo Coordinator em {PORT}...")
        device.open()

        print("Endereço local do Coordinator:")
        print(device.get_64bit_addr())

        xbee_network = device.get_network()

        print("\nIniciando descoberta de nós...")
        xbee_network.start_discovery_process()

        while xbee_network.is_discovery_running():
            time.sleep(0.5)

        devices = xbee_network.get_devices()

        print("\nNós encontrados:")

        if not devices:
            print("Nenhum nó encontrado.")
        else:
            for remote in devices:
                print("------------------------")
                print("64-bit:", remote.get_64bit_addr())
                print("16-bit:", remote.get_16bit_addr())
                try:
                    print("NI:", remote.get_node_id())
                except Exception:
                    print("NI: não disponível")

    except Exception as e:
        print("Erro:", e)

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == "__main__":
    main()
