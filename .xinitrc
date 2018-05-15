#! /bin/sh

userresources=$HOME/.Xresources
usermodmap=$HOME/.Xmodmap
sysresources=/etc/X11/xinit/.Xresources
sysmodmap=/etc/X11/xinit/.Xmodmap

# merge in defaults and keymaps

if [ -f $sysresources ]; then
    xrdb -merge $sysresources
fi

if [ -f $sysmodmap ]; then
    xmodmap $sysmodmap
fi

if [ -f "$userresources" ]; then
    xrdb -merge "$userresources"
fi

if [ -f "$usermodmap" ]; then
    xmodmap "$usermodmap"
fi

# start some nice programs

if [ -d /etc/X11/xinit/xinitrc.d ] ; then
 for f in /etc/X11/xinit/xinitrc.d/?*.sh ; do
  [ -x "$f" ] && . "$f"
 done
 unset f
fi

eval $(/usr/bin/gnome-keyring-daemon --start --components=pkcs11,secrets,ssh)
export SSH_AUTH_SOCK

xrandr --output eDP-1 --mode 1920x1080 --pos 0x0 --rotate normal --output HDMI-1 --off
xrandr --output eDP-1-1 --mode 1920x1080 --pos 0x0 --rotate normal --output HDMI-1-1 --off

/usr/lib/mate-polkit/polkit-mate-authentication-agent-1 &
mate-power-manager &
/usr/lib/mate-settings-daemon/mate-settings-daemon &
xss-lock -- i3lock -c 000000 &
compton -b --config $HOME/.config/compton.conf &
dunst &
nm-applet &
mate-volume-control-applet &
blueman-applet &
xset s off

exec i3
