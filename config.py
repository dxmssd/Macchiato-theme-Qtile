# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, hook, Screen, KeyChord
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.dgroups import simple_key_binder



mod = "mod4" #aka Windows key
terminal = "ghostty" #This is an example on how flexible Qtile is, you create variables then use them in a keybind for example (see below)
mod1 = "mod1" #alt key
filemanager = "thunar"

# Sticky windows

sticky_windows = []

@lazy.function
def toggle_sticky_windows(qtile, window=None):
    if window is None:
        window = qtile.current_screen.group.current_window
    if window in sticky_windows:
        sticky_windows.remove(window)
    else:
        sticky_windows.append(window)
    return window

@hook.subscribe.setgroup
def move_sticky_windows():
    for window in sticky_windows:
        window.togroup()
    return

@hook.subscribe.client_killed
def remove_sticky_windows(window):
    if window in sticky_windows:
        sticky_windows.remove(window)

# Below is an example how to make Firefox Picture-in-Picture windows automatically sticky.
@hook.subscribe.client_managed
def auto_sticky_windows(window):
    info = window.info()
    if (info['wm_class'] == ['Toolkit', 'firefox']
            and info['name'] == 'Picture-in-Picture'):
        sticky_windows.append(window)

# █▄▀ █▀▀ █▄█ █▄▄ █ █▄░█ █▀▄ █▀
# █░█ ██▄ ░█░ █▄█ █ █░▀█ █▄▀ ▄█

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    # Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
     
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle focused window to fullscreen"),
    Key([mod], "v", lazy.window.toggle_floating(), desc="Toggle focused window to floating"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    #WOFI 
    Key([mod], "space", lazy.spawn("rofi -show drun -show-icons"), desc="Spawn a command using a prompt widget"),


##CUSTOM
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume 0 +1%"), desc='Volume Up'),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume 0 -1%"), desc='volume down'),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"), desc='Volume Mute'),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc='playerctl'),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc='playerctl'),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc='playerctl'),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl s 5%+"), desc='brightness UP'),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl s 5%-"), desc='brightness Down'),
    
##Misc keybinds
    Key([], "Print", lazy.spawn("flameshot gui"), desc='Screenshot'),
    Key(["control"], "Print", lazy.spawn("flameshot full -c -p ~/Pictures/"), desc='Screenshot'),
    Key([mod], "e", lazy.spawn(filemanager), desc="Open file manager"),
    Key([mod], "s",toggle_sticky_windows(), desc="Toggle state of sticky for current window"),
]   

# █▀▀ █▀█ █▀█ █░█ █▀█ █▀
# █▄█ █▀▄ █▄█ █▄█ █▀▀ ▄█

#======================================================================================
#================== ETONORNOS VIRUTALES INDEPENDIENTE POR MONITO ======================
#======================================================================================
from libqtile.config import Group, Key
from libqtile.lazy import lazy
# 1. Definimos los grupos físicos (3 para la pantalla 0, 3 para la pantalla 1)
groups = [
    Group("1", screen_affinity=0),
    Group("2", screen_affinity=0),
    Group("3", screen_affinity=0),
    Group("4", screen_affinity=1),
    Group("5", screen_affinity=1),
    Group("6", screen_affinity=1),
]
# 2. Función mágica para cambiar de escritorio estilo Hyprland/GNOME
def go_to_group(name):
    @lazy.function
    def __inner(qtile):
        # Detecta en qué monitor físico estás parado ahora mismo
        current_screen = qtile.current_screen.index
        
        # Si estás en el Monitor Principal (0), las teclas 1,2,3 te llevan al 1,2,3
        # Si estás en el Monitor Secundario (1), las teclas 1,2,3 te llevan al 4,5,6
        target_group = name
        if current_screen == 1:
            if name == "1": target_group = "4"
            elif name == "2": target_group = "5"
            elif name == "3": target_group = "6"
            
        qtile.groups_map[target_group].toscreen()
    return __inner

# 3. Función para enviar ventanas al escritorio del monitor actual
def move_to_group(name):
    @lazy.function
    def __inner(qtile):
        current_screen = qtile.current_screen.index
        target_group = name
        if current_screen == 1:
            if name == "1": target_group = "4"
            elif name == "2": target_group = "5"
            elif name == "3": target_group = "6"
            
        qtile.current_window.togroup(target_group)
    return __inner

# 4. Mapeamos las teclas "1", "2" y "3" de tu teclado
for i in ["1", "2", "3"]:
    keys.extend([
        # Super + 1, 2 o 3: Cambia el escritorio SOLO en el monitor donde está el mouse
        Key([mod], i, go_to_group(i)),
        # Super + Shift + 1, 2 o 3: Mueve la ventana al escritorio correspondiente de ese monitor
        Key([mod, "shift"], i, move_to_group(i)),
    ])

###𝙇𝙖𝙮𝙤𝙪𝙩###

BORDER_FOCUS_BASE = "#9c77c9d8"
BORDER_NORMAL_OSCURO = '#1e1e2e'



layouts = [ #cambiar el color de los borde de las pantallas 
    layout.Columns(
        margin = 0,
        border_focus = BORDER_FOCUS_BASE,
        border_normal = BORDER_NORMAL_OSCURO,
        border_width = 2,
        
    ),
    
    layout.Max(
        border_focus = BORDER_FOCUS_BASE,
        border_normal = BORDER_NORMAL_OSCURO,
        margin = 3,
        border_width = 0,
    ),
    
    layout.Floating(
        border_focus = BORDER_FOCUS_BASE,
        border_normal = BORDER_NORMAL_OSCURO,
        margin = 3,
        border_width = 3,
    ),
    # Try more layouts by unleashing below layouts
   #  layout.Stack(num_stacks=2),
   #  layout.Bsp(),
     layout.Matrix(
        border_focus = BORDER_FOCUS_BASE,
        border_normal = BORDER_NORMAL_OSCURO,
        margin = 3,
        border_width = 3,
    ),
     
    layout.MonadWide(
        border_focus = BORDER_FOCUS_BASE,
        border_normal = BORDER_NORMAL_OSCURO,
        margin = 3,
        border_width = 3,
    ),
    layout.Tile(
        border_focus = BORDER_FOCUS_BASE,
        border_normal = BORDER_NORMAL_OSCURO,
        margin = 3,
        border_width = 3,
    ),
   #  layout.TreeTab(),
   #  layout.VerticalTile(),
   #  layout.Zoomy(),
]


widget_defaults = dict(
    font = "JetBrainsMono Nerd Font",
    fontsize = 12,
    padding = 4,
)

extension_defaults = widget_defaults.copy()


def open_launcher():
    qtile.cmd_spawn("rofi -theme rounded-green-dark -show drun")

def open_btop():
    qtile.cmd_spawn("alacritty --hold -e btop")

def limpiar_nombre_ventana(text):
    if not text:
        return ""
    #listas de apps
    apps = {
        "firefox": "Firefox",
        "code": "VS Code",
        "visual studio code": "VS Code",
        "ghostty": "Terminal",
        "alacritty": "Terminal",
        "kitty": "Terminal",
        "thunar": "Archivos",
        "discord": "Discord",
        "spotify": "Spotify"
    }
    
    text_lower = text.lower()
    for key, value in apps.items():
        if key in text_lower:
            return value
    #en el caso que la app no este en la lista, tambien corta el texto si es muy largo
    return text if len(text) <= 15 else text[:15] + "..."

#formato fecha
def obtener_hora_am_pm():
    import datetime
    ahora = datetime.datetime.now()
    
    # Calculamos el indicador a mano
    indicador = "PM" if ahora.hour >= 12 else "AM"
    
    # Formateamos la hora en formato de 12 horas (%I) y los minutos (%M)
    # Usamos .strftime para los meses en español
    fecha_hora = ahora.strftime("%d %b | %I:%M")
    return f"{fecha_hora} {indicador} |"


#clima
def obtener_clima():
    import urllib.request
    try:
        # Forzamos que devuelva solo el número de la temperatura sin rodeos
        url = "https://wttr.in/Santiago,Chile?format=%t"
        req = urllib.request.Request(url, headers={'User-Agent': 'curl/7.81.0'}) # <--- Engañamos al server diciendo que somos un curl de terminal
        
        with urllib.request.urlopen(req, timeout=4) as response:
            temp = response.read().decode('utf-8').strip()
        
        # wttr.in a veces devuelve "+3°C", limpiamos el signo de más si te molesta
        temp = temp.replace("+", "")
        
        return f"  {temp}"
    except Exception:
        return "   --°C"
    
            
# █▄▄ ▄▀█ █▀█
# █▄█ █▀█ █▀▄

BASE = '#1e2030'  # El fondo de los widgets
COLOR_SECOND = "#2b2e44" 
COLOR_CILE = '#c19cf2'
TEXT_COLOR = '#cdd6f4' #color de texto
SUBTEXT = '#a6adc8' 
BORDER_COL = '#c19cf2'
BASE_TRANSPARENTE = "#00000000"
FONT = 'JetBrainsMono Nerd Font'
COLOR_ICONS = '#f0e9eb'

#========================================================================
# ============================ SCREEN ===================================
#========================================================================

screens = [
    Screen(
        #ESPACIO ENTRE EL BORDE
        top = bar.Bar( 
            [
                widget.Spacer(
                    length = 10,
                ),
                #border redondeados lado izquierdo
                widget.TextBox(
                    text = "",
                    foreground = BASE,        # El colro base 
                    fontsize = 27.5,            # Tamaño del arco
                    padding = 0
                ),
                #ESPACIO DE LOS ENTORNOS DE PANTALLAS (TRABAJO)
                widget.GroupBox(
                    visible_groups = ['1', '2', '3'] if Screen == 0 else ['4', '5', '6'],
                    font = FONT,
                    highlight_method = 'block',
                    inactive = COLOR_SECOND, #color que tomara cuando no este ocupando el escritorio
                    active = COLOR_SECOND,
                    foreground = COLOR_SECOND, #color como se va a ver los textos
                    background = BASE,
                    this_current_screen_border = COLOR_CILE,
                    disable_drag = True,
                    
                    #redondeo 
                    rounded = True,
                    borderwidth = 2,
                    
                    #tamaño de las capsulas
                    padding_x = 10, #espacio horizonal interno del ovalo
                    padding_y = 6, #espacio vertical interno del ovalo
                    margin_x = 5, #separacion entre los numeros
                    margin_y = 3, 
                    
                ),
                #border redondeados lado derecho
                widget.TextBox(
                    text = "",
                    foreground = BASE,        # El colro base 
                    fontsize = 27.5,            # Tamaño del arco
                    padding = 0
                ),
                widget.Spacer(
                    length = 10,
                     
                ),
                #border redondeados lado izquierdo
                widget.TextBox(
                    text = "",
                    foreground = BASE,        # El colro base 
                    fontsize = 27.5,            # Tamaño del arco
                    padding = 0
                ),
                #CONFUGURACION PARA EL TIPO DE VENTANA (COLUMNS, MATRIX, MAX, FLOATING, ETC..)
                widget.CurrentLayout(
                    background =BASE,
                    foreground = TEXT_COLOR,
                    font = FONT,
                    fontsize = 15,
                    padding = 0,
                ),
                #border redondeados lado derecho
                widget.TextBox(
                    text = "",
                    foreground = BASE,        # El colro base 
                    fontsize = 27.5,            # Tamaño del arco
                    padding = 0
                ),
                widget.Spacer(
                    length = 10,
                ),
                #border redondeados lado izquierdo
                widget.TextBox(
                    text = "",
                    foreground = BASE,        # El colro base 
                    fontsize = 27.5,            # Tamaño del arco
                    padding = 0
                ),
                #CONFIGURACION PARA LOS TEXTO DE LAS APLICACIONES EN LA BARRA DE TAREA
                widget.WindowName(
                    background =BASE,
                    foreground = TEXT_COLOR,
                    fontsize = 15,
                    parse_text = limpiar_nombre_ventana,
                    #padding = 10,
                    width = bar.CALCULATED,
                ),
                widget.TextBox(
                    text = "",
                    foreground = BASE,        # El colro base 
                    fontsize = 27.5,            # Tamaño del arco
                    padding = 0
                ),
                widget.Spacer(
                    length = 500,
            
                ),
                #border redondeados lado izquierdo
                widget.TextBox(
                    text = "",
                    foreground = BASE,        # El colro base 
                    fontsize = 27.5,            # Tamaño del arco
                    padding = 0
                ),
                widget.GenPollText(
                    func = obtener_hora_am_pm,
                    update_interval = 1,
                    format = "%I:%M", 
                    background = BASE,
                    font = FONT,
                    fontsize = 15,
                    padding = 0,
                    mouse_callbacks = {
                      'Button1': lazy.spawn('gsimplecal')  
                    },
                ), 
                widget.GenPollText(
                    func = obtener_clima,
                    update_interval = 900,  # Se actualiza cada 15 minutos (900 segundos) para no saturar tu red
                    background = BASE,
                    font = FONT,
                    fontsize = 15,
                    padding = 10,           # Le damos un poquito de aire a los lados
                    foreground = COLOR_ICONS,
                ),
                #border redondeados lado derecho
                widget.TextBox(
                    text = "",
                    foreground = BASE,        # El colro base 
                    fontsize = 27.5,            # Tamaño del arco
                    padding = 0
                ),
                widget.Spacer(
                    length = 500,
            
                ),
                
                #border redondeados lado izquierdo
                widget.TextBox(
                    text = "",
                    foreground = BASE,        # El colro base 
                    fontsize = 27.5,            # Tamaño del arco
                    padding = 0
                ),
                #volumen 
                widget.TextBox(
                    text="  ",
                    foreground="#c19cf2", # Tu morado/magenta característico
                    background="#1e1e2e", # El fondo oscuro de tu barra
                    padding=2
                ),
                widget.Volume(
                    foreground="#c19cf2",
                    background="#1e1e2e",
                    fmt="{} ",
                    padding=5
                ),
                widget.TextBox(
                    text="|",
                    foreground="#44475a", # Un gris sutil para separar del siguiente widget
                    background="#1e1e2e",
                    padding=2
            ),
                #bluetooth
                #monitoreo
                #idioma de telcado 
                
                widget.TextBox(
                    #inicio de wifi 
                    text = "󰤨", # Ícono premium de Nerd Fonts
                    font = FONT,
                    fontsize = 18,
                    foreground = COLOR_ICONS,   
                    background = BASE,
                    padding = 6,
                    # Al hacerle click izquierdo, te abre el gestor de red en la terminal
                    mouse_callbacks = {
                        'Button1': lambda: qtile.spawn('bash -c "sh ~/.config/qtile/wifimenu.sh"')
                    }
                    #finde wifi
                ),
                #boton para el pagado
                widget.TextBox(
                    #inicio del boton apagado
                    text = "",
                    foreground = COLOR_ICONS,
                    background = BASE,
                    fontsize = 18,
                    padding = 10,
                    mouse_callbacks = {
                            'Button1': lambda: qtile.spawn('bash -c "sh ~/.config/qtile/powermenu.sh"')
                        }
                    #fin del boton apagado
                    
                    ),
                
                #border redondeados lado derecho
                widget.TextBox(
                    text = "",
                    foreground = BASE,        # El colro base 
                    fontsize = 27.5,            # Tamaño del arco
                    padding = 0
                ),
                widget.Spacer(
                    length = 8, # es el espacio transparente que tendra 

                ),

                
            ],
            30,
            background= BASE_TRANSPARENTE,
            margin = [5,0,5,0]
        ),
        wallpaper='~/.config/qtile/Wallpaper/wall.png',
        wallpaper_mode="fill",

    ),
    
    
    
    #monitor 2


    Screen(
        #ESPACIO ENTRE EL BORDE
        top = bar.Bar( 
            [
                widget.Spacer(
                    length = 8, # es el espacio transparente que tendra 

                ),
                #border redondeados lado izquierdo
                widget.TextBox(
                    text = "█",
                    foreground = BASE,        # El colro base 
                    fontsize = 27.5,            # Tamaño del arco
                    padding = 0
                ),
                #ESPACIO DE LOS ENTORNOS DE PANTALLAS (TRABAJO)
                widget.GroupBox(
                    visible_groups = ['1', '2', '3'] if Screen == 0 else ['4', '5', '6'],
                    font = FONT,
                    highlight_method = 'block',
                    inactive = COLOR_SECOND, #color que tomara cuando no este ocupando el escritorio
                    active = COLOR_SECOND,
                    foreground = COLOR_SECOND, #color como se va a ver los textos
                    background = BASE,
                    this_current_screen_border = COLOR_CILE,
                    disable_drag = True,
                    
                    #redondeo 
                    rounded = True,
                    borderwidth = 2,
                    
                    #tamaño de las capsulas
                    padding_x = 10, #espacio horizonal interno del ovalo
                    padding_y = 6, #espacio vertical interno del ovalo
                    margin_x = 5, #separacion entre los numeros
                    margin_y = 3, 
                    
                ),
                #border redondeados lado derecho
                widget.TextBox(
                    text = "",
                    foreground = BASE,        # El colro base 
                    background = '#000000.0', # El fondo transparente de la barra
                    fontsize = 27.5,            # Tamaño del arco
                    padding = 0
                ),
                widget.Spacer(
                    length = 10,
                    background = '#000000.0',    
                ),
                #border redondeados lado izquierdo
                widget.TextBox(
                    text = "",
                    foreground = BASE,        # El colro base 
                    background = '#000000.0', # El fondo transparente de la barra
                    fontsize = 27.5,            # Tamaño del arco
                    padding = 0
                ),
                #CONFUGURACION PARA EL TIPO DE VENTANA (COLUMNS, MATRIX, MAX, FLOATING, ETC..)
                widget.CurrentLayout(
                    background =BASE,
                    foreground = TEXT_COLOR,
                    font = FONT,
                    fontsize = 15,
                    padding = 0,
                ),
                #border redondeados lado derecho
                widget.TextBox(
                    text = "",
                    foreground = BASE,        # El colro base 
                    background = '#000000.0', # El fondo transparente de la barra
                    fontsize = 27.5,            # Tamaño del arco
                    padding = 0
                ),
                widget.Spacer(
                    length = 10,
                    background = '#000000.0',
                ),
                #border redondeados lado izquierdo
                widget.TextBox(
                    text = "",
                    foreground = BASE,        # El colro base 
                    background = '#000000.0', # El fondo transparente de la barra
                    fontsize = 27.5,            # Tamaño del arco
                    padding = 0
                ),
                #CONFIGURACION PARA LOS TEXTO DE LAS APLICACIONES EN LA BARRA DE TAREA
                widget.WindowName(
                    background =BASE,
                    foreground = TEXT_COLOR,
                    fontsize = 15,
                    parse_text = limpiar_nombre_ventana,
                    #padding = 10,
                    width = bar.CALCULATED,
                ),
                #border redondeados lado derecho
                widget.TextBox(
                    text = "",
                    foreground = BASE,        # El colro base 
                    background = '#000000.0', # El fondo transparente de la barra
                    fontsize = 27.5,            # Tamaño del arco
                    padding = 0
                ),
                widget.Spacer(
                    length = 550,
                    background = '#000000.0',
            
                ),
                #border redondeados lado izquierdo
                widget.TextBox(
                    text = "",
                    foreground = BASE,        # El colro base 
                    background = '#000000.0', # El fondo transparente de la barra
                    fontsize = 27.5,            # Tamaño del arco
                    padding = 0
                ),
                widget.GenPollText(
                    func = obtener_hora_am_pm,
                    update_interval = 1,
                    format = "%I:%M", 
                    background = BASE,
                    font = FONT,
                    fontsize = 15,
                    padding = 0,
                    mouse_callbacks = {
                      'Button1': lazy.spawn('gsimplecal')  
                    },
                ), 
                widget.GenPollText(
                    func = obtener_clima,
                    update_interval = 900,  # Se actualiza cada 15 minutos (900 segundos) para no saturar tu red
                    background = BASE,
                    font = FONT,
                    fontsize = 15,
                    padding = 10,           # Le damos un poquito de aire a los lados
                    foreground = TEXT_COLOR,
                ),
                #border redondeados lado derecho
                widget.TextBox(
                    text = "",
                    foreground = BASE,        # El colro base 
                    background = '#000000.0', # El fondo transparente de la barra
                    fontsize = 27.5,            # Tamaño del arco
                    padding = 0
                ),
                widget.Spacer(
                    length = 500,
                    background = '#000000.0',
            
                ),
                
                #border redondeados lado izquierdo
                widget.TextBox(
                    text = "",
                    foreground = BASE,        # El colro base 
                    background = '#000000.0', # El fondo transparente de la barra
                    fontsize = 27.5,            # Tamaño del arco
                    padding = 0
                ),
                #boton para el pagado
                widget.TextBox(
                    text = "", # Icono de apagado de Nerd Fonts
                    font = FONT,
                    fontsize = 14,
                    
                
                    padding = 6,
                    # Al hacer clic izquierdo (Button 1), abre tu menú de apagado (puedes usar rofi si lo tienes)
                    mouse_callbacks = {
                        'Button1': lazy.spawn('systemctl poweroff'), # Clic izquierdo: Apaga el PC
                        'Button3': lazy.spawn('systemctl reboot'),   # Clic derecho: Reinicia el PC
                    },
                ),
                
                #border redondeados lado derecho
                widget.TextBox(
                    text = "",
                    foreground = BASE,        # El colro base 
                    background = '#000000.0', # El fondo transparente de la barra
                    fontsize = 27.5,            # Tamaño del arco
                    padding = 0
                ),
                widget.Spacer(
                    length = 8, # es el espacio transparente que tendra 
                    background = '#000000.0',

                ),

                
            ],
            33,
            background= BASE_TRANSPARENTE,
        ),
        wallpaper='~/.config/qtile/Wallpaper/wall.png',
        wallpaper_mode="fill",

    ),
    

 
    
    #monitor 3
    Screen(
        top = bar.Bar(
            [   
                widget.Spacer(
                    length = 18,
                    background = "#1e2030",
                ),
                
                widget.Image(
                    filename = '~/.config/qtile/Assets/launch_Icon.png',
                    background = '#1e2030',
                    mouse_callbacks = {'Button1': open_launcher},
                ),

                widget.Image(
                    filename = '~/.config/qtile/Assets/6.png',
                ),

                widget.GroupBox(
                    fontsize = 16,
                    borderwidth = 0,
                    highlight_method = 'block',
                    active = '#c19cf2', #Active workspaces circle color
                    block_highlight_text_color = '#c19cf2', #Current workspace circle color
                    highlight_color = '#4B427E',
                    inactive = "#ffffff", #Empty workspace circle
                    foreground = '#c19cf2',
                    background = '#1e2030',
                    this_current_screen_border = "#1e2030", #Circle background color
                    this_screen_border = '#52548D',
                    other_current_screen_border = '#c19cf2',
                    other_screen_border = '#52548D',
                    urgent_border = '#52548D',
                    rounded = True,
                    disable_drag = True,
                 ),

                widget.Image(
                    filename = '~/.config/qtile/Assets/5.png',
                ),

                widget.Image(
                    filename = '~/.config/qtile/Assets/2.png',
                ),
                
                widget.CurrentLayout(
                    background ='#1e2030',
                    font = 'IBM Plex Mono Medium',
                    fontsize = 15,
                    padding = 0,
                ),

                widget.Image(
                    filename = '~/.config/qtile/Assets/5.png',                
                ),

                widget.Image(
                    filename = '~/.config/qtile/Assets/2.png',
                ),

                widget.WindowName(
                    background = '#1e2030',
                    format = "{name}",
                    font = 'IBM Plex Mono Medium',
                    fontsize = 14,
                    empty_group_string = 'Desktop',
                    padding = 0,
                ),

                widget.Image(
                    filename = '~/.config/qtile/Assets/5.png',                
                ),  

                widget.Image(
                    filename = '~/.config/qtile/Assets/1.png',                
                    background = '#1e2030',
                ),

                widget.CPU(
                    font = "IBM Plex Mono Medium",
                    format='CPU:({load_percent:.1f}%/{freq_current}GHz)',
                    fontsize = 15,
                    margin = 0,
                    padding = 0,
                    background = '#1e2030',
                    mouse_callbacks = {'Button1': open_btop},
                ),

                widget.Image(
                    filename = '~/.config/qtile/Assets/5.png',
                ),

                widget.Image(
                    filename = '~/.config/qtile/Assets/2.png',                
                    background = '#1e2030',
                ),  
  
                widget.Systray(
                    background = '#1e2030',
                    icon_size = 24,
                    padding = 3,
                ),

                widget.Image(
                    filename = '~/.config/qtile/Assets/5.png',
                ),

                widget.Image(
                    filename = '~/.config/qtile/Assets/2.png',                
                    background = '#1e2030',
                ),                    
                                                
                widget.Spacer(
                    length = 0,
                    background = '#1e2030',
                ),  
               
                widget.Memory(
                    format = 'RAM:({MemUsed:.0f}MB/{MemTotal:.0f}MB)',
                    font = "IBM Plex Mono Medium",
                    fontsize = 15,
                    padding = 0,
                    background = '#1e2030',
                    mouse_callbacks = {'Button1': open_btop},
                ),

                widget.Spacer(
                    length = 6,
                    background = '#1e2030',
                ),  

                widget.Image(
                    filename = '~/.config/qtile/Assets/Bar-Icons/volume.svg',
                    background = '#1e2030',
                    margin_y = 3,
                    scale = True,
                    mouse_callbacks = {'Button1': open_btop},
                ),

                widget.Spacer(
                    length = 4,
                    background = '#1e2030',
                ), 
                
                widget.PulseVolume(
                    font= 'IBM Plex Mono Medium',
                    fontsize = 15,
                    padding = 0,
                    background = '#1e2030',
                ),

                widget.Image(
                    filename = '~/.config/qtile/Assets/5.png',
                ),                


                widget.Image(
                    filename = '~/.config/qtile/Assets/1.png',                
                    background = '#1e2030',
                ),

                widget.Image(
                    filename = '~/.config/qtile/Assets/Bar-Icons/calendar.svg',
                    background = '#1e2030',
                    margin_y = 3,
                    scale = True,
                ),

                widget.Spacer(
                    length = 6,
                    background = '#1e2030',
                ), 
        
                widget.Clock(
                    format = '%d/%m/%y ', #Here you can change between USA or another timezone
                    background = '#1e2030',
                    font = "IBM Plex Mono Medium",
                    fontsize = 15,
                    padding = 0,
                ),

                widget.Image(
                    filename = '~/.config/qtile/Assets/Bar-Icons/clock.svg',
                    background = '#1e2030',
                    margin_y = 3,
                    margin_x = 5,
                    scale = True,
                ),

                widget.Clock(
                    format = '%H:%M', 
                    background = '#1e2030',
                    font = "IBM Plex Mono Medium",
                    fontsize = 15,
                    padding = 0,
                ),

                widget.Spacer(
                    length = 18,
                    background = '#1e2030',
                ),
            ],
            30,  # Bar size (all axis)
            margin = [0,8,6,8] # Bar margin (Top,Right,Bottom,Left)
        ),
        wallpaper='~/.config/qtile/Wallpaper/Skyscraper.png',
        wallpaper_mode="fill",
    ),
]





# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False #This basically puts your mouse in the center on the screen after you switch to another workspace
floating_layout = layout.Floating(
	border_focus= BORDER_FOCUS_BASE,
	border_normal= BORDER_NORMAL_OSCURO,
	border_width=3,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        
        Match(wm_class="FloatingTUI"),
        
    ]
)

from libqtile import hook
# some other imports
import os
import subprocess
# stuff
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/scripts/autostart.sh') # path to my script, under my user directory
    subprocess.call([home])

auto_fullscreen = True
focus_on_window_activation = "smart" #or focus
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"



import os
import subprocess
from libqtile import hook

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen(['sh', home])
    
    
    
    
    