import funciones_tuneles as fun

def pedirNumeroEntero():
 
    correcto=False
    num=0
    while(not correcto):
        try:
            num = int(input("Introduce un numero entero: "))
            correcto=True
        except ValueError:
            print('Error, introduce un numero entero')
     
    return num

option=0
end_program=False

while not end_program:

    print("1. Login:")
    print("2. Borrar en core:")
    print("3. Borrar en borde")
    # print("4. Borrar los tuneles creados")
    # print("5. Ingrese ip del Tunnel")
    # print("4. Configuraciones en Fermi.")
    # print("5. Probar conexion entre borde y Fermi")
    # print("6. Enviar Iperf entre sites")
    # print("7. Eliminar configuraciones de borde.")
    # print("8. Eliminar configuraciones de Fermi")
    # print("9. Terminar programa")

    option=pedirNumeroEntero()
    if option == 1:
        fun.Login_borde()        
    if option == 2:
        fun.borrar_core()
    if option == 3:
        fun.borrar_borde()
    if option == 4:
        fun.borrar_tuneles()
    if option == 5:
        fun.Ip_tunnel()
    if option == 6:
        fun.Iperf_testing()
    if option == 7:
        fun.Del_config_sites()
    if option == 8:
        fun.Del_tunnel_fermi()
    if option == 9:
        end_program=True

#fun.Host_in_site()
#fun.Open_telnet_sites()
#fun.Config_sites()
#fun.Del_config_sites()

