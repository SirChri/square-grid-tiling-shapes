% Square (1 way):
%   a)
%       S11  S12
%       S13  S14
% 
% Rectangle (2 ways):
%   a) 
%       R11  R12  R13
%   b)
%       R21
%       R22
%       R23
%
% L (4 ways):
%   a)
%       L11
%       L12  L13
%   b)
%       L22  L21
%       L23
%   c)
%       L33  L32
%            L31
%   d)
%            L43
%       L41  L42
% 
% 

dom(eee;xxx;l11;l12;l13;l21;l22;l23;l31;l32;l33;l41;l42;l43;r11;r12;r13;r21;r22;r23;s11;s12;s13;s14).
nat(1..n).

1 { val(X,Y,V) : dom(V) } 1 :- nat(X), nat(Y).

0 { val(1..n,1..n,l11);val(1..n,1..n,l21);val(1..n,1..n,l31);val(1..n,1..n,l41)} l.
0 { val(1..n,1..n,s11)} s.
0 { val(1..n,1..n,r11); val(1..n,1..n,r21)} r.

% if there's no enough pieces to cover all the free area, then give a lower bound of eee cells (to speed up the minimize part)
{ val(1..n, 1..n, eee) } >= (n*n - 3*l - 4*s - 3*r - f).

% there are exactly f xxx cells
f { val(1..n,1..n,xxx) } f.

%L rot1
:- val(X,n,l11).
:- val(n,Y,l11).
val(X+1,Y, l12) :- val(X,Y,l11), nat(X), nat(Y).
val(X+1, Y+1, l13) :- val(X,Y,l11), nat(X), nat(Y).

:- val(1,Y,l12).
:- val(X,n,l12).
val(X-1,Y, l11) :- val(X, Y, l12), nat(X), nat(Y).
val(X,Y+1, l13) :- val(X, Y, l12), nat(X), nat(Y).

:- val(X,1,l13).
:- val(1,Y,l13).
val(X-1,Y-1, l11) :- val(X, Y, l13), nat(X), nat(Y).
val(X,Y-1, l12) :- val(X, Y, l13), nat(X), nat(Y).


%L rot2
:- val(X,1,l21).
:- val(n,Y,l21).
val(X,Y-1, l22) :- val(X,Y,l21), nat(X), nat(Y).
val(X+1, Y-1, l23) :- val(X,Y,l21), nat(X), nat(Y).

:- val(X,n,l22).
:- val(n,Y,l22).
val(X, Y+1, l21) :- val(X,Y,l22), nat(X), nat(Y).
val(X+1, Y, l23) :- val(X,Y,l22), nat(X), nat(Y).

:- val(X,n,l23).
:- val(1,Y,l23).
val(X-1, Y+1, l21) :- val(X,Y,l23), nat(X), nat(Y).
val(X-1, Y, l22) :- val(X,Y,l23), nat(X), nat(Y).


%L rot3
:- val(X,1,l31).
:- val(1,Y,l31).
val(X-1,Y, l32) :- val(X,Y,l31), nat(X), nat(Y).
val(X-1, Y-1, l33) :- val(X,Y,l31), nat(X), nat(Y).

:- val(X,1,l32).
:- val(n,Y,l32).
val(X+1, Y, l31) :- val(X,Y,l32), nat(X), nat(Y).
val(X, Y-1, l33) :- val(X,Y,l32), nat(X), nat(Y).

:- val(X,n,l33).
:- val(n,Y,l33).
val(X+1, Y+1, l31) :- val(X,Y,l33), nat(X), nat(Y).
val(X, Y+1, l32) :- val(X,Y,l33), nat(X), nat(Y).


%L rot4
:- val(X,n,l41).
:- val(1,Y,l41).
val(X,Y+1, l42) :- val(X,Y,l41), nat(X), nat(Y).
val(X-1, Y+1, l43) :- val(X,Y,l41), nat(X), nat(Y).

:- val(X,1,l42).
:- val(1,Y,l42).
val(X, Y-1, l41) :- val(X,Y,l42), nat(X), nat(Y).
val(X-1, Y, l43) :- val(X,Y,l42), nat(X), nat(Y).

:- val(X,1,l43).
:- val(n,Y,l43).
val(X+1, Y-1, l41) :- val(X,Y,l43), nat(X), nat(Y).
val(X+1, Y, l42) :- val(X,Y,l43), nat(X), nat(Y).


%Q rot0
:- val(n,Y,s11).
:- val(X,n,s11).
val(X,Y+1, s12) :- val(X,Y,s11), nat(X), nat(Y).
val(X+1,Y, s13) :- val(X,Y,s11), nat(X), nat(Y).
val(X+1,Y+1, s14) :- val(X,Y,s11), nat(X), nat(Y).

:- val(n,Y,s12).
:- val(X,1,s12).
val(X,Y-1, s11) :- val(X,Y,s12), nat(X), nat(Y).
val(X+1,Y-1, s13) :- val(X,Y,s12), nat(X), nat(Y).
val(X+1,Y, s14) :- val(X,Y,s12), nat(X), nat(Y).

:- val(1,Y,s13).
:- val(X,n,s13).
val(X-1,Y, s11) :- val(X,Y,s13), nat(X), nat(Y).
val(X-1,Y+1, s12) :- val(X,Y,s13), nat(X), nat(Y).
val(X,Y+1, s14) :- val(X,Y,s13), nat(X), nat(Y).

:- val(1,Y,s14).
:- val(X,1,s14).
val(X-1,Y-1, s11) :- val(X,Y,s14), nat(X), nat(Y).
val(X-1,Y, s12) :- val(X,Y,s14), nat(X), nat(Y).
val(X,Y-1, s13) :- val(X,Y,s14), nat(X), nat(Y).


%R rot0
:- val(X,n-1,r11).
:- val(X,n,r11).
val(X,Y+1, r12) :- val(X,Y,r11), nat(X), nat(Y).
val(X,Y+2, r13) :- val(X,Y,r11), nat(X), nat(Y).

:- val(X,n,r12).
:- val(X,1,r12).
val(X,Y-1, r11) :- val(X,Y,r12), nat(X), nat(Y).
val(X,Y+1, r13) :- val(X,Y,r12), nat(X), nat(Y).

:- val(X,1,r13).
:- val(X,2,r13).
val(X,Y-2, r11) :- val(X,Y,r13), nat(X), nat(Y).
val(X,Y-1, r12) :- val(X,Y,r13), nat(X), nat(Y).


%R rot1
:- val(n,Y,r21).
:- val(n-1,Y,r21).
val(X+1,Y, r22) :- val(X,Y,r21), nat(X), nat(Y).
val(X+2,Y, r23) :- val(X,Y,r21), nat(X), nat(Y).

:- val(1,Y,r22).
:- val(n,Y,r22).
val(X-1,Y, r21) :- val(X,Y,r22), nat(X), nat(Y).
val(X+1,Y, r23) :- val(X,Y,r22), nat(X), nat(Y).

:- val(1,Y,r23).
:- val(2,Y,r23).
val(X-2,Y, r21) :- val(X,Y,r23), nat(X), nat(Y).
val(X-1,Y, r22) :- val(X,Y,r23), nat(X), nat(Y).

conta_empty(S) :- S = #count{ X,Y : nat(X), nat(Y), val(X, Y, eee)  }.

#minimize { S : conta_empty(S) }.

#show val/3.