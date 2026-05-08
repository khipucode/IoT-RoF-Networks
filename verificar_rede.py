from digi.xbee.devices import XBeeDevice

BAUD_RATE = 57600

DEVICES = {
    "Coordinator": "/dev/ttyUSB0",
    "Router": "/dev/ttyUSB1"
}

PARAMS = [
    "AI",  # Association Indication
    "OP",  # Operating PAN ID
    "OI",  # Operating 16-bit PAN ID
    "CH",  # Operating channel
    "ID",
    "SC",
    "CE",
    "AP",
    "BD",
    "SH",
    "SL",
    "DH",
    "DL"
]


def read_param(device, param):
    try:
        value = device.get_parameter(param)
        print(f"{param} = {value.hex().upper()}")
    except Exception as e:
        print(f"{param} = não disponível ({e})")


def main():
    for name, port in DEVICES.items():
        print("\n" + "=" * 50)
        print(f"{name} em {port}")
        print("=" * 50)

        device = XBeeDevice(port, BAUD_RATE)

        try:
            device.open()

            for param in PARAMS:
                read_param(device, param)

        except Exception as e:
            print(f"Erro ao abrir {port}: {e}")

        finally:
            if device is not None and device.is_open():
                device.close()


if __name__ == "__main__":
    main()
