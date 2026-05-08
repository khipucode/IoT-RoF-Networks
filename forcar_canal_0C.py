from digi.xbee.devices import XBeeDevice
import time

BAUD_RATE = 57600

DISPOSITIVOS = [
    ("Coordinator", "/dev/ttyUSB0"),
    ("Router", "/dev/ttyUSB1"),
]


def set_param(device, param, value):
    device.set_parameter(param, value)
    print(f"{param} configurado para {value.hex().upper()}")


def configurar(nome, porta):
    device = XBeeDevice(porta, BAUD_RATE)

    try:
        print(f"\nAbrindo {nome} em {porta}...")
        device.open()

        print("Canal antes:")
        ch_antigo = device.get_parameter("CH")
        print(f"CH = {ch_antigo.hex().upper()}")

        # Força canal 0C nos dois módulos
        set_param(device, "CH", bytearray([0x0C]))

        # Mantém PAN ID
        set_param(device, "ID", bytearray.fromhex("1234"))

        # Mantém API mode
        set_param(device, "AP", bytearray([0x01]))

        # Mantém 57600 bps
        set_param(device, "BD", bytearray([0x06]))

        print("Salvando...")
        device.write_changes()

        print("Aplicando...")
        device.apply_changes()

        time.sleep(1)

        print("Canal depois:")
        ch_novo = device.get_parameter("CH")
        print(f"CH = {ch_novo.hex().upper()}")

    except Exception as e:
        print(f"Erro em {nome}: {e}")

    finally:
        if device is not None and device.is_open():
            device.close()


def main():
    for nome, porta in DISPOSITIVOS:
        configurar(nome, porta)

    print("\nFinalizado. Agora rode verificar_rede.py novamente.")


if __name__ == "__main__":
    main()
