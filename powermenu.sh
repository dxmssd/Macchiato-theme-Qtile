#!/usr/bin/env bash

# Opciones en formato Rofi (Icono + Texto)
opcion_apagar=" Apagar"
opcion_reiniciar=" Reiniciar"
opcion_suspender="󰤄 Suspender"
opcion_salir="󰈆 Cerrar Sesión"

# Juntamos las opciones separadas por saltos de línea
opciones="$opcion_apagar\n$opcion_reiniciar\n$opcion_suspender\n$opcion_salir"

# Lanzamos Rofi con un estilo limpio de menú/lista
seleccionado=$(echo -e "$opciones" | rofi -dmenu -i -p "Sistema:" -theme-str 'window {width: 15%;} listview {lines: 4;}')

# Ejecutar la acción según lo que se apretó
case "$seleccionado" in
    "$opcion_apagar")
        systemctl poweroff
        ;;
    "$opcion_reiniciar")
        systemctl reboot
        ;;
    "$opcion_suspender")
        systemctl suspend
        ;;
    "$opcion_salir")
        qtile cmd-obj -o cmd -f shutdown
        ;;
esac
