from digi.xbee.devices import XBeeDevice

PORT = "/dev/ttyUSB1"
BAUD_RATE = 57600

PARAMS_TO_READ = [
    "VR",  # Firmware version
    "HV",  # Hardware version
    "AP",
    "BD",
    "ID",
    "SC",
    "CE",
    "SM",
    "JV",
    "NI",
    "SH",
    "SL",
    "DH",
    "DL"
]


def read_param(device, param):
    try:
        value = device.get_parameter(param)
        print(f"[OK] {param} = {value.hex().upper()}")
    except Exception as e:
        print(f"[ERRO] {param} -> {e}")


def main():
    device = XBeeDevice(PORT, BAUD_RATE)

    try:
        print(f"Abrindo {PORT} em {BAUD_RATE} bps...")
        device.open()

        print("\nLendo parâmetros disponíveis:\n")

        for param in PARAMS_TO_READ:
            read_param(device, param)

    except Exception as e:
        print(f"\nErro geral: {e}")

    finally:
        if device is not None and device.is_open():
            device.close()
            print("\nPorta fechada.")


if __name__ == "__main__":
    main()
