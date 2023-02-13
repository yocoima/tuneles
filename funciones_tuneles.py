# import menu_tuneles as fun
import getpass
import os
from signal import pause
import sys
import telnetlib
import time
import re
import string
import random
import ipaddress

global tn


def Login_borde():
        """ Esta funcion recibe los datos del router de borde, tiempo de test, 
        usuario y clave 
        """
        global Host, user, password, TIEMPO, online_cpe, nombre_cpe          
        # Host=input("Ingrese ip de monitor de router de borde: ")
        Host="10.10.10.180" 
        # Host=""
        # user=input("Enter User name: ")
        user="yhs"
        
        # password=getpass.getpass()
        password="P1r@m1d3_1ooo*"
                   
        ping_successful=os.system("ping -c 2 " + Host)
        online_cpe = True
        if ping_successful == 0: 
                print(" \n ")
                print("Router de borde disponible")
                online_cpe = True               
                Open_telnet_cpe()
                # Login_concentrador_principal(Host,user,password)
                # return Host + user + password
        else:
                online_cpe = False 
                
                correcto = False
                while (not correcto):
                        try:
                                nombre_cpe = ((input("Indique el nombre del router cpe, SIN ESPACIOS: ")))
                                if nombre_cpe.count(" ") >= 1:
                                        print(" \n ")
                                        print("** Debe ingresar una opcion valida **")
                                else:
                                        correcto=True
                        except ValueError:

                                print(" \n ")
                                print("** Debe ingresar una opcion valida **")                       


                # Login_concentrador_principal(Host,user,password)
                # return Host + user + password
                # Login_concentrador_principal(Host,user,password)
                # return Host + user + password 
        cantidad_de_tuneles()    
       
        
def Login_concentrador_principal():       
        global Host_taylor, user_taylor, password_taylor, TIEMPO   

        # Host_taylor="192.168.100.228"  #temporalmente zeeman para pruebas
        Host_taylor="192.168.100.246"               
        user_taylor= user
        password_taylor= password              
        Open_telnet_principal(Host_taylor, user_taylor, password_taylor)               
        return Host_taylor + user_taylor + password_taylor

def Login_concentrador_respaldo():
        global Host_chagall, user_chagall, password_chagall, TIEMPO
       
        Host_chagall="10.230.10.8"   #temporalmente acg para pruebas
        # Host_chagall="192.168.100.225"               
        user_chagall= user
        password_chagall= password               
        Open_telnet_respaldo(Host_chagall, user_chagall, password_chagall)               
        return Host_chagall + user_chagall + password_chagall
      

def Open_telnet_cpe():
        """
        Funcion con inicio de sesion a borde.
        No cierra sesion, pasa la sesion a otras funciones. 
        """
        global tn, router_name 
        tn=telnetlib.Telnet(Host)
        tn.read_until(b"Username: " )
        tn.write(user.encode('ascii') + b"\n")
        if password:
                tn.read_until(b"Password: ")
                tn.write(password.encode('ascii')+b"\n")
        tn.write(b" terminal length 512 \n")        
        hostname=(tn.read_until(b"#", timeout=120 ))
        router_name=hostname.decode('ascii')
        print(" \n ")
        print("Conexion abierta a",router_name[2:-1].strip()) 
        return tn, router_name

def Open_telnet_principal(Host_taylor, user_taylor, password_taylor):     
        global tn, router_name_ppl
        tn=telnetlib.Telnet(Host_taylor)
        tn.read_until(b"Username: " )
        tn.write(user_taylor.encode('ascii') + b"\n")
        if password_taylor:
                tn.read_until(b"Password: ")
                tn.write(password_taylor.encode('ascii')+b"\n")
        tn.write(b" terminal length 512 \n")        
        hostname=(tn.read_until(b"#", timeout=120 ))
        router_name_ppl=hostname.decode('ascii')
        print(" \n ")
        print("Conexion abierta a",router_name_ppl[2:-1].strip()) 
        return tn, router_name_ppl 
        

def Open_telnet_respaldo(Host_chagall, user_chagall, password_chagall):     
        global tn, router_name_bk        
        tn=telnetlib.Telnet(Host_chagall)
        tn.read_until(b"Username: " )
        tn.write(user_chagall.encode('ascii') + b"\n")
        if password:
                tn.read_until(b"Password: ")
                tn.write(password_chagall.encode('ascii')+b"\n")
        tn.write(b" terminal length 512 \n")
        hostname=(tn.read_until(b"#", timeout=120 ))
        router_name_bk=hostname.decode('ascii')
        print(" \n ")
        print("Conexion abierta a",router_name_bk[2:-1].strip())         
        return tn , router_name_bk

def Tipo_conexion(): 
        global tipo_conexion
        
        print("1. xg:")
        print("2. ftth/vsat:")
        correcto=False        
        while(not correcto):
                try:
                        option = int(input("Indique el tipo de conexion: "))       
                        if option != 1 and option != 2:                
                                print(" \n ")
                                print("** Debe ingresar una opcion valida **")                
                                Tipo_conexion()
                        else:
                                correcto=True
                except ValueError:

                        print(" \n ")
                        print("** Debe ingresar una opcion valida **")                
                        Tipo_conexion()               
        
        # tipo_conexion=""
        if option == 1:
                tipo_conexion= "xg"        
        if option == 2:
                tipo_conexion= "ftth/vsat"  
        
        print("El conexion seleccionada es del tipo: " + tipo_conexion )

        Numero_interfaz_ppl()        

def valida_vrf_admin_borde():
        Open_telnet_cpe()
        vrf_admin = "admin"        
        compara_vrf=tn.write(b"sh ip vrf \n" ) 
        time.sleep(1)        
        resultado= tn.read_very_eager().decode('ascii')        
        comparacion=re.search(vrf_admin.encode('ascii'), resultado.encode('ascii'))      
        if comparacion:
                print("VRF Correcta!!")                             
                
        else:                
                print("La VRF " + vrf_admin  +" no existe")
                print("Desea crear la vrf " + vrf_admin)
                print("1. si")
                print("2. no")
                opcion=int(input("Ingrese su opcion: "))
                if opcion == 1:
                        tn.write(b"configure terminal \n")
                        print(tn.write(b"ip vrf " + str(vrf_admin).encode('ascii') + b"\n"))
                        tn.write(b"ip vrf " + str(vrf_admin).encode('ascii') + b"\n")
                        tn.write(b"do write \n")
                        time.sleep(1)
                        valida_vrf_admin_borde()
                        
                if opcion == 2:                       
                        print("El programa continua sin la vrf")
                
def Consulta_vrf_ppl(vrf):
        Login_concentrador_principal()        
        compara_vrf=tn.write(b"sh ip vrf \n" ) 
        time.sleep(1)        
        resultado= tn.read_very_eager().decode('ascii')        
        comparacion=re.search(vrf.encode('ascii'), resultado.encode('ascii'))      
        if comparacion:
                print("VRF Correcta!!")
                if num_de_tuneles == 1:
                        consulta_vrf_bkup(vrf)
                if num_de_tuneles == 8:
                        consulta_vrf_bkup_8_tun(vrf)               
                
        else:                
                print("La VRF no existe, intente de nuevo o cree la vrf")
                return cantidad_de_tuneles() 


def consulta_vrf_bkup(vrf):  
        Login_concentrador_respaldo()        
        compara_vrf=tn.write(b"sh ip vrf \n" ) 
        time.sleep(1)        
        resultado= tn.read_very_eager().decode('ascii')        
        comparacion=re.search(vrf.encode('ascii'), resultado.encode('ascii'))      
        if comparacion:
                print("VRF Correcta !!")                
                Tipo_conexion()              
        else:                
                print("La VRF no existe en Chagall, aunque si existe en Taylor, el programa no puede continuar. \n Revise el proceso")

def consulta_vrf_bkup_8_tun(vrf):  
        Login_concentrador_respaldo()        
        compara_vrf=tn.write(b"sh ip vrf" b"\n" ) 
        time.sleep(1)        
        resultado= tn.read_very_eager().decode('ascii')        
        comparacion=re.search(vrf.encode('ascii'), resultado.encode('ascii'))      
        if comparacion:
                print("VRF Correcta !!")                
                Numero_interfaz_ppl()  
                              
        else:                
                print("La VRF no existe en Chagall, aunque si existe en Taylor, el programa no puede continuar. \n Revise el proceso")

def consulta_vrf_borde_8_tun(vrf):
        Open_telnet_cpe()
        compara_vrf=tn.write(b"sh ip vrf" b"\n" ) 
        time.sleep(1)        
        resultado= tn.read_very_eager().decode('ascii')        
        comparacion=re.search(vrf.encode('ascii'), resultado.encode('ascii'))      
        if comparacion:
                print("VRF Correcta!!")                
                Consulta_vrf_ppl(vrf)  
                              
        else:                
                print("La VRF no existe en  Borde, el programa no puede continuar. \n Revise el proceso")

def consulta_vrf_borde(vrf):
        Open_telnet_cpe()
        compara_vrf=tn.write(b"sh ip vrf" b"\n" ) 
        time.sleep(1)        
        resultado= tn.read_very_eager().decode('ascii')        
        comparacion=re.search(vrf.encode('ascii'), resultado.encode('ascii'))      
        if comparacion:
                print("VRF Correcta!!")                
                Consulta_vrf_ppl(vrf)                               
        else:                
                print("La VRF no existe en  Borde, el programa no puede continuar. \n Revise el proceso")
                        
def cantidad_de_tuneles():
        global num_de_tuneles, vrf, define_vrf  
        print(" \n ")
        print("Indique el numero de tuneles que van a ser creados: ")
        print(" \n ")
        print("1-. Tunel unico")
        print("2-. Full, 8 tuneles")
        correcto=False
        
        while(not correcto):
                try:
                        num_de_tuneles= int(input("Indique la opcion: "))        
                        if num_de_tuneles != 1 and num_de_tuneles != 2:                
                                print(" \n ")
                                print("** Debe ingresar una opcion valida **")                
                                cantidad_de_tuneles()
                        else:
                                correcto=True
                except ValueError:
                        print(" \n ")
                        print("** Debe ingresar una opcion valida **")                
                        cantidad_de_tuneles()
                    
                if num_de_tuneles == 1:
                        print("Se va a crear un tunel unico")                
                        num_de_tuneles = 1
                        
                        print("Indique la VRF a continuacion:")
                        print("1-. VRF de administracion")
                        print("2-. VRF de datos")
                        option = int(input("Indique la opcion: "))
                        if option == 1:
                                vrf= "admin"
                                print("La VRF indicada es " + vrf)
                                Tipo_conexion()                        
                                
                        if option == 2:                                      
                                define_vrf= str(input("Digite la VRF:"))
                                vrf= define_vrf               
                                print("La VRF indicada es " + vrf)
                                if online_cpe == True:
                                        consulta_vrf_borde(vrf)
                                if online_cpe == False:        
                                        Consulta_vrf_ppl(vrf)                                             
                
                if num_de_tuneles == 2:
                        print("Se van a crear 8 tuneles")                
                        num_de_tuneles = 8
                        define_vrf= str(input("Digite la VRF:"))
                        vrf= define_vrf               
                        print("La VRF indicada es " + vrf)
                        if online_cpe == True:
                                consulta_vrf_borde_8_tun(vrf)
                        if online_cpe == False:
                                Consulta_vrf_ppl(vrf)        

def Numero_interfaz_ppl():
        if num_de_tuneles == 1:
                Login_concentrador_principal()
                Host_taylor 
                correcto=False
                while(not correcto):
                        try:
                                tunnel=(int(input("Ingrese el numero de la interfaz tunel: ")))
                                correcto=True
                        except ValueError:
                                print(" \n ")
                                print("** Debe ingresar una opcion valida **") 
                                Numero_interfaz_ppl()
                                                
                existe_taylor= True                      
                compara_num_tunnel=tn.write(b"sh run interface tunnel " + str(tunnel).encode('ascii') + b"\n" ) 
                time.sleep(1)       
                resultado= tn.read_very_eager().decode('ascii')        
                comparacion=re.search("% Invalid input detected",resultado)              
                if comparacion:                                            
                        # print("El tunel  " + str(tunnel) + " esta diponible para ser creado en el router " + str(Host_taylor) )   
                        existe_taylor= False
                        Numero_interfaz_bkup(tunnel)                                                
                else:                
                        print("El tunel ya existe, intente otro")
                                
                        return Numero_interfaz_ppl()                        
          
        if num_de_tuneles == 8:

                Login_concentrador_principal()
                Host_taylor       
                tunnel=(int(input("Ingrese el numero de la interfaz tunel: ")))
                consulta_hasta= int(tunnel) + 4
                existe_taylor= True
                while int(tunnel) < consulta_hasta:      
                        compara_num_tunnel=tn.write(b"sh run interface tunnel " + str(tunnel).encode('ascii') + b"\n" ) 
                        time.sleep(1)       
                        resultado= tn.read_very_eager().decode('ascii')        
                        comparacion=re.search("% Invalid input detected",resultado)                
                        # print(comparacion)                                                                             
                        if comparacion:                                            
                                # print("El tunel  " + str(tunnel) + " esta diponible para ser creado en el router " + str(Host_taylor) )   
                                existe_taylor= False
                                                
                        else:                
                                print("El tunel ya existe, intente otro")
                                
                                return Numero_interfaz_ppl()
                        tunnel += 1
                if existe_taylor == False:
                        Numero_interfaz_bkup(tunnel - 4)       
          

def Numero_interfaz_bkup(tunnel):
        if num_de_tuneles == 1:
                Login_concentrador_respaldo()
                Host_chagall                
                existe_chagall= True
                compara_num_tunnel=tn.write(b"sh run interface tunnel " + str(tunnel).encode('ascii') + b"\n" )  
                time.sleep(1)       
                resultado= tn.read_very_eager().decode('ascii')        
                comparacion=re.search("% Invalid input detected",resultado)                                                                                                    
                if comparacion:                                               
                        # print("El tunel  " + str(tunnel) + " esta diponible para ser creado en el router " + str(Host_chagall) )                       
                        existe_chagall= False
                        crea_tuneles_ppl(tunnel)                                
                else:                
                        print("El tunel ya existe, intente otro")                                
                        return Numero_interfaz_ppl()                       
               

        if num_de_tuneles == 8:

                Login_concentrador_respaldo()
                Host_chagall
                consulta_hasta= int(tunnel) + 4 
                existe_chagall= True  
                while int(tunnel) < consulta_hasta:      
                        compara_num_tunnel=tn.write(b"sh run interface tunnel " + str(tunnel).encode('ascii') + b"\n" ) 
                        time.sleep(1)       
                        resultado= tn.read_very_eager().decode('ascii')        
                        comparacion=re.search("% Invalid input detected",resultado)
                        # print(comparacion)                                                                             
                        if comparacion:                                               
                                # print("El tunel  " + str(tunnel) + " esta diponible para ser creado en el router " + str(Host_chagall) )                       
                                existe_chagall= False
                                
                        else:                
                                print("El tunel ya existe, intente otro")
                                
                                return Numero_interfaz_ppl()
                        tunnel += 1
                if existe_chagall == False:
                        crea_tuneles_ppl(tunnel - 4)

                
def crea_tuneles_ppl(tunnel):
        if num_de_tuneles == 1:
                Login_concentrador_principal()              
                tn.write(b"configure terminal \n")             
                tn.write(b"interface tunnel " + str(tunnel).encode('ascii') + b"\n")                        
                return crea_tuneles_bkup(tunnel)
        if num_de_tuneles == 8:
                Login_concentrador_principal()              
                tn.write(b"configure terminal \n")              
                crea_hasta= int(tunnel) + 4 
                while int(tunnel) < crea_hasta:                
                        tn.write(b"interface tunnel " + str(tunnel).encode('ascii') + b"\n")                        
                        tunnel += 1
                return crea_tuneles_bkup(tunnel)

                 
def crea_tuneles_bkup(tunnel):
        if num_de_tuneles == 1:                       
                time.sleep(2)
                Login_concentrador_respaldo()
                tn.write(b"configure terminal \n")                
                # siguiente_tunnel= int(tunnel) + 4
                 
                tn.write(b"interface tunnel " + str(tunnel).encode('ascii') + b"\n")                             
                return borrar_tuneles(tunnel)
        if num_de_tuneles == 8:
                tunnel= tunnel - 4        
                time.sleep(2)
                Login_concentrador_respaldo()
                tn.write(b"configure terminal \n")                
                crea_hasta= int(tunnel) + 4 
                while int(tunnel) < crea_hasta:                
                        tn.write(b"interface tunnel " + str(tunnel).encode('ascii') + b"\n")                        
                        tunnel += 1 
                return borrar_tuneles(tunnel - 4)
                

def borrar_tuneles(tunnel):
        if num_de_tuneles == 1:  
                print("Se han creado el tunel en Taylor y Chagall: ")    
                print("Tunnel: "+ str(tunnel))                
                print("Si esta todo bien y desea continuar, marque 1: ")
                print("Si existe algun error y necesita borrar los tuneles creados, marque 2: ")
                opcion=int(input("Ingrese su opcion: "))
                if opcion == 1:
                        Ip_tunnel_ppl(tunnel)
                if opcion == 2:
                        print("Se va a borrar el tunel: " + str(tunnel))
                        Login_concentrador_principal()
                        tn.write(b"configure terminal \n")                        
                        tn.write(b"no interface tunnel" + str(tunnel).encode('ascii') + b"\n")                                
                        time.sleep(2)                        
                        Login_concentrador_respaldo()                
                        tn.write(b"configure terminal \n")
                        tn.write(b"no interface tunnel" + str(tunnel).encode('ascii') + b"\n")                                
                        print("Se han borrado todos los tuneles creados anteriormente")
                        Numero_interfaz_ppl()
        if num_de_tuneles == 8:
                print("Se han creado los siguientes tuneles en Taylor y Chagall: ")    
                borrar_hasta= int(tunnel) + 4 
                while int(tunnel) < borrar_hasta:               
                        print("Tunnel: "+ str(tunnel))
                        tunnel += 1
                tunnel = tunnel - 4 
                print("Si esta todo bien y desea continuar, marque 1: ")
                print("Si existe algun error y necesita borrar los tuneles creados, marque 2: ")
                opcion=int(input("Ingrese su opcion: "))
                if opcion == 1:
                        Ip_tunnel_ppl(tunnel)
                if opcion == 2:
                        print("Aqui empiezo a borrar desde el tunel: " + str(tunnel))
                        Login_concentrador_principal()
                        tn.write(b"configure terminal \n")
                        while int(tunnel) < borrar_hasta:
                                tn.write(b"no interface tunnel" + str(tunnel).encode('ascii') + b"\n")
                                tunnel += 1
                        time.sleep(3)
                        tunnel = tunnel - 4 
                        Login_concentrador_respaldo()                
                        tn.write(b"configure terminal \n")
                        while int(tunnel) < borrar_hasta:
                                tn.write(b"no interface tunnel" + str(tunnel).encode('ascii') + b"\n")
                                tunnel += 1
                        print("Se han borrado todos los tuneles creados anteriormente")
                        Numero_interfaz_ppl()                        
                
def Auntentica_taylor():
        global auth_taylor
        number_of_strings = 1
        length_of_string = 8
        for x in range(number_of_strings):
                auth_taylor=(''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string)))
        compara_auth=tn.write(b"do sh run | in authentication \n" )
        time.sleep(2)
        tn.write(b" \n")        
        tn.write(b" \n") 
        resultado= tn.read_very_eager().decode('ascii')        
        comparacion=re.search(auth_taylor,resultado)         
        if comparacion:                                                
                print("La clave de autenticacion existe, intente con otra") 
                Auntentica_taylor()
        else:               
                print("Auntenticacion OK") 
                return auth_taylor                   
def Auntentica_chagall():
        global auth_chagall
        number_of_strings = 1
        length_of_string = 8
        for x in range(number_of_strings):
                auth_chagall=(''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string)))
        compara_auth=tn.write(b"do sh run | in authentication \n" )
        time.sleep(2)
        tn.write(b" \n")        
        tn.write(b" \n") 
        resultado= tn.read_very_eager().decode('ascii')        
        comparacion=re.search(auth_chagall,resultado)         
        if comparacion:                                                
                print("La clave de autenticacion existe, intente con otra") 
                Auntentica_chagall()
        else:               
                print("Auntenticacion OK") 
                return auth_chagall                   


def Ip_tunnel_ppl(tunnel):
        global key_taylor_dato_ftth, key_taylor_dato_xg, key_taylor_admin_xg,key_taylor_admin_ftth, auth_taylor_dato_xg, auth_taylor_dato_ftth, auth_taylor_admin_xg, auth_taylor_adm_ftth, ipv4_tun_taylor_vrf_datos, ipv4_tun_taylor_vrf_admin, ipv4_tun_taylor, ipv4_borde_a_taylor, ipv4_borde_a_taylor_xg, ipv4_borde_a_taylor_datos_ftth, ipv4_borde_a_taylor_datos_xg, ipv4_tun_taylor_vrf_admin_xg, ipv4_tun_taylor_vrf_datos_xg 
        if num_de_tuneles == 1:
                        
                Login_concentrador_principal()
                Consulta_key_taylor(tunnel)
                Auntentica_taylor()                 
                mask=" 255.255.255.252" 
                
                correcto=False
                while(not correcto):
                        try:
                                ip_tun_taylor=(input("Ingrese la ip del tunel para Taylor SIN la mascara: ")) 
                                ipv4_tun_taylor = ipaddress.ip_address(ip_tun_taylor)
                                correcto=True
                        except ValueError:
                                print(" \n ")
                                print("** Debe ingresar una opcion valida **")  

                ipv4_borde_a_taylor = ipv4_tun_taylor + 1           
                consuta=tn.write(b"sh ip interface brief | include " + str(ipv4_tun_taylor).encode('ascii') + b"\n" )                
                time.sleep(1)
                resultado= tn.read_very_eager().decode('ascii') 
                comparacion=re.search("YES",resultado)         
                if comparacion:                                                
                        print("La ip ya esta en uso, utilice otra ip!") 
                        Ip_tunnel_ppl(tunnel)   

                tn.write(b"configure terminal \n")
                tn.write(b"interface tunnel " + str(tunnel).encode('ascii') + b"\n")                

                if vrf == "admin" and tipo_conexion == "xg" and online_cpe == True:
                        tn.write(b"ip vrf forwarding cuanta \n")
                        tn.write(b"ip address " + str(ipv4_tun_taylor).encode('ascii') + str(mask).encode('ascii') + b"\n")
                        ipv4_borde_a_taylor_xg = ipv4_tun_taylor +1
                        tn.write(b"description tun" + str(tunnel).encode('ascii') + b" a tun22 en " + str(router_name[2:-1].strip()).encode('ascii') + b" del servicio ADMIN - XG \n")
                        tn.write(b"ip nhrp responder Loopback0 \n")
                        tn.write(b"tunnel source Loopback0 \n")
                        tn.write(b"tunnel protection ipsec profile lab shared \n")
                        tn.write(b"delay 20000 \n")
                                         
                        
                if vrf == "admin" and tipo_conexion == "ftth/vsat" and online_cpe == True:
                        tn.write(b"ip vrf forwarding cuanta \n")
                        tn.write(b"ip address " + str(ipv4_tun_taylor).encode('ascii') + str(mask).encode('ascii') + b"\n")
                        ipv4_borde_a_taylor = ipv4_tun_taylor + 1
                        tn.write(b"description tun" + str(tunnel).encode('ascii') + b" a tun10 en " + str(router_name[2:-1].strip()).encode('ascii') + b" del servicio ADMIN - FTTH/VSAT \n")
                        tn.write(b"ip nhrp responder Loopback1 \n")
                        tn.write(b"tunnel source Loopback1 \n")
                        tn.write(b"tunnel protection ipsec profile LAB2 shared \n")

                if vrf != "admin" and tipo_conexion == "xg" and online_cpe == True:
                        tn.write(b"ip vrf forwarding " + str(vrf).encode('ascii') + b"\n") 
                        tn.write(b"ip address " + str(ipv4_tun_taylor).encode('ascii') + str(mask).encode('ascii') + b"\n")
                        ipv4_borde_a_taylor_datos_xg = ipv4_tun_taylor + 1
                        tn.write(b"description tun" + str(tunnel).encode('ascii') + b" a tun21 en " + str(router_name[2:-1].strip()).encode('ascii') + b" del servicio DATOS - XG \n")
                        tn.write(b"ip nhrp responder Loopback0 \n")
                        tn.write(b"tunnel source Loopback0 \n")
                        tn.write(b"tunnel protection ipsec profile lab shared \n")
                        tn.write(b"delay 20000 \n")

                if vrf != "admin" and tipo_conexion == "ftth/vsat" and online_cpe == True:
                        tn.write(b"ip vrf forwarding " + str(vrf).encode('ascii') + b"\n") 
                        tn.write(b"ip address " + str(ipv4_tun_taylor).encode('ascii') + str(mask).encode('ascii') + b"\n")
                        ipv4_borde_a_taylor_datos_ftth = ipv4_tun_taylor + 1
                        tn.write(b"description tun" + str(tunnel).encode('ascii') + b" a tun1 en " + str(router_name[2:-1].strip()).encode('ascii') + b" del servicio DATOS - FTTH/VSAT \n")
                        tn.write(b"ip nhrp responder Loopback1 \n")
                        tn.write(b"tunnel source Loopback1 \n")
                        tn.write(b"tunnel protection ipsec profile LAB2 shared \n")
                        
                
                if vrf == "admin" and tipo_conexion == "xg" and online_cpe == False:
                        tn.write(b"ip vrf forwarding cuanta \n")
                        tn.write(b"ip address " + str(ipv4_tun_taylor).encode('ascii') + str(mask).encode('ascii') + b"\n")
                        ipv4_borde_a_taylor_xg = ipv4_tun_taylor + 1
                        tn.write(b"description tun" + str(tunnel).encode('ascii') + b" a tun22 en " + str(nombre_cpe).encode('ascii') + b" del servicio ADMIN - XG \n")
                        tn.write(b"ip nhrp responder Loopback0 \n")
                        tn.write(b"tunnel source Loopback0 \n")
                        tn.write(b"tunnel protection ipsec profile lab shared \n")
                        tn.write(b"delay 20000 \n")
                                         
                        
                if vrf == "admin" and tipo_conexion == "ftth/vsat" and online_cpe == False:
                        tn.write(b"ip vrf forwarding cuanta \n")
                        tn.write(b"ip address " + str(ipv4_tun_taylor).encode('ascii') + str(mask).encode('ascii') + b"\n")
                        ipv4_borde_a_taylor = ipv4_tun_taylor + 1
                        tn.write(b"description tun" + str(tunnel).encode('ascii') + b" a tun10 en " + str(nombre_cpe).encode('ascii') + b" del servicio ADMIN - FTTH/VSAT \n")
                        tn.write(b"ip nhrp responder Loopback1 \n")
                        tn.write(b"tunnel source Loopback1 \n")
                        tn.write(b"tunnel protection ipsec profile LAB2 shared \n")

                if vrf != "admin" and tipo_conexion == "xg" and online_cpe == False:
                        tn.write(b"ip vrf forwarding " + str(vrf).encode('ascii') + b"\n") 
                        tn.write(b"ip address " + str(ipv4_tun_taylor).encode('ascii') + str(mask).encode('ascii') + b"\n")
                        ipv4_borde_a_taylor_datos_xg = ipv4_tun_taylor + 1
                        tn.write(b"description tun" + str(tunnel).encode('ascii') + b" a tun21 en " + str(nombre_cpe).encode('ascii') + b" del servicio DATOS - XG \n")
                        tn.write(b"ip nhrp responder Loopback0 \n")
                        tn.write(b"tunnel source Loopback0 \n")
                        tn.write(b"tunnel protection ipsec profile lab shared \n")
                        tn.write(b"delay 20000 \n")

                if vrf != "admin" and tipo_conexion == "ftth/vsat" and online_cpe == False:
                        tn.write(b"ip vrf forwarding " + str(vrf).encode('ascii') + b"\n") 
                        tn.write(b"ip address " + str(ipv4_tun_taylor).encode('ascii') + str(mask).encode('ascii') + b"\n")
                        ipv4_borde_a_taylor_datos_ftth = ipv4_tun_taylor + 1
                        tn.write(b"description tun" + str(tunnel).encode('ascii') + b" a tun1 en " + str(nombre_cpe).encode('ascii') + b" del servicio DATOS - FTTH/VSAT \n")
                        tn.write(b"ip nhrp responder Loopback1 \n")
                        tn.write(b"tunnel source Loopback1 \n")
                        tn.write(b"tunnel protection ipsec profile LAB2 shared \n")         
                        
                tn.write(b"no ip redirects \n")
                tn.write(b"ip mtu 1344 \n")               
                tn.write(b"ip nhrp map multicast dynamic \n")                 
                tn.write(b"ip nhrp holdtime 300 \n") 
                tn.write(b"ip tcp adjust-mss 1300 \n") 
                tn.write(b"tunnel mode gre multipoint \n") 
                tn.write(b"tunnel path-mtu-discovery \n")                              
                tn.write(b"ip nhrp network-id " + str(key_taylor).encode('ascii') + b"\n")
                tn.write(b"tunnel key " + str(key_taylor).encode('ascii') + b"\n")                
                time.sleep(1)
                tn.write(b"ip nhrp authentication " + auth_taylor.encode('ascii') + b"\n") 
                time.sleep(1)               
                ip_tunnel_bkup(tunnel, ipv4_tun_taylor)

        if num_de_tuneles == 8:

                print("\b") 
                print("** Para vrf ADMIN del servicio FTTH/VSAT en Taylor ** ")
                print("\b")  
                Login_concentrador_principal()
                Consulta_key_taylor(tunnel)
                Auntentica_taylor()                
                mask=" 255.255.255.252"
                
                correcto=False
                while(not correcto):
                        try:
                                ip_tun_taylor_vrf_admin=(input("Ingrese la ip SIN la mascara: "))
                                ipv4_tun_taylor_vrf_admin = ipaddress.ip_address(ip_tun_taylor_vrf_admin)
                                correcto=True
                        except ValueError:
                                print(" \n ")
                                print("** Debe ingresar una opcion valida **")              
                                

                
                ipv4_borde_a_taylor = ipv4_tun_taylor_vrf_admin + 1                  
                consuta=tn.write(b"sh ip interface brief | include " + str(ipv4_tun_taylor_vrf_admin).encode('ascii') + b"\n" )                
                time.sleep(1)
                resultado= tn.read_very_eager().decode('ascii') 
                comparacion=re.search("YES",resultado)         
                if comparacion:                                                
                        print("La ip ya esta en uso, utilice otra ip!") 
                        Ip_tunnel_ppl(tunnel)                
                tn.write(b"configure terminal \n")  
                tn.write(b"interface tunnel " + str(tunnel).encode('ascii') + b"\n") 
                tn.write(b"ip vrf forwarding cuanta \n")                          
                tn.write(b"ip address " + str(ipv4_tun_taylor_vrf_admin).encode('ascii') + str(mask).encode('ascii') + b"\n")
                if online_cpe == True:
                        tn.write(b"description tun" + str(tunnel).encode('ascii') + b" a tun10 en " + str(router_name[2:-1].strip()).encode('ascii') + b" del servicio ADMIN FTTH/VSAT \n")
                else:
                        tn.write(b"description tun" + str(tunnel).encode('ascii') + b" a tun10 en " + str(nombre_cpe).encode('ascii') + b" del servicio ADMIN FTTH/VSAT \n")
                tn.write(b"no ip redirects \n")
                tn.write(b"ip mtu 1344 \n")                
                tn.write(b"ip nhrp responder Loopback1 \n") 
                tn.write(b"ip nhrp map multicast dynamic \n")                 
                tn.write(b"ip nhrp holdtime 300 \n") 
                tn.write(b"ip tcp adjust-mss 1300 \n") 
                tn.write(b"tunnel source Loopback1 \n") 
                tn.write(b"tunnel mode gre multipoint \n") 
                tn.write(b"tunnel path-mtu-discovery \n") 
                tn.write(b"tunnel protection ipsec profile LAB2 shared \n")                
                tn.write(b"ip nhrp network-id " + str(key_taylor).encode('ascii') + b"\n")
                tn.write(b"tunnel key " + str(key_taylor).encode('ascii') + b"\n")
                key_taylor_admin_ftth = key_taylor 
                key_taylor_4_tun = key_taylor + 1                
                time.sleep(1)
                auth_taylor_adm_ftth = auth_taylor
                tn.write(b"ip nhrp authentication " + auth_taylor_adm_ftth.encode('ascii') + b"\n") 
                time.sleep(1) 
                print("Se creo el tunel " + str(tunnel) + " con la ip " + str(ipv4_tun_taylor_vrf_admin) + str(mask))
                time.sleep(1)
                

                print("\b") 
                print("** Para vrf ADMIN del servicio XG en Taylor **")
                print("\b") 

                valida_key_taylor(tunnel + 1, key_taylor_4_tun )
                Auntentica_taylor() 
                ipv4_tun_taylor_vrf_admin_xg = ipv4_tun_taylor_vrf_admin + 8 
                ipv4_borde_a_taylor_xg = ipv4_tun_taylor_vrf_admin_xg +1              
                consuta=tn.write(b"sh ip interface brief | include " + str(ipv4_tun_taylor_vrf_admin_xg).encode('ascii') + b"\n" )                
                time.sleep(1)
                resultado= tn.read_very_eager().decode('ascii') 
                comparacion=re.search("YES",resultado)         
                if comparacion:                                                
                        print("La ip ya esta en uso, utilice otra ip!") 
                        Ip_tunnel_ppl(tunnel)
                tunnel = tunnel + 1                
                tn.write(b"configure terminal \n")                  
                tn.write(b"interface tunnel " + str(tunnel).encode('ascii') + b"\n") 
                tn.write(b"ip vrf forwarding cuanta \n")                          
                tn.write(b"ip address " + str(ipv4_tun_taylor_vrf_admin_xg).encode('ascii') + str(mask).encode('ascii') + b"\n")
                if online_cpe == True:
                        tn.write(b"description tun" + str(tunnel).encode('ascii') + b" a tun22 en " + str(router_name[2:-1].strip()).encode('ascii') + b" del servicio ADMIN XG \n")
                else:
                        tn.write(b"description tun" + str(tunnel).encode('ascii') + b" a tun22 en " + str(nombre_cpe).encode('ascii') + b" del servicio ADMIN XG \n")
                tn.write(b"no ip redirects \n")
                tn.write(b"ip mtu 1344 \n")                
                tn.write(b"ip nhrp responder Loopback0 \n") 
                tn.write(b"ip nhrp map multicast dynamic \n")                 
                tn.write(b"ip nhrp holdtime 300 \n") 
                tn.write(b"ip tcp adjust-mss 1300 \n") 
                tn.write(b"tunnel source Loopback0 \n") 
                tn.write(b"tunnel mode gre multipoint \n") 
                tn.write(b"tunnel path-mtu-discovery \n") 
                tn.write(b"delay 20000 \n") 
                tn.write(b"tunnel protection ipsec profile lab shared \n")                
                tn.write(b"ip nhrp network-id " + str(key_taylor_4_tun).encode('ascii') + b"\n")
                tn.write(b"tunnel key " + str(key_taylor_4_tun).encode('ascii') + b"\n")
                key_taylor_admin_xg = key_taylor_4_tun
                key_taylor_4_tun +=1                
                time.sleep(1)
                auth_taylor_admin_xg = auth_taylor
                tn.write(b"ip nhrp authentication " + auth_taylor_admin_xg.encode('ascii') + b"\n") 
                time.sleep(1) 
                print("Se creo el tunel " + str(tunnel) + " con la ip " + str(ipv4_tun_taylor_vrf_admin_xg) + mask )
                time.sleep(1)

                print("\b") 
                print("** Para vrf DATOS del servicio FTTH/VSAT en Taylor **")
                print("\b") 

                valida_key_taylor(tunnel + 1, key_taylor_4_tun )
                Auntentica_taylor()

                correcto=False
                while(not correcto):
                        try:
                                ip_tun_taylor_vrf_datos=(input("Ingrese la ip SIN la mascara: "))
                                ipv4_tun_taylor_vrf_datos = ipaddress.ip_address(ip_tun_taylor_vrf_datos)
                                correcto=True
                        except ValueError:
                                print(" \n ")
                                print("** Debe ingresar una opcion valida **")              
                ipv4_borde_a_taylor_datos_ftth = ipv4_tun_taylor_vrf_datos +1
                consuta=tn.write(b"sh ip interface brief | include " + str(ipv4_tun_taylor_vrf_datos).encode('ascii') + b"\n" )
                time.sleep(1)
                resultado= tn.read_very_eager().decode('ascii') 
                comparacion=re.search("YES",resultado)         
                if comparacion:                                                
                        print("La ip ya esta en uso, utilice otra ip!") 
                        Ip_tunnel_ppl(tunnel)                 
                tn.write(b"configure terminal \n")
                tunnel = tunnel + 1    
                tn.write(b"interface tunnel " + str(tunnel).encode('ascii') + b"\n") 
                tn.write(b"ip vrf forwarding " + str(vrf).encode('ascii') + b"\n")                           
                tn.write(b"ip address " + str(ipv4_tun_taylor_vrf_datos).encode('ascii') + str(mask).encode('ascii') + b"\n")
                if online_cpe == True:
                        tn.write(b"description tun" + str(tunnel).encode('ascii') + b" a tun1 en " + str(router_name[2:-1].strip()).encode('ascii') + b" del servicio DATOS FTTH/VSAT \n")
                else:
                        tn.write(b"description tun" + str(tunnel).encode('ascii') + b" a tun1 en " + str(nombre_cpe).encode('ascii') + b" del servicio DATOS FTTH/VSAT \n")                
                tn.write(b"no ip redirects \n")
                tn.write(b"ip mtu 1344 \n")                
                tn.write(b"ip nhrp responder Loopback1 \n") 
                tn.write(b"ip nhrp map multicast dynamic \n")                 
                tn.write(b"ip nhrp holdtime 300 \n") 
                tn.write(b"ip tcp adjust-mss 1300 \n") 
                tn.write(b"tunnel source Loopback1 \n") 
                tn.write(b"tunnel mode gre multipoint \n") 
                tn.write(b"tunnel path-mtu-discovery \n")                  
                tn.write(b"tunnel protection ipsec profile LAB2 shared \n")                
                tn.write(b"ip nhrp network-id " + str(key_taylor_4_tun).encode('ascii') + b"\n")
                tn.write(b"tunnel key " + str(key_taylor_4_tun).encode('ascii') + b"\n")
                key_taylor_dato_ftth = key_taylor_4_tun
                key_taylor_4_tun +=1                     
                time.sleep(1)
                auth_taylor_dato_ftth = auth_taylor
                tn.write(b"ip nhrp authentication " + auth_taylor_dato_ftth.encode('ascii') + b"\n") 
                time.sleep(1) 
                print("Se creo el tunel " + str(tunnel) + " con la ip " + str(ipv4_tun_taylor_vrf_datos) + str(mask))
                time.sleep(1)

                print("\b") 
                print("** Para vrf DATOS del servicio XG en Taylor **")
                print("\b") 

                valida_key_taylor(tunnel + 1, key_taylor_4_tun )
                Auntentica_taylor() 
                ipv4_tun_taylor_vrf_datos_xg = ipv4_tun_taylor_vrf_datos + 8
                ipv4_borde_a_taylor_datos_xg = ipv4_tun_taylor_vrf_datos_xg + 1                
                consuta=tn.write(b"sh ip interface brief | include " + str(ipv4_tun_taylor_vrf_datos_xg).encode('ascii') + b"\n" )                
                time.sleep(1)
                resultado= tn.read_very_eager().decode('ascii') 
                comparacion=re.search("YES",resultado)         
                if comparacion:                                                
                        print("La ip ya esta en uso, utilice otra ip!") 
                        Ip_tunnel_ppl(tunnel)                
                tn.write(b"configure terminal \n")
                tunnel = tunnel + 1  
                tn.write(b"interface tunnel " + str(tunnel).encode('ascii') + b"\n")  
                tn.write(b"ip vrf forwarding " + str(vrf).encode('ascii') + b"\n")                          
                tn.write(b"ip address " + str(ipv4_tun_taylor_vrf_datos_xg).encode('ascii') + str(mask).encode('ascii') + b"\n")
                if online_cpe == True:
                        tn.write(b"description tun" + str(tunnel).encode('ascii') + b" a tun21 en " + str(router_name[2:-1].strip()).encode('ascii') + b" del servicio DATOS XG \n")
                else:
                        tn.write(b"description tun" + str(tunnel).encode('ascii') + b" a tun21 en " + str(nombre_cpe).encode('ascii') + b" del servicio DATOS XG \n")                
                tn.write(b"no ip redirects \n")
                tn.write(b"ip mtu 1344 \n")                
                tn.write(b"ip nhrp responder Loopback0 \n") 
                tn.write(b"ip nhrp map multicast dynamic \n")                 
                tn.write(b"ip nhrp holdtime 300 \n") 
                tn.write(b"ip tcp adjust-mss 1300 \n") 
                tn.write(b"tunnel source Loopback0 \n") 
                tn.write(b"tunnel mode gre multipoint \n") 
                tn.write(b"tunnel path-mtu-discovery \n")
                tn.write(b"delay 20000 \n")                   
                tn.write(b"tunnel protection ipsec profile lab shared \n")                
                tn.write(b"ip nhrp network-id " + str(key_taylor_4_tun).encode('ascii') + b"\n")
                tn.write(b"tunnel key " + str(key_taylor_4_tun).encode('ascii') + b"\n")
                key_taylor_dato_xg = key_taylor_4_tun               
                time.sleep(1)
                auth_taylor_dato_xg = auth_taylor
                tn.write(b"ip nhrp authentication " + auth_taylor_dato_xg.encode('ascii') + b"\n") 
                time.sleep(1) 
                print("Se creo el tunel " + str(tunnel) + " con la ip " + str(ipv4_tun_taylor_vrf_datos_xg) + mask )
                time.sleep(1)
                tunnel= tunnel - 3

                ip_tunnel_bkup(tunnel, ipv4_tun_taylor_vrf_admin)      


def ip_tunnel_bkup(tunnel, ipv4_tun_taylor):
        global key_chagall_dato_xg, key_chagall_dato_ftth ,key_chagall_admin_xg, key_chagall_admin_ftth, auth_chagall_dato_xg, auth_chagall_dato_ftth, auth_chagall_admin_xg, auth_chagall_admin_ftth, ipv4_tun_chagall_vrf_datos, ipv4_tun_chagall_vrf_datos_xg, ipv4_borde_a_chagall, ipv4_tun_chagall, ipv4_borde_a_chagall_xg, ipv4_borde_a_chagall_dato_ftth, ipv4_borde_a_chagall_dato_xg, ipv4_tun_chagall_vrf_admin_xg, ipv4_tun_chagall_vrf_admin
        if num_de_tuneles == 1:
                                       
                Login_concentrador_respaldo()
                Consulta_key_chagall(tunnel)
                Auntentica_chagall()                  
                mask=" 255.255.255.252"
                ipv4_tun_chagall= ipv4_tun_taylor + 4 
                ipv4_borde_a_chagall = ipv4_tun_chagall + 1               
                consuta=tn.write(b"sh ip interface brief | include " + str(ipv4_tun_chagall).encode('ascii') + b"\n" )                
                time.sleep(1)
                resultado= tn.read_very_eager().decode('ascii') 
                comparacion=re.search("YES",resultado)         
                if comparacion:                                                
                        print("La ip ya esta en uso en Chagall, utilice otra ip!") 
                        Ip_tunnel_ppl(tunnel)                
                tn.write(b"configure terminal \n")  
                tn.write(b"interface tunnel " + str(tunnel).encode('ascii') + b"\n")                           
                                         
                if vrf == "admin" and tipo_conexion == "xg" and online_cpe == True:
                        tn.write(b"ip vrf forwarding cuanta \n")
                        tn.write(b"ip address " + str(ipv4_tun_chagall).encode('ascii') + str(mask).encode('ascii') + b"\n")
                        ipv4_borde_a_chagall_xg= ipv4_tun_chagall + 1
                        tn.write(b"description tun" + str(tunnel).encode('ascii') + b" a tun42 en " + str(router_name[2:-1].strip()).encode('ascii') + b" del servicio ADMIN - XG \n")
                        tn.write(b"ip nhrp responder Loopback0 \n")
                        tn.write(b"tunnel source Loopback0 \n")
                        tn.write(b"tunnel protection ipsec profile RIEMANN_CEL shared \n")
                        tn.write(b"delay 70000 \n")               
                        
                if vrf == "admin" and tipo_conexion == "ftth/vsat" and online_cpe == True:
                        tn.write(b"ip vrf forwarding cuanta \n")
                        tn.write(b"ip address " + str(ipv4_tun_chagall).encode('ascii') + str(mask).encode('ascii') + b"\n")
                        ipv4_borde_a_chagall= ipv4_tun_chagall + 1
                        tn.write(b"description tun" + str(tunnel).encode('ascii') + b" a tun20 en " + str(router_name[2:-1].strip()).encode('ascii') + b" del servicio ADMIN - FTTH/VSAT \n")
                        tn.write(b"ip nhrp responder Loopback1 \n")
                        tn.write(b"tunnel source Loopback1 \n")
                        tn.write(b"tunnel protection ipsec profile RIEMANN_FO shared \n")
                        tn.write(b"delay 40000 \n")

                if vrf != "admin" and tipo_conexion == "xg" and online_cpe == True:
                        tn.write(b"ip vrf forwarding " + str(vrf).encode('ascii') + b"\n") 
                        tn.write(b"ip address " + str(ipv4_tun_chagall).encode('ascii') + str(mask).encode('ascii') + b"\n")
                        ipv4_borde_a_chagall_dato_xg= ipv4_tun_chagall + 1
                        tn.write(b"description tun" + str(tunnel).encode('ascii') + b" a tun41 en " + str(router_name[2:-1].strip()).encode('ascii') + b" del servicio DATOS - XG \n")
                        tn.write(b"ip nhrp responder Loopback0 \n")
                        tn.write(b"tunnel source Loopback0 \n")
                        tn.write(b"tunnel protection ipsec profile RIEMANN_CEL shared \n")
                        tn.write(b"delay 70000 \n")

                if vrf != "admin" and tipo_conexion == "ftth/vsat" and online_cpe == True:
                        tn.write(b"ip vrf forwarding " + str(vrf).encode('ascii') + b"\n") 
                        tn.write(b"ip address " + str(ipv4_tun_chagall).encode('ascii') + str(mask).encode('ascii') + b"\n")
                        ipv4_borde_a_chagall_dato_ftth= ipv4_tun_chagall + 1
                        tn.write(b"description tun" + str(tunnel).encode('ascii') + b" a tun2 en " + str(router_name[2:-1].strip()).encode('ascii') + b" del servicio DATOS - FTTH/VSAT \n")
                        tn.write(b"ip nhrp responder Loopback1 \n")
                        tn.write(b"tunnel source Loopback1 \n")
                        tn.write(b"tunnel protection ipsec profile RIEMANN_FO shared \n")
                        tn.write(b"delay 40000 \n")   
                
                
                if vrf == "admin" and tipo_conexion == "xg" and online_cpe == False:
                        tn.write(b"ip vrf forwarding cuanta \n")
                        tn.write(b"ip address " + str(ipv4_tun_chagall).encode('ascii') + str(mask).encode('ascii') + b"\n")
                        ipv4_borde_a_chagall_xg= ipv4_tun_chagall + 1
                        tn.write(b"description tun" + str(tunnel).encode('ascii') + b" a tun42 en " + str(nombre_cpe).encode('ascii') + b" del servicio ADMIN - XG \n")
                        tn.write(b"ip nhrp responder Loopback0 \n")
                        tn.write(b"tunnel source Loopback0 \n")
                        tn.write(b"tunnel protection ipsec profile RIEMANN_CEL shared \n")
                        tn.write(b"delay 70000 \n")               
                        
                if vrf == "admin" and tipo_conexion == "ftth/vsat" and online_cpe == False:
                        tn.write(b"ip vrf forwarding cuanta \n")
                        tn.write(b"ip address " + str(ipv4_tun_chagall).encode('ascii') + str(mask).encode('ascii') + b"\n")
                        ipv4_borde_a_chagall= ipv4_tun_chagall + 1
                        tn.write(b"description tun" + str(tunnel).encode('ascii') + b" a tun20 en " + str(nombre_cpe).encode('ascii') + b" del servicio ADMIN - FTTH/VSAT \n")
                        tn.write(b"ip nhrp responder Loopback1 \n")
                        tn.write(b"tunnel source Loopback1 \n")
                        tn.write(b"tunnel protection ipsec profile RIEMANN_FO shared \n")
                        tn.write(b"delay 40000 \n")

                if vrf != "admin" and tipo_conexion == "xg" and online_cpe == False:
                        tn.write(b"ip vrf forwarding " + str(vrf).encode('ascii') + b"\n") 
                        tn.write(b"ip address " + str(ipv4_tun_chagall).encode('ascii') + str(mask).encode('ascii') + b"\n")
                        ipv4_borde_a_chagall_dato_xg= ipv4_tun_chagall + 1
                        tn.write(b"description tun" + str(tunnel).encode('ascii') + b" a tun41 en " + str(nombre_cpe).encode('ascii') + b" del servicio DATOS - XG \n")
                        tn.write(b"ip nhrp responder Loopback0 \n")
                        tn.write(b"tunnel source Loopback0 \n")
                        tn.write(b"tunnel protection ipsec profile RIEMANN_CEL shared \n")
                        tn.write(b"delay 70000 \n")

                if vrf != "admin" and tipo_conexion == "ftth/vsat" and online_cpe == False:
                        tn.write(b"ip vrf forwarding " + str(vrf).encode('ascii') + b"\n") 
                        tn.write(b"ip address " + str(ipv4_tun_chagall).encode('ascii') + str(mask).encode('ascii') + b"\n")
                        ipv4_borde_a_chagall_dato_ftth= ipv4_tun_chagall + 1
                        tn.write(b"description tun" + str(tunnel).encode('ascii') + b" a tun2 en " + str(nombre_cpe).encode('ascii') + b" del servicio DATOS - FTTH/VSAT \n")
                        tn.write(b"ip nhrp responder Loopback1 \n")
                        tn.write(b"tunnel source Loopback1 \n")
                        tn.write(b"tunnel protection ipsec profile RIEMANN_FO shared \n")
                        tn.write(b"delay 40000 \n")   
                                                             
                                                 
                tn.write(b"no ip redirects \n")
                tn.write(b"ip mtu 1344 \n")               
                tn.write(b"ip nhrp map multicast dynamic \n")                 
                tn.write(b"ip nhrp holdtime 300 \n") 
                tn.write(b"ip tcp adjust-mss 1300 \n") 
                tn.write(b"tunnel mode gre multipoint \n") 
                tn.write(b"tunnel path-mtu-discovery \n")                
                tn.write(b"ip nhrp network-id " + str(key_chagall).encode('ascii') + b"\n")
                tn.write(b"tunnel key " + str(key_chagall).encode('ascii') + b"\n")
                time.sleep(1)
                tn.write(b"ip nhrp authentication " + auth_chagall.encode('ascii') + b"\n") 
                time.sleep(1)
                tuneles_borde(tunnel, ipv4_borde_a_taylor, ipv4_borde_a_chagall)                            

        if num_de_tuneles == 8: 

                print("\b")           
                print("** Para vrf ADMIN del servicio FTTH/VSAT en Chagall **")
                print("\b") 
                Login_concentrador_respaldo()
                Consulta_key_chagall(tunnel)
                Auntentica_chagall()                  
                mask=" 255.255.255.252"
                ipv4_tun_chagall_vrf_admin= ipv4_tun_taylor_vrf_admin + 4 
                ipv4_borde_a_chagall = ipv4_tun_chagall_vrf_admin + 1                             
                consuta=tn.write(b"sh ip interface brief | include " + str(ipv4_tun_chagall_vrf_admin).encode('ascii') + b"\n" )
                time.sleep(1)
                resultado= tn.read_very_eager().decode('ascii') 
                comparacion=re.search("YES",resultado)         
                if comparacion:                                                
                        print("La ip ya esta en uso, utilice otra ip!") 
                        Ip_tunnel_ppl(tunnel)                 
                tn.write(b"configure terminal \n")                  
                tn.write(b"interface tunnel " + str(tunnel).encode('ascii') + b"\n")  
                tn.write(b"ip vrf forwarding cuanta \n")                           
                tn.write(b"ip address " + str(ipv4_tun_chagall_vrf_admin).encode('ascii') + str(mask).encode('ascii') + b"\n")
                if online_cpe == True:
                        tn.write(b"description tun" + str(tunnel).encode('ascii') + b" a tun20 en " + str(router_name[2:-1].strip()).encode('ascii') + b" del servicio ADMIN FTTH/VSAT \n")
                else:
                        tn.write(b"description tun" + str(tunnel).encode('ascii') + b" a tun20 en " + str(nombre_cpe).encode('ascii') + b" del servicio ADMIN FTTH/VSAT \n")
                tn.write(b"no ip redirects \n")
                tn.write(b"ip mtu 1344 \n")                
                tn.write(b"ip nhrp responder Loopback1 \n") 
                tn.write(b"ip nhrp map multicast dynamic \n")                 
                tn.write(b"ip nhrp holdtime 300 \n") 
                tn.write(b"ip tcp adjust-mss 1300 \n") 
                tn.write(b"tunnel source Loopback1 \n") 
                tn.write(b"tunnel mode gre multipoint \n") 
                tn.write(b"tunnel path-mtu-discovery \n") 
                tn.write(b"delay 40000 \n") 
                tn.write(b"tunnel protection ipsec profile RIEMANN_FO shared \n")                
                tn.write(b"ip nhrp network-id " + str(key_chagall).encode('ascii') + b"\n")
                tn.write(b"tunnel key " + str(key_chagall).encode('ascii') + b"\n")
                key_chagall_admin_ftth = key_chagall 
                key_chagall_4_tun = key_chagall + 1               
                time.sleep(1)
                auth_chagall_admin_ftth= auth_chagall
                tn.write(b"ip nhrp authentication " + auth_chagall_admin_ftth.encode('ascii') + b"\n") 
                time.sleep(1)
                print("Se creo el tunel " + str(tunnel) + " con la ip " + str(ipv4_tun_chagall_vrf_admin) + str(mask))
                time.sleep(1) 

                print("\b") 
                print("** Para vrf ADMIN del servicio XG en Chagall **")
                print("\b") 

                valida_key_chagall(tunnel + 1, key_chagall_4_tun)
                Auntentica_chagall()
                ipv4_tun_chagall_vrf_admin_xg = ipv4_tun_chagall_vrf_admin + 8
                ipv4_borde_a_chagall_xg = ipv4_tun_chagall_vrf_admin_xg + 1  
                consuta=tn.write(b"sh ip interface brief | include " + str(ipv4_tun_chagall_vrf_admin_xg).encode('ascii') + b"\n" )                
                time.sleep(1)
                resultado= tn.read_very_eager().decode('ascii') 
                comparacion=re.search("YES",resultado)         
                if comparacion:                                                
                        print("La ip ya esta en uso, utilice otra ip!") 
                        Ip_tunnel_ppl(tunnel)                
                tn.write(b"configure terminal \n")
                tunnel = tunnel + 1  
                tn.write(b"interface tunnel " + str(tunnel).encode('ascii') + b"\n") 
                tn.write(b"ip vrf forwarding cuanta \n")                           
                tn.write(b"ip address " + str(ipv4_tun_chagall_vrf_admin_xg).encode('ascii') + str(mask).encode('ascii') + b"\n")
                if online_cpe == True:
                        tn.write(b"description tun" + str(tunnel).encode('ascii') + b" a tun42 en " + str(router_name[2:-1].strip()).encode('ascii') + b" del servicio ADMIN XG \n") 
                else:
                        tn.write(b"description tun" + str(tunnel).encode('ascii') + b" a tun42 en " + str(nombre_cpe).encode('ascii') + b" del servicio ADMIN XG \n")               
                tn.write(b"no ip redirects \n")
                tn.write(b"ip mtu 1344 \n")                
                tn.write(b"ip nhrp responder Loopback0 \n") 
                tn.write(b"ip nhrp map multicast dynamic \n")                 
                tn.write(b"ip nhrp holdtime 300 \n") 
                tn.write(b"ip tcp adjust-mss 1300 \n") 
                tn.write(b"tunnel source Loopback0 \n") 
                tn.write(b"tunnel mode gre multipoint \n") 
                tn.write(b"tunnel path-mtu-discovery \n") 
                tn.write(b"delay 70000 \n") 
                tn.write(b"tunnel protection ipsec profile RIEMANN_CEL shared \n")                
                tn.write(b"ip nhrp network-id " + str(key_chagall_4_tun).encode('ascii') + b"\n")
                tn.write(b"tunnel key " + str(key_chagall_4_tun).encode('ascii') + b"\n")
                key_chagall_admin_xg = key_chagall_4_tun
                key_chagall_4_tun +=1                
                time.sleep(1)
                auth_chagall_admin_xg = auth_chagall
                tn.write(b"ip nhrp authentication " + auth_chagall_admin_xg.encode('ascii') + b"\n") 
                time.sleep(1)
                print("Se creo el tunel " + str(tunnel) + " con la ip " + str(ipv4_tun_chagall_vrf_admin_xg) + mask )
                time.sleep(1)

                print("\b") 
                print("** Para vrf DATOS del servicio FTTH/VSAT  en Chagall **")
                print("\b") 

                valida_key_chagall(tunnel + 1, key_chagall_4_tun)
                Auntentica_chagall() 
                ipv4_tun_chagall_vrf_datos = ipv4_tun_taylor_vrf_datos + 4
                ipv4_borde_a_chagall_dato_ftth = ipv4_tun_chagall_vrf_datos + 1                   
                consuta=tn.write(b"sh ip interface brief | include " + str(ipv4_tun_chagall_vrf_datos).encode('ascii') + b"\n" )
                time.sleep(1)
                resultado= tn.read_very_eager().decode('ascii') 
                comparacion=re.search("YES",resultado)         
                if comparacion:                                                
                        print("La ip ya esta en uso, utilice otra ip!") 
                        Ip_tunnel_ppl(tunnel)                
                tn.write(b"configure terminal \n")
                tunnel = tunnel + 1    
                tn.write(b"interface tunnel " + str(tunnel).encode('ascii') + b"\n")
                tn.write(b"ip vrf forwarding " + str(vrf).encode('ascii') + b"\n")                            
                tn.write(b"ip address " + str(ipv4_tun_chagall_vrf_datos).encode('ascii') + str(mask).encode('ascii') + b"\n")
                if online_cpe == True:
                        tn.write(b"description tun" + str(tunnel).encode('ascii') + b" a tun2 en " + str(router_name[2:-1].strip()).encode('ascii') + b" del servicio DATOS FTTH/VSAT \n")                
                else:
                        tn.write(b"description tun" + str(tunnel).encode('ascii') + b" a tun2 en " + str(nombre_cpe).encode('ascii') + b" del servicio DATOS FTTH/VSAT \n")
                tn.write(b"no ip redirects \n")
                tn.write(b"ip mtu 1344 \n")                
                tn.write(b"ip nhrp responder Loopback1 \n") 
                tn.write(b"ip nhrp map multicast dynamic \n")                 
                tn.write(b"ip nhrp holdtime 300 \n") 
                tn.write(b"ip tcp adjust-mss 1300 \n") 
                tn.write(b"tunnel source Loopback1 \n") 
                tn.write(b"tunnel mode gre multipoint \n") 
                tn.write(b"tunnel path-mtu-discovery \n")
                tn.write(b"delay 40000 \n")                   
                tn.write(b"tunnel protection ipsec profile RIEMANN_FO shared \n")                
                tn.write(b"ip nhrp network-id " + str(key_chagall_4_tun).encode('ascii') + b"\n")
                tn.write(b"tunnel key " + str(key_chagall_4_tun).encode('ascii') + b"\n") 
                key_chagall_dato_ftth = key_chagall_4_tun
                key_chagall_4_tun += 1               
                time.sleep(1)
                auth_chagall_dato_ftth = auth_chagall
                tn.write(b"ip nhrp authentication " + auth_chagall_dato_ftth.encode('ascii') + b"\n") 
                time.sleep(1) 
                print("Se creo el tunel " + str(tunnel) + " con la ip " + str(ipv4_tun_chagall_vrf_datos) + str(mask))
                time.sleep(1)

                print("\b") 
                print("** Para vrf DATOS del servicio XG en Chagall **")
                print("\b") 
                
                valida_key_chagall(tunnel + 1, key_chagall_4_tun)
                Auntentica_chagall() 
                ipv4_tun_chagall_vrf_datos_xg = ipv4_tun_chagall_vrf_datos + 8
                ipv4_borde_a_chagall_dato_xg = ipv4_tun_chagall_vrf_datos_xg + 1               
                consuta=tn.write(b"sh ip interface brief | include " + str(ipv4_tun_chagall_vrf_datos_xg).encode('ascii') + b"\n" )                
                time.sleep(1)
                resultado= tn.read_very_eager().decode('ascii') 
                comparacion=re.search("YES",resultado)         
                if comparacion:                                                
                        print("La ip ya esta en uso, utilice otra ip!") 
                        Ip_tunnel_ppl(tunnel)                 
                tn.write(b"configure terminal \n")
                tunnel = tunnel + 1  
                tn.write(b"interface tunnel " + str(tunnel).encode('ascii') + b"\n") 
                tn.write(b"ip vrf forwarding " + str(vrf).encode('ascii') + b"\n")                           
                tn.write(b"ip address " + str(ipv4_tun_chagall_vrf_datos_xg).encode('ascii') + str(mask).encode('ascii') + b"\n")
                if online_cpe == True:
                        tn.write(b"description tun" + str(tunnel).encode('ascii') + b" a tun41 en " + str(router_name[2:-1].strip()).encode('ascii') + b" del servicio DATOS XG \n")                
                else:
                        tn.write(b"description tun" + str(tunnel).encode('ascii') + b" a tun41 en " + str(nombre_cpe).encode('ascii') + b" del servicio DATOS XG \n")
                tn.write(b"no ip redirects \n")
                tn.write(b"ip mtu 1344 \n")                
                tn.write(b"ip nhrp responder Loopback0 \n") 
                tn.write(b"ip nhrp map multicast dynamic \n")                 
                tn.write(b"ip nhrp holdtime 300 \n") 
                tn.write(b"ip tcp adjust-mss 1300 \n") 
                tn.write(b"tunnel source Loopback0 \n") 
                tn.write(b"tunnel mode gre multipoint \n") 
                tn.write(b"tunnel path-mtu-discovery \n")
                tn.write(b"delay 70000 \n")                   
                tn.write(b"tunnel protection ipsec profile RIEMANN_CEL shared \n")                
                tn.write(b"ip nhrp network-id " + str(key_chagall_4_tun).encode('ascii') + b"\n")
                tn.write(b"tunnel key " + str(key_chagall_4_tun).encode('ascii') + b"\n") 
                key_chagall_dato_xg = key_chagall_4_tun                            
                time.sleep(1)
                auth_chagall_dato_xg = auth_chagall
                tn.write(b"ip nhrp authentication " + auth_chagall_dato_xg.encode('ascii') + b"\n") 
                time.sleep(1)  
                print("Se creo el tunel " + str(tunnel) + " con la ip " + str(ipv4_tun_chagall_vrf_datos_xg) + mask )
                time.sleep(1)
                tunnel= tunnel - 3
                tuneles_borde(tunnel,ipv4_borde_a_taylor, ipv4_borde_a_chagall)

def Consulta_key_taylor(tunnel):
        global key_taylor

        key_taylor = int(input("Para el tunel " + str(tunnel) + " ingrese el key: " ))
        compara = tn.write(b"sh run | sec key \n" )        
        time.sleep(2)
        tn.write(b" \n" )        
        tn.write(b" \n" )    
        resultado= tn.read_very_eager().decode('ascii')        
        comparacion=re.search(str(key_taylor).encode('ascii'), resultado.encode('ascii'))             
        if comparacion:                                                
                print("El KEY existe, intente con otro") 
                Consulta_key_taylor(tunnel)
        else:                
                

                print("KEY OK") 
                
                return key_taylor


def valida_key_taylor(tunnel , key_taylor_4_tun):        

        compara = tn.write(b"sh run | sec key \n" )        
        time.sleep(2)
        tn.write(b" \n" )        
        tn.write(b" \n" )    
        resultado= tn.read_very_eager().decode('ascii')        
        comparacion=re.search(str(key_taylor_4_tun).encode('ascii'), resultado.encode('ascii'))             
        if comparacion:                                                
                print("El KEY existe, intente con otro") 
                Consulta_key_taylor(tunnel)
        else:               
                
                print("KEY OK") 
                return key_taylor_4_tun                  
        
def Consulta_key_chagall(tunnel):
        global key_chagall

        # Login_concentrador_respaldo()  
        key_chagall = int(input("Para el tunel " + str(tunnel) + " ingrese el key: " ))
        compara = tn.write(b"sh run | sec key \n" )        
        time.sleep(2)
        tn.write(b" \n" )        
        tn.write(b" \n" )    
        resultado= tn.read_very_eager().decode('ascii')        
        comparacion=re.search(str(key_chagall).encode('ascii'), resultado.encode('ascii'))             
        if comparacion:                                                
                print("El KEY existe, intente con otro") 
                Consulta_key_chagall(tunnel)
        else:                
                # tn.write(b"ip nhrp authentication " + auth.encode('ascii') + b"\n") 

                print("KEY OK") 
                return key_chagall  

def valida_key_chagall(tunnel , key_chagall_4_tun):        

        compara = tn.write(b"sh run | sec key \n" )        
        time.sleep(2)
        tn.write(b" \n" )        
        tn.write(b" \n" )    
        resultado= tn.read_very_eager().decode('ascii')        
        comparacion=re.search(str(key_chagall_4_tun).encode('ascii'), resultado.encode('ascii'))             
        if comparacion:                                                
                print("El KEY existe, intente con otro") 
                Consulta_key_taylor(tunnel)
        else:               
                
                print("KEY OK") 
                return key_chagall_4_tun 

def tuneles_borde(tunnel, ipv4_borde_a_taylor, ipv4_borde_a_chagall):
        mask=" 255.255.255.252"
        
        if online_cpe == True:                
                valida_vrf_admin_borde()
                
                if num_de_tuneles == 1:
                        # ipv4_borde_a_taylor
                        # ipv4_borde_a_chagall                        
                        
                        # aqui consulto para tunel a taylor

                        
                        
                        tn.write(b"configure terminal \n")
                        if vrf == "admin" and tipo_conexion == "xg":
                                ipv4_borde_a_chagall_xg
                                ipv4_borde_a_taylor_xg
                                
                                consuta_taylor=tn.write(b"do sh ip interface brief | include " + str(ipv4_borde_a_taylor_xg).encode('ascii') + b"\n" )                
                                time.sleep(1)
                                resultado= tn.read_very_eager().decode('ascii') 
                                comparacion=re.search("YES",resultado)         
                                if comparacion:                                                
                                        print("La ip ya esta en uso, utilice otra ip!") 
                                        Ip_tunnel_ppl(tunnel)
                                
                                
                                consuta_interface= tn.write(b"do sh ip interface brief \n" )
                                time.sleep(1)
                                resultado=tn.read_very_eager().decode('ascii')
                                print(resultado)
                                interface_source=input("Indique la interface source para el tunel XG: ")
                                tn.write(b"interface tunnel 22 \n") 
                                tn.write(b"ip vrf forwarding admin \n")
                                tn.write(b"ip address " + str(ipv4_borde_a_taylor_xg).encode('ascii') + str(mask).encode('ascii') + b"\n")
                                tn.write(b"description tun22 a tun" + str(tunnel).encode('ascii') + b" en Taylor del servicio ADMIN - XG \n")
                                tn.write(b"ip nhrp map multicast 143.255.24.59 \n")
                                tn.write(b"tunnel source " + str(interface_source).encode('ascii') + b"\n")
                                tn.write(b"ip nhrp map " + str(ipv4_tun_taylor).encode('ascii') + b" 143.255.24.59 \n")                                
                                tn.write(b"ip mtu 1344 \n")                                
                                tn.write(b"ip nhrp registration timeout 50 \n")
                                tn.write(b"ip tcp adjust-mss 1300 \n")                        
                                tn.write(b"tunnel mode gre multipoint \n")                        
                                tn.write(b"ip nhrp holdtime 300 \n")                      
                                tn.write(b"tunnel protection ipsec profile lab shared \n")
                                tn.write(b"ip nhrp nhs " + str(ipv4_tun_taylor).encode('ascii') + b"\n")
                                tn.write(b"delay 20000 \n")
                                tn.write(b"tunnel key " + str(key_taylor).encode('ascii') + b"\n")
                                tn.write(b"ip nhrp network-id " + str(key_taylor).encode('ascii') + b"\n")
                                tn.write(b"ip nhrp authentication " + auth_taylor.encode('ascii') + b"\n") 
                                tn.write(b"exit \n") 
                                
                                time.sleep(1) 

                        # aqui consulto para tunel a chagall
                         
                                consuta_chagal=tn.write(b"do sh ip interface brief \n")                
                                time.sleep(1)
                                print(consuta_chagal)
                                resultado_2= tn.read_very_eager().decode('ascii') 
                                comparacion2=re.search(str(ipv4_borde_a_chagall_xg),resultado_2)
                                print(resultado_2)         
                                if comparacion2:                                                
                                        print("La ip ya esta en uso, utilice otra ip!") 
                                        Ip_tunnel_ppl(tunnel)                       
                                
                                                        
                                tn.write(b"interface tunnel 42 \n") 
                                tn.write(b"ip vrf forwarding admin \n")
                                tn.write(b"ip address " + str(ipv4_borde_a_chagall_xg).encode('ascii') + str(mask).encode('ascii') + b"\n")
                                tn.write(b"description tun42 a tun" + str(tunnel).encode('ascii') + b" en Chagall del servicio ADMIN - XG \n")
                                tn.write(b"ip nhrp map multicast 143.255.26.59 \n")
                                tn.write(b"tunnel source " + str(interface_source).encode('ascii') + b"\n")                        
                                tn.write(b"ip nhrp map " + str(ipv4_tun_chagall).encode('ascii') + b" 143.255.26.59 \n")                        
                                tn.write(b"ip nhrp registration timeout 50 \n")
                                tn.write(b"ip tcp adjust-mss 1300 \n") 
                                tn.write(b"ip mtu 1344 \n")                         
                                tn.write(b"tunnel mode gre multipoint \n")                        
                                tn.write(b"tunnel protection ipsec profile RIEMANN_CEL shared \n")
                                tn.write(b"delay 70000 \n")
                                tn.write(b"ip nhrp nhs " + str(ipv4_tun_chagall).encode('ascii') + b"\n")
                                tn.write(b"tunnel key " + str(key_chagall).encode('ascii') + b"\n")
                                tn.write(b"ip nhrp network-id " + str(key_chagall).encode('ascii') + b"\n")
                                tn.write(b"ip nhrp authentication " + auth_chagall.encode('ascii') + b"\n")
                                time.sleep(1) 
                                
                                print("\b")
                                print(" ** Se han creado los tunenes correctamente!!")
                                print("\b")
                        
                        if vrf == "admin" and tipo_conexion == "ftth/vsat":
                                ipv4_borde_a_chagall                               
                                ipv4_borde_a_taylor
                                consuta_interface= tn.write(b"do sh ip interface brief \n" )
                                time.sleep(1)
                                resultado=tn.read_very_eager().decode('ascii')
                                print(resultado)
                                interface_source=input("Indique la interface source para el tunel ftth/vasat: ")
                                tn.write(b"interface tunnel 10 \n") 
                                tn.write(b"ip vrf forwarding admin \n")
                                tn.write(b"ip address " + str(ipv4_borde_a_taylor).encode('ascii') + str(mask).encode('ascii') + b"\n")
                                tn.write(b"description tun10 a tun" + str(tunnel).encode('ascii') + b" en Taylor del servicio ADMIN - FTTH/VSAT \n")
                                tn.write(b"ip nhrp map multicast 143.255.24.60 \n")
                                tn.write(b"tunnel source " + str(interface_source).encode('ascii') + b"\n")
                                tn.write(b"ip nhrp map " + str(ipv4_tun_taylor).encode('ascii') + b" 143.255.24.60 \n")                                
                                tn.write(b"ip mtu 1344 \n")                                
                                tn.write(b"ip nhrp registration timeout 50 \n")
                                tn.write(b"ip tcp adjust-mss 1300 \n")                        
                                tn.write(b"tunnel mode gre multipoint \n")                        
                                tn.write(b"ip nhrp holdtime 300 \n")                      
                                tn.write(b"tunnel protection ipsec profile LAB2 shared \n")
                                tn.write(b"ip nhrp nhs " + str(ipv4_tun_taylor).encode('ascii') + b"\n")                                
                                tn.write(b"tunnel key " + str(key_taylor).encode('ascii') + b"\n")
                                tn.write(b"ip nhrp network-id " + str(key_taylor).encode('ascii') + b"\n")
                                tn.write(b"ip nhrp authentication " + auth_taylor.encode('ascii') + b"\n") 

                        # aqui consulto para tunel a chagall
                         
                                consuta_chagal=tn.write(b"do sh ip interface brief | include " + str(ipv4_borde_a_chagall).encode('ascii') + b"\n" )                
                                time.sleep(1)
                                resultado= tn.read_very_eager().decode('ascii') 
                                comparacion=re.search("YES",resultado)         
                                if comparacion:                                                
                                        print("La ip ya esta en uso, utilice otra ip!") 
                                        Ip_tunnel_ppl(tunnel)                       
                                                        
                                tn.write(b"interface tunnel 20 \n") 
                                tn.write(b"ip vrf forwarding admin \n")
                                tn.write(b"ip address " + str(ipv4_borde_a_chagall).encode('ascii') + str(mask).encode('ascii') + b"\n")
                                tn.write(b"description tun20 a tun" + str(tunnel).encode('ascii') + b" en Chagall del servicio ADMIN - FTTH/VSAT \n")
                                tn.write(b"ip nhrp map multicast 143.255.26.60 \n")
                                tn.write(b"tunnel source " + str(interface_source).encode('ascii') + b"\n")                        
                                tn.write(b"ip nhrp map " + str(ipv4_tun_chagall).encode('ascii') + b" 143.255.26.60 \n")                        
                                tn.write(b"ip nhrp registration timeout 50 \n")
                                tn.write(b"ip tcp adjust-mss 1300 \n") 
                                tn.write(b"ip mtu 1344 \n")                         
                                tn.write(b"tunnel mode gre multipoint \n")                        
                                tn.write(b"tunnel protection ipsec profile RIEMANN_FO shared \n")
                                tn.write(b"delay 40000 \n")
                                tn.write(b"ip nhrp nhs " + str(ipv4_tun_chagall).encode('ascii') + b"\n")
                                tn.write(b"tunnel key " + str(key_chagall).encode('ascii') + b"\n")
                                tn.write(b"ip nhrp network-id " + str(key_chagall).encode('ascii') + b"\n")
                                tn.write(b"ip nhrp authentication " + auth_chagall.encode('ascii') + b"\n")
                                print("\b")
                                print(" ** Se han creado los tunenes correctamente!! ** ")
                                print("\b")  
                                
                        if vrf != "admin" and tipo_conexion == "xg":
                                
                                
                                                                
                                consuta_interface= tn.write(b"do sh ip interface brief \n" )
                                time.sleep(1)
                                resultado=tn.read_very_eager().decode('ascii')
                                print(resultado)
                                interface_source=input("Indique la interface source para el tunel XG: ")
                                tn.write(b"interface tunnel 21 \n") 
                                tn.write(b"ip vrf forwarding " + str(vrf).encode('ascii') + b"\n") 
                                tn.write(b"ip address " + str(ipv4_borde_a_taylor_datos_xg).encode('ascii') + str(mask).encode('ascii') + b"\n")
                                tn.write(b"description tun21 a tun" + str(tunnel).encode('ascii') + b" en Taylor del servicio DATOS - XG \n")
                                tn.write(b"ip nhrp map multicast 143.255.24.59 \n")
                                tn.write(b"tunnel source " + str(interface_source).encode('ascii') + b"\n")
                                tn.write(b"ip nhrp map " + str(ipv4_tun_taylor).encode('ascii') + b" 143.255.24.59 \n")                                
                                tn.write(b"ip mtu 1344 \n")                                
                                tn.write(b"ip nhrp registration timeout 50 \n")
                                tn.write(b"ip tcp adjust-mss 1300 \n")                        
                                tn.write(b"tunnel mode gre multipoint \n")                        
                                tn.write(b"ip nhrp holdtime 300 \n")  
                                tn.write(b"delay 20000 \n")                    
                                tn.write(b"tunnel protection ipsec profile lab shared \n")
                                tn.write(b"ip nhrp nhs " + str(ipv4_tun_taylor).encode('ascii') + b"\n")                                
                                tn.write(b"tunnel key " + str(key_taylor).encode('ascii') + b"\n")
                                tn.write(b"ip nhrp network-id " + str(key_taylor).encode('ascii') + b"\n")
                                tn.write(b"ip nhrp authentication " + auth_taylor.encode('ascii') + b"\n") 

                        # aqui consulto para tunel a chagall
                         
                                consuta_chagal=tn.write(b"do sh ip interface brief | include " + str(ipv4_borde_a_chagall).encode('ascii') + b"\n" )                
                                time.sleep(1)
                                resultado= tn.read_very_eager().decode('ascii') 
                                comparacion=re.search("YES",resultado)         
                                if comparacion:                                                
                                        print("La ip ya esta en uso, utilice otra ip!") 
                                        Ip_tunnel_ppl(tunnel)                       
                                                        
                                tn.write(b"interface tunnel 41 \n") 
                                tn.write(b"ip vrf forwarding " + str(vrf).encode('ascii') + b"\n") 
                                tn.write(b"ip address " + str(ipv4_borde_a_chagall_dato_xg).encode('ascii') + str(mask).encode('ascii') + b"\n")
                                tn.write(b"description tun41 a tun" + str(tunnel).encode('ascii') + b" en Chagall del servicio DATOS - XG  \n")
                                tn.write(b"ip nhrp map multicast 143.255.26.59 \n")
                                tn.write(b"tunnel source " + str(interface_source).encode('ascii') + b"\n")                        
                                tn.write(b"ip nhrp map " + str(ipv4_tun_chagall).encode('ascii') + b" 143.255.26.59 \n")                        
                                tn.write(b"ip nhrp registration timeout 50 \n")
                                tn.write(b"ip tcp adjust-mss 1300 \n") 
                                tn.write(b"ip mtu 1344 \n")                         
                                tn.write(b"tunnel mode gre multipoint \n")                        
                                tn.write(b"tunnel protection ipsec profile RIEMANN_CEL shared \n")
                                tn.write(b"delay 70000 \n")
                                tn.write(b"ip nhrp nhs " + str(ipv4_tun_chagall).encode('ascii') + b"\n")
                                tn.write(b"tunnel key " + str(key_chagall).encode('ascii') + b"\n")
                                tn.write(b"ip nhrp network-id " + str(key_chagall).encode('ascii') + b"\n")
                                tn.write(b"ip nhrp authentication " + auth_chagall.encode('ascii') + b"\n")
                                print("\b")
                                print(" ** Se han creado los tunenes correctamente!! ** ")
                                print("\b")
                        
                        if vrf != "admin" and tipo_conexion == "ftth/vsat":
                                
                                ipv4_borde_a_chagall_dato_ftth
                                ipv4_borde_a_taylor_datos_ftth
                                
                                consuta_interface= tn.write(b"do sh ip interface brief \n" )
                                time.sleep(1)
                                resultado=tn.read_very_eager().decode('ascii')
                                print(resultado)
                                interface_source=input("Indique la interface source para el tunel ftth/vasat: ")
                                tn.write(b"interface tunnel 1 \n") 
                                tn.write(b"ip vrf forwarding " + str(vrf).encode('ascii') + b"\n") 
                                tn.write(b"ip address " + str(ipv4_borde_a_taylor).encode('ascii') + str(mask).encode('ascii') + b"\n")
                                tn.write(b"description tun1 a tun" + str(tunnel).encode('ascii') + b" en Taylor del servicio DATOS - FTTH/VSAT \n")
                                tn.write(b"ip nhrp map multicast 143.255.24.60 \n")
                                tn.write(b"tunnel source " + str(interface_source).encode('ascii') + b"\n")
                                tn.write(b"ip nhrp map " + str(ipv4_tun_taylor).encode('ascii') + b" 143.255.24.60 \n")                                
                                tn.write(b"ip mtu 1344 \n")                                
                                tn.write(b"ip nhrp registration timeout 50 \n")
                                tn.write(b"ip tcp adjust-mss 1300 \n")                        
                                tn.write(b"tunnel mode gre multipoint \n")                        
                                tn.write(b"ip nhrp holdtime 300 \n")
                                tn.write(b"tunnel protection ipsec profile LAB2 shared \n")
                                tn.write(b"ip nhrp nhs " + str(ipv4_tun_taylor).encode('ascii') + b"\n")                                
                                tn.write(b"tunnel key " + str(key_taylor).encode('ascii') + b"\n")
                                tn.write(b"ip nhrp network-id " + str(key_taylor).encode('ascii') + b"\n")
                                tn.write(b"ip nhrp authentication " + auth_taylor.encode('ascii') + b"\n") 

                        # aqui consulto para tunel a chagall
                         
                                consuta_chagal=tn.write(b"do sh ip interface brief | include " + str(ipv4_borde_a_chagall).encode('ascii') + b"\n" )                
                                time.sleep(1)
                                resultado= tn.read_very_eager().decode('ascii') 
                                comparacion=re.search("YES",resultado)         
                                if comparacion:                                                
                                        print("La ip ya esta en uso, utilice otra ip!") 
                                        Ip_tunnel_ppl(tunnel)                       
                                                        
                                tn.write(b"interface tunnel 2 \n") 
                                tn.write(b"ip vrf forwarding " + str(vrf).encode('ascii') + b"\n") 
                                tn.write(b"ip address " + str(ipv4_borde_a_chagall).encode('ascii') + str(mask).encode('ascii') + b"\n")
                                tn.write(b"description tun2 a tun" + str(tunnel).encode('ascii') + b" en Chagall del servicio DATOS - FTTH/VSAT \n")
                                tn.write(b"ip nhrp map multicast 143.255.26.60 \n")
                                tn.write(b"tunnel source " + str(interface_source).encode('ascii') + b"\n")                        
                                tn.write(b"ip nhrp map " + str(ipv4_tun_chagall).encode('ascii') + b" 143.255.26.60 \n")                        
                                tn.write(b"ip nhrp registration timeout 50 \n")
                                tn.write(b"ip tcp adjust-mss 1300 \n") 
                                tn.write(b"ip mtu 1344 \n")                         
                                tn.write(b"tunnel mode gre multipoint \n")                        
                                tn.write(b"tunnel protection ipsec profile RIEMANN_FO shared \n")
                                tn.write(b"delay 40000 \n")
                                tn.write(b"ip nhrp nhs " + str(ipv4_tun_chagall).encode('ascii') + b"\n")
                                tn.write(b"tunnel key " + str(key_chagall).encode('ascii') + b"\n")
                                tn.write(b"ip nhrp network-id " + str(key_chagall).encode('ascii') + b"\n")
                                tn.write(b"ip nhrp authentication " + auth_chagall.encode('ascii') + b"\n")
                                print("\b")
                                print(" ** Se han creado los tunenes correctamente!! ** ")
                                print("\b")

                if num_de_tuneles == 8:
                        
                        print("\n")                       
                        print("Este es el numero de tunel que viene del backup " + str(tunnel))
                        print("\n")  

                        tn.write(b"configure terminal \n") 
                        consuta_taylor=tn.write(b"do sh ip interface brief | include " + str(ipv4_borde_a_taylor).encode('ascii') + b"\n" )                
                        time.sleep(1)
                        resultado= tn.read_very_eager().decode('ascii') 
                        comparacion=re.search("YES",resultado)         
                        if comparacion:                                                
                                print("La ip ya esta en uso, utilice otra ip!") 
                                Ip_tunnel_ppl(tunnel)   
                        consuta_interface= tn.write(b"do sh ip interface brief \n" )
                        time.sleep(1)
                        resultado=tn.read_very_eager().decode('ascii')
                        print(resultado)
                        interface_source_ftth=input("Indique la interface source para el tunel ftth/vsat: ")
                        tn.write(b"interface tunnel 10 \n") 
                        tn.write(b"ip vrf forwarding admin \n")
                        tn.write(b"ip address " + str(ipv4_borde_a_taylor).encode('ascii') + str(mask).encode('ascii') + b"\n")
                        tn.write(b"description tun10 a tun" + str(tunnel).encode('ascii') + b" en Taylor del servicio ADMIN - FTTH/VSAT \n")
                        tn.write(b"ip nhrp map multicast 143.255.24.60 \n")
                        tn.write(b"tunnel source " + str(interface_source_ftth).encode('ascii') + b"\n")
                        tn.write(b"ip nhrp map " + str(ipv4_tun_taylor_vrf_admin).encode('ascii') + b" 143.255.24.60 \n")                                
                        tn.write(b"ip mtu 1344 \n")                                
                        tn.write(b"ip nhrp registration timeout 50 \n")
                        tn.write(b"ip tcp adjust-mss 1300 \n")                        
                        tn.write(b"tunnel mode gre multipoint \n")                        
                        tn.write(b"ip nhrp holdtime 300 \n")                      
                        tn.write(b"tunnel protection ipsec profile LAB2 shared \n")
                        tn.write(b"ip nhrp nhs " + str(ipv4_tun_taylor_vrf_admin).encode('ascii') + b"\n")                                
                        tn.write(b"tunnel key " + str(key_taylor_admin_ftth).encode('ascii') + b"\n")
                        tn.write(b"ip nhrp network-id " + str(key_taylor_admin_ftth).encode('ascii') + b"\n")
                        tn.write(b"ip nhrp authentication " + auth_taylor_adm_ftth.encode('ascii') + b"\n") 
                        
                        
                        
                        # aqui consulto para tunel a taylor

                        consuta_taylor=tn.write(b"sh ip interface brief | include " + str(ipv4_borde_a_taylor_xg).encode('ascii') + b"\n" )                
                        time.sleep(1)
                        resultado= tn.read_very_eager().decode('ascii') 
                        comparacion=re.search("YES",resultado)         
                        if comparacion:                                                
                                print("La ip ya esta en uso, utilice otra ip!") 
                                Ip_tunnel_ppl(tunnel)
                        
                        tn.write(b"configure terminal \n")
                        
                        consuta_interface= tn.write(b"do sh ip interface brief \n" )
                        time.sleep(1)
                        resultado=tn.read_very_eager().decode('ascii')
                        print(resultado)
                        interface_source_xg=input("Indique la interface source para el tunel XG: ")
                        tn.write(b"interface tunnel 22 \n") 
                        tn.write(b"ip vrf forwarding admin \n")
                        tn.write(b"ip address " + str(ipv4_borde_a_taylor_xg).encode('ascii') + str(mask).encode('ascii') + b"\n")
                        tn.write(b"description tun22 a tun" + str(tunnel).encode('ascii') + b" en Taylor del servicio ADMIN - XG \n")
                        tn.write(b"ip nhrp map multicast 143.255.24.59 \n")
                        tn.write(b"tunnel source " + str(interface_source_xg).encode('ascii') + b"\n")
                        tn.write(b"ip nhrp map " + str(ipv4_tun_taylor_vrf_admin_xg).encode('ascii') + b" 143.255.24.59 \n")                                
                        tn.write(b"ip mtu 1344 \n")                                
                        tn.write(b"ip nhrp registration timeout 50 \n")
                        tn.write(b"ip tcp adjust-mss 1300 \n")                        
                        tn.write(b"tunnel mode gre multipoint \n")                        
                        tn.write(b"ip nhrp holdtime 300 \n")                      
                        tn.write(b"tunnel protection ipsec profile lab shared \n")
                        tn.write(b"ip nhrp nhs " + str(ipv4_tun_taylor_vrf_admin_xg).encode('ascii') + b"\n")
                        tn.write(b"delay 20000 \n")
                        tn.write(b"tunnel key " + str(key_taylor_admin_xg).encode('ascii') + b"\n")
                        tn.write(b"ip nhrp network-id " + str(key_taylor_admin_xg).encode('ascii') + b"\n")
                        tn.write(b"ip nhrp authentication " + auth_taylor_admin_xg.encode('ascii') + b"\n") 

                # aqui consulto para tunel a chagall
                        
                        consuta_chagal=tn.write(b"do sh ip interface brief | include " + str(ipv4_borde_a_chagall_xg).encode('ascii') + b"\n" )                
                        time.sleep(1)
                        resultado= tn.read_very_eager().decode('ascii') 
                        comparacion=re.search("YES",resultado)         
                        if comparacion:                                                
                                print("La ip ya esta en uso, utilice otra ip!") 
                                Ip_tunnel_ppl(tunnel)                       
                                                
                        tn.write(b"interface tunnel 42 \n") 
                        tn.write(b"ip vrf forwarding admin \n")
                        tn.write(b"ip address " + str(ipv4_borde_a_chagall_xg).encode('ascii') + str(mask).encode('ascii') + b"\n")
                        tn.write(b"description tun22 a tun" + str(tunnel).encode('ascii') + b" en Chagall del servicio ADMIN - XG \n")
                        tn.write(b"ip nhrp map multicast 143.255.26.59 \n")
                        tn.write(b"tunnel source " + str(interface_source_xg).encode('ascii') + b"\n")                        
                        tn.write(b"ip nhrp map " + str(ipv4_tun_chagall_vrf_admin_xg).encode('ascii') + b" 143.255.26.59 \n")                        
                        tn.write(b"ip nhrp registration timeout 50 \n")
                        tn.write(b"ip tcp adjust-mss 1300 \n") 
                        tn.write(b"ip mtu 1344 \n")                         
                        tn.write(b"tunnel mode gre multipoint \n")                        
                        tn.write(b"tunnel protection ipsec profile RIEMANN_CEL shared \n")
                        tn.write(b"delay 70000 \n")
                        tn.write(b"ip nhrp nhs " + str(ipv4_tun_chagall_vrf_admin_xg).encode('ascii') + b"\n")
                        tn.write(b"tunnel key " + str(key_chagall).encode('ascii') + b"\n")
                        tn.write(b"ip nhrp network-id " + str(key_chagall).encode('ascii') + b"\n")
                        tn.write(b"ip nhrp authentication " + auth_chagall_admin_xg.encode('ascii') + b"\n")
                                                

                        

                # aqui consulto para tunel a chagall
                        
                        consuta_chagal=tn.write(b"do sh ip interface brief | include " + str(ipv4_borde_a_chagall).encode('ascii') + b"\n" )                
                        time.sleep(1)
                        resultado= tn.read_very_eager().decode('ascii') 
                        comparacion=re.search("YES",resultado)         
                        if comparacion:                                                
                                print("La ip ya esta en uso, utilice otra ip!") 
                                Ip_tunnel_ppl(tunnel)                       
                                                
                        tn.write(b"interface tunnel 20 \n") 
                        tn.write(b"ip vrf forwarding admin \n")
                        tn.write(b"ip address " + str(ipv4_borde_a_chagall).encode('ascii') + str(mask).encode('ascii') + b"\n")
                        tn.write(b"description tun20 a tun" + str(tunnel).encode('ascii') + b" en Chagall del servicio ADMIN - FTTH/VSAT \n")
                        tn.write(b"ip nhrp map multicast 143.255.26.60 \n")
                        tn.write(b"tunnel source " + str(interface_source_ftth).encode('ascii') + b"\n")                        
                        tn.write(b"ip nhrp map " + str(ipv4_tun_chagall_vrf_admin).encode('ascii') + b" 143.255.26.60 \n")                        
                        tn.write(b"ip nhrp registration timeout 50 \n")
                        tn.write(b"ip tcp adjust-mss 1300 \n") 
                        tn.write(b"ip mtu 1344 \n")                         
                        tn.write(b"tunnel mode gre multipoint \n")                        
                        tn.write(b"tunnel protection ipsec profile RIEMANN_FO shared \n")
                        tn.write(b"delay 40000 \n")
                        tn.write(b"ip nhrp nhs " + str(ipv4_tun_chagall_vrf_admin).encode('ascii') + b"\n")
                        tn.write(b"tunnel key " + str(key_chagall).encode('ascii') + b"\n")
                        tn.write(b"ip nhrp network-id " + str(key_chagall).encode('ascii') + b"\n")
                        tn.write(b"ip nhrp authentication " + auth_chagall_admin_ftth.encode('ascii') + b"\n")
                        
                        
                        consuta_chagal=tn.write(b"do sh ip interface brief | include " + str(ipv4_borde_a_taylor_datos_xg).encode('ascii') + b"\n" )                
                        time.sleep(1)
                        resultado= tn.read_very_eager().decode('ascii') 
                        comparacion=re.search("YES",resultado)         
                        if comparacion:                                                
                                print("La ip ya esta en uso, utilice otra ip!") 
                                Ip_tunnel_ppl(tunnel)   
                                            
                        tn.write(b"interface tunnel 21 \n") 
                        tn.write(b"ip vrf forwarding " + str(vrf).encode('ascii') + b"\n") 
                        tn.write(b"ip address " + str(ipv4_borde_a_taylor_datos_xg).encode('ascii') + str(mask).encode('ascii') + b"\n")
                        tn.write(b"description tun21 a tun" + str(tunnel).encode('ascii') + b" en Taylor del servicio DATOS - XG \n")
                        tn.write(b"ip nhrp map multicast 143.255.24.59 \n")
                        tn.write(b"tunnel source " + str(interface_source_xg).encode('ascii') + b"\n")
                        tn.write(b"ip nhrp map " + str(ipv4_tun_taylor_vrf_datos_xg).encode('ascii') + b" 143.255.24.59 \n")                                
                        tn.write(b"ip mtu 1344 \n")                                
                        tn.write(b"ip nhrp registration timeout 50 \n")
                        tn.write(b"ip tcp adjust-mss 1300 \n")                        
                        tn.write(b"tunnel mode gre multipoint \n")                        
                        tn.write(b"ip nhrp holdtime 300 \n")  
                        tn.write(b"delay 20000 \n")                    
                        tn.write(b"tunnel protection ipsec profile lab shared \n")
                        tn.write(b"ip nhrp nhs " + str(ipv4_tun_taylor_vrf_datos_xg).encode('ascii') + b"\n")                                
                        tn.write(b"tunnel key " + str(key_taylor_dato_xg).encode('ascii') + b"\n")
                        tn.write(b"ip nhrp network-id " + str(key_taylor_dato_xg).encode('ascii') + b"\n")
                        tn.write(b"ip nhrp authentication " + auth_taylor_dato_xg.encode('ascii') + b"\n") 

                # aqui consulto para tunel a chagall
                        
                        consuta_chagal=tn.write(b"do sh ip interface brief | include " + str(ipv4_borde_a_chagall_dato_xg).encode('ascii') + b"\n" )                
                        time.sleep(1)
                        resultado= tn.read_very_eager().decode('ascii') 
                        comparacion=re.search("YES",resultado)         
                        if comparacion:                                                
                                print("La ip ya esta en uso, utilice otra ip!") 
                                Ip_tunnel_ppl(tunnel)                       
                                                
                        tn.write(b"interface tunnel 41 \n") 
                        tn.write(b"ip vrf forwarding " + str(vrf).encode('ascii') + b"\n") 
                        tn.write(b"ip address " + str(ipv4_borde_a_chagall_dato_xg).encode('ascii') + str(mask).encode('ascii') + b"\n")
                        tn.write(b"description tun41 a tun" + str(tunnel).encode('ascii') + b" en Chagall del servicio DATOS - XG  \n")
                        tn.write(b"ip nhrp map multicast 143.255.26.59 \n")
                        tn.write(b"tunnel source " + str(interface_source_xg).encode('ascii') + b"\n")                        
                        tn.write(b"ip nhrp map " + str(ipv4_tun_chagall_vrf_datos_xg).encode('ascii') + b" 143.255.26.59 \n")                        
                        tn.write(b"ip nhrp registration timeout 50 \n")
                        tn.write(b"ip tcp adjust-mss 1300 \n") 
                        tn.write(b"ip mtu 1344 \n")                         
                        tn.write(b"tunnel mode gre multipoint \n")                        
                        tn.write(b"tunnel protection ipsec profile RIEMANN_CEL shared \n")
                        tn.write(b"delay 70000 \n")
                        tn.write(b"ip nhrp nhs " + str(ipv4_tun_chagall_vrf_datos_xg).encode('ascii') + b"\n")
                        tn.write(b"tunnel key " + str(key_chagall).encode('ascii') + b"\n")
                        tn.write(b"ip nhrp network-id " + str(key_chagall).encode('ascii') + b"\n")
                        tn.write(b"ip nhrp authentication " + auth_chagall_dato_xg.encode('ascii') + b"\n")                                                      

                        
                        consuta_chagal=tn.write(b"do sh ip interface brief | include " + str(ipv4_borde_a_taylor_datos_ftth).encode('ascii') + b"\n" )                
                        time.sleep(1)
                        resultado= tn.read_very_eager().decode('ascii') 
                        comparacion=re.search("YES",resultado)         
                        if comparacion:                                                
                                print("La ip ya esta en uso, utilice otra ip!") 
                                Ip_tunnel_ppl(tunnel)   
                        
                        tn.write(b"interface tunnel 1 \n") 
                        tn.write(b"ip vrf forwarding " + str(vrf).encode('ascii') + b"\n") 
                        tn.write(b"ip address " + str(ipv4_borde_a_taylor_datos_ftth).encode('ascii') + str(mask).encode('ascii') + b"\n")
                        tn.write(b"description tun1 a tun" + str(tunnel).encode('ascii') + b" en Taylor del servicio DATOS - FTTH/VSAT \n")
                        tn.write(b"ip nhrp map multicast 143.255.24.60 \n")
                        tn.write(b"tunnel source " + str(interface_source_ftth).encode('ascii') + b"\n")
                        tn.write(b"ip nhrp map " + str(ipv4_tun_taylor_vrf_datos).encode('ascii') + b" 143.255.24.60 \n")                                
                        tn.write(b"ip mtu 1344 \n")                                
                        tn.write(b"ip nhrp registration timeout 50 \n")
                        tn.write(b"ip tcp adjust-mss 1300 \n")                        
                        tn.write(b"tunnel mode gre multipoint \n")                        
                        tn.write(b"ip nhrp holdtime 300 \n")
                        tn.write(b"tunnel protection ipsec profile LAB2 shared \n")
                        tn.write(b"ip nhrp nhs " + str(ipv4_tun_taylor_vrf_datos).encode('ascii') + b"\n")                                
                        tn.write(b"tunnel key " + str(key_taylor_dato_ftth).encode('ascii') + b"\n")
                        tn.write(b"ip nhrp network-id " + str(key_taylor_dato_ftth).encode('ascii') + b"\n")
                        tn.write(b"ip nhrp authentication " + auth_taylor_dato_ftth.encode('ascii') + b"\n") 

                # aqui consulto para tunel a chagall
                        
                        consuta_chagal=tn.write(b"do sh ip interface brief | include " + str(ipv4_borde_a_chagall_dato_ftth).encode('ascii') + b"\n" )                
                        time.sleep(1)
                        resultado= tn.read_very_eager().decode('ascii') 
                        comparacion=re.search("YES",resultado)         
                        if comparacion:                                                
                                print("La ip ya esta en uso, utilice otra ip!") 
                                Ip_tunnel_ppl(tunnel)                       
                                                
                        tn.write(b"interface tunnel 2 \n") 
                        tn.write(b"ip vrf forwarding " + str(vrf).encode('ascii') + b"\n") 
                        tn.write(b"ip address " + str(ipv4_borde_a_chagall_dato_ftth).encode('ascii') + str(mask).encode('ascii') + b"\n")
                        tn.write(b"description tun2 a tun" + str(tunnel).encode('ascii') + b" en Chagall del servicio DATOS - FTTH/VSAT \n")
                        tn.write(b"ip nhrp map multicast 143.255.26.60 \n")
                        tn.write(b"tunnel source " + str(interface_source_ftth).encode('ascii') + b"\n")                        
                        tn.write(b"ip nhrp map " + str(ipv4_tun_chagall_vrf_datos).encode('ascii') + b" 143.255.26.60 \n")                        
                        tn.write(b"ip nhrp registration timeout 50 \n")
                        tn.write(b"ip tcp adjust-mss 1300 \n") 
                        tn.write(b"ip mtu 1344 \n")                         
                        tn.write(b"tunnel mode gre multipoint \n")                        
                        tn.write(b"tunnel protection ipsec profile RIEMANN_FO shared \n")
                        tn.write(b"delay 40000 \n")
                        tn.write(b"ip nhrp nhs " + str(ipv4_tun_chagall_vrf_datos).encode('ascii') + b"\n")
                        tn.write(b"tunnel key " + str(key_chagall).encode('ascii') + b"\n")
                        tn.write(b"ip nhrp network-id " + str(key_chagall).encode('ascii') + b"\n")
                        tn.write(b"ip nhrp authentication " + auth_chagall_dato_ftth.encode('ascii') + b"\n")
                        print("\b")
                        print(" ** Se han creado los tunenes correctamente!! ** ")
                        print("\b")
                                
                        
        if online_cpe == False:
                
                if num_de_tuneles == 1:
                        ipv4_borde_a_taylor
                        ipv4_borde_a_chagall
                        
                        #archivo-salida.py
                        f = open ("config_" + str(nombre_cpe) + ".txt",'w')
                                                                    
                        
                        # configuracion para taylor
                        
                        f.write("configuracion para taylor")
                        f.write("\n")                                             
                        f.write("\n")                                             
                        
                        if vrf == "admin" and tipo_conexion == "xg":                                
                                interface_source=input("Indique la interface source para XG: ")
                                f.write("interface tunnel 22 \n") 
                                f.write("ip vrf forwarding admin \n")
                                f.write("ip address " + str(ipv4_borde_a_taylor) + str(mask) +"\n")
                                f.write("description tun22 a tun" + str(tunnel) + " en Taylor del servicio ADMIN - XG \n")
                                f.write("ip nhrp map multicast 143.255.24.59 \n")
                                f.write("tunnel source " + str(interface_source) +"\n")
                                f.write("ip nhrp map " + str(ipv4_tun_taylor) + " 143.255.24.59 \n")                                
                                f.write("ip mtu 1344 \n")                                
                                f.write("ip nhrp registration timeout 50 \n")
                                f.write("ip tcp adjust-mss 1300 \n")                        
                                f.write("tunnel mode gre multipoint \n")                        
                                f.write("ip nhrp holdtime 300 \n")                      
                                f.write("tunnel protection ipsec profile lab shared \n")
                                f.write("ip nhrp nhs " + str(ipv4_tun_taylor) +"\n")
                                f.write("delay 20000 \n")
                                f.write("tunnel key " + str(key_taylor) +"\n")
                                f.write("ip nhrp network-id " + str(key_taylor) +"\n")
                                f.write("ip nhrp authentication " + auth_taylor +"\n") 
                                f.write("\n") 
                                f.write("\n") 
                                
                                                      

                        # configuracion para chagall                    
                                f.write("configuracion para chagall")
                                f.write("\n") 
                                f.write("\n") 
                                f.write("interface tunnel 42 \n") 
                                f.write("ip vrf forwarding admin \n")
                                f.write("ip address " + str(ipv4_borde_a_chagall) + str(mask) +"\n")
                                f.write("description tun42 a tun" + str(tunnel) + " en Chagall del servicio ADMIN - XG \n")
                                f.write("ip nhrp map multicast 143.255.26.59 \n")
                                f.write("tunnel source " + str(interface_source)+"\n")                        
                                f.write("ip nhrp map " + str(ipv4_tun_chagall)+ " 143.255.26.59 \n")                        
                                f.write("ip nhrp registration timeout 50 \n")
                                f.write("ip tcp adjust-mss 1300 \n") 
                                f.write("ip nhrp holdtime 300 \n") 
                                f.write("ip mtu 1344 \n")                         
                                f.write("tunnel mode gre multipoint \n")                        
                                f.write("tunnel protection ipsec profile RIEMANN_CEL shared \n")
                                f.write("delay 70000 \n")
                                f.write("ip nhrp nhs " + str(ipv4_tun_chagall)+"\n")
                                f.write("tunnel key " + str(key_chagall) +"\n")
                                f.write("ip nhrp network-id " + str(key_chagall) +"\n")
                                f.write("ip nhrp authentication " + auth_chagall +"\n")
                                f.write("\n")  
                                f.write("\n")  
                                
                                f.close()
                                
                                print("\n")       
                                print(" ** Se ha creado el archivo con el script ** ")
                                print("\n")       
                                
                        
                        if vrf == "admin" and tipo_conexion == "ftth/vsat":                                
                                
                                interface_source=input("Indique la interface source para FTTH/VSAT: ")
                                f.write("interface tunnel 10 \n") 
                                f.write("ip vrf forwarding admin \n")
                                f.write("ip address " + str(ipv4_borde_a_taylor) + str(mask) + "\n")
                                f.write("description tun10 a tun" + str(tunnel) + " en Taylor del servicio ADMIN - FTTH/VSAT \n")
                                f.write("ip nhrp map multicast 143.255.24.60 \n")
                                f.write("tunnel source " + str(interface_source) + "\n")
                                f.write("ip nhrp map " + str(ipv4_tun_taylor) + " 143.255.24.60 \n")                                
                                f.write("ip mtu 1344 \n")                                
                                f.write("ip nhrp registration timeout 50 \n")
                                f.write("ip tcp adjust-mss 1300 \n")                        
                                f.write("tunnel mode gre multipoint \n")                        
                                f.write("ip nhrp holdtime 300 \n")                      
                                f.write("tunnel protection ipsec profile LAB2 shared \n")
                                f.write("ip nhrp nhs " + str(ipv4_tun_taylor)+ "\n")                                
                                f.write("tunnel key " + str(key_taylor)+ "\n")
                                f.write("ip nhrp network-id " + str(key_taylor)+"\n")
                                f.write("ip nhrp authentication " + auth_taylor + "\n")
                                f.write("\n")  
                                f.write("\n")

                        # configuracion para chagall                         
                                           
                                f.write("configuracion para chagall")
                                f.write("\n") 
                                f.write("\n")                
                                f.write("interface tunnel 20 \n") 
                                f.write("ip vrf forwarding admin \n")
                                f.write("ip address " + str(ipv4_borde_a_chagall) + str(mask) + "\n")
                                f.write("description tun20 a tun" + str(tunnel) + " en Chagall del servicio ADMIN - FTTH/VSAT \n")
                                f.write("ip nhrp map multicast 143.255.26.60 \n")
                                f.write("tunnel source " + str(interface_source) + "\n")                        
                                f.write("ip nhrp map " + str(ipv4_tun_chagall) + " 143.255.26.60 \n")                        
                                f.write("ip nhrp registration timeout 50 \n")
                                f.write("ip tcp adjust-mss 1300 \n")
                                f.write("ip nhrp holdtime 300 \n") 
                                f.write("ip mtu 1344 \n")                         
                                f.write("tunnel mode gre multipoint \n")                        
                                f.write("tunnel protection ipsec profile RIEMANN_FO shared \n")
                                f.write("delay 40000 \n")
                                f.write("ip nhrp nhs " + str(ipv4_tun_chagall) + "\n")
                                f.write("tunnel key " + str(key_chagall) + "\n")
                                f.write("ip nhrp network-id " + str(key_chagall) + "\n")
                                f.write("ip nhrp authentication " + auth_chagall + "\n")

                                f.close()
                                print("\n")       
                                print(" ** Se ha creado el archivo con el script ** ")
                                print("\n")       
                        
                        if vrf != "admin" and tipo_conexion == "xg":
                                
                                interface_source=input("Indique la interface source para DATOS - XG: ")
                                f.write("interface tunnel 21 \n") 
                                f.write("ip vrf forwarding " + str(vrf) + "\n") 
                                f.write("ip address " + str(ipv4_borde_a_taylor) + str(mask) + "\n")
                                f.write("description tun21 a tun" + str(tunnel) + " en Taylor del servicio DATOS - XG \n")
                                f.write("ip nhrp map multicast 143.255.24.59 \n")
                                f.write("tunnel source " + str(interface_source) + "\n")
                                f.write("ip nhrp map " + str(ipv4_tun_taylor) + " 143.255.24.59 \n")                                
                                f.write("ip mtu 1344 \n")                                
                                f.write("ip nhrp registration timeout 50 \n")
                                f.write("ip tcp adjust-mss 1300 \n")                        
                                f.write("tunnel mode gre multipoint \n")                        
                                f.write("ip nhrp holdtime 300 \n")  
                                f.write("delay 20000 \n")                    
                                f.write("tunnel protection ipsec profile lab shared \n")
                                f.write("ip nhrp nhs " + str(ipv4_tun_taylor) + "\n")                                
                                f.write("tunnel key " + str(key_taylor) + "\n")
                                f.write("ip nhrp network-id " + str(key_taylor) + "\n")
                                f.write("ip nhrp authentication " + auth_taylor + "\n")
                                f.write("\n")  
                                f.write("\n")  

                        # configuracion para chagall  
                         
                                          
                                f.write("configuracion para chagall")
                                f.write("\n") 
                                f.write("\n")               
                                f.write("interface tunnel 41 \n") 
                                f.write("ip vrf forwarding " + str(vrf) + "\n") 
                                f.write("ip address " + str(ipv4_borde_a_chagall) + str(mask) + "\n")
                                f.write("description tun41 a tun" + str(tunnel) + " en Chagall del servicio DATOS - XG  \n")
                                f.write("ip nhrp map multicast 143.255.26.59 \n")
                                f.write("tunnel source " + str(interface_source) + "\n")                        
                                f.write("ip nhrp map " + str(ipv4_tun_chagall) + " 143.255.26.59 \n")                        
                                f.write("ip nhrp registration timeout 50 \n")
                                f.write("ip tcp adjust-mss 1300 \n") 
                                f.write("ip mtu 1344 \n")                         
                                f.write("tunnel mode gre multipoint \n")                        
                                f.write("tunnel protection ipsec profile RIEMANN_CEL shared \n")
                                f.write("delay 70000 \n")
                                f.write("ip nhrp holdtime 300 \n")
                                f.write("ip nhrp nhs " + str(ipv4_tun_chagall) + "\n")
                                f.write("tunnel key " + str(key_chagall) + "\n")
                                f.write("ip nhrp network-id " + str(key_chagall) + "\n")
                                f.write("ip nhrp authentication " + auth_chagall + "\n") 
                                f.close()
                                print(" ** Se ha creado el archivo con el script ** ")       
                        
                        if vrf != "admin" and tipo_conexion == "ftth/vsat":                                
                                
                                interface_source=input("Indique la interface source para XG: ")
                                f.write("interface tunnel 1 \n") 
                                f.write("ip vrf forwarding " + str(vrf) + "\n") 
                                f.write("ip address " + str(ipv4_borde_a_taylor) + str(mask) + "\n")
                                f.write("description tun1 a tun" + str(tunnel) + " en Taylor del servicio DATOS - FTTH/VSAT \n")
                                f.write("ip nhrp map multicast 143.255.24.60 \n")
                                f.write("tunnel source " + str(interface_source) + "\n")
                                f.write("ip nhrp map " + str(ipv4_tun_taylor) + " 143.255.24.60 \n")                                
                                f.write("ip mtu 1344 \n")                                
                                f.write("ip nhrp registration timeout 50 \n")
                                f.write("ip tcp adjust-mss 1300 \n")                        
                                f.write("tunnel mode gre multipoint \n")                        
                                f.write("ip nhrp holdtime 300 \n")
                                f.write("tunnel protection ipsec profile LAB2 shared \n")
                                f.write("ip nhrp nhs " + str(ipv4_tun_taylor) + "\n")                                
                                f.write("tunnel key " + str(key_taylor) + "\n")
                                f.write("ip nhrp network-id " + str(key_taylor) + "\n")
                                f.write("ip nhrp authentication " + auth_taylor + "\n")
                                f.write("\n")  
                                f.write("\n") 

                        # configuracion para chagall 
                         
                                           
                                f.write("configuracion para chagall")
                                f.write("\n") 
                                f.write("\n")                  
                                f.write("interface tunnel 2 \n") 
                                f.write("ip vrf forwarding " + str(vrf) + "\n") 
                                f.write("ip address " + str(ipv4_borde_a_chagall) + str(mask) + "\n")
                                f.write("description tun2 a tun" + str(tunnel) + " en Chagall del servicio DATOS - FTTH/VSAT \n")
                                f.write("ip nhrp map multicast 143.255.26.60 \n")
                                f.write("tunnel source " + str(interface_source) + "\n")                        
                                f.write("ip nhrp map " + str(ipv4_tun_chagall) + " 143.255.26.60 \n")                        
                                f.write("ip nhrp registration timeout 50 \n")
                                f.write("ip tcp adjust-mss 1300 \n") 
                                f.write("ip mtu 1344 \n")                         
                                f.write("tunnel mode gre multipoint \n")                        
                                f.write("tunnel protection ipsec profile RIEMANN_FO shared \n")
                                f.write("delay 40000 \n")
                                f.write("ip nhrp holdtime 300 \n")
                                f.write("ip nhrp nhs " + str(ipv4_tun_chagall) + "\n")
                                f.write("tunnel key " + str(key_chagall) + "\n")
                                f.write("ip nhrp network-id " + str(key_chagall) + "\n")
                                f.write("ip nhrp authentication " + auth_chagall + "\n")
                                f.close()
                                print("\n")       
                                print(" ** Se ha creado el archivo con el script ** ")
                                print("\n")

                if num_de_tuneles == 8:

                        ipv4_borde_a_chagall
                        ipv4_borde_a_chagall_xg
                        ipv4_borde_a_chagall_dato_ftth
                        ipv4_borde_a_chagall_dato_xg
                        ipv4_borde_a_taylor
                        ipv4_borde_a_taylor_xg
                        ipv4_borde_a_taylor_datos_ftth
                        ipv4_borde_a_taylor_datos_xg
                        # print(ipv4_borde_a_chagall) 
                        # print(ipv4_borde_a_chagall_xg) 
                        # print(ipv4_borde_a_chagall_dato_ftth) 
                        # print(ipv4_borde_a_chagall_dato_xg)
                        # print(ipv4_borde_a_taylor) 
                        # print(ipv4_borde_a_taylor_xg) 
                        # print(ipv4_borde_a_taylor_datos_ftth) 
                        # print(ipv4_borde_a_taylor_datos_xg)

                        #archivo-salida.py
                        f = open ("config_" + str(nombre_cpe) + ".txt",'w')
                                                                    
                        
                        # configuracion para taylor
                        
                        f.write("configuracion para taylor")
                        f.write("\n")                                             
                        f.write("\n")                                           
                        interface_source_xg=input("Indique la interface source para XG: ")
                        f.write("interface tunnel 22 \n") 
                        f.write("ip vrf forwarding admin \n")
                        f.write("ip address " + str(ipv4_borde_a_taylor_xg) + str(mask) +"\n")
                        f.write("description tun22 a tun" + str(tunnel + 1) + " en Taylor del servicio ADMIN - XG \n")
                        f.write("ip nhrp map multicast 143.255.24.59 \n")
                        f.write("tunnel source " + str(interface_source_xg) +"\n")
                        f.write("ip nhrp map " + str(ipv4_tun_taylor_vrf_admin_xg) + " 143.255.24.59 \n")                                
                        f.write("ip mtu 1344 \n")                                
                        f.write("ip nhrp registration timeout 50 \n")
                        f.write("ip tcp adjust-mss 1300 \n")                        
                        f.write("tunnel mode gre multipoint \n")                        
                        f.write("ip nhrp holdtime 300 \n")                      
                        f.write("tunnel protection ipsec profile lab shared \n")
                        f.write("ip nhrp nhs " + str(ipv4_tun_taylor_vrf_admin_xg) +"\n")
                        f.write("delay 20000 \n")
                        f.write("tunnel key " + str(key_taylor_admin_xg) +"\n")
                        f.write("ip nhrp network-id " + str(key_taylor_admin_xg) +"\n")
                        f.write("ip nhrp authentication " + auth_taylor_admin_xg +"\n") 
                        f.write("\n") 
                        f.write("\n")

                        f.write("interface tunnel 21 \n") 
                        f.write("ip vrf forwarding " + str(vrf) + "\n") 
                        f.write("ip address " + str(ipv4_borde_a_taylor_datos_xg) + str(mask) + "\n")
                        f.write("description tun21 a tun" + str(tunnel + 3) + " en Taylor del servicio DATOS - XG \n")
                        f.write("ip nhrp map multicast 143.255.24.59 \n")
                        f.write("tunnel source " + str(interface_source_xg) + "\n")
                        f.write("ip nhrp map " + str(ipv4_tun_taylor_vrf_datos_xg) + " 143.255.24.59 \n")                                
                        f.write("ip mtu 1344 \n")                                
                        f.write("ip nhrp registration timeout 50 \n")
                        f.write("ip tcp adjust-mss 1300 \n")                        
                        f.write("tunnel mode gre multipoint \n")                        
                        f.write("ip nhrp holdtime 300 \n")  
                        f.write("delay 20000 \n")                    
                        f.write("tunnel protection ipsec profile la shared \n")
                        f.write("ip nhrp nhs " + str(ipv4_tun_taylor_vrf_datos_xg) + "\n")                                
                        f.write("tunnel key " + str(key_taylor_dato_xg) + "\n")
                        f.write("ip nhrp network-id " + str(key_taylor_dato_xg) + "\n")
                        f.write("ip nhrp authentication " + auth_taylor_dato_xg + "\n")
                        f.write("\n")  
                        f.write("\n")  

                        

                        interface_source_ftth=input("Indique la interface source para FTTH/VSAT: ")
                        f.write("interface tunnel 10 \n") 
                        f.write("ip vrf forwarding admin \n")
                        f.write("ip address " + str(ipv4_borde_a_taylor) + str(mask) + "\n")
                        f.write("description tun10 a tun" + str(tunnel) + " en Taylor del servicio ADMIN - FTTH/VSAT \n")
                        f.write("ip nhrp map multicast 143.255.24.60 \n")
                        f.write("tunnel source " + str(interface_source_ftth) + "\n")
                        f.write("ip nhrp map " + str(ipv4_tun_taylor_vrf_admin) + " 143.255.24.60 \n")                                
                        f.write("ip mtu 1344 \n")                                
                        f.write("ip nhrp registration timeout 50 \n")
                        f.write("ip tcp adjust-mss 1300 \n")                        
                        f.write("tunnel mode gre multipoint \n")                        
                        f.write("ip nhrp holdtime 300 \n")                      
                        f.write("tunnel protection ipsec profile LA2 shared \n")
                        f.write("ip nhrp nhs " + str(ipv4_tun_taylor_vrf_admin)+ "\n")                                
                        f.write("tunnel key " + str(key_taylor)+ "\n")
                        f.write("ip nhrp network-id " + str(key_taylor)+"\n")
                        f.write("ip nhrp authentication " + auth_taylor_adm_ftth + "\n")
                        f.write("\n")  
                        f.write("\n") 

                        f.write("interface tunnel 1 \n") 
                        f.write("ip vrf forwarding " + str(vrf) + "\n") 
                        f.write("ip address " + str(ipv4_borde_a_taylor_datos_ftth) + str(mask) + "\n")
                        f.write("description tun1 a tun" + str(tunnel + 2) + " en Taylor del servicio DATOS - FTTH/VSAT \n")
                        f.write("ip nhrp map multicast 143.255.24.60 \n")
                        f.write("tunnel source " + str(interface_source_ftth) + "\n")
                        f.write("ip nhrp map " + str(ipv4_tun_taylor_vrf_datos) + " 143.255.24.60 \n")                                
                        f.write("ip mtu 1344 \n")                                
                        f.write("ip nhrp registration timeout 50 \n")
                        f.write("ip tcp adjust-mss 1300 \n")                        
                        f.write("tunnel mode gre multipoint \n")                        
                        f.write("ip nhrp holdtime 300 \n")
                        f.write("tunnel protection ipsec profile LA2 shared \n")
                        f.write("ip nhrp nhs " + str(ipv4_tun_taylor_vrf_datos) + "\n")                                
                        f.write("tunnel key " + str(key_taylor_dato_ftth) + "\n")
                        f.write("ip nhrp network-id " + str(key_taylor_dato_ftth) + "\n")
                        f.write("ip nhrp authentication " + auth_taylor_dato_ftth + "\n")
                        f.write("\n")  
                        f.write("\n")                                        
                                                

                # configuracion para chagall                    
                        f.write("configuracion para chagall")
                        f.write("\n") 
                        f.write("\n") 
                        f.write("interface tunnel 42 \n") 
                        f.write("ip vrf forwarding admin \n")
                        f.write("ip address " + str(ipv4_borde_a_chagall_xg) + str(mask) +"\n")
                        f.write("description tun42 a tun" + str(tunnel + 1) + " en Chagall del servicio ADMIN - XG \n")
                        f.write("ip nhrp map multicast 143.255.26.59 \n")
                        f.write("tunnel source " + str(interface_source_xg)+"\n")                        
                        f.write("ip nhrp map " + str(ipv4_tun_chagall_vrf_admin_xg)+ " 143.255.26.59 \n")                        
                        f.write("ip nhrp registration timeout 50 \n")
                        f.write("ip tcp adjust-mss 1300 \n") 
                        f.write("ip nhrp holdtime 300 \n") 
                        f.write("ip mtu 1344 \n")                         
                        f.write("tunnel mode gre multipoint \n")                        
                        f.write("tunnel protection ipsec profile RIEMANN_CEL shared \n")
                        f.write("delay 70000 \n")
                        f.write("ip nhrp nhs " + str(ipv4_tun_chagall_vrf_admin_xg)+"\n")
                        f.write("tunnel key " + str(key_chagall_admin_xg) +"\n")
                        f.write("ip nhrp network-id " + str(key_chagall_admin_xg) +"\n")
                        f.write("ip nhrp authentication " + auth_chagall_admin_xg +"\n")
                        f.write("\n")  
                        f.write("\n") 

                        f.write("interface tunnel 41 \n") 
                        f.write("ip vrf forwarding " + str(vrf) + "\n") 
                        f.write("ip address " + str(ipv4_borde_a_chagall_dato_xg) + str(mask) + "\n")
                        f.write("description tun41 a tun" + str(tunnel + 3) + " en Chagall del servicio DATOS - XG  \n")
                        f.write("ip nhrp map multicast 143.255.26.59 \n")
                        f.write("tunnel source " + str(interface_source_xg) + "\n")                        
                        f.write("ip nhrp map " + str(ipv4_tun_chagall_vrf_datos_xg) + " 143.255.26.59 \n")                        
                        f.write("ip nhrp registration timeout 50 \n")
                        f.write("ip tcp adjust-mss 1300 \n") 
                        f.write("ip mtu 1344 \n")                         
                        f.write("tunnel mode gre multipoint \n")                        
                        f.write("tunnel protection ipsec profile RIEMANN_CEL shared \n")
                        f.write("delay 70000 \n")
                        f.write("ip nhrp holdtime 300 \n")
                        f.write("ip nhrp nhs " + str(ipv4_tun_chagall_vrf_datos_xg) + "\n")
                        f.write("tunnel key " + str(key_chagall_dato_xg) + "\n")
                        f.write("ip nhrp network-id " + str(key_chagall_dato_xg) + "\n")
                        f.write("ip nhrp authentication " + auth_chagall_dato_xg + "\n")
                        f.write("\n")  
                        f.write("\n")                                  
                                                              
                                        
                        f.write("interface tunnel 20 \n") 
                        f.write("ip vrf forwarding admin \n")
                        f.write("ip address " + str(ipv4_borde_a_chagall) + str(mask) + "\n")
                        f.write("description tun20 a tun" + str(tunnel) + " en Chagall del servicio ADMIN - FTTH/VSAT \n")
                        f.write("ip nhrp map multicast 143.255.26.60 \n")
                        f.write("tunnel source " + str(interface_source_ftth) + "\n")                        
                        f.write("ip nhrp map " + str(ipv4_tun_chagall_vrf_admin) + " 143.255.26.60 \n")                        
                        f.write("ip nhrp registration timeout 50 \n")
                        f.write("ip tcp adjust-mss 1300 \n")
                        f.write("ip nhrp holdtime 300 \n") 
                        f.write("ip mtu 1344 \n")                         
                        f.write("tunnel mode gre multipoint \n")                        
                        f.write("tunnel protection ipsec profile RIEMANN_FO shared \n")
                        f.write("delay 40000 \n")
                        f.write("ip nhrp nhs " + str(ipv4_tun_chagall_vrf_admin) + "\n")
                        f.write("tunnel key " + str(key_chagall_admin_ftth) + "\n")
                        f.write("ip nhrp network-id " + str(key_chagall_admin_ftth) + "\n")
                        f.write("ip nhrp authentication " + auth_chagall_admin_ftth + "\n")                         
                
                    
                        f.write("\n") 
                        f.write("\n")                  
                        f.write("interface tunnel 2 \n") 
                        f.write("ip vrf forwarding " + str(vrf) + "\n") 
                        f.write("ip address " + str(ipv4_borde_a_chagall_dato_ftth) + str(mask) + "\n")
                        f.write("description tun2 a tun" + str(tunnel + 2) + " en Chagall del servicio DATOS - FTTH/VSAT \n")
                        f.write("ip nhrp map multicast 143.255.26.60 \n")
                        f.write("tunnel source " + str(interface_source_ftth) + "\n")                        
                        f.write("ip nhrp map " + str(ipv4_tun_chagall_vrf_datos) + " 143.255.26.60 \n")                        
                        f.write("ip nhrp registration timeout 50 \n")
                        f.write("ip tcp adjust-mss 1300 \n") 
                        f.write("ip mtu 1344 \n")                         
                        f.write("tunnel mode gre multipoint \n")                        
                        f.write("tunnel protection ipsec profile RIEMANN_FO shared \n")
                        f.write("delay 40000 \n")
                        f.write("ip nhrp holdtime 300 \n")
                        f.write("ip nhrp nhs " + str(ipv4_tun_chagall_vrf_datos) + "\n")
                        f.write("tunnel key " + str(key_chagall_dato_ftth) + "\n")
                        f.write("ip nhrp network-id " + str(key_chagall_dato_ftth) + "\n")
                        f.write("ip nhrp authentication " + auth_chagall_dato_ftth + "\n")
                        f.close()
                        print("\n")       
                        print(" ** Se ha creado el archivo con el script ** ")
                        print("\n")
















def borrar_core():
        Login_para_borrar()
        tn.write(b"configure terminal \n")
        time.sleep(1)
        tn.write(b"no interface tunnel 700 \n")
        tn.write(b"no interface tunnel 701 \n")
        tn.write(b"no interface tunnel 702 \n")
        tn.write(b"no interface tunnel 703 \n")
        time.sleep(1)
        Login_concentrador_respaldo_borrar()
        tn.write(b"configure terminal \n")
        time.sleep(1)
        tn.write(b"no interface tunnel 700 \n")
        tn.write(b"no interface tunnel 701 \n")
        tn.write(b"no interface tunnel 702 \n")
        tn.write(b"no interface tunnel 703 \n")

def borrar_borde():
        Login_borde_borrar()
        tn.write(b"configure terminal \n")
        time.sleep(1)
        tn.write(b"no interface tunnel 1 \n")
        tn.write(b"no interface tunnel 2 \n")
        tn.write(b"no interface tunnel 10 \n")
        tn.write(b"no interface tunnel 20 \n")
        tn.write(b"no interface tunnel 21 \n")
        tn.write(b"no interface tunnel 22 \n")
        tn.write(b"no interface tunnel 41 \n")
        tn.write(b"no interface tunnel 42 \n")

def Login_borde_borrar():
        global tn, router_name_ppl
        Host = "10.10.10.180"
        user_taylor = "yhs"
        password_taylor = "P1r@m1d3_1ooo*"
        tn=telnetlib.Telnet(Host)
        tn.read_until(b"Username: " )
        tn.write(user_taylor.encode('ascii') + b"\n")
        if password_taylor:
                tn.read_until(b"Password: ")
                tn.write(password_taylor.encode('ascii')+b"\n")
        tn.write(b" terminal length 512 \n")        
        hostname=(tn.read_until(b"#", timeout=120 ))
        router_name_ppl=hostname.decode('ascii')
        print(" \n ")
        print("Conexion abierta a",router_name_ppl[2:-1].strip()) 
        return tn, router_name_ppl 

def Login_para_borrar():
        global Host_taylor, user_taylor, password_taylor   

        # Host_taylor="192.168.100.228"  #temporalmente zeeman para pruebas        
        user_taylor="yhs"
        
        # password=getpass.getpass()
        password_taylor="P1r@m1d3_1ooo*"
        Host_taylor="192.168.100.246"               
                    
        Open_telnet_principal(Host_taylor, user_taylor, password_taylor)               
        return Host_taylor + user_taylor + password_taylor

def Open_telnet_borrar(Host_taylor, user_taylor, password_taylor):     
        global tn, router_name_ppl
        tn=telnetlib.Telnet(Host_taylor)
        tn.read_until(b"Username: " )
        tn.write(user_taylor.encode('ascii') + b"\n")
        if password_taylor:
                tn.read_until(b"Password: ")
                tn.write(password_taylor.encode('ascii')+b"\n")
        tn.write(b" terminal length 512 \n")        
        hostname=(tn.read_until(b"#", timeout=120 ))
        router_name_ppl=hostname.decode('ascii')
        print(" \n ")
        print("Conexion abierta a",router_name_ppl[2:-1].strip()) 
        return tn, router_name_ppl 

def Login_concentrador_respaldo_borrar():
        user_taylor="yhs"
        
        # password=getpass.getpass()
        password_taylor="P1r@m1d3_1ooo*"
        Host_taylor="10.230.10.8"               
                    
        Open_telnet_principal_borrar(Host_taylor, user_taylor, password_taylor)               
        return Host_taylor + user_taylor + password_taylor

def Open_telnet_principal_borrar(Host_taylor, user_taylor, password_taylor):
        global tn, router_name_ppl
        tn=telnetlib.Telnet(Host_taylor)
        tn.read_until(b"Username: " )
        tn.write(user_taylor.encode('ascii') + b"\n")
        if password_taylor:
                tn.read_until(b"Password: ")
                tn.write(password_taylor.encode('ascii')+b"\n")
        tn.write(b" terminal length 512 \n")        
        hostname=(tn.read_until(b"#", timeout=120 ))
        router_name_ppl=hostname.decode('ascii')
        print(" \n ")
        print("Conexion abierta a",router_name_ppl[2:-1].strip()) 
        return tn, router_name_ppl 


# Login_borde() 