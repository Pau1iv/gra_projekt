E=2 #END
X=1 #PLATFORM
L=3 #LAVA
#P=4 #MOVING_PLATFORM
M=6 #monster
S=5 #START
C=7#COIN
W=8 #WIN

level3=[
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[X,0,0,0,0,0,0,0,0,0,0,0,0,C,W],
[0,X,0,0,0,M,0,0,0,0,M,0,0,0,X],
[0,0,0,X,X,X,X,X,0,X,X,X,0,X,0],
[0,0,X,0,0,0,0,0,0,0,0,0,0,0,0],
[X,0,0,0,M,0,0,0,0,0,0,0,0,0,0],
[0,X,X,0,X,X,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,X,0,0,0,0,0,C,0],
[S,0,0,0,0,C,X,X,0,X,X,0,X,X,0],
[X,X,L,L,X,X,X,X,X,L,L,L,L,L,L]
]