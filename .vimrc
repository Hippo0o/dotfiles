call vundle#begin()

Plugin 'itchyny/lightline.vim'

call vundle#end()            
filetype plugin indent on    

let g:lightline = {
      \ 'colorscheme': 'wombat',
      \ 'component': {
      \   'readonly': '%{&readonly?"readonly":""}',
      \ }
      \ }
set laststatus=2

syntax on
set number
set nowrap

set t_Co=256            	" use 256 colors in vim

set nocompatible	

set tabstop=4
set shiftwidth=4
set expandtab

colorscheme elflord
