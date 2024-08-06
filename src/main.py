from registro_usuario import registrar_usuario
from verificacion_usuario import verificar_usuario

def main():
    print("1. Registrar nuevo usuario")
    print("2. Verificar usuario")

    choice = input("Elige una opción (1/2): ")

    if choice == "1":
        nombre_usuario = input("Introduce el nombre de usuario: ")
        registrar_usuario(nombre_usuario)
    elif choice == "2":
        nombre_usuario = input("Introduce el nombre de usuario: ")
        verificar_usuario(nombre_usuario)
    else:
        print("Opción inválida.")

if __name__ == "__main__":
    main()