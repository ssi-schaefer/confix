eps_objects = autoconf.eps automake.eps packdep.eps confix.eps provreq.eps namespace.eps
gif_objects = autoconf.gif automake.gif packdep.gif confix.gif provreq.gif namespace.gif

eps: $(eps_objects)
gif: $(gif_objects)

$(eps_objects): %.eps: %.fig
	fig2dev -L eps $< $@

$(gif_objects): %.gif: %.fig
	fig2dev -L gif $< $@
