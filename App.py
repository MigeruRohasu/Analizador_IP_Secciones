#!/usr/bin/env python3

import ipaddress

print("\n")
cantidad_equipos=10
holgura=0.1

ipv4="192.168.1.0/20"
ipv6="2001:db8::/32"

diccionario_global_ipv4 = {}
diccionario_global_ipv6 = {}

ipv6_old=ipv6
ipv4_old=ipv4




def ipConfig(ip, tipo):
    if tipo == "ipv4":
        network = ipaddress.IPv4Network(ip, strict=False)
        return network.network_address, network.broadcast_address, network
    elif tipo == "ipv6":
        network = ipaddress.IPv6Network(ip, strict=False)
        return network.network_address, network.broadcast_address, network


def calcular_segmentos_de_red(cantidad_equipos_memory,ip,version):
    # Obtener la cantidad mínima de bits necesarios para la cantidad de equipos
    bits_necesarios = int(cantidad_equipos_memory - 1).bit_length()
    mascara_subred=0
    network=0
    ip,_=str(ip).split("/")
    # Calcular la máscara de subred necesaria
    if (version=="ipv4"):
        #print("ipv4",ip+"/", str( 32 - bits_necesarios))
        mascara_subred = ipaddress.IPv4Network(ip+"/"+ str( 32 - bits_necesarios), strict=False).netmask
        network=ipaddress.IPv4Network(ip+"/"+ str(32 - bits_necesarios), strict=False)

        print("\n")
        # Imprime los resultados para IPv4
        #print(f"Para {cantidad_equipos} equipos IPv4:")
        print(f"Bits necesarios: {bits_necesarios}")
        #print(f"Máscara de subred: {mascara_subred}")

    elif(version=="ipv6"):
        #print("ipv6", ip , "/" , str(128 - bits_necesarios))
        mascara_subred = ipaddress.IPv6Network(ip + "/" + str(128-bits_necesarios), strict=False).netmask
        network=ipaddress.IPv6Network(ip + "/" + str(128- bits_necesarios), strict=False)
    
        print("\n")
        #print(f"Para {cantidad_equipos} equipos IPv6:")
        #print(f"Bits necesarios: {bits_necesarios}")
        #print(f"Máscara de subred: {mascara_subred}")

    # Calcular el número de segmentos de red necesarios
    numero_segmentos = 2 ** bits_necesarios

    return network


def calcular_rango_por_ciento(numero,porcentaje):
    limite_superior=numero*(1+porcentaje/100)+2
    #limite_superior = numero + (numero * porcentaje)
    print("\n")
    print("Cantidad de equipos calculados:" ,limite_superior)
    return int(limite_superior)


def obtener_informacion_segmento(ip, tipo):
    global diccionario_global_ipv4,diccionario_global_ipv6
    
    subnet_mask_components, broadcast_address, network = ipConfig(ip, tipo)

    # Calcular el primer segmento de direcciones
    first_ip = network.network_address + 1
    last_ip = network.network_address + network.num_addresses - 2
    
    if tipo == "ipv4":
          # Actualizar el diccionario global con la información del segmento actual
        diccionario_global_ipv4[ip] = {
            'Dirección de red': subnet_mask_components,
            'Mascara de red':network.netmask,
            'Dirección de broadcast': broadcast_address,
            'Primer dirección del segmento': first_ip,
            'Última dirección del segmento': last_ip,
            #**informacion_adicional
        }

    elif tipo == "ipv6":
        # Actualizar el diccionario global con la información del segmento actual
        diccionario_global_ipv6[ip] = {
            'Dirección de red': subnet_mask_components,
            'Mascara de red':network.netmask,
            'Dirección de broadcast': broadcast_address,
            'Primer dirección del segmento': first_ip,
            'Última dirección del segmento': last_ip,
            #**informacion_adicional
        }

def imprimir_diccionario(diccionario,tipo):

    if tipo == "ipv4":
        print(f"\nDiccionario global ipv4:")

        for key, value in diccionario.items():
            print(f"{key}:")
            print(f"  Dirección de red: {value['Dirección de red']}")
            print(f"  Mascara de red: {value['Mascara de red']}")
            print(f"  Dirección de broadcast: {value['Dirección de broadcast']}")
            print(f"  Primer dirección asignable: {value['Primer dirección del segmento']}")
            print(f"  Última dirección asignable: {value['Última dirección del segmento']}")

    elif tipo == "ipv6":
        print(f"\nDiccionario global ipv6:")

        for key, value in diccionario.items():
            print(f"{key}:")
            print(f"  Dirección de red: {value['Dirección de red']}")
            print(f"  Mascara de red: {value['Mascara de red']}")
            print(f"  Dirección de broadcast: {value['Dirección de broadcast']}")
            print(f"  Primer dirección asignable: {value['Primer dirección del segmento']}")
            print(f"  Última dirección asignable: {value['Última dirección del segmento']}")

def encontrar_siguiente_segmento(direccion,dirreccion_anteior, lista_segmentos, tipo):
    # Extraer la máscara de la dirección de entrada
    direccion_ip, mascara = str(direccion).split("/")

    print(direccion,dirreccion_anteior, tipo,lista_segmentos.get(direccion))

    print(type(direccion),type(dirreccion_anteior))

    if None == lista_segmentos.get(direccion):
        return direccion

    if tipo == "ipv4":
        info = lista_segmentos[dirreccion_anteior]
        next_address = str(ipaddress.IPv4Address(info['Dirección de broadcast']) + 1) + "/" + mascara
        return ipaddress.IPv4Network(next_address,strict=False)
    elif tipo == "ipv6":
        info = lista_segmentos[dirreccion_anteior]
        next_address = str(ipaddress.IPv6Address(info['Dirección de broadcast']) + 1) + "/" + mascara
        return ipaddress.IPv6Network(next_address,strict=False)

    return None

def App():
    while True:
        global ipv4,ipv6,diccionario_global_ipv4,diccionario_global_ipv6,ipv4_old,ipv6_old

        print(ipv4,"\n",ipv6)
        
        ipv4 = input("Ingrese la Ipv4 a calcular: ")
        ipv6 = input("Ingrese la Ipv6 a calcular: " )

        while True:
            cantidad_equipos = int(input("Ingrese numeros de equipos para nuevo seccion: "))
            holgura=float(input("Ingrese holgura: "))

            cantidad_equipos=calcular_rango_por_ciento(cantidad_equipos,holgura)

            ipv4 = calcular_segmentos_de_red(cantidad_equipos, ipv4,"ipv4")
            ipv6 = calcular_segmentos_de_red(cantidad_equipos, ipv6,"ipv6")            

            obtener_informacion_segmento(ipv4,"ipv4")
            obtener_informacion_segmento(ipv6,"ipv6")

            ipv4_old=ipv4
            ipv6_old=ipv6

            ipv4=encontrar_siguiente_segmento(ipv4,ipv4_old,diccionario_global_ipv4,"ipv4")
            ipv6=encontrar_siguiente_segmento(ipv6,ipv6_old,diccionario_global_ipv6,"ipv6")
            
            ipv4_old=ipv4
            ipv6_old=ipv6

            imprimir_diccionario(diccionario_global_ipv4,"ipv4")
            imprimir_diccionario(diccionario_global_ipv6,"ipv6")

            if "1"==input("salir: "):
                break
        print(diccionario_global_ipv4,"\n",diccionario_global_ipv6)
        if "1"==input("salir: "):
                break
App()

