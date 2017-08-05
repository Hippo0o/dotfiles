
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

[[ $DISPLAY ]] && shopt -s checkwinsize

PS1='\[\033[01;31m\][\u@\h\[\033[01;37m\] \W\[\033[01;31m\]]\$\[\033[00m\] '

# custom global bash
shopt -s expand_aliases

alias ll='ls -alFh --group-directories-first --color=auto'
alias update='yaourt -Syua'

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

# Enable history appending instead of overwriting.  #139609
shopt -s histappend

#enable colors for some commands
alias ls='ls --color=auto'
alias grep='grep --colour=auto'
alias egrep='egrep --colour=auto'
alias fgrep='fgrep --colour=auto'

# better yaourt colors
export YAOURT_COLORS="nb=1:pkg=1:ver=1;32:lver=1;45:installed=1;42:grp=1;34:od=1;41;5:votes=1;44:dsc=0:other=1;35"

# yaourt editor
export VISUAL="vim"

#local binary path
PATH=$PATH:$HOME/.local/bin:$(ruby -rubygems -e 'puts Gem.user_dir')/bin:$HOME/.local/lib/node_modules/bin:$HOME/.config/composer/vendor/bin

#
# # ex - archive extractor
# # usage: ex <file>
ex ()
{
  if [ -f $1 ] ; then
    case $1 in
      *.tar.bz2)   tar xjf $1   ;;
      *.tar.gz)    tar xzf $1   ;;
      *.bz2)       bunzip2 $1   ;;
      *.rar)       unrar x $1     ;;
      *.gz)        gunzip $1    ;;
      *.tar)       tar xf $1    ;;
      *.tbz2)      tar xjf $1   ;;
      *.tgz)       tar xzf $1   ;;
      *.zip)       unzip $1     ;;
      *.Z)         uncompress $1;;
      *.7z)        7z x $1      ;;
      *)           echo "'$1' cannot be extracted via ex()" ;;
    esac
  else
    echo "'$1' is not a valid file"
  fi
}

# neofetch
neofetch --color_blocks off --ascii_distro arch --ascii_colors 7 --colors 1 7 7 1
