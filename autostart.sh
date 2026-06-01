#!/bin/bash

#!/bin/bash

# Configuración real y limpia para las 3 pantallas (Master-G | Xiaomi | Laptop)
xrandr --output DP-1-0 --mode 1920x1080 --rate 60.00 --pos 0x0 --rotate normal \
       --output HDMI-1-0 --primary --mode 1920x1080 --rate 144.00 --pos 1920x0 --rotate normal \
       --output eDP-1 --mode 1920x1080 --rate 59.98 --pos 3840x0 --rotate normal &



picom &
