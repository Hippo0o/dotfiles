#local binary path
PATH=$PATH:$HOME/.local/bin:$(ruby -e 'puts Gem.user_dir')/bin:$HOME/.local/lib/node_modules/bin:$HOME/.config/composer/vendor/bin:$(go env GOPATH)/bin

export DE="mate"
export QT_QPA_PLATFORMTHEME="qt5ct"

if [ -z "$DISPLAY" ] && [ -n "$XDG_VTNR" ] && [ "$XDG_VTNR" -eq 1 ]; then
#  exec startx-custom
fi
if [ -z "$DISPLAY" ] && [ -n "$XDG_VTNR" ] && [ "$XDG_VTNR" -eq 4 ]; then
  if [ -f "/tmp/nvidia" ]; then
    exec Xnvidia
  else
    exit
  fi
fi
