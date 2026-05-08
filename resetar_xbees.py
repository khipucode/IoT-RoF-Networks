from digi.xbee.devices import XBeeDevice
import time

BAUD_RATE = 57600

DISPOSITIVOS = [
    ("Coordinator", "/dev/ttyUSB0"),
    ("Router", "/dev/ttyUSB1"),
]


def resetar(nome, porta):
    device = XBeeDevice(porta, BAUD_RATE)

    try:
        print(f"Resetando {nome} em {porta}...")
        device.open()

        # FR = software reset
        device.set_parameter("FR", bytearray([]))

        print(f"{nome} resetado.")
        time.sleep(3)

    except Exception as e:
        print(f"Erro ao resetar {nome}: {e}")

    finally:
        if device is not None and device.is_open():
            device.close()


def main():
    # Primeiro o Coordinator, depois o Router
    resetar("Coordinator", "/dev/ttyUSB0")
    time.sleep(5)

    resetar("Router", "/dev/ttyUSB1")
    time.sleep(5)

    print("\nReset concluído. Aguarde mais alguns segundos antes de verificar a rede.")


if __name__ == "__main__":
    main()
