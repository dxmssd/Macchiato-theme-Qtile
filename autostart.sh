#!/bin/bash

# Configuración forzada y permanente para las 3 pantallas
xrandr --output DP-1-0 --mode 1920x1080 --pos 0x0 --rotate normal \
       --output HDMI-1-0 --primary --mode 1920x1080 --rate 180 --pos 1920x0 --rotate normal \
       --output eDP-1 --mode 1920x1080 --rate 60 --pos 3840x0 --rotate normal &
