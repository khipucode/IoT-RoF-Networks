from digi.xbee.devices import XBeeDevice
import time

PORT = "/dev/ttyUSB0"
BAUD_RATE = 57600

PAN_ID = "1234"

# Canal 20:
# IEEE 802.15.4 usa canais de 11 a 26.
# Canal 20 => bit = 20 - 11 = 9
# Máscara SC = 0x0200
SCAN_CHANNELS = "0200"


def to_bytes(hex_string):
    return bytearray.fromhex(hex_string)


def print_param(device, param):
    try:
        value = device.get_parameter(param)
        print(f"{param} = {value.hex().upper()}")
    except Exception as e:
        print(f"Não foi possível ler {param}: {e}")


def main():
    device = XBeeDevice(PORT, BAUD_RATE)

    try:
        print(f"Abrindo {PORT} em {BAUD_RATE} bps...")
        device.open()

        print("Configurando módulo como COORDINATOR...")

        # CE = 1 -> Coordinator
        device.set_parameter("CE", bytearray([0x01]))

        # AP = 1 -> API mode sem escape
        # Recomendado para usar com a biblioteca digi-xbee
        device.set_parameter("AP", bytearray([0x01]))

        # ID -> PAN ID
        device.set_parameter("ID", to_bytes(PAN_ID))

        # SC -> máscara de canais
        device.set_parameter("SC", to_bytes(SCAN_CHANNELS))

        # BD = 6 -> 57600 bps
        device.set_parameter("BD", bytearray([0x06]))

        # Nome do nó
        device.set_parameter("NI", bytearray("COORDINATOR", "utf8"))

        # Salvar configuração na memória
        device.write_changes()

        # Aplicar alterações
        device.apply_changes()

        time.sleep(1)

        print("\nConfiguração salva.")
        print("Parâmetros principais:")

        print_param(device, "CE")
        print_param(device, "AP")
        print_param(device, "ID")
        print_param(device, "SC")
        print_param(device, "BD")
        print_param(device, "NI")
        print_param(device, "SH")
        print_param(device, "SL")

        print("\nCoordinator configurado com sucesso.")

    except Exception as e:
        print(f"\nErro ao configurar Coordinator: {e}")

    finally:
        if device is not None and device.is_open():
            device.close()
            print("Porta fechada.")


if __name__ == "__main__":
    main()
