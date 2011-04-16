% higgs_scalar_correction.mp -- do not edit, generated automatically by dissertation.tex
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
vconnect ("dashes", __i, __v1, __v1, __o);
vdot (__v1);
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
