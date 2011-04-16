% Higgstrahlung.mp -- do not edit, generated automatically by dissertation.tex
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
vconnect ("fermion", __i1, __v1);
vconnect ("fermion", __v1, __i2);
vconnect ("boson,label=$Z^*$", __v1, __v2);
vconnect ("boson", __v2, __o2);
vconnect ("dashes", __v2, __o1);
vlabel ("$u$", __i1);
vlabel ("$d$", __i2);
vlabel ("$H$", __o1);
vlabel ("$Z$", __o2);
vfreeze;
vdraw;
endsubgraph;
endchar;
% the end.
end.
endinput;
