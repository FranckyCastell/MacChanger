import random
import subprocess

# Función para generar una MAC aleatoria
def random_mac():
    mac = [ 0x00, 0x16, 0x3e,
            random.randint(0x00, 0x7f),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff) ]
    return ':'.join(map(lambda x: "%02x" % x, mac))

# Función para generar una MAC que parezca que proviene de un dispositivo Apple
def apple_mac():
    mac = [ 0x00, 0x05, 0x5d,
            random.randint(0x00, 0x7f),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff) ]
    return ':'.join(map(lambda x: "%02x" % x, mac))

# Función para obtener las interfaces de red disponibles
def get_interfaces():
    result = subprocess.run(["ifconfig", "-s"], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error al obtener las interfaces de red disponibles.")
        return []
    output = result.stdout.strip().split('\n')[1:]
    interfaces = [line.split()[0] for line in output]
    return interfaces

# Pide al usuario que elija una opción
print("¿Qué tipo de MAC deseas usar?")
print("1. Aleatoria")
print("2. Apple")
print("3. Ingresar una MAC manualmente")
option = input("Ingresa el número de la opción que deseas: ")

# Genera la MAC según la opción elegida
if option == "1":
    mac = random_mac()
elif option == "2":
    mac = apple_mac()
elif option == "3":
    mac = input("Ingresa la dirección MAC que deseas usar (en formato XX:XX:XX:XX:XX:XX): ")
else:
    print("Opción inválida.")
    exit()

# Imprime la MAC elegida
print("La MAC elegida es:", mac)

# Obtiene las interfaces de red disponibles
interfaces = get_interfaces()

# Si no hay interfaces disponibles, muestra un mensaje y sale del programa
if not interfaces:
    print("No se encontraron interfaces de red disponibles.")
    exit()

# Muestra las interfaces de red disponibles
print("Interfaces de red disponibles:")
for i, interface in enumerate(interfaces):
    print(f"{i+1}. {interface}")

# Pide al usuario que elija una interfaz de red
selection = input("Ingresa el número de la interfaz de red que deseas usar: ")
try:
    index = int(selection) - 1
    interface = interfaces[index]
except (ValueError, IndexError):
    print("Selección inválida.")
    exit()

# Comando para cambiar la MAC
cmd = "ifconfig " + interface + " hw ether " + mac

# Ejecuta el comando
subprocess.call(cmd, shell=True)
