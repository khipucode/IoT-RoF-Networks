from digi.xbee.devices import XBeeDevice
import time

PORT = "/dev/ttyUSB1"
BAUD_RATE = 57600

PAN_ID = "1234"
SCAN_CHANNELS = "0200"


def to_bytes(hex_string):
    return bytearray.fromhex(hex_string)


def set_param_safe(device, param, value, description=""):
    try:
        device.set_parameter(param, value)
        print(f"[OK] {param} configurado {description}")
        return True
    except Exception as e:
        print(f"[AVISO] Não foi possível configurar {param} {description}: {e}")
        return False


def get_param_safe(device, param):
    try:
        value = device.get_parameter(param)
        print(f"{param} = {value.hex().upper()}")
    except Exception as e:
        print(f"{param} = não disponível ({e})")


def main():
    device = XBeeDevice(PORT, BAUD_RATE)

    try:
        print(f"Abrindo {PORT} em {BAUD_RATE} bps...")
        device.open()

        print("\nConfigurando módulo como ROUTER...\n")

        set_param_safe(device, "CE", bytearray([0x00]), "-> Router")
        set_param_safe(device, "AP", bytearray([0x01]), "-> API mode")
        set_param_safe(device, "ID", to_bytes(PAN_ID), "-> PAN ID")
        set_param_safe(device, "SC", to_bytes(SCAN_CHANNELS), "-> canal 20")
        set_param_safe(device, "BD", bytearray([0x06]), "-> 57600 bps")
        set_param_safe(device, "SM", bytearray([0x00]), "-> sleep desativado")
        set_param_safe(device, "NI", bytearray("ROUTER", "utf8"), "-> nome do nó")

        print("\nSalvando alterações...")
        device.write_changes()

        print("Aplicando alterações...")
        device.apply_changes()

        time.sleep(1)

        print("\nConfiguração final:\n")

        params = [
            "VR",
            "HV",
            "CE",
            "AP",
            "ID",
            "SC",
            "BD",
            "SM",
            "NI",
            "SH",
            "SL",
            "DH",
            "DL"
        ]

        for param in params:
            get_param_safe(device, param)

        print("\nRouter configurado com sucesso.")

    except Exception as e:
        print(f"\nErro geral ao configurar Router: {e}")

    finally:
        if device is not None and device.is_open():
            device.close()
            print("\nPorta fechada.")


if __name__ == "__main__":
    main()
