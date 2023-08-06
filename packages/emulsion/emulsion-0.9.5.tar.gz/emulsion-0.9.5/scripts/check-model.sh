#!/bin/bash
textx $3 visualize $1.tx $2
#dot -Tpng -O $2.dot
unflatten -c 6 $2.dot |\
    dot -Tpng -Nfontname='Helvetica Neue LT'\
	-Efontname='Linux Libertine O'\
	-Gnodesep=1.5 -Granksep=1.5 -o $2.dot.png
open $2.dot.png
