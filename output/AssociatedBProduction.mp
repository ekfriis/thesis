% AssociatedBProduction.mp -- do not edit, generated automatically by dissertation.tex
input feynmp
require_RCS_revision "1.30";
beginchar(1, 250*1.0pt#, 200*1.0pt#, 0);
"feynmf: 1";
LaTeX_unitlength:=1.0pt;
subgraph (0, 0, w, h);
vinit;
pickup pencircle scaled thin;
vbottom (__P1, __P2);
vtop (__P1', __b1, __H', __b2, __P2');
vconnect ("fermion,tension=2,lab=$P_1$", __P1, __g1);
vconnect ("fermion,tension=2,lab=$P_2$", __P2, __g2);
vblob ((.16w), __g1, __g2);
vconnect ("gluon,lab.side=right", __g1, __v1);
vconnect ("gluon,lab.side=right", __v2, __g2);
vconnect ("fermion,tension=.6", __b1, __H, __v1, __v2, __b2);
vdot (__H, __v1, __v2);
vconnect ("dashes,lab=$H$,tension=0", __H, __H');
vconnect ("fermion", __g1, __P1');
vconnect ("fermion", __g2, __P2');
vvertex ("lab=$g(x_1,,Q^2)$,lab.dist=.1w", __g1);
vvertex ("lab=$g(x_2,,Q^2)$,lab.dist=.1w", __g2);
vlabel ("$\overline b$", __b1);
vlabel ("$b$", __b2);
vfreeze;
idraw ("plain", vpath(__P1,__g1) shifted (thick*(2,0)));
idraw ("plain", vpath(__P1,__g1) shifted (thick*(-2,1)));
idraw ("plain", vpath(__P2,__g2) shifted (thick*(2,1)));
idraw ("plain", vpath(__P2,__g2) shifted (thick*(-2,0)));
idraw ("plain", vpath(__g1,__P1') shifted (thick*(-2,-1)));
idraw ("plain", vpath(__g1,__P1') shifted (thick*(2,0)));
idraw ("plain", vpath(__g2,__P2') shifted (thick*(-2,0)));
idraw ("plain", vpath(__g2,__P2') shifted (thick*(2,-1)));
vfreeze;
vdraw;
endsubgraph;
endchar;
% the end.
end.
endinput;
