% nonperturbative_qcd_diagram.mp -- do not edit, generated automatically by dissertation.tex
input feynmp
require_RCS_revision "1.30";
beginchar(1, 150*1.0pt#, 100*1.0pt#, 0);
"feynmf: 1";
LaTeX_unitlength:=1.0pt;
subgraph (0, 0, w, h);
vinit;
pickup pencircle scaled thin;
vleft (__i1, __i2);
vright (__o1, __o2);
vconnect ("fermion", __i1, __v1, __v2, __o1);
vconnect ("phantom", __i2, __v3, __v4, __v5, __v6, __o2);
vconnect ("fermion, tension=0.6", __i2, __v3, __v4, __v5, __v6, __o2);
vconnect ("gluon,tension=0.5", __v1, __v4);
vconnect ("gluon,tension=0.5", __v2, __v5);
vfreeze;
vconnect ("gluon,left,tension=0.2", __v3, __v6);
vlabel ("$u$", __i1);
vlabel ("$u$", __o1);
vlabel ("$d$", __i2);
vlabel ("$d$", __o2);
vfreeze;
vdraw;
endsubgraph;
endchar;
% the end.
end.
endinput;
