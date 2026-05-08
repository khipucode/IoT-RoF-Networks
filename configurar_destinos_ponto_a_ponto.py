from digi.xbee.devices import XBeeDevice
import time

PORT_COORDINATOR = "/dev/ttyUSB0"
PORT_ROUTER = "/dev/ttyUSB1"
BAUD_RATE = 57600


def read_address(device):
    sh = device.get_parameter("SH")
    sl = device.get_parameter("SL")
    return sh, sl


def address_to_string(sh, sl):
    return sh.hex().upper() + sl.hex().upper()


def get_param(device, param):
    value = device.get_parameter(param)
    return value.hex().upper()


def main():
    coordinator = XBeeDevice(PORT_COORDINATOR, BAUD_RATE)
    router = XBeeDevice(PORT_ROUTER, BAUD_RATE)

    try:
        print("Abrindo Coordinator...")
        coordinator.open()

        print("Abrindo Router...")
        router.open()

        coord_sh, coord_sl = read_address(coordinator)
        router_sh, router_sl = read_address(router)

        coord_addr = address_to_string(coord_sh, coord_sl)
        router_addr = address_to_string(router_sh, router_sl)

        print("\nEndereços detectados:")
        print(f"Coordinator: {coord_addr}")
        print(f"Router:      {router_addr}")

        print("\nConfigurando destino do Coordinator para o Router...")
        coordinator.set_parameter("DH", router_sh)
        coordinator.set_parameter("DL", router_sl)

        print("Configurando destino do Router para o Coordinator...")
        router.set_parameter("DH", coord_sh)
        router.set_parameter("DL", coord_sl)

        print("\nSalvando...")
        coordinator.write_changes()
        router.write_changes()

        print("Aplicando...")
        coordinator.apply_changes()
        router.apply_changes()

        time.sleep(1)

        print("\nVerificação final:")

        print("\nCoordinator:")
        print("DH =", get_param(coordinator, "DH"))
        print("DL =", get_param(coordinator, "DL"))

        print("\nRouter:")
        print("DH =", get_param(router, "DH"))
        print("DL =", get_param(router, "DL"))

        print("\nLink ponto a ponto configurado com sucesso.")

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        if coordinator is not None and coordinator.is_open():
            coordinator.close()

        if router is not None and router.is_open():
            router.close()


if __name__ == "__main__":
    main()
