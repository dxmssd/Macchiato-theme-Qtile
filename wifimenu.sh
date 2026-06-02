#!/usr/bin/env bash

# Escanear redes Wi-Fi activas
wifi_list=$(nmcli --fields SSID,SECURITY device wifi list | sed '1d' | grep -v ' -- ')

# Si no hay redes, avisar
if [ -z "$wifi_list" ]; then
    rofi -e "No se encontraron redes Wi-Fi"
    exit 1
fi

# Darle un formato lindo con íconos para Rofi
opciones_menu=$(echo "$wifi_list" | awk -F'  +' '{print "󰤨  " $1 " (" $2 ")"}')
opciones_menu="󰤮  Desconectar\n$opciones_menu"

# Lanzar Rofi flotante
seleccionada=$(echo -e "$opciones_menu" | rofi -dmenu -i -p "Selecciona Wi-Fi:" -theme-str 'window {width: 25%;} listview {lines: 6;}')

# Obtener solo el nombre de la red (SSID)
ssid=$(echo "$seleccionada" | sed 's/󰤨  //g' | cut -d'(' -f1 | sed 's/[ \t]*$//')

if [ -z "$seleccionada" ]; then
    exit 0
elif [ "$seleccionada" = "󰤮  Desconectar" ]; then
    nmcli device disconnect wlan0
else
    # Revisar si la red ya está guardada o pide clave
    if nmcli connection show | grep -q "$ssid"; then
        nmcli connection up "$ssid"
    else
        # Pedir la contraseña usando el mismo Rofi de forma elegante
        pass=$(rofi -dmenu -p "Contraseña para $ssid:" -password -theme-str 'window {width: 20%;} listview {lines: 0;}')
        if [ -n "$pass" ]; then
            nmcli device wifi connect "$ssid" password "$pass"
        fi
    fi
fi