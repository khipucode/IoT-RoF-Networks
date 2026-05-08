from digi.xbee.devices import XBeeDevice
import time

PORT = "/dev/ttyUSB0"
BAUD_RATE = 57600


def main():
    device = XBeeDevice(PORT, BAUD_RATE)

    try:
        print(f"Abrindo Coordinator em {PORT}...")
        device.open()

        print("Endereço local:")
        print(device.get_64bit_addr())

        network = device.get_network()

        print("\nDescobrindo nós...")
        network.start_discovery_process()

        while network.is_discovery_running():
            time.sleep(0.5)

        devices = network.get_devices()

        if not devices:
            print("Nenhum nó encontrado.")
            return

        remote_router = None

        for remote in devices:
            addr64 = str(remote.get_64bit_addr())
            node_id = remote.get_node_id()

            print(f"Nó encontrado: {addr64} | NI={node_id}")

            if addr64 == "0013A20041839DCA" or node_id == "ROUTER":
                remote_router = remote

        if remote_router is None:
            print("Router não encontrado na descoberta.")
            return

        print("\nRouter selecionado:")
        print(remote_router.get_64bit_addr())

        contador = 0

        print("\nEnviando unicast usando nó descoberto...")
        print("Pressione Ctrl+C para sair.\n")

        while True:
            mensagem = f"Unicast {contador} do Coordinator"

            try:
                device.send_data(remote_router, mensagem)
                print("Enviado com sucesso:", mensagem)
            except Exception as e:
                print("Falha ao enviar:", e)

            contador += 1
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nEncerrando transmissor.")

    except Exception as e:
        print("Erro geral:", e)

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == "__main__":
    main()
