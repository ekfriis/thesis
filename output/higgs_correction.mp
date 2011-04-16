% higgs_correction.mp -- do not edit, generated automatically by dissertation.tex
input feynmp
require_RCS_revision "1.30";
beginchar(1, 150*1.0pt#, 100*1.0pt#, 0);
"feynmf: 1";
LaTeX_unitlength:=1.0pt;
subgraph (0, 0, w, h);
vinit;
pickup pencircle scaled thin;
vleft (__i);
vright (__o);
vconnect ("dashes", __i, __v1);
vconnect ("dashes", __v2, __o);
vconnect ("fermion,left,tension=0.2,tag=1,lab=$f$", __v1, __v2);
vconnect ("fermion,left,tension=0.2,tag=2", __v2, __v1);
vdot (__v1, __v2);
vlabel ("$H$", __i);
vlabel ("$H$", __o);
vfreeze;
vfreeze;
vdraw;
endsubgraph;
endchar;
% the end.
end.
endinput;
