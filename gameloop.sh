#!/bin/bash

# Script para recargar el juego cuando se modifica cualquier archivo.
# Se monitorizan los cambios con watchmedo y cualquier cambio mata
# el juego y lo vuelve a ejecutar

# Requiere: python3-watchdog
# apt install python3-watchdog

main="extranion/game.py"
windowpos="0 50"

if [[ "$1" == "" ]]
then
	bash $0 start
	watchmedo shell-command --drop --patterns "*.py;*.yaml" --recursive --command="bash $0 \${watch_src_path}"
	exit 0
fi

[[ $1 != "start" ]] && echo -e "\e[1;33m* Modified $1\e[0m"

# Obtenemos la posición de la ventana para luego restaurarla
# Así evitamos que al reiniciar el juego se nos ponga encima de la pantalla
# de desarrollo y tengamos que moverla cada vez
oldpid=$(pgrep -f "python3 $main")
if [[ $oldpid ]]
then
	oldwid=$(xdotool search --onlyvisible --pid $oldpid)
	windowpos=$(xdotool getwindowgeometry $oldwid | grep Position | awk '{print $2}' | tr ',' ' ')
	echo "oldpid: $oldpid"
	echo "oldwid: $oldwid"
fi
echo "windowpos: $windowpos"

# cerramos el juego
pkill -f "python3 $main"
# esperamos a que se cierre
while pgrep -f "python3 $main" > /dev/null
do
	sleep 0.1
done

# iniciamos nuevo juego
echo "Iniciamos juego"
python3 $main &

# obtenemos pid del proceso
pid=$(pgrep -f "python3 $main")
echo "pid: $pid"
# esperamos a que se inicie la ventana y obtengamos su id
wid=""
while [[ $wid == "" ]]
do
	wid=$(xdotool search --onlyvisible --pid $pid 2>/dev/null)
done
wid=$(xdotool search --onlyvisible --pid $pid 2>/dev/null)
echo "wid: $wid"
# restauramos posición
xdotool windowmove $wid $windowpos

