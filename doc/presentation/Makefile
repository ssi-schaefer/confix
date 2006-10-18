all: mgp

mgp-base: eps-drawings
mgp: mgp-base
mgp-ps: mgp-base threads.ps
mgp-embed: mgp-base threads-emb.mgp

confix.ps: confix.mgp
	mgp2ps $< > $@

confix-emb.mgp: confix.mgp
	mgpembed $< > $@

gif-drawings:
	$(MAKE) -C drawings gif

eps-drawings:
	$(MAKE) -C drawings eps
