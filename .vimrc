syntax on
set number
set nowrap

set t_Co=256            	" use 256 colors in vim
colorscheme elflord		" an appropriate color scheme

set nocompatible		" be iMproved, required
filetype off			" required

call vundle#begin()

Plugin 'itchyny/lightline.vim'

" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required

let g:lightline = {
      \ 'colorscheme': 'wombat',
      \ 'component': {
      \   'readonly': '%{&readonly?"":""}',
      \ }
      \ }
set laststatus=2

