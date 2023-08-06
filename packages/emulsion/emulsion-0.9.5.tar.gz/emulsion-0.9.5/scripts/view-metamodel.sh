#!/bin/bash
textx visualize $1.tx
#dot -Tpng -O $1.tx.dot
unflatten -c 6 $1.tx.dot |\
    dot -Tpng -Nfontname='Helvetica Neue LT' -Nfontsize=16\
	-Efontname='Linux Libertine O' -Efontsize=18\
	-Gnodesep=1.5 -Granksep=1.5 -o $1.tx.dot.png
open $1.tx.dot.png
