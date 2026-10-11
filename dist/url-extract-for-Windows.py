from __future__ import annotations

"""URL-Extract 最终单文件版：自动识别视频或漫画链接并下载到 Downloads。"""

import argparse
import base64
import hashlib
import importlib.util
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
import uuid
import zlib
from pathlib import Path
from typing import Optional, Sequence


CORE_SPECS = {
    'video': {
        "filename": 'video_core.py',
        "sha256": '2bf255a12d0e413f2f499359dbfb24fe055365a576be88d7f1352be54cc6731b',
        "payload": (
            'c-'
            'rl~`+pl(wK)2_|B7MG_mY`Zk{?Oj)Ku+t5~uZPV*A)mN{?gaD_bL5M3#g`a%@uHPYaZ$P@3>)p|k}Gl=cFBaDcwj$NzGPoa86|g}'
            'c_;?>&1)a*_h~+|zT2M>G4m_S$Q&y`H}BFSI({%334#w(Hfn<(*qR<HbAOPG!B@>Uha!+-'
            'P_~(ycVBl}^=b)Ym$d&aSuCYIPGR)b<*c-MAB$eBU1#sdZXgUKG`O-Cie-BCo#HhQ_^0v)Sray7g8w85t4pIveduCyB-H^;V-'
            '1ud_1pRkI5tfiA_H%}TPV{bYaOMQJPUR;rb5CH<w>tvBS`cBNYF#EI<T>q)CAp0_I9P4V24CEATjx7O-'
            'xiQgSL;AB&8I%%z6jJxtzZ>`;Ft!q6cyYjIcZ?$XnhHR+2*@-LFdUHd*sBg)Sy-ovX(TTs&i<7SPHtuv<9r><TuZrhy)>#j<9stJ'
            'mUZ)c`yCt?TiCC9q>Up8nYRv4!>pfU+R%5ff)evQR%{W=Fv}5(9MC;ZO1s+{KduD;&up(`MBMeS_UO=$Yhwg40CMn*}cH<6WUBNq'
            'BY2$~2w}g{yuJf+=9H}!=iGD=iNDBBBingjTJ$}7aZ_-23Zq&OYBO}q$xrK%K#pRh((WCQA%S&F_yFB8-'
            'fBsq>T800W)>~VC!SgR&x>T~?txX&$b+_@U+Uo7rn|fLO4QsI;CuXtT7Jzvz*2`c`<25f;T8r^{NAE%Y=w7OK0ZMi|#%s?9z%(~|'
            'YkCXTtF3yHRJQGA^tZCir9`x0yf`+#zA<h$pugM$ke{77H9H;s$GPb<v&*wH1ag0~zOe~-'
            'i)~cu5n>yzxevw9&z_o@j}~YC<J|1x%-NYaeT{azQMJ+br|_u=Pv!E&*u-'
            'S%cxn6rF#uL1ioc$yVnz5>E{{REF;VPfXSdyLRa;vz7HjXW%ilZY@{tm(vn;yV?Y4KY6g^-'
            '&6VRdf3UpxiQU_+!rH16Ma(TQoIYF)LjYNy*=9XvA&O{6IvvbQci_zTl*%_FYPn5L?6t%t`m%2M$AeE<PPEVgZvmBj1eRg5yk?22'
            'X7b2v*WiL>}Nv1|eH|kx!l%prQYjdNgPj9v3jpB)3y-'
            '`g@J8>hfByloYZCz?MT9xXk&#G5oH?LutB7&|s_5l9>_|f9AaZ#dHqlTI=$<hS8FK*nwRvDXopmwx2Uc6LqP9808v>QeI4CKTg30'
            '*^8dUSf?*d$KzXnYhZKTxY2pFDbeeEi7xM0Ij~{P+XM;>ywE_a9k{E4AZC?>`ogj~_pNZ1PAgj*s16tE?ZN96NUG=;YYAFPlF#Gd'
            'DjJJgRZC)qrz}9vq<9o+v#~niTWJLdBiqlMzg;y^b@4f=O{J*<QCNC`X{CH-0QWc4Ta9ZEUS_Wc|qG1IH@&Pfm<i9~c{-'
            '9IM=abTVFlAijTmY+~a0dK^z4d7x6OJWxG$e5^JZA6c)C!}OxF(_f92=jYEv(~Bn`ojpGjop@rIw#mfAn0MHN%18O1k!W`AJZz&='
            '(c`mor{*7DicZg-nc>LPAqvt4@*Z>!tvvY9ls|gm!jlglzOXYkR=lt?URymBj>w9OGfOjz=Yb4jZEcI4oS(x@xv)rorq6v9|ID2`'
            '!}0xaP=g|8FE@KzYjJ1K_uvfl*blGX^g5O1MjVV6V6<VVYMfbE9<m1Pl@qgPX7PW~>?vzj{%COG{K{DIf$8FZR*K(Ty)O(No?01w'
            '_}^Ba{9mCDlRGtk?upqsS4G-'
            'rqXAY<SNm$Tv^>3hZpqo>!&CLq@L}L{y1fK`#7X#YRy${BmzJi_J6l=#+9;GCefWQ2xs#6^8+Vnebk;Y45G1mFUjETDOMvsU(e(2'
            '2;_QiY%hqZWm^+7{L>UI;2M;ei_>Eqx8&@A%`I--{_)p?1AWiiqyeYt&@K6C8n0;h!esSjH^wP|T?B$HBZMn%-'
            'zIGwG;2(PMq1F2yzEIja(mM`4UU*o&J{&&mJKBC?`P7*Oz`0XE(@!o(XXZ~n2K`6|r*sCmqyWk-OrLxVaPs8z8TU9Y>|F>hB!>^t'
            'getqZn;*gvTqr%c^0h;&;o<NQd@jKMu*4c{`-'
            'eCv@wG2nNe;8Oyeu`B>~5{K8cC|T60r^!f<qUcJai%C+W<y(YJM3;Sr}2HUY>t!X3k#J3u`*UURd*0`BSrx%+l%RkBv_pIeKjJ{^'
            'Ji+*4C?WZDX_k^^1+IW~=>;PSWjdU)tII=Jbh^K!zT9boSpLJ9Bn!e&IhBmzK|+fBdUY{3no*g>xs)%$|(S!Jdw$AAv(t(Z{o`Z`'
            'K=)%ILAum=`?Gh?@rm#>YxyU-2GCdj1t}XYy$1ae6r2Za3n`<F&`?-O*!5?k^pg^n%BbnJWO3e=+tRiPtZ-'
            'Lhs}zFk|uP_)%yF|4&q30t(lui<&dl4OIk5>Bz`>qmm@vIp7PIx|NN126@$BvDZZImVSg&tR>%{_G<N=xa#$wa51UWVlTle-'
            'WD*>@b@cTGu{R=g7*PH?gSve1$gfPfoZhXD-Ev-'
            '+<(21usaCvI9h^*X?CCJ0%LHdwXqR*WOt9naT~5UZMbegr|Pa#gGPuwZg=Y273kp7X592D9*wA0X*AX<>leLC0A{b#YqH+3Nmxnv'
            '-&$`YNa9AVAcj2!v*?6g@gZ-n)r?v145@$#Z_-Ou|5ByXgdK7hEzo7)4(fAwosFyY$|AdFu#!=fG~kj4*Em2jADC-AA~s<s#~oq{'
            'F9MPQn#%!1QN3C3Mo}R9VS|C1G?0SFD^CfQe}&${KdS`~Tccu<Ut);n7(O;zf>xm<{A<4EUBIVmeZ3p-'
            'pP^X@`+^eqN6vpSPFjuaxOyJDb^t)O;CJiY2663lKW%oSdKG^qtzKt6jyRmQ5S;WHu&Wzy>~e}iEvOq=RO?hWw%{S*-v`4}{-'
            'SX($jWzWNY)26I_m=sbjs`YfEujmNKo)frP8X_0-s2_$JAV=;Kc6&(2f^!myjla=L7yVKdE`ZclE<8q~-'
            '*L)DN=|%@4lQU#mW!5!U99sZpfn#>SI+t>_LR5MWc>*(Q;PYcs*suic|t(N?8%G443G5!*ei=oH<fVPjKq_A3jltOoSM9xQNB0|*'
            'a#P{Us6tu^ZF3qUp4Wj;{%dQPZQgL4g_*M_QLNtOdx0qO2W>zfsTSS=|pcY1MXFHsjT5cjJh2*|1KnZ;1P6G3~m`UYTFqn=Q4EV;'
            '7kK&%La1>FG!x9drLZMdQ^p-3R?=}IH95H{MZSK)>cRpWMd6N-$f1>J-z3iJU-TBi%g8edm<;#9HH?RG@xY#RzFcux{|S63a7uGg'
            '@M(mL=ywN|4Vgve!I_LKEaz1?MmXP1$wW=p+9*%L^#;0CT*%9z7_Wp7-'
            'T!7<j?dfix3RvLAfGn{f6sbII_n>}5OalfhdN*i%E@IhJzh|}HmLp;^(ugwbF-'
            '$SFB?MkB;I~wA&!YU1;!+v2QSVeP41|qINL2Vj{3RDHDMZF!UcH@S7&g^(_fmg#I+yy%9*mS1S^FgF9GNkuIN2B_tD8Z>3H>&|P7'
            'N!soKBdv`3&1P_a~h!rB3w~NxVwNY+nx685m0>Y_?R<!kX5^ehqJ<(0udaeFvy8m4ZV)BU#x)-'
            '(Y{94+^vs{5RqnL(l$|a_yHGhl-sH)r-(i4i_3M(j>90-'
            '3Y0*0Q>7Ne5sjN<AH@(*U|k0t0Np6@R1S#sXsvx6xbA{?7?{BZ5Is;MG{ln8&|rvcFnl2ZqD@pjtjE{@QAG_hok|^q!}_Hn@cYmF'
            'vH!_a{onuS#-~5-'
            'zxrPPwWs!f`m6mHul(()Z*i*7?d+;12%3zOq#Gc1qm~JeYX)zWKhx`YXC3gtJCB=;y7VduW4`ZVTpo$MnLMA*J}`$^O4c{ytytd?'
            'Un+C4m@kW>%%#=kH8xvG7fGl7m3_gB7JdQnQhB-wq)N4cF}TzMrH@@oTLFI4K&Bl83*N22erNyVYyHokx&8X}8=roD^CxeCeqecF'
            '2`7n@f<*_y39xa1!(A&6ro3~<s=`8odZ7_<eGd#z>V8V~ws;+wa0=b)o7buY3Czv@szHr5H~z57l<G;e(P*tz8VALl8z27Q*0(?1'
            'fBxD2wIA-k`p5lOKi<Fc(#<!Y-hcJEo1gyh=Ji(<y7T>soUz=Tbk`9S0_Puyn}J0W0qH=og<QCMOS3Mp1$__kTA>6jB9-'
            'r_*NMY{*ow;lo2`|jt1DxxBs|2Qc=RyU8XkvOy56j{0&KS69X)!afLf)v%!@36ya{A{i!;+_!##a5=a=qar^-'
            'G0=NJ3$JlB8bty^#YX8#x0vi2)3ubK{a*4zz<gt;(}{|yxe(3~aiG*w&S@S{y*#owNKnqdVz-'
            '1z*pn=if$cyjy4pWXW4T_^yxbZp`1K?;zFs~iJ$eLsBoB8VxF`DSFCP=!5mn$5MeSYJmydO`dQ(Qwg@>~O2n?7^nMViA_2x>~>ak'
            '^_WA3$I9U=`4tIs<LGlW&>U2JT>3DAlJi5Ft%G9PS`BRes;|pfc>~|9k^b0pf;T6)p$oqyeGBQbM8CdMW_j92<}m<P0DcnVkD*@r'
            '1(;xAfz%=rqrWgmV#rW(Yh3gp<;15c&%a_p751F+21=o7+&1mPS@Yl`5Ox)z`u<V9b~JclSh-'
            ')u>i2*vkLyIxO%YPI>eGT6vQ>PaF+uYQO;^ryMmI)A5Vy8H$Wl-'
            '9C#p_ByJbKN2qHCK6lLG;aFv4kdKUkcH_v{1padb|G6LkIc{CFP+*Azfc_kPDe2nfy^vi1M1}N?hRzfIHGQGUCKb2d{b2u3-'
            '@5(m5Bl%?9O%T&Pd@Iy_rsg7ytDtSXBibyM~4*h4A=*#e^<a3g9@!i;A&QHYWE&7@e++Sf^8IW{Yz+zDiw@)FCzz<<NhCC-'
            '+%GFTkk(}>+@$BEx+;M_in#@O(%OO<&8-2$QbfKldnnXuR0<nqY7f+lT63~qGGnQnMBL$wuJCl$m7u{gO0-'
            'l&NdPt6JS7b*<@#Imfo)f7A1in`32T=C|LedhduaSi7y#P4Bn=~ivx8crkm4`YL7pyOpPBOTQv&Osjta$VQjoG)3yYD2|61O;lwZ'
            'X+9Wx`t(2j>bj_vaN0<4pJzqa^_)EUFO%U=&m2Hskqxk_}Wi(V_M-'
            '3B{MT}gvfIs2VwoD9Qrv?^MII!7jCCKP`XBUo=5e#Swx|`6n*8=1KYk@9Wzrgo+2P8fCjMyNN05JjukxnesR)hf`=xDu)DvEMy@Z'
            'Kmu<uW$6SK4YH<tWx_??zl33kqj?cWD#)S51{@T#0`19I_iPxU97ggiCg7cP(W~VwFS(8fOY}(|fi;8NygpIdxlGb<iC(c0JxF?A'
            '2bg4u=Ft4RC!JnZ~nyy@kT53auG8>xz>*TsUJL#<g`oiI6Twt$|7mZ&h?{GO9s6c899@HsrO7peY1)uG?kS%bvMjQbNpXmJo|0Bw'
            'C>0FJ0y@@%J9;V2WIQR^(9B4i1CSr-?#Ky!jG9v>Et2peIG9yrWhq!d>Aw&a4t8+)y#tC3b=qiOSk_xDtmYW)v3qm1MnM_q7v<-'
            'vmxW-5El3>u#5cs+q?ZtP6)mdgmxWmU_)by?HS}dn!PnsCCg2fgikMzIjr}9kAgDEkUR@6<Nk`?9?C`XwOsW_N=R*R=6}^ZbA-'
            ')r(v?mJLcpt66BC;`$^SX<r~`W$T6xy9zhs!DaH)KU~v45h@`q$m1JUp&A?j&;W1GR5GRrqZ1W<TKLCo8Nn?%C^)5<P8Xirq<6Q#'
            's(cO$a+$-'
            'v=mz<O~%S<wm+CqTq1aSs5$qjLxPiXPcjK&&8Oa^M$jgf;wsryTcUrbSSd+j(Gw`pbi{yt^1zyJ<nr%)0GLjNJTV346a_k;bHp1p'
            'DX{hNQje)IY-;o7|alXv%@f12@zH-'
            'G*eyh#7<yEk8Xseko{{SUvL=7>`(!&j$6{M}INbAUA(cAf5It?tQs@eRL=))o<*ksBzwfD3MmP!(8u_hsCoFjzDuZ7fz{_aFAGm|'
            'I?^jJCPV&JP;ZRvu33bv6||8}ybU{s}G_9nPEjVM?t7UGQ=yXu&3=*$q;VtNBl~ddpze>)rV9`?o&*^w#IE^gsUH-'
            '#_{JW!}o3Ur1E~!F}1k&~bdhqpb|K;xH_@2zDF=8ogwbsI2*o%Pt!RgleFK1q1%74j!6@HR%33&+lKk_V-Vo-'
            '+%iz{a4@WU%S%(=>6Nj{PV3hzkB=FKSbm&q(-'
            'KVL@s|54CO10`Zwc<wC&M1K&n&k?gqv$#}x_&Z4_aWe>mYRlj3|q7#r=azr1z(*{ipo`N7Rk-'
            '?0V%e76~WiLrx%1!Wa$yVlrEejD&u7_M_&Eef4T@+5G2wcw@aJCc%>!GW+uU3%O`+FPrW5ki64HC@tP!P!G6i70uo38?RpG^t0&u'
            '{d1>{K`YF1p^D{3(3v`HPC^Ys&SvBGQ$WWZ@>Q6+pqn4|G!=bnPdOzy9~jAqB7z2{$HO~%K=Tx0i!B|+lr^`l(s560rg)%EpE9{*'
            ';=bsNIX2{1tc^cU-cgH#tI()!5_v}!*FGS>G7eB`c`i%YJ;I!BO&{Toq(4zq|MZk9G_L~L6BkH{qWSN5;!X&wT@_ZK;uXa2*)BuT'
            'P|C}Vr>ypL>yxhXH#}}qER-!RWWI^rSyD3)?*fNOk7M=%#_!)MgY^n0&EMCxjH{WxRg%6{OKGXvt7p%Nq>tL-'
            't4z6<Rt@T_9wkJJq`CbcbF2n%00Wt=1~F6t;b!DIUeAx5a}ZU8#gK!HiC#kAb7h4a-'
            'rS3+^E)u(LE~EDxtShrOWAAt7F)%F%K9R8J+Hj@59GRuUc=dRMt8Vl_!s`j=H|mOLapGQ+=V-9}v!ml|@^C`_?-'
            'CDnF2tIB#hF5Z&3G$i|11ko&9wkXBp$7wjU`hgJ@Lxyzueavfbt%!Alv*cS;l1;y>hwX$1rXCsa{ZzYH5<6T@U1>d`1Sm6_<a!xG'
            'N2gP=RloGRYYJccu!Oj@`R*=f4M^5ORe%*v?8?#JJTptCem;Pq(fcSmI#T;tpg+4RtjnJeT_H2{X6AAEbd<J`B2jDJuD-Wc?;Oj}'
            '$VMi0w8eAsl4`}bQj|?pb621%f_H^>ZTi^sqh`I?WIYSH;V^BT>+$!Brg{jdHp}_Y@8Gy|~D-'
            'Dn?HAuDBMFA7o%>b5z{R0py=68vz5$eg~eP|LU`c0+?)T`i(={0OP5PT3VSGE$oV1c$q$izjQ$z|0d)SD*8K4Bk(8C5l2r!u~=+j'
            '${6Oj!3i<E#yUedYa|3y2GMnTv(dFAV4G?|~u|#Lu|k`Tz&%K8bM!?t<OsIM;FQ`Td{1-'
            '+%s@{<S|ap0NL;=YgB$tZZnlE}gFtY`Xz#Is`U^8I~(@HTWGU9EOp-'
            '{rl%{z5Ddd>p$NA#j7?W%PrwaOlRN(rz2Sdk@eJ2=pKYbM=;&EHDo!xRT2W?ih)>7GeZ%g{DOb5#llPX&)y|zdH<b{`Y*qgVW7i1'
            'ul71ZaaM!*cI`2W@0yN|-<X4Cz$6+&L9^-z^LiL#`~-g?j5DcU%{J8B57~P&WnJdjC;D<^ZA7s`m-'
            '(J42<6J&RKCD4C9FsRQ}0qjk_KY|CncI02wkhcF&h}@cMY2#@2VgYl>K1evYN?v4@5AwfzZ%_c0Evo+b@1@?;&G_r8%83P3H)0fH'
            ';6e<E3jH2)Sh+q4%ISG2|BEw<YJm*|kJ(w@5s>_TnKbF<yc@hds2z-'
            'dJgT*qv&TPc|OdxHmq0>ejP=Ng0ix@kWF`^_B&P&VOfHa=4iG16y)rnxmu%i_$5hm7m)PMf^v0D}3l>-'
            'Nph}8FcjpKGHJ#BaKqZN5%>czS+`hmk4GC(VC$@xM0KCEHOK!Tkl@)Uww(Iz-jGneE$0W)9<Eimh45tI12|dyD@>U%hY9&11<t=F'
            '91Jt=D6F%I2iPC@>>7*b{UvFBx?b-7+jgjw!wI~Fh0vNmTC{nU8J!iLrg}k+Tt-DDS>l7Y+Zm^@6_W&S@)*z*n~}VYMC~_BL|)<@'
            '2o&aa(Is=QbH28g1zk00neV`)a4ypd@g-fpkMu>WoCCKI9P+r#ie?cJX5%sh6X-'
            '`tu&kQMg=1iL?{}j_lyycwS*oO^;~pA!Mn;}Nd)XkC`1x{7eJ+8OZLM$hvTd4O&*QL#>Q54W<fMJ<<fHD0VoPEag=N|93Zf>3JUF'
            'Nu0R<7Gl^1KHIN5d1FZUghjXiK#uR}f4AY7M8;CBg1EQ)!YoOon%+*oEQ`O^eknW0%K2#wx4_Sk8yvo$}NTI)gbK0QHK*1zF2OgE'
            'gWm)gZ)iPAqIc8faDHJ!dthDQngDqbQ$f%OTBb4s-^j6t=o!}jMr>2)41va3LBEU|ox3TF}TkAcP0f8Kl7X}`)4YqP!b-'
            '4%TY#q0y9uJ|E#26zWFnkh9D7w%%K&%F05NTd+l{PJ}L)(*vhq%#<Q^`?Rm{2OFz&LC#`{>VIoZdheD<B>zfAqajvm?3tiRBZ|6W'
            '+}~ybQL?`!Bq~Xea*vi&ubfdMD0%{i`1+vbnZRbe$S6ZNTcZgK<vs>+vPVaj=tE0mQ-'
            '4DuY`dC;_m`h#oY$GkPgrE5ZuL9f)ock7Dzdo{w{imwg-'
            '*KoS4!*?fwG2R5Ltf<AeDj12)7{bXSpZ{XYEZ~@*#fraE!+T>Md_(jks;aEk!M)Z~WVR2amK~{Z(-<k3Ut~VwHAa_-vS3(ObUg{z'
            'XB+~%T@PKn>X00hESg7+_O|<?Z3qrA$b|fesOyn}H58JFLKfR~O(x&KX^oJbBjf!g5EylID18%}oYUptJAG8<UXqP${bUaL-'
            '8nm8MxXO-i-'
            '#~%$_{9B=PqikTAn^6**wN#z&)}|o5i6VDviAXk=+5^6cb&=J2g#<suJS?k$~T1gk;v1V$pZy<$hD|gfE8t;8p7<ARa;D(D#qDbC'
            'a~4SOhmFG=CaiU2l8sGv9^l>pjxA{t_$9%AnixqvZ@(oh-#^X>-'
            'NCzL7?J8V|6TK4Ar*9(V1ebl;Y4OTc`u9gjQ1^c%dq0n`F$8Zq+@`bi-VtqcyBzL)__(;wJ`*>&uyUBDJVYIu}~(hK4pdtr(NBTH'
            'seH&5)2YQwGZtn2{pN2Bmd{j3}EFKt)t2D;Sw^Bg!VF)5AvuiX|j4gp!MpVoQrh&8SUNHEN5!;^Iz4AcwM_#7ObLA=%<oRqVEiP^'
            '-~^zuR1Y7I3|h7GZ%&HDqXjf)%KMUsS;zrrv2ax0vY>7=rN^B{c1n?z8I`!7L0BkarV_SIW3bjDT0^#M|{2xu<A7Fzi}*V)@bexr'
            'OQFNBL&dO04K#SGh5i=q&W^^U!J*`7VGG{F2=up%u@}Pt)1<ndv7UUz~m9(dFpGA{gq=EG|VxPkatwYpjLJE3S3G2Ljz&44g$!1_'
            '<o{t&3s`M2Qzkxa4?#k%c%^!S~=7Up0!rg29REy)7S>MH``Ef4Uy=ej^@FR2moLsrvcgG%a#v9YsNgI@j`k^3igx4qFDCW-'
            'l^#EPo9&vln%RF1p@El}r+&m89546u0o3o5hoJzR-'
            'j6$u%my=K7{J$3TH9(@RePO>;p~wRE7eW#avy!yc*Mi^Xa^!38R=p($#y7FQ^!Xn7h!4sOvd0)Lop2jjU`xu)I{`7xVE-'
            'c5;h06wD-CN^%A{jDUfZlIzGcRZ?0nYkNAj7`egXx#ErtsjnrYPYFPM)($yC3zHS*Kpv<K=fEGSo?W6qG2=xM59YCDk>Ii3CabQr'
            'iOKAzO1w<d@fV=J8b<Bi5;)W^c_ydvfu00ipMQxlEjWl8Px1Bm-'
            'X2CN)Eeahc_U_|8;!;0F^Z$x#X<mxWEBXVylk4o5i^)?#+r7=I{UY>a91gfM&4&?05UWeYXGGKi&Gv8>Rv$rP<0ruAxwANV)GY1H'
            'Sfd|9fv~19pghZ81+;1Y8$3s3sr8rM)Od4O6>nEW1KLR*IzW1A74(3k9WZX`?ndqA<Hby2i<NKtl$q$~uT7gK$uDa<D>rMDcUEpb'
            'dBf*iJ&y#@-'
            'EzA;xL<h!8Px^~989pfUUlan3tMYO%<IcI^~dXjbtHrAWy2;0tXQBH9e^oX%fpF^i*i!^audLzlH1w#dK+b#__w2?}|vWF`_KVTl'
            'Tb=}8JeN)@qsPE8A`I<@1R6)z%Zk)W^Mz?tZ!M)W8fEBHWTrH6Xcb4?2w6Jb^`>eHnOi%a1;s#U2)5*1Gfui|d9QXF43OcOBXQi6'
            '^rn%I^>hcCR0)m9{~vdC#m8iRTJra2>zpr_+7^oU{ru>y$-'
            'y#hKykjaVAY_`S>gRM=C7!Fu=Tukb?c4)=FaA+06S5_`TJP>H^NqU&AhV%jATux!&OMJczEwJd_0q;88qYsDlyEWTxq`+|mz{0iS'
            'GP$O3X#!PQ6<u6d5Eun27E>4Z3A|rn!Zun0z!l>cu$&WPW2S_kd^GFKnGVLyC50x64Ka5JdCG>t`^P&VX~>Pyth$dYHHJ*@bU8=f'
            '%T!J`FiqK_c(-bpQwdrZNf5)-C3rI?-'
            '|N($6uX)|%+lW{1=1OqaLC=t!h^I^A6j8COCfk^Df+*PtCx=y_E_~p1;@O#V}8mRkIS487q$BIH7zn=mAF-lhKH$}z4~UwxYG6_?'
            'WI7K)ZE`7{y@hFhm>ueAeb*67E#w#vI1ZZxdj3hQQ2vPka4Fl&6+4yzGN#)$!?RB6`o8O0Ke6Do!6bE5(kfH!qtp|Nnvs@2)2{vP'
            '^7n}HHv_|HMKj2?3Ld?kXIgbG0EZH_zewO;nhmb_>#D{1&0q0ywRB`hReUv1Bbl`&=5>_=-'
            '&+UzJbnNnGrmwRgs~gWQ32hxJrFd+#RsCDr+qy748y*?IZ4r!tyH$LKj?13=IC^!=s1c;L|`8TB2f#=p<_48ql^0UH6nKKQ>ZG&k'
            'vE*inP|q!%W7#7-'
            'B(0Py>B)qC_<_TnAYJN_#mtYYK4SOzuq`2&BAGZj<8Zi^qEP(<`M!jf0|mWX)A$C#B>oTl8s(H}_Hnq_IFX(#kp8L3s?aff^$<#Y'
            'r`1G7J1Cz*ca?c*G?RlueJM3#nilh9RJvi5_y+LVQW#cDVQ{Jy|0-'
            'WRc2pOIBy2G{%UNBBO^=2N}USUHg$Y75**uf54({fZsfCVwgd(8hN9_n22&<?(0?-u<`z-'
            '>bjdJdAm05gZH3ScKDcbFrqCh2Z^)ML2x2lSof~On}b}OulS*M3(=4{Z92id?8?NgxknXb0w8sf&zJyisW7t@>yFBYq+e0BSK=|d'
            'xq9tj<3j&0XJZaK68vv0{n|;%BxqA2A7xIGb<fr5uW{AAll9AAL+3hDj~EUXBhrPrb&b{27pg<IZuSRUto;0D$iK^Z6L<ZGx84DR'
            '&Ro`<rOjAg_Y#X62l9P6LY%y#wcyzCLm-'
            '#nKE#E<+0W(78PeH3Wey~}uui*BWvKnksU@W_QwmOGjgwPHAkUO^2hJ|b2>RMCcwl0%HvHu-'
            'z2|_ZeHSw?KB)@G|CNxe3W)gy!N{eqb?S<geT~lKrd8$8J&27~x8+`KRke`u9YT^L3l2&KNCCxH5tTWhsBl*ihQvpYfvlo%5VXVq'
            'RGlErSF`aG-sg|U>^r=Z^`Z_itXd6jWOOPzCkdu#XchL5H{I!gxdUDV17W(x=<X8tn4E4jf<ts19RgE`1QLS;+gR~(7HgJtxf&V6'
            'XqUKe<Wgtdd-6&6ov?>PhrW`*Lv^_?%%hcLn(NDJcolb-'
            'N6W>m9iM6k_in3(gJOVOVvamzIH?W^a2@i#{N>E;XVnbIG=y4ThJZ*Hff+6_eh7)Md%%0JiYWF8=-'
            'M3)KlmIV?By&4uyde)sft$SDBw^4N#5eMi*+{kQ>@4dASx$YfSb5JV`26bSi=lwWs|@;o@UN6+a={E^W`sl>L<3C4c+Y$niKCXQ6'
            'vix@s58b=i(-MhxP-'
            '8Y+Ua9ILdtwfd+PM>QD$1$>_{g2~D;Rg{(;v_y7+bjA0mNtV8Jg_ll^Po0(S+##3ZL3*{1tycbkA#`{{O8{gag4@Oe|v;F`7z5P>'
            'W64uCR@v~SM+T&BkX3r`r$i|dLLbA$kazIUa`CB)GSIXMXB$f}Dg5n{MiS%;_N5<f&9?h5N8d4aWW>OKIZ00p((Np$PKmdsz<lqB'
            'a8Q&l7zNQ=A>V#yV6owa;yWObGePZdGpDEjL^v&_diu&)meM!FsDU}>_)6%>N$dLf=sAj+UO-PrD6(3@Fn>EQ0%E<9Cpaobl=2%W'
            'OQR@&4teT?s+((2j{(!q?8U-lpFF!CiFPh?CMS=)-h6yV~8aEpc9OoJ3k-&5-'
            'JjgNV6{k?8q6N@&jGw8E&8n@9shr}z=a(orF|Vg(&<JxpVQ@x~bYPI_CR6SU1S`vjK~CRN1Un&-'
            't2HiY<B(1Z&TVT7#+f=?&cK!9LCO47U<fxTGATU2K?@K#Y`l5479K4w{T=5BpJ}S;ui~Pakc}?e)UHk}$YFohE6c?E&TM^Lex5h3'
            'zo2W@nA@icnwH8Ez#_agG3u<@h0u1bHz0;^U~4Wpj_AA1$kvc=!kDT56t1)*w&58w?KKU|)ZMylI83O_*Q1u9t!RypUfAGK<M-'
            '4f>m=(4JhFtfneetcMO`zWEFcCDceGxsqcawdK?6cFj6WfLu^6O8wu>Ctr`<>#Zfv48?TiUcm#=KXBAeDJiy)|G!#ed#IfkYEX$H'
            'CA4DfIM9>!D{*3U+6;nbkj=FV~zk|olfzFMo?NTpM`BuFTuv=)eL8o}YI*SKt2MHyBaQrl(ra}et<X1i;ZG@AnpJ)CKQSuzwb_)*'
            '9`K`0K=i1hD3ovYgP>d8(aCt?$>uC8hc^?FT5BRN&gU|P&{AL2Rbv6~p{qF(NC<8`^srgAzkZH*)&Czm-de2V3MJvCgy0j|-'
            'tIl!ELOo4Tp9UUBUMVhx|5erS(F*3B>K&szVIxA&XC(H0`Jy!Okw4>;V9+i}e$YfY(peG{zgBBE?g|!~V^Eb`#Y`9{NXfVYL^L&1'
            'WY`3a-jQE2f>(C==3u#E|Q?ZI<BRm7F<*28nD$s^3X0KZlnl^+c$Ao)cABItn`4sxLrxSWwuuXJ;-'
            'VKYzVS4AjTcgq}bktTgbDxh4>o{0DO4DnPF&Loi6&Za;jX?AIh_w|=U#3Dl&YZU?tE#$1xvMztkQ$B3)g)zK$K(bp46h>AJ=ujWH'
            '@vg@x)La>jc~x_Kefj+wVu|M)Mw>UN>RvUF~nOJP0Z6CD&QKnG9oaOv(+@k(9&20BSWm+ovhcLtWjvXZDLxK7@{lJD!oQm10?1G('
            'mvo8ETA)~Kv+3H)t)@#SFrSIMoGahM^sqY|Ee>LPHQ{NF`n54#<shTbN5?zzT0NSI;v2FLpb&YB)CD5m6lX8Y`F6!`fxih^?7Pw='
            '7!;d5GI2Tqm(abX0#9@B7q&FI5gw)vQAg{xK?e?Q8!sOLuY4)W6?vhM8f^l5hPd)Ldc`^D8cE#EV?ginn>zlSy-Prv4UNa4YRUae'
            'u42^>`@;uRP@AZm?Z=;L)hxm#ePTJ!uq=zNX9tuaKoEyq|9B&s|HbpH>P5U@)uf`v-MUdP5<mRO_C;?zE3rZIXvxw&?1bv>Q1P-'
            '6RR$|XHg(Qrve&oL8B1V9`}1z(THpUrbjc0%u0N{tQuL^C=7ncCXVjNCg}kYP9SM)iTS)3ksj|YVNm4!pGq3EVf=rJIHbq@Pa_Za'
            'VknN0+@sJ2!p_><Br<z#F#JwP2R+rL0fXhMDLE65@N@Orjn7`e_>?dHB^{sA^bI{A{)2~99ho;L=IateSJZqhO*iazk{}{>i#Buc'
            'nw;B2*9>Fp4m%xf09lP$mdJT1st?nJrFw6vj|WB9tdL{*F)Ieft*~NOm|7Cci8(itg%-'
            '`i2tgr$1c!kuc7@%C3_PI$&$rLKdlRQ4Yp!=0v4fr2?%8J7V#m8#>+T|SK=^i+3oYulB8>EQWKwuXGw)?1j$EbD-mI*}<TT`ujZY'
            'jodTjFk;}2BU)}gVD&HC3bHnt#A{Wm~d)!V+bv-'
            '{0bQAqm}xK5!pX9E|S!T{reLYJLYGW@qbhzRQS4UA;Wq{0t!3tQm;S6NGR=d>Co$3tTUWY*#h(w<U0;jLD+rWdTn4T{Bu`;iKuEp'
            'w%YZh&JL$Cm{mZq`En*lV<Tb%?StAvq$^AD+h4q#-'
            'wl`3e@R$m_7QV>#8>zz&zaBa@o*nwV9!zESTQbCOLRh8kf;@5s4QRqb4D#&I=4ccdmpF+ejHIVgx(d<;bis&O<Zhj(}askXc?d*h'
            'Zrr_m&qmMz@JXZDacK9vfCsIoZ6pf!Sk6ah=;3@Lum`It?{IOUAQ$M|)H+CT<)9FXM5WR~xdQP$4=rxb*7<>H9Da;e>F2Wc^$V`v'
            '-$Q@yCxd69_gFvRLs>)Wulv}(KrprKe@V`Uq0O{|87UPiOHoEmp9s7L*4CPLZWVj3*irBgYji{l1KCh1Hdh{+1I#WDl2Au){vu6l'
            '_X5y>2rf^6+X;4KLn6_%v3+qwvd!jnhqKHsSTm@aZhpq7<!i;u_S$3oasw9(r2umohZnKTTeK4=<@@-'
            'D{oDL~~88S}w`odo_^NeFxGkeSB7zt~`z810{w;$QW&KD{2Mk923wNe9aOYP7UGy?k!zp2w5?s^<(Q+5hmR{@d4Xe)5tLQBp3BJF'
            'KK|Yk>jrl%$t^@&u6e3TVI&ID+hWF6xAPB8CDb7#Jr0pbBcZUTv1NwoBbh^{ow3*LN?)F{Nz<oPPK+jd#ztgYM}$4IoPf%bfS6vY'
            'N#ph%y$QDTZ%+_yU6^dLBRj5#(qyLNdw>YnrN1i5)4{mXaS<!2qb<NaaK!R6WJM`L56<yk1JFOdFlP;ZEnJrbhA|Gg&b+c>{aL<-'
            'S(h1|@E6f?FLRd9+cl`3|qtl$=qD6hO3G!^@@Kjrw5eg0?H2dZkJFKvjm<;h%gvB%vy(&5Q0ODFY%`Aad4fX6!%b#F&bmYO=_~td'
            'Xf9Tw{4za|!rMheD8WSJOphyOgE|X)6+pPE7UjKsWLMx?qPq|G<vqnR5`zUsv3fAymQIQcz10o{F;gQeI#ydhLSY0mrT+p9b`^-'
            '64(CdMc<$$H&;Nqrrvh<%z<vy>Lf9p=vZMB8|f?UnCQBYX|WR*OD|!3qCl-ou4MM{eHEHFlp;hu1JEU-'
            'l1lbO)pz5iId>4x2cHCWoZVTa!HC0pi9ltW6JOV@(da3RAPrwI_$n?!8elHu37S2)wwg=r#s~E4xPmHQFfe;UY5ryk2lQS$BiQn-'
            '}$CNn6z>ww{3>JkYsY|_}HqoE-cjrv7)-'
            'Fe`v7;CA$FtGV!)PUZ<c!F+2B4Mlo^#l({!?lQqi_OOiD}yuqRkI)oc2+EF<_vhD?eX^>Xpf%|}XT{wh1#37B|sgH*)_z(f<kblV'
            'a(Z4{ZAEUne;|2T(|C+Z1x{~l4iZ*6Qe-5daccv&dH;-'
            '0lL|sFwg(WcS5uy$I@etjgAzJ9k$7W7Nr)D3SU0zBD+mfsX>sCgKKu!VTMB)`b?(i%Hx%tw?b<*sxMAz*=wv;lsQi-gbG0qH52vZ'
            'VLFCaQ$AQ@Oi&Wb-A=D@j+wWMPKD<PJm*TfjE!WtEm2)4Uggt6?HVyvQ!)shq9OF-'
            ')6^qDi6fxg&qnF7)X^n|#g+Y}|cTWc*kA~nP}YVZ<hr^Ri^p48A&yYpn!=Ori+gdSyv<2Aob(Z9?d9-Y2RXYq-'
            '^VD3G2w4wZ`Y$Ctb2=9F?<l7(}4Vwv&lo>920XTyA&nGR-WB6|_2AaxB6Ym;;3)#%(Ml`Dsh6REj5No|W|Jcl22`nE118M~U{?HL'
            '<OSBbQ8G<$&V812K!oZn0I}LW0DJKgz728ezJ?TR}9Y+eonF>4ZO!gWi){R69qJ3u;m#Bv3-SLZ_mG?(ZP+H-'
            'z;`cVcw)g0nB~RyEM#N4?aVR#eFl~DbnOO$+Jcx5vHyDd^rVKTxDZoHrDaJX-'
            ';+PAW40Gt>j!~Pg?TnPliFbe491d8nVq^ZO$dX&~4TKY%_egdsA<6QwJ;A)Bw!o;UvW*+Vhy{rbI))pETZFcNZIEb;i_qA%qvht_'
            'c6hr2hhUGz&PGWZ1@QX!%64UmjtD738_t1ifM0{l1*<1=^oVJxJf-BGCS-SKXP1_y&ky18pj#K4%x;bc*iar{ihv-MG1JwgsVe38'
            'Bp}k^n0)}7Rn&0`>lB?^)Q-|#lZWJFwfXE;l}U>ZGRu$S0G=9W0qdsEd&9bFAlWu=I9Y`Jo*Eq78-'
            '1t&vpdy`8rKXCjsbdK#p^?P^9E$60Z+<DCd``v+kwZ%*Ej9~Y3P7F5#-IBL|~&tAYdT1`UZCq{@0-'
            'bCm%UBjx?YKuF3RrNXMspxAil54Rpz2P-8iLsUgh$!r$g`9g0~+A$*Cl1gPz<S`O1mbg9C>FU`*}2YjASSEkk-'
            ')(q7U6mW#i$_$<(+%@E!B(u}pq#feo+{P@=ZpC~#yl7GqD@zo559#Bv@&2`M-'
            '~92b|3e`ERS4v9lRgq#MaF$i2vQnD>{xh4N{KQoPANqiK!+5Cw2wrzK>K)p{*))UI+9NF_B_<??|LHYJ6y2Pegk>Q*n4z&d0|P?O'
            'koC!0=9;TDX6>T{M*b|m(LzK=MR<Jz5nWa{nwsiO#H3Sf6{;D7b<lf((U~ZpXvYLMI+@i_Fif3f{S2Nu63ygyQIT2`r!bIUoFneo'
            'jNnSwCoc#!@^`4FXe*x#<Wy*jS_RS|K#2M=bwiEzj^)b{a607|I&LfxSR0sqqiNS!-'
            'T!{8X!i5*1^@z7Om2NUerwc&p*?@_6ON3g5lKS*}s4CeE)<0>OcMJ{@cH{?lj__3Zbxr;coSEjZJl}|BYS?6mjeTF$D_^$S$vmA|'
            'zsvQkTvdfqn(qx>%Xim7{j(+~RE6zw9_kMZ@8qe@I*|5IbSV<{nd-'
            'i>oG0Mar_Y5t3iSEBt0lt@sE8A=blfvOuA%J#7Q{;ea+cFFYGfFE207o;bHWW5^s}Eeq6am}k0}ZZ!?j^!l)74Kap)p~=|=*(3&R'
            '$Ja7FHV`=s-dkVmp>YU-$>DXcl3fdvGV_~qy)~`|dZhQxA&Be#wI>T<fbrNN7<+N`zOW4M{9xs4{_5e-e-'
            'a)F@DLtivq79I%|0?Wzc_PpdTA!KO<h(@S}#b&s)hd(p)``v-l&KX!iZXZKVm?Ub>@%(aX*Ma>M>j-'
            'dua0#GqpIEGjpI5*5mfjQ9Pggt!kP3gzr<{nu&&}x?$N&eR9~Q&I2IFXJ<~$PEXle1Cfe^q7DqxW7tknfZ>#Ik*YJEZ25_W8Rq9|'
            '90t?pPR-6UMXXl%k;VCQ3&q(}erSJzUFm0L)Z@MxnhP4$Tv6?T@#j$6kk`ZB(1SsW-'
            '$eFpuK0IbfVgqM_8%viXF;x546@r8nGk|)k~T{pw17*?i!;+_i?eg5rv|zv-|4af<rBec6(5-vebNk=P#3KVr&d|$7g0iJ-'
            'Q^pbJOjiLWCr<%uB}icTB>jqx@kx<eST&USkvN(>A6#n&z{1(b9icMC9E$g>9i?NRM)?b?~o|^1-'
            '<FTnWgzN=ay&Z=UgGOb2RbyLJL1o1MjxG$<({Mb?$lkcDXEtgNCObW?upp=-V+{L2nQQTo)ZZh~}`xDGVD-'
            '+U3k5MdG#{P!<z;<HPHWkCb9@$ZDb7L$3Y|a=&Vpd&>DCQ=6|0nH;)&p=IIih{Mmx0xNz2gL+MU0Sw$A0`}O<6Di6C5|qtWb$Cj}'
            '7WnK8q?9~mo;LQ;#9NjoZ*%i=bUsbbEEUHmj=PNAI5-V&{hWCz$~?2Q1mu8Cu;6L)Jw3m8c6u4c?oLr9d*Z(-'
            'yNims#EfFGuV}Yh1vC45W)YiC0J94TB^zy#^W_PU;`i3#Q)gU-'
            'z#*WEi6ueIQo>ye>0(8_#hBR|JX%59=8moiZMMjVKcPrW@Jm}U=@x~)>pTLtwGAA|Pl44~x|LK03AjwvW0Yp3lN0*QRs=DmnlSn#'
            'tAKEv$^6c5@b2%)#d=$2=X4jT;WV*&;7EcED@PKH!}sAM^J;;R?GKeFkFJiozS2v7#2Lih?QrJyQ1pjvJao<mf@E}XN-'
            'G#s3Ae$05N3WgZxlSaGzO<%&2ADy&9298ID#skhx5X<y6huj(F2NX$;P=8;Ja|ovZaABZozdsLI*?OM9}_piUl{a$~9UW8zeA`mN'
            '5QF_X*sHXXvF~R>g8#Z&Z@RTdLGzxrqY#WRU^f=dgiVZPdiajaoriorf;sL|?e*PfPN{J)wDS7kbSz!ibnn>O(kO=yR>FFpEkiJw'
            '_14_)|Sl+NS7<<x^)CqD8oT!1ZuBIx~OrF>`J$NX3Ma=wKj>cEIc`GEx$sBHl>~hzWpOHV|yGY7&}Y_6KRjQJjqg6Lg>(u_i9Wq('
            'V5+A;ZE8o<*zx@{T-'
            'v0B<N0WT~m%;Yf}42f+#>6Y0<y8E6<x3uhuQr?ZrFOHj5r!{ApbA5_T_B|l&9k~uevIWIo4l&<ESoS_MaoNNlnBSS`5bn$e%-'
            '6EcfEXd-mH-EGLi)**ueS=Ht$wk8%UQq=+WG8Qg-'
            '`N=+aquYh2d$`i=I2!qNvaB(tUOmgm$p?;X<mi{f=fv3R#7N5nQktsg$Gm`0lSn8>XRP!pn!pn7=x-'
            'GTg#I(Q8q<ua_A{S&fa=ZLE#}}%|U*M*fEyq=DS>`pzAO+!GRT)Pc-'
            'E8643(G@nVDAM64in4uIK_=&~XnJ1ygREHkcuu|gYfBUM}1oKPrDA#zjA*x$>JJf_rFdVDQ(G7{O#Y)xQhIa@nuWhY~yi}_92&@n'
            'l#t~^{a0tp33mnm0S$T*H|CiJ@qaX%cH$@U5as8EaRk=~m*OP~N^l+6W6PRSgg90(x1i#r7gxW{a*!9}Yo1S$w4V(i61OV~v>R!-'
            '|N4J-'
            '~yMvTY{qeRVVP!tM5#8>J5ZO$BbC5ggPK^WL)9)5uhOoo<2h#sgGcTry*(NmwX3lE7<$5n_aOd}@iNr3S%%eul{>@{?Xp$(QUQ%R'
            'M{01lvrxG|VYkRi{CtQZ;n-'
            '~R}tA^U%QTBoQE9kZ!a){YLH?#q=|ha#8La!3~Bq~u`>e0mJm3(e>RuAkj#1O4GFQ)XpMKAg!4`YO@6U|WK0!=_x5wjj1&6U%CBN'
            ')LSuUknD~n$p^*_`$p0ZmS0g<YRBM2NECsJ6u}$u>gBi&nV<m!~m4^v?K}FKi_)ygZ?vDZoYiI|LKeR``f>N{?@xs-'
            '~83n`pX;Fe|GCHAKiNMTQ^_*zH}}SiUCj%^Yqcs8wUqdI*FHjvf=Qyrni3g^!}f|#YXqHr=Dhm+Q0JB?O(sv|LsfrFI?Gw?b{AjE'
            'f<P0<3|yXmlXKohdYOR7DL6u)0>ffDTH|1Uda)9IfJ`lan^O_#xzzD)*6G^m;)Nzeep(E%9QF~))sU40MQv%n~9cLH5F%D%365=B'
            'dTzQeUeJkD$eH-J=mzDWQu1nDwvWc3E`}9bAW3p>^1kvts}kTmXjj_d8-'
            '|7U~L|}&uVwbfVkWWH3J&Lp_hw}{@KQ=|Efk&W<bzEW@4tu>)tr4r5x4noxQ3Q%ix5JBm_((PK2IiOwS_WlIGcl@uWGRUkt-'
            'c+t{@1oKbC(R|um#833W1$^oj|sg*AeXLo1nrUo-DDT5z2*T5QSI5N=5qz!#B2|kE4yAczY7-'
            'h|z^HQZ0u?Y1TrshbPW2WlJa^TDj;mi@?&K1GdE?vr%HG-'
            '8bT}noMd)eu3nwyJ6a1jG|fh^jtRnNL&=P$L<L|Xa9_Q3Fg0CZf@{X{bLuZ+IyP++e51>=iut_$Ct@?^I^_3(-'
            '6xvVXZzjOMgS!VAeU(5`19lA2|yr}JlQV%6nyvy`2s#z=S4w35M0D8qC0_`AK02Kjh1u@SFa|hry+APQpzbdW)0|0lJW(5Xz2@}d'
            'S)-Y?Gw0FHT<zOnf#4uqcAmIBh6L~{bYJoJz{2c{~fO8O&%~-GKXK4-'
            'PSkST=Y(m|aj9TV(i47MZ%xMw@uShiojF<Wxitl>8OG#ce_?q@`cAlo<6xDnZ^-'
            '<!c8P6P~`g+jbG*y5>sf1XZ9TX|GIBP;jf^tezOaxdguTvSH6aG;jLn$MPl>DyAoU;pQVv4j)j>9^|r<wZs-KJQl0Rb;X-'
            'H{yf#2tDfi%jK!laFG`I{~{(DO@D0V6<q|WFgvk{rrs0=pM;@O`uq>2@Zz!2Gc3?y9aMY-{TqQ2T@gI#UStF2B)jpsjfjMwu}UV-'
            'v>Y|KsG)gg+Q^xm0#U{`L{@N-'
            'KQL*!`T4Pz^5`7mLlNVdvH`m*_@QVIoBqRl)Br#K_1rXV59;6%iOa@fiTlFMr=M&Trek<c73Q_XpdDT?Q)Jv`<y+d-'
            '1J@t9TXA#9YNP2KoD4Ccj%{sw8IEx(UM*^91KA-)ZH+{%-'
            'Epf#Egba7{?d|hQ3Ur+5hdIZvEvA5S;D5`uiK7evTGvBw_=czIpw{Tc1C>|I$bOPp)d5gxP1ln~6}Da_R4<Kkh&G16`l0HEV7RVf'
            's$jr3jKIuU`!K-N};IrTr{~Wj&Yr)cnif6uk$AArz)#??MM`>zP6#27Q>!s%5Dq)P=LxjA}I$Z%DfyMk3hDDQ}^I-'
            'rItnPMK#32o!tWcCX8djaUL@(zZi?ZOpGzT8`0>3V?8mbl0uUZqV+;wfat(k-'
            'H*GxZ`7d%1)WJi)M02>JS^cqP}Li*Mj>yDBhu@FlfecXi7)RVp-'
            'F#D5GV0&M<Mh#jt8!NN)%jHx5iBQo)bPJ_Sb*$ib3ZJ@l=K%g`hgM~JkXK^Y49#U^Y(h@gr)uDA&Rfv^~m?4(1#LF(NAH>w8yAQb'
            'Y=>Cq_3d|8KxO$O*AxP#OH=-'
            'S~y<cbNt(t8^RizW_~F~Bdv?r2?tO9Q=0&~Snb56_&jjfJgxb)VfWXb7QJmPc7cc=$#5fz6FgZBLESy!ngqsS3PUl_tW(W=KVjuI'
            '3VUSD8(Xv8FV!OnVnirM4=h;9WV41BZJ89~ahK_eqD>-ev8ywrh>b1~UVz!M%gbCh1cR|HY7Z_+yvPm?3hws-'
            '18UI21KhgSwsC#)jZD+L@SSZ35nb!jF0Z%<B<#F0OZ|-|^$@*Hnd+gcTZfagF_)I5v6l-i)3M=J~h*-vS+eh4kF4-'
            'NbiwuL*{y7XxICVX{%{q7@({^FA+v<|E8N`w7O3>tIS$0wNa3F^EHx^~F+blKC%xq)?&IZQ1X2Yej?_?Wm;eb0;ZyBeKU&f&u&F8'
            '2wXV5l9##55U=s8x5C%kMK60U*ZnN+BlcwBl9@UxFip_5mPjh{zvckuU)}^S(r6L<LJtXYGw1Nme@gpi$#H+Ns`Xj2l!tk*+J%6K'
            'j6~7|Gn>7!|K2H^sV1KbK}F0F*>cGyvm`aQ$|=aIv3c%Ax<TttSUMdzGNe2G!Br2h_SpWYo>+V^_^2gx-~QU&-'
            'hzLP|K=Ihz?xyX>`TQ)a~A7R&`}+d~%hCl9NZMU>+H#CXWV2{T!lJI-H?9MxoJ)lx4CCAix~#-'
            'BsxhtKVlhh7D=&#aHGxPwoHm4dCZxOdGaDPP7rJ1Zi}-'
            'dH9;s6PGb2GzA62+`Vq)j)`h9XbIT;nVTUertu}JU#YP329=|=SBOYnu)q#NWZeF{A0YsK`z-'
            'K<pt!&F>03(uK|{e6VM!QBg2czi*Oo01_e^DY#hENafr6?J&}r+!9WgmA8GuLwRIo4(U?K1g$P)E0cTO&{rS=Z|3j%Uv$=U9)cr|'
            'r5b0*GI`^F^-pVZL6X;~_+ta?sl&9ISK+LuH(Le;}-'
            'DZK)^4+b`{!#pWGS4zUHxG^tC+LVo|Hi`m}_|%1jkBfFh34PV`M4M<6Mg@ta3RAEnV-'
            'U{%$k+t_a|HjnAOAVNHyp*+sVJxWbfd|o^0@D~0~i~S;QdLSdxn2aOYzB5kAFS*@NPc~R)jzAU;80bD&BnMo&8@u%Y5*2N1Kay!X'
            'jB>f*4;oAh{x4J;d@)r7ds=Cy7O9;qNd^XA2b#d`U_&4i2yW)gRvc$uEHr-MoI4+o1gXI}(UymK|mb4(9hvqa=rDEbK`poGYG*n;'
            'YOEkQ%mZ01tZc1CDxlgu5wBR3&=gA47;FIf2~I_}IkJ!-'
            'tO?e3G}`e+Dku{db=0Kl4`qw{P~}yL#ip@7;d+T6%hvzEQ@YG?q~#T_v)|_jlHO;++_~LcEH@)|*6bbh-AXG@#+>8sLoh#4?0uY('
            'V$1Sc23_X5e5}bP%lWJ<Lq5n!r$^kQ-U!)eF`dy<{^8zv8u$QVj$)>w)nVJwjUP7z-'
            'l@A_e<@e0~4L_w)(rQ_&<4%p6<_Ae6pF7cUfqPgIUglRD6b_X9JDhVl%c(?+-'
            'l<oX9N2Yu5mKu%@_X0saJjj6uD_iGZTET)YQ$FxQs+Y>e;*-'
            'ZW*p&A<k(k!4{SFSPh$NiU{y>b10V@Z*N6W*Qqp=4|)bjm<*mmvqTUEHnw2LEhVcC@99bieeJU9Hm_ojwXjbTYUd!UtXUmCDlL9G'
            'Y~6mZofaY)XikA^g<ChowJyIaq<98W2;%cSp|{$#Q?UI@8?8Vc_;iEXQ!$4O}%gWVi$Y7$a1I!NH3z1a`Aq0Hjiv-pFpI+mzc14O'
            'Ys@ZJ=!lg%i)Q!_it+tg`b;G6ef0Kf40A-bsL_dmE(5%D9oHG$}hEK5loy3&>w;t_zDbD*V#(^Ok0A9*H+O!L?H391y(eug~}2_-'
            'X%7-'
            '@@}04%6TM+#tB_iz%nN*_s7RbGB38>TR()BuViw!zkxt1cyYf^}8}0u&u!6#+(t$n$raBj>OQwKuYQEC*^C}oogV2%eBwNhRxvKF'
            '>`Cqejv(H^xwaJXaD1C!|`a!T~JPl&%yA)kDJ27<R365X(2=%4z`q|KJT7+VRk!ga59iG4Lile2<b+=-'
            'q~$;qe`4WOan0VB)z|K6(so37M0KSZT@H@EQd0bC7+P-'
            'No0laO?}&XAs6ERfS36b<IxsqD*f;Ms{ihH`&V&$;)GwkqDhi)YA10nt!is4E}g8mH_=Uiv7yikJ02QvxB{lYZwNwgDIo0~{x~~-'
            'Y9=~);v`Ow(xPEYa-'
            '7`cv&ysiQ7bD&mP48~shyYb4$|b6W%&nb=D0DasM7v23bMk>tzsA#{;UypF=E!|R8f@Hk52lgbA=*?8`8bR3f>{Zut|%n^PGap&~'
            'L>xXphpEfewQQ8I-zbERZnw3wA8Sq9P~m%LE*}%s(LF+aNaa#1qTFKg~TdGd0Xvi6|y(c>OEi-GAq={r7$@WBH{$L+&zm$=$@xl5'
            'tP8ur&vWYC@5<cp#H0r%e#8VNPT^JLFa>29^<Hk9Ui%ViZSZI3dTu!z!i&`{hM6n_jr5YjV%PmKm0iHlr)}AiFbAY{20VJqxVh2X'
            '*_~Z?QuIM2k1y{wxEq@@_Ot_{70*VOJRo7B<;288MyGB{H-'
            'P(48gZ%E3%}g>hf3G(WxI;Eyo&46$m!sf>h@4xT1uL<Q{rA;~H*IhWu@2o|NvF0Qf5#a+AgxKU-'
            '%>FIzVdZ@^tjP1#KCPPD*3YcOTw{na3sIdTKVA9ZaUr{pkwIVR5nrDzQBewYpr$wCT9;m}aj<H+XDjaaDlr-WP0?wBvj=@0|h^F8'
            '^t&6t^8>h)G9R|VivDXA?A$TaRk$XQgYH0~aM!YMG7bulD%h4j&FJu{Pam_J@>jb;W;!k!Qk1O+-'
            '<xP}FE`USF3}qI8UbTkGqCsM|cmbXF-h%k4?C584@3BY4f5sxqZ&sFN$JJBxIK=9*D-($><Vc)ryVPy9DKm+Cebb3|`N-'
            'v^o^BCh{ut173$(d54zqX@+M2R0!P}ZjyQ|cCXefYoo4h+n@=IxJhp<H8VuO1F0Ie}+0!Z;W*KX8;nLC7?XlfW}in3uiAfg-'
            '*9UY`4CV>o;hibMCbU^IVl+HhwW&!{q!nI`#AnxH+mQOtIPA)nRO@`6bO<R<mrG`!MwzAhSd(6W3OHgHkxCn|8@3blOU6e<fA@EF'
            '3$ZOPflVc<wroj!W3dr&peH`GfdHeN``yXGmZ#s_qC7YU9!_wA8cn+9RUn1;rb^r}byMTlrlTsg~Zg~#BESLm{J?dbVzMWktKio6'
            'FT}C1$)tIsV)@%EwAXoZ}yDm_KTL{MYALnM~PP*<4mm&>jZjR8U?$s;m(vsnsV6M#k_$nlBcHx7yoD>aI>om-dJ56lk!C2>i)Xi$'
            'B!Tbx}tuih-'
            'u*3Lv`HH@wTqlx#Z5ni2!$@>)L37S^BV%v|b!1ID;*kMz(Xh4lXV3dCFFbvc0x#>^kfCZ462G@NyE;BuKp%q*7I%iX?oQS0lr-ge'
            'X5`3|-u>?FAH8w=#n1a6|1N7+rNg%Wx4Ep|J=U0KVJ_Cd3=zKu`Q+&M;?$w#Dp5&3C<LGVE3ft6{C@xWmw?zXYnlC@eFkm_-'
            't2j|l3&Zvm@gJBFspxUtQIBCvWq0JI7}iT43F=yhbK=%OtLElbC=D-'
            'a%${YRai*wnJoYU!TMRYm8#ja{RgYyH2s*$Fmd2!5JF1&74bUD=)qy{aFFZ@BJqTp#h!mCm1n`hQh<5M_<vv7O7=FkWGY|i)<yEJ'
            'Z(hLbKyoDanXI3a@Za@z{K9u3@3wf^n9P6EJ*b9hbD261Z|$ss8BP?Z2}osK2Y~S(HpvbTj?S23;wH5e=Rz%Eg576!(&T?*lw$y7'
            'I{utQDrt{~(9E96T1!hPm5sF?^U*dOK2Y)yGkwIWolj!bOe!+avO%+w7+~4(Pfs0{l{RXijnL3Jq{u{^r}&@@0qIO>Mn0Gf`w`n2'
            ')A;2G%fh;4jj(5GD!o|R_y!uG2#bF^iJhF7#ZA&{HU{>bF$P(Gh%xBn2r_y|$u)uuaD=>?kzC%k^I&FKDf4|9q9e=6azqhTE(Oy('
            'G$WuT`rE?=6_7P^&lYS~O=XL3dP9P-'
            '%RxOgauF=N6UR_=f;fm<Xs6Zciqlm&Vk&|6UAuOueWB6xfkIBBrsefPLmpMJ9%(pcj00UQFl1;1Ys2ZIwc=<EJ9gO?jh{W~<7W{+'
            'o#Vg5Ii$tS(g`Si4G%THPU%}YVu!v_8wZEXeu1wlsCcYEU&<%fdT;pWTHlnfuK9ua?b@YX4z*?xbgs>+B^Z^1)t05Bc76TguKj&1'
            'RiSRZp|H0G{%eq1O%rrc$~HQsC31KPo3%p2eb?z4oSV%q-A}%AaG1g(t?E5-1~z;6SN3Sl@)-RRdW;UVCm$Tz>4X20zAu_h7&9-'
            '|jNC=KQVI?mK`bolsa6AUL5voz8Nz#$)DmgY3ruZ*b?{+|XKaL0JgddP_PKo#tTFIrU6KL8xfOS0^jVMbTX_G3{E`^YM3@>GD#M&'
            '5HXya)jMK#@Nt<9>`Tyh3WV3ZC!f4%fmX(AJr%ch0DHdg+%F|L$v1sjOo_ho@Px6~1@{V6@5&B}rWRAIXDK$%4iA`Ksnqov9uT$7'
            '-ezh@q#8&S!J5p;b8e*H2OCh=In9M`>VbPi)H2Owdxh6wH>rN5}%WbX314j|eHRYt}N^70rqL_W-'
            ';k)qqkN1D^swQxDIqeB)4ynB&pm3%!qHvO<4VW#OsnTEvZ3)^IR-'
            '6oL6YQwRx`C^L1~(y#3I3fscgD`elZCbiB(6@Ylc9<209J<sDjys37ndPl|LvdkUwv!;2fysUb`|2^>|go){!4EwjLbH}fk9BfTv'
            'F5~Hhrg0+{xQAr{PpvUUarq_%YkVOS{DkD{)W?eifTf<z5*DHy+F|gEXAS6vs0_kJfjWarm;rxTQi5=7vAwU^jzw-Ie*Z74OT8iu'
            'BIsw}1K$tiB!|$+^?jvJ9)V$JivDZQ*$wv7a0a5n_qj+N$w_9emCeY)%U(Nb3iir|LS|)60?~v5bx&e?X_I%G<_11S#s82k&f{pF'
            'U00um9|KA-cc-m+gU<VRO3~H)DbA=Jgl>s}8q}OETjxV93?<RT-'
            '~E;@l}A4?EZ%Dl;?>i|*%EmF1?+Gt*V2okX)8Y=?<NXo4X7`&zHwsPeA4FKBkp!!)R{kV`T0iy~0+OE`&3c9pEOp^m(HnQMxXt=%'
            'i?kZR>E(Vef$kRUt&a6)J1z^QC}w8N$e+9D^%C*iaR%p&;N=Bz^!q-'
            '>&O`0!qN2_x}%EH2LwK_w*NE!c#ff8m54sTokA2rf+>rT`ilc4@VC3t6t~cx2rB_@zVGd%CZl1syJ&NBtre4WrXA%>;9~e(Ftr%N'
            'V?H!XQtKv&5kh48!(`N=CMN%C{q%%is#-'
            '_YBt1nF|k?25=Zk1k<1)M4&zEkpn0mCV(q2oo%<kXq#Ex0gK+nTW^WK0*wrc&N@7|POo{f3H#UA<@Pmyy?r^^O-'
            'iulBqhVleo+7Gt<Ij~eI0nly&`=OoxxAu9q3(oKx#f#srd_%bx;&_BPF%4xLQ6MI-'
            '0ezp;|yr{qVF#6<LvIA}sR0eE49($Qnx<;#>lzCEB3)C+C3LpnmL9m?~Zh+h064w>*1xCR&)EodYwvXm0xKjL?bk3eHFaF@UPR9S'
            'hz=6s6Etq{>MtHHBu)xMqrW$fhWf)(P@8bPb{zOe!98A5gzk@<nI_v$iEQlsVr)Sgs~4s)W`)(j^EoH+-'
            'Ey%RA<6sCqa8RhIMDIk8}QNyGm{j>{K|=}Sc~JD%DV7=dL)t!Zr8m5W8qd{Voo^ZUD{s@7!Xyp&+0tzz_Am6HMig$o1|QP7DYY%{'
            'WI5@?cjx8To<>k2k$>#aiq|Cvh9-'
            '3<}xJ?fw$TKr6zh`X{?Wsw?pj!#DLL?JhjFo518flDQNTuwl6n2CHPG`~IE`0VrjYaj3b;yeB8AK$qC3^Ue2=j<Dw{=j>jT!0b}d'
            'MZvH)x1qHdm@?kqti-'
            '3OG@=k*gQD<f*0_0^f)2I5sQ@+uUIYsh=9UwcsW<9Va1zLmZOHp<T<>@)q#TUG=p{k!S}=+h+ytPEXSPn?SBCAgFm?W+?D-'
            'T|2WifK1dkP*P5eaN^%JHBE~CdJUfQ?osN6NZ~~|c=U+JLtHwUe+i>XdhN%ESH=7`ua3U}&a1<NxIHQRKc^93WfVYB+F<_xM`|+?'
            ';xfb{ds>l>Scp@S^QItMbt&~{q_`<+Z*6NTMim)FHn&Remy#w-'
            'CZlQW60*jBuX~+(J`t;d_nMWeX6|HPWRAo(BAUhP6Ni<AV6tY$Aw4qQBGv9=E;x17sHC;)(H9Db=IQ=9_^fWnj%ATe#oGcfb0>XM'
            '{cz?ib((L4(^E0Iw;Wv1DsM@She3@jk*R3~7;0gwok`@RUI^`6m?`plQ#<c@Xyi0+Ot)5vi)K4@1-DpKCkTO6S1UfT^+p3#!(-'
            '=N;6NDO`kUD>z*rV=F*FOML7jcq~?Dz0|UAh^*Dl|m9Z6_BfJGS{iYHCPkkd@8j2vx8lF+ItM8;zvaG2OyJ7X&Rq|66ZhcJ7>p+0'
            'V7Qr_tY8DA!*7{r+>G^{>3=DJIl|jH{l;Z0fpV$_x)Y4+!$N)&MO6RC)pxCpXMBW|YX-KFp@3DH3Rcmo{Tk^`e0_UQ>7@2xLT;I0'
            '06L>5TcM3$af5xrtK;7m2KNVSQNtBf8#1AUA$0ah3&4Jue_bHtL6AN(EzLFxdu|C@)AB&hqslE=NC_k)HxUK`5Lg@uIobq81WW55'
            '<Z>Pp!=Ke8aOWOJ<IGu&Zv=$Yu)I^fo56ts)DWY)ErF^eVlCws0v%U+3Iiv09~hsykS$Wb{}#XyXcP)nFoB>;O(sZSEm6Z|+zPmi'
            'gaw++AkRPE^oRYNev>l2%K4TPB+oi0aJCrb95Ltn&uNNDaB0<p#6u+N>m-IAPXJaF0Uv9z0yHl?Kq)WEB41U4-'
            'qGD|F;vF=Q`s$N!4KdbNT5Pq5wtF67H^ec|zXDN#=)K@T@AL$0s#-'
            'n+dHzlh*x!+?Yt75qa2{QfJ%_8kDNFA8cBn~1i9QvoHo%^9-cdy^Xm_#lorh-'
            '7R8oAC~NGDTo|ECF`xWJ(tF)gC4h$RLn<OOH+$p+j%~SFgjyv}F;)#4dJG#-'
            'U;tOICoh!6;)J6ltFkvms;!|2ew=4u4?2>z$f8J$>$s{lPl*hinm`1;A35T230>UC4_R>t%rN%(K4-'
            '(B1gxIZp^M8SSKFrT_Uew_m^BzxMq8Pv76adhNz%uZVS1OO?%8$&f7?a8vwLnS%n3d&g|pytUlY`i3q?XQ#g!Ezi%NiKZ7%K014T'
            'Cc>xyOICJfdFvrlg-p%OomqbxmTL!)iXPN}@_-UiLrr+6l28}A{5xbeTp}@*ckA<Ow_Zog7$^oE#va+0d+M3qb#E-'
            'PKA9*zP?{X%73Lc1Q1VZ>lqod@Ln6c2#l)MtR5Snqpt~l9vO|VDcS=mT;JIctw5~yDpN5btjaZc5P$JSwka&Y*eZqdQwGjmjZIXV'
            '7WGj!X4Xahs{E)zTVjWIG6xxVsP(nVTuamMJNVO;4k&AbUMula4Gfwz`!5v_L_Ib(1GOR`3fn2R{0K$xnPczSSObAAtwqpbsI15d'
            '?v3&9_{u8A8)XdzxIED(MyEM&D6}RcUo8H?Yj`Qq62!t>jg5ZDF+bEn0_<#sR%+Abd6UROgzK}B&aY`!+pI3*EA>rDp{TIG}^OOG'
            '@{Q1dp`#V{oLI&CTncFKhcRmTmn#-~@b;^iED=Dm<hUDOxF+Pdg(VGTafIJR?-'
            'X3?BNoS8YH;v24in!cFiqyEpk(b(ELu^BXY6~mTeC5@muDXUBM5_UEFE}E%>qy*CSyk~idX)~^zhe+!(s3aaQ0xeT!WhreiY7+1O'
            'pRIVDUF(bP^Sc_y5KQMM*iXF&E4p<4|>iBDm^5byvtL7i=){&P#B8VvMNJTTlvb+hdBIN6-'
            'l<LD8mhdCOdC0g079+74;)oH!{37`E!Y}+>-jt7-Z)$rLCor7GzLHHeolmTOYjJ|Li-'
            'ifMg9iL|}xMQ@u!ud`ROK=3-M`Dl&#s!tXi-GMZ$2OS7pdn5Hv(Mq7I}>>w3rAZ9}6N^V<s0!}6!gsa=F-'
            '%*s9tMBeV_a>e^4sRxIBuVU>p=Q_kJWY`$IlTc59E8_V$6Q*^FSjMMhtJBzoOLNSV|oOZOwly3Aw!ECusg6=9>l4kj%p1LK8eNBu'
            'c%6^`DgN_FXl{kD+2?^^h`jx3uv$l(<Y@%pgaJ-23I>MRw)g-dlU{;xr2NUY@{Yyx!mj3!E_e>ISMB-$lUfy-'
            'L3Y3hV^(cPFGSJ;3cW8?t(PKHKs6hs3nK6!^+{NHMT4@gMt9G!JRoc9bo{>6awS|Ps-0gd!u5eT0v+S;*$@o#}h}RL_--ZXpQKx>'
            'dIx`2sR_@3c&-N1N@n{W-'
            '~=PwPm~z$PsRQ_S&t#zQiSDuY3$bw449++0EDAVIqc<Sb>fZO{O7NC?YRNWI}lF98N;KTCFE65TEj55w6V6<S@dd)ah&GO4%SPAc'
            '~7e43;|3-Z-'
            '0~;}CBG?m`G_7$;_B(*g>?skbMYS>C?1yEQ|Y>(fWN%`$MHwh)3@R)Bz2N+yJmc`9?c9BVmT4bzMcn)&DzRdXbVor5AiQ`Y-'
            'o?z*LzBdF=PRSH<F;P+Lsz12DwOHX%Rw(!~cE)=3O3mAqBrESDg!=|6@7PUq4x1OOmkmDtA5Eq2ZN@{~>1D4h?c9SBe6)VQko9Xl'
            '0z(Ded2|;@oYy+j{oy9H_zqB^(fc!3$<~=Ikd_o6mpT(uXwS&I#51%QmW)T(zkK`hJ6T;jgNn17Q2*udoxZ^VW0qq{vN6E^s!fgL'
            'fa$wmZoaK)&UqH+bqlX!H7(Fn8w34U+=Z|WG@#ABqu~6(^W<_!U850kIP-b-*pHaDQ%@-'
            '2CN|lE{W;e1H&_=iduLl^tjE^OK#pStiwvz4jPS*<Oj$IF7sKmwvArj+@!B|>2z?!B@8z54^OAEzUL3}^+STuLy%*n?fC~P=H*m^'
            'TDw^JaL0>eXP38mp>K{wxiuK(FH>;PfHpqnqe+yC{q;o1Z4T(^JnH0Z5BJmi)H895QgbL=oEuDh8yu95N}%>?uCAU-#zgE-'
            'X>uesi6B`GmF$Me7rXZ6KO43w&E#b0;=!Y|LATRwf<N9yX2`{^QQrk{9xarTi%m!lJl^N%mhEG|V0)60)i1>E<#8wZ440zPhIvs+'
            'y2fG~tq|MuZJ_&_xn75Djne)iPNe6$EL#b+01&d$s&FR2sXlxG_!pb!d?zms9|N^8a6mVg#QCXHaMVAgi(WZNCIP4I93?j=yVGIW'
            'NJ#QSgm2I3Vk7i#Xku3`HB^VIL)|1r`OtYaCw<reMtLZrh9c}li_2TLFVaNo@mXgA}Cg~GNhyi|0^bc^yZ2g7mFmEn`7#b22kpIm'
            'izRjr%8UWRr?8;?t-'
            'qqU*DpwLBOXgFvsWL=`w==8NLS&K<Ui|HFxTG;J8NDk`aVmglNTnY2!157m>U}$&+VmoqIFU)pw{vtw{xFYFfyUb+!P!Hv|GBi>U'
            'u)>3x-|*X&7K-'
            '8TpZuJK>S4zv#y)4aF1l~Ym_0YIf5$21a_o~kP|RiTIK5rU$AWmAjc7o<w9U9T6sBjdm8~@~H)2}+>0%0uqXXK=@DX;1ojO}^*2|'
            'vj8{k?SM;uu*r7{u95e!NNAaOdT?hPea(VNYcspt!(i&De^P^v(9%vMt0L3YR9gu{tQ^sy8M`Q3(hb5PywAvN^Y<6;lmTx`cN!!0'
            'nay#3VA!P?4*t2-p`F&y8aGiADY)QS1|WeCbUy|6HIN^)^r#)K&>o2YH>urxUVQDh}tQVE{1Ah-9VsPG*SnFSA*S1w%m--n~idly'
            'zNtOnt~-FKl_`qGnMez?3EQqGQoM-'
            '7H{+RP@>O6D4Ks8smM)R!Ixo(Mqm_fK8{ApZRmNKNv~zdiNz1wZ`zC(r%uDX>8O{vnls9W1yb9wairA6fz-'
            '>Ft2;k(Yo!LL(u1^h>7538Ndc;*eN_HH(Css>-aPPzf$|{4<MdEXu-~MN8)v7Umb1XHG?r&Mz%5Nk*O-'
            'ghvSkOomGz2eO$NRKi#(SJCyNR)^twvZ9CP-oaAnq2XE$HJ^klxN<D8vQVdT9tE_q$mcal61l_D!>4UXG*1r5{=vi~B@{`*++c~x'
            'l;Pp2(b1K!T}U2$=)$UVl~(Wb3nCCR#)~YQnb95Ye<))~p&kq%H+)<tA^ejO<sGg*{EDjNkOLCIlUNPgEhWGTXu2z@8%78qCKDu>'
            'W|-GN7eyfx<*!ir3;|%PL-'
            '&d(Mr}|I1Ou<F5^f6{r`x<Qb~pU50*T5Z6<vgr#_U)O&>!75fge7_^{32S39zm>!@V2uH)A3s9YNO^Amd~MVr)a+Hogeln}LBAaO'
            '~2hOOOiy7=QR52!OUmDNe@diSy&wFe*$;!Fa?3Rnd|0@j%GixHKHyOwc5JH8(n@viBFFKgyoqjEzz7+_5o~yDM+(K`#Keit+IQhs'
            'W(#p8~a`w?I?yj+Dm7Jq%m-%3p5(;b*#JoXfZ&`yQyJH?}RAo@07-'
            ';Q>Ghgd7*tqvz6eXQPKQw*~rwh9G2c0~0DMaXk;o^5f6;Uw8vdSuwBm%Wug`I#w(}D&(lb+k&96MO^$Mtx>^a&SGVV)``qb7q}W9'
            'U1l2Xvd=HLzq@|(<IlmGcK<g|<ut2H5qV%EjgMd7Y}MhCQVvwiZ_rWIi)bOw(peTX3p3gUWi33o_{7J>uHS!o>-'
            'Mu(fvny9{vU7t;rnc`x3B-~);qu5fAuL`m0vx5^Mz-'
            'D^i9voe!Lr>zjpJ*mstVGh;Zw(x1db_qxWyW{DT{xzQC&Z1wF)@3xr5JVFpcj1J{;^CB*t4{kebjJ-'
            '!xKUSi>Kpqm>X{{fWL`>$WoBJ=}tq~h2B?64v7p(E@WF{mjp_9&Z(uuPEh#bvGxI3$vPvhw%`2c8f%>b--ALePNJDKmy;3>u*&3K'
            'f@KpYH|EHT~wP{a?P}Fc5O>{&2*;Ir|)FS}P(*YbrcA4IaPPSAFdWm1WpDno3p0)Y4!j{_Y32KKpV1nKz7W1WTta8sM0A=L$#6gr'
            'nIUgCTOkbsj3Mq2BY258vh~Jg)v!WyjGXD6;XImqISTVgf53S@EOyne{uc12E(M_doAH^XJ<?ef#EH--ldzSUn}VLe>BrGOT-'
            '!TrQoLR?B6JLDTj0s9!fee8CDJ<(uMNVPfP8*{R#%TMivrho}|6-iXCU_`-'
            'iERT!FKfIcjA1?Od8rf9HoteS^)#`bi^TXUGGtJdj5m?2rz+8@{3e=OczYk^7MEMC_-'
            'y>{1b*}rl9djET`8;RD2=;Meni(qE{G&jJPmiRg{=i24lBZ6BpVac8{Ums@DBO^$vNGK6S6b>+o@brx$ZUV^m*wStSm)4n`I%Y<O'
            'vpEb${$JiqNXY'
        ),
    },
    'comic': {
        "filename": 'comic_core.py',
        "sha256": 'c9e44583c41ac3da2e59ec4895f739a8fec26fc411dcd66f54dee1e6bf9b3167',
        "payload": (
            'c-rNCYj+&gwcz*u6-'
            'CWVTxGgTk{`rZ&^SVtjRxCNBssuHx;3Tll2mc4yHnL|TL`UXZUDpOVY7G#CxP&s1Z<K3;o1iN%fv0opZE*2_dbt0r|MLzg~`2HYn'
            '-6&t~&3t_dff5Y}=l0#hqZO5n4gFv)YQIB&=H_M{2FLsAip+IcbF#I&o0zv|=k+4I2&1NjmjLv}CoKjdj<vZM#%jj$3P%?=N>d-'
            '8l4pD_UzqqgK#twmLy4YBiHmNj!^J+CiLz;&-jp>_89Dpm?$xB&*8Ls2$YnahN3X0ewITZ!PQu^`H~v-'
            '*h`sLp*KCn(ao=S#HH^;&&`Zk*umUl2+|(*pa`wOYOK-Q$~=i%deeqt-TyIWJ8^3O@8loqdHp}m}IRR$6>SMu{BD>63wl~VNjoLw'
            'Hgx_!de$rnbp8))fz#Pq($W;R${fY*6?U4V^QMaxl<>n=?N>+4m!A!;`KEAWG_1F?WnmT$ME>{gg^f9#P}nVr%#lv@u1N_cqm(^f'
            ';N^bTeIP>x?!^xvfACafon{Ci#EE=Uv*m@r~@y5*@~L<C22RJ4($B0-'
            'o<Fif`8Q1^yEp=!sJ@85|&D(@u^dj<NnOV&(BQGOq`lHJvVDrtqrPTuXZ}^3-&1gQmqbq2ab3ncA33}?Oi_~M=PrxERz1JR!6-'
            '14tT?&9CV5WrlUrqbsk<G@D8Rg+w1N6GS$Z~)#`oT$Ps$GS@LJjoSvIJHQ`TBO`e{cnDI}Kotl8b*@P<<z>(-&=yfi103-'
            'bAho|PI{OPf|hoM9qdQhefaN@-'
            'FP<yr2X$?8^!<Bzoyw@E%y70ejx8%=`&y1aV=;VYyHak0c;xx`&uSw&J?S&=h=;*m1UP$hBk0!M^ScARtqxwR!ziOAU0@R+GnHV3'
            'NohYg8{$lLpnTb6&3ID;%ea_M82NHmVM)=_TzwTRz7n+Ov-F;6k*!ZH}>MqfX1)INFu%E;iOF>MJllvclnYzwV-rW69KJes!cU`{'
            'b+K|gQ=E+lICno&aGslllJ~n~-55V$7*i6EXvtfI`Y_GsX@iSy!+D-O(K3r<sn^6DM*kiEtC#dS-'
            ';bHcGHTuxwbM*MWL)Lz4WcYyiP|Hk1uP3q4$ndZ~%>ILgJTpB#H8VGHjF&n-'
            'HFIiAh0X{ec!)*?@bf>XCr;p~*i#%L!rW=)84VX6K05KxGy||~7pJC<<)(iU8<;uq5dRp%&+$`_KO!eSGjR+sXPicMxFmo2vvXr}'
            'XJ)hQ9ULAhTL*^^;Gcu|=coAR2sSo-?6`kydXlY!2P-'
            'gn8enMhnE&YH>0?um&icnEPfl<gP$7KZ`~we;+CvKqPafUBaAA13vT$K!d2t`KC@RiO%udYw0;Y+zl@%PHI*rqro}rJiGmqiN=`$'
            'xepzL>+p~$I?W_N8Vj5loyh`GgnSW(l8gXT);z;s52T{o?9a(ZsS8n6S?XC68U<OkMi#)lms9As!>pK3h;6eAcq><wGaqfxWoI-g'
            'ijU<B6YehVJlcj$iW!hMHa%VrhE+U-'
            'X8Xt?x9)EPQ_@TcCv`z+@Xq|s%o5uFXK6JhOa%eBT=ff9y8BZr_J{GX^k8!QKLBx+97SJEOjAW5l2hk<nl$o*^w;AtX`Td_0KZQ>'
            'b3KU_v>;fNlymZJ-Bu6LnuB?*>8E5Rz(8k}nIdB4>R&%u)5VH`xw1h#VxsJR7;)o9g%hE<1?Hfkj7v@iWk9z_m=r0QJU1=^o9TAh'
            'TxyL@otNExT02R0J6@}scy9r}GXTpxvz#PkCW4EAHs9h?f9(Q=q{SSLxV8`nZ#Hiys7x8k!v(9)heQKu26?-'
            'in#mTAMdlToYFg>9UdGbvl1=Pk<R_a~bO_>Hg=YGWzbh-sjdz*k|@bX;4FpmsKa-3c4@#OkaDz#-'
            'w@bixK~jkOd5kio{R1?#XU&3YK~E#RF~m+7(Zq+io6$6Jj?SnCkK20esUn~gzmPq6o49bf}dBd{3Xx5j6|dc%hNUrYh!&yAhX=?A'
            '^Te;YQ?`T+5DDM&*4jPY-+)xeJsHolHuR%1p0iDF01cDI9H8d38se&U$$6L^bY4ZpC>#Ba!iQknD6@Fw-'
            '^vXMPJdF<H4X@73wvAO&JH*DD3s7<{jo%IH_)oi5?k%I%iFhu%E?bX9&;ANv`)bV{M2^-6<Re8`l-'
            'D+|mCV1(#VYOXPmIKTI1nT&;)d2XsWdWqJJTyb>s-'
            'FU$^&~Y4qs0%s=qfOUaN7E?4jll&MwE2sp~@l@o?q09QiFpOJQpR=(qKjDd=h0C{HFshTjuYJrj~qw<=WY7OXYNfXb8JEBNn6{wm'
            'Yj(U^w%htwPb;)u>(%n?4E}N*OBjGeowi279yGs;B!ObUJag)a`_cgI|;U4Ac=5gw&&2N4{E2VI>ZM<8N9U&0q}<NkER}R-'
            '^8?qt>~g(Ipyd^K%Ibl=)LQoT%T;6ed@LW*z1T<BdB&ya_bR7JMUUDqDk&Q-'
            '@@z4~qeRm7&R(G?oP3vt`UKN?K5eDk|o&%H9fmwdp-'
            '#o9%ie6*z8M8RP>T1x%TBlf~zBu>E%QUSLzQO;)R%q<|<|x6}cFL<bn$S?6O)=T3E6E29KZwxR13i($6f98r>OcEl`UsoKyS?5l>'
            '}%E(qnY~$24P%oNR;rKLED5{P0SFam2eR&Ad=>(<3g9<*daf8G@<5AIEceEDhxXD)uKyFMxuJw7{Tpa{`znm*qw)_+%h>B=6U48V'
            '+`3c~b8%BsnUOGAs;fRFv0`wm%Q8Q>LFZFImb1ecrg>47U0hX)@@R;ut|2fT89oY*pUHHFvf{ZA#U!Zt#l<B%SD_(}Pv)O+{f^%='
            '&+!KYUdmz&TBT+C&6`s?Da?4ikg<L3jDObSlGZqegpb<*9Rq_-jIHpAq!*!r;*^;244kxPH63txKOfR7cB$?W=ut(a-'
            'I1U3VK<9OaHq&S`G*T_d#{>W62h88;L)<In*2xUvf`Pj1PJSwV$&b>mLUnc{N~SgoiN8AZEX^P6V9>fl>;us)ypW22jj*YsUBv>4'
            'utNW3&>aS=l$@uA7Uzc-aY=Bea^PPN8~GZei@9=3z&oGKK>{KghXedt1PF3eyDSi6MAT~7syL|(i>Yyp0u!;0YhIN;uw~|K2WYbp'
            'u1pND-d?FhtXwT<wwe)0u|CN*J`*V%q-;`1q*YZAA4EXT!FA&Gv|s83kWT0}Wg~3x;e{HE)A|JxCzAWDAhAOHqHu!&DA+AkICSi-'
            'TYuVq?dI)ouJ&Gi>dvd*ZoT~B*1NZQw=QqJ`R>;1&;9-'
            '4zX5?Gbt$z)O|1o;8gj9Uo)J{bjRrk;*kYjimkkV7)6pm4CAHO1<43J~s!Xq%*s>_hfVZ{UN;=4&GImvEn7o()knP#54Q@LC=xJ*'
            '$v4&6sK@CL-odp_mBulk{&V$TeFDk{R4=?2lcdtv_`|g=L@7>&b>w52*PkXm6ZvW<KY4vz`Zf<(k;)UP)k~Tn9Bfz=?fH*V=ZzXP'
            'Z+s+8*XF0RK%vN%AXh>NNuK3;Ht!x6P$iE6uMa_(lM_dPiN(WJX=&7P3K`s0o6`PDpC8Y}aBah+5E7W`E+wJEs@fGM@{k-'
            '?vi`%zu^gj4=x(I+z^$0L5WQc&;emT;z-'
            'lIDJ3d!bD0zmeFssIJ}@gratn;6^l+uwY*{n{shUA;@6ZM}32w_csF5#f^VGN{mCRA@zUxVb|`G+_CuNcJ?o3*5sU)Y0!Bg-'
            '^8NoHg5Eg8iXG2RGFsd;xf&jEa766x{1R<RJ)vCX7KRSxrrYUexya*9^TXAk3!L<eI>aiKohP5hH>>_&YC3{FO#)DQFBn?b~0!wD'
            'aq4wqCr{yYkA`)lavs-uU~)r?x+SYU}Fr@a6V*zukWQ?XBnD00Oo1x9d;<)?xdbSGI3nO_zcb7>P9+>0p{YpCHLe$%RfQ`lBP&`b'
            'VK6BegqUKD~A03ftp8M;vU!?&xAhlm6(@A1(Tz!yYF0{||ht)Bf?`o4`=OHq5)#IG2Jq%smU;DMt*z0@iyxql<8Yb%d>G=MbysW>'
            '}s4{_u?;ZPx~@)!O_ak^xAxfS)AGkOu+Er&u~_F1H+PmcXct=J&A5i_A`qKLVz?nTfGe?xwn#Q?qxES$}=KckTJ!GoS2y{QlPOt`'
            'uPzZhAT?uG%5!H^CqObW`|XmIL;fG(Ms&_dgACIG_+40!AfAY9vNAWi_clbf#ZrpVC^XVpCyu<ZG_N1dbOhhc4{BDpScCut4>&23'
            '<C?!c~rjXM56k3<;rf^seMM0NhH0^=s^NxASW2jZ3$0e$~7367qnbzq0lE=e^I~1de#?-Ag;ypH-KhoI$vNC5%T7x~Op8H7{)$EO'
            '%%hBc~EFLy=7lz!8jIfX<>(2ETzYVi8MCt&^!rxBrzDhJ80N(B&pS@~5fhEo)|07T$QvU_PU%y4g3iMk@&&jYK<hfcv!4WrbY3dt'
            'zl_1Md9x58F3i-TK|r49mCQyS8)fgB*TSTU>}oeJ=V;Fm9cOr-'
            '}Ejfp67RylX*xmRZetJx!;QzST90_RjUcZNGi9_s#3JuBf!x)83Vrw|@WO_SF}%uNy5;FIup-'
            '=c4d@_T`;FzPNM!sqJ^4%D!Oaj=j#ls|9V4*MjWh+c)3Z`Qkqc$AQH3#T$3tzS4W{tL!_}GK1bWS_ZH}FE{1AJ2*$owzK!yTfM8F'
            'utfoi$EJX!kA?@Nj}2t!+IM%}yvBy}{jC>!fBQ@CsjFL`{ej~m>*>6-'
            'Pw<^iZ5Arcmj%^PrggL6qG@iVf#WV3R1`OQbE1Ni*5+ylPI#XbgjcI3)&IcNMJvrUAl8V<2FEHd34<8)Bq`R)x>B*C`%UF*poYrO'
            'p~6uqI$}|f3Fp-elIWdtje^bGt?ayBOdl%gNBcHl6#9rJH2@^db(u@oU34xQ_#vI6+t_Yh=iAbH&@|!Le`X7~*q}e{b7Jp;y<5+J'
            'e)~WE+`Ig5a6~F1O-T%{4=AW?ISxs}d!{5;b}0f6;t;pgXUI&UQ;L3qutWXbOLzY87El^(4$r*-'
            'oLBG0WzGkD{Y>wr*V8GX1QAL+W@B)z2d&icZa~5ZUG04J%+7b07~#JC^}hpY%g{3BG$gDusF_V21n_-3=c@o^%9gamE5-'
            '4oN}DXxcj6OL8y*}w1xu?CIqt_~0Fm8Ro~<Wad6+*OVZc#sT~l<7#;$%KWJ2><Xv{Q^EZJR7qxbUfdmq2RgbveWxVs(GnWj@xh9m'
            'e|DYK<2P?eeE<8`&eg+qtX{Ab&i03r>EV($&Yf+8Te>UR!|PlR#HNAD)&Cx@8<Ne&?O81t9b1%NQ05CTW(KZfAAu_@f&0C0s947p'
            'i!_*s^PR4A&9Nc7#-Aylq(TGP7M8o~Wm#!kdCEuldLtMdTV(flMc^TL-fAbdkp*b_kBx%5)+gO`xN7$7s#(LDRWrIG9Bn3p7N1Bc'
            '{+4C=ra!F#vC0gko}se~ilJ{b|yx^!{H-1LYCO%Sm6xk8|U60HtM>Il_|$Gdd{e&(4sIe)b3A{}#zRzr7U730wKCpy-qr;kLZs)A'
            'YaH5Zqv{4;$)hf<aPmh(p$)Ii+U4=lxHf#y-'
            'Azh&;Y#|3r_oj_d+;i33p5Y7?WxL7Po>C!LKGbmIb`_jIo;#Pr>%anG#7oX`}`IAx9Rn`~!;&VvC6=eKCs)T)aR7X?ra#Lqi&Uu;'
            'A9N|++zcZ|H#YwZ)h@kO(3CbBAlwK>u@mkay0Rr*_n*0l^A;eye$V$KPXn6O9VWuxLJHxiZymM}T0P38x%8227@dNiAIdXV7S8{|'
            'Etw$>%Y3+E7khfMp3?AOnqP78p*|a?fRROmdFh7CJa)H(1WVIfF@Y;&WrCsZ|Y8^T-@-GJtGwOIm-'
            'D(F^5Dsf)zA^$nbpJy(gQNoD2M%yhh{=H|lzvEcpU4wKKl(b#!dyK1TekL>tvvxui6BO4LV+CWT7Zp!7HbJO^u#(Jfp=pUf~~-'
            '@U<D(8>Oi2H2?l17x*L4MxpQ})$Q%XJKmpJMhX(N2VoIs9I;I@rNtH(i?=paeK3vqw`KS(V8yt4oqty@tdGOhwSl#>lM(_I9g?+3'
            '6fJj@GG3;W{j&`2^OYfWiv-Qb)V6X=*X7BQwTd!T;dhw~WQ$}f#0iuP>>5&*NSIv|pg$WHDG-'
            'i%BP*qV|0btfY#AmeE9YehbMFF<RrqjG=?sxw5R`13~sJs2@ueWc0xbxjx$P7OBY>o$nc!B_ZUl8-O-'
            'T;|s6tW}&tk2(N%MJ}?3Uh?RgPj3jGd#~(M%v-'
            'BXdsE6P>fmzCm?D!>jT41$o1SfD%vRbTMlcCs6i#2Yf1M6N;=>#hiW2fQE!17(8|jtPzvT<9<kf}zAN?btrm<&mrBi}EUYZn9Svx'
            'mFz-'
            't!AP$^t9cQ>KS5oc=p?LZnmX3|rH8?tA1KPMUW!&sxAx6iD89FI8G_5T}P;&MIl*(OD2y+wBiil^BE*C6@h<%{?i^NbK6`8tvv-i'
            'OCkYb%_xkV7=eCprM%OP(Fw3re6lHz#OTKXmMajN&Y2#CdCM@D~n6e$;$)Gi&#1CxVk3fY;MFa*+cF^r})r4w~+lQtX|NXBS9-'
            'b$G9bXBUAGoVZ>S4CmS;Xg8a2zqCT#e~t+qZk$;sU8miKJ_wu;i~*I^D^!x9dMmIm#wK0JTVCmo&LLtk8A>+0J$JJ9W^ir3So}|-'
            'FOpxBFqO>6v%6>$fC;M=JBoAEXGtcC@fw34cNq(sJ;EpHQ-'
            '0H)?>p47=VK`uj(GjVY!)Rz>hs@cEjA(do)@f;LB(0=a^8Bik8*El=d{!txw<UrxhywER7iV_*Xz<ApWrlrvaJ5VC_F2t^fHD7<o'
            'XBy6U1xW5$Vzxr}||pA@0dRwm#q=brmRG5l_@d>~B!(XstU#CRjt4~qHtZym!I`yju;1Nldz2TYF;f=M8C^;o0%@8<iIj@L(twty'
            'KB{|d2S!^RNY%Ge49|BPyJ!uF<KMctul19<s*kXqzN3vJY?izJx5%s6y#*mUG&sIrH|Qnf~_%b$^V)M69#ftWF%nVO8!JJ)aaF2B'
            'L{R5d%~&D7j^LndtSNxEz_;PV`ZSSMyZjFJ*a;hJO^V>uIm$9X8AAW_^B#=utM@dv6n)CSjlu6X0!_~Mbz=vOOV7bD<RAYvzKb+L'
            '-l10xgDkIy|kbsAl=g#{=rF|WQQm2W3@L}#dbbXv@xGzr`AOLl|aDdIb+C~RZfC&wOtbY}9z!*l*aGZ1J$F*ECHJ@GkMLu!7E3Xd'
            '{QbQKpar9&z=$ams}l%537KH$+UyF$^qO2!R}=A~Vus9%g}kGg9%Y>P5Nxz!BEc)vbB#{Cun84wpeoRTrdd_P4rWhu47*AO~=2*+'
            '<WT0uPl9LyXUHgs|>0zm_1YMduv=@QVwv&w;Iqo<%Ba3s#>0Z>X(NPLKmJh56CKg}E26q9QN-DXOR_#B;dsYdyPXqN1&@LXey278'
            '5$W1Ws#OI=j9O}rmSsDn^AZ&xbyD8UV?EMYixWjPEe)l78^(#ot67LCI~#~2P?w--(Hkhuu)Zamh3gG!@j*r?iTU_DsD_-Ukk7@p'
            '3f@^J)JWi+mlb}0RDAWX3>MKXdnpR|j<uN+fA4}m_{%NcwgjA&@hkWmXY25DX&56Wd^8Qz`#5FAJ_zY)+|2wP{9*NHIzvEebPBZ0'
            'N7+TG4_<w%ChA{v-'
            'f?Kp(FV5qy^Cwe8Cm?z4`WO{)tld?z!l8{^okL^0~N%!P6NJQN;DJJZ#FE8(W{9NztPkNW0?R{_wq62om_)zCiG{EWuTmym9fJf0'
            'F1HN*-_wS!512&vP;DgYS{B*rl>*6vx^i)IL)Wri6Y%H;aSC9ya(rZuzYBM+&tuU5y30$jUbZiqGF~p0-'
            'faPe`k1@Maf_ot}u>1*P2zKl7-'
            '+7b;A51Yq;##SghcW>vR?yLu!u3QUTbG7eacCqRsn4GR5k}_@r2~DTi+B~$Xf`NH%ZH))zA1!(CL7>V=0wX<T0pR>zT+DAOiaJ;o'
            '(;algDunmYySfm(5$U9I5!(>8U@7vnoT+%K&lLsAu?{FZ8D4)cZm#JvfeV#1)}TeS!~-'
            'Fvj3pM50EI6P#U>8?nm|zq*n`rrXzO3gW1RHvtfe{9cLf9$IXk30M#`5ADEX_uoBaceXe`IsSnaS;{iMt$HBUX<fNdVu|~t$=V<}'
            '*pdeU58}^F+cwa_7^Abo91eTT+oGF%ue#b;E24|lP)ZXV>Klw>f0THmBnFy!La<!m=bXM>K(l{-'
            'tDZwx&*boR3uy1mj;>$!Mq~8(n3o-'
            'i6Dm`t&R;l)6Cbk?pjJdTkMq!rdX0Os5%XlZ*0WVo^*8HFySu$xK{7&DObj3*KtwUM{g=Z`2(Yh=vPjz=@&&?<`)<=z!H!u#U>Sx'
            'u_iXnJnXaD|Px#hetZ|q0u%Of0h?EU+P_5(j>CZDdc1)dv1G=xLNM^15RZv|Ym9p;XWn2aO_xXF5Jjc3e2uAPzt=}=*Au`d-'
            'dS3w9OU)U8!mhd<)XuOY;xK36LtPOUPPi~PlKbUqy^%LK<q5u+ubNN4$I3Lu0)dfb!v`d4;0n7kjn0on(>X20uom!14vM9aP`PHy'
            'VM{yJ@?3C(6<_{bTpdk^5A%mhRZG3>eAmda1KriB!3!^H^R<>KE>muhpy$fasV}c}VT4|u#unh^SGOFo=?hl+p4ysK=Uzwsh-'
            'vZ;GVciR4gmk{By^)bncLn-so8lA``UpOCB9dbMqdL^H@R(6c$uWoN`2f-'
            'tbr*i=lR33)ooPmp{h<TV2w|NbO{75}nB=S#2Qk^QS<|2cTDGy@$_9})?y@+1xW0+0UAd^hq!cy`13YM(P6w&%$pdz(>DU*RY&uJ'
            's(5!C+Rp?`|$(<xQ9qgcbSj?3fE<+$u3~yv|yA-B2^Udz2tIas78X7I9<qc+SaoF8AoH1wPYB`E-'
            '+AUxiK)=ppi~?%~FI2%oJSi3KYeXEheZQ^7Pnc53q=?1*3-'
            'QneH4?=}m{Xxrzv|eGc9Lv++_8OdlZobd|Cjf`QGMsT*Lv^#j`^gREhQjwhmf7Ot|f<4{XuH0-'
            'R4=Aiis~KhQWgKC1yKw3kD||1xE>VC8ajZJOW9PyfpWdSMt%Cn;#@XPqmBmKKQuz`DN8QVrr2gq6h3LaDavp^Y_b*ZnBzz22f2eB'
            'ctqyGU%DqQW;RfXy%GT=r5@OL3Nb6tf^isRGb5Y;#bSzV=$w+=9d2Fo4wz?aQo|*d#}FKyYX7@{m-'
            '}FdKsLQZhw7o=h7GXmB~1s?bm(IwB2Hvf%iV7-'
            'mfojfAMaS5lb5k^^FHdX7LqYr@nrMxyJION4WV)nw9hSO}S9!dsYP}OQOK&V7bA<Q`H<eUK*9k(_n1c`PNj2;gnvc56gWryctCru'
            '0tE-OxxH8@n*}*`?!&qxi66yAn0iJVFKlS%&@W#(@F2!v`a=5&QxTXmy4(aFPsGDLWd2tY%!p&+H;e~j{{XkMh%0dfhL0rI5=-'
            'WTC=Ct?mb|x=>cU5*-'
            '%yz$>B5gLCDMkA655vIyL!IkG`zuJw#Xwn$n3!x)*UUsvfGW;g~6Gmhy=S&1yapFNGSf+e9;ovlb;NQ~0g3nVhW#oL=Tgz5VH@mI'
            '`5;7Mw=6zkXron{ObnfxAJPmCVL{NSUUhL1mdrfj%q*q?obH^O0mQ#b1kB+8~LKECc~g#Cc_cbVM?ZRWnm`5ovZltU@ouqbddul|'
            'WD0YcFoS{)IVCf=|m^I}6%$9>61P2;l`7jJ}-&#`&ujV2~GtO|ZHK&JstAV|SS{2r7>1Aq^s)1Ydb;LEGVMBID-!N&t-Im-'
            '_<(PPS7$(2mydo~m(am5dFvWuT@;x(zxkb=O$o!2^;RIPbC#QpSU}^-'
            'MJNWfr;XqzR9KGy&KzQ9j_DF0Y0fT9&q>D9t>aEK82<+gu|nV}@l0GRw2Icx2wD;%U8?PQ+mQ^pm#7zs--'
            '1909IcEl8ou1OYNUgBQ-Fk?^{0N-'
            'IqcOXghprnxNJ{s#ZGX=_P>*h8@~n4FY02G42E!=<KIMk2~q|NTm(P>jAwldS05tt?(i3ru5)7|*W)cv^^_YDR6IUkj2Ur;%uI#E'
            '!6IdD*rck;dP(jrlpUGa_za1IM|!!I=^dFZal%G^i@MGmujF$ngNJ_cqe!_-'
            'GTkoC?1Vrvhgtcol^GY@S4RSSN}!Y|0>;Bw0Piaaf`Wq-'
            '4oNUV|ZG`_#;qMkg*UF9;FFoG`=3x7%sBr*4aqRIwOLADD~;b$1*Xfh>|V5(^_xSp>@{HX$XlH%-'
            'pSbpCiz3y7Xza{yH#*NGep(V|_SC2hhKZ}nJ2<|8;~#go&pt@1m~j{PeA*F}qDR4U{rFM|Qta4?!dJBfT=j=synLY(>O0l)-'
            'tn}=*H^SqQ%@UtDkI7)x15j4;8eZnTIYL~3Fs?u{du$O6cph?4?II3$#1KkV37Ye(_drm-yGjuFO$DI>kS`*ivq)*jLP;yThV=kY'
            'v8&c-'
            'e?bLGiD7%bIJ!>%o;y60e2FPvTIsY9Rmg{v|Tv?!13>xj#AX9M#mB{2&<Je=ynt7hzG=M>R)RT`Z8{(nniZaY9O`G=)&LzZRXG7~'
            'J#T~~U!Wb_gZTiE<*f%?){nE<Jc9%M)y2StYt@$VdAk|Y4mqBR1Y7Y~T=IU|S?Nf0amuVK^Gc#BPa{JYPDC#8BVGIm9=$BAOnH|C'
            'rrS_)gt)p&fp;*HT4Tx>o3Mn)wef24BgowL>io1i1yMT_nf{?+XM5AT9wX!Ez$-'
            'qk%d*}64JryKpZFeyx@tE1oXD6+r?eQ{Ri{i^*+6-xcTTaYvXq2O<4WT6-'
            '_;65*r@*SKH|$?6G&j=2X%mt(3^O^MA5H8@ZEc}BByBC$vDQNK=L=04Hf#q;Es7MrE<cRIxo5^%G<zJ9zAZD{=$^2x$#N?FNUy}F'
            'QA4#1Z1Oo{S-Fb}=xp{I;y9ZdAEB}oS+-B(40aE~qv&IwhiT&(%!LnXhQ~$o&{X!L9jv2RJ!&x`rHPTCOk-jMaQ@iV=ECp>1BMG5'
            '90nGK&0C#%!cb^=vKkyXe4oP`yjS$9$CUFau(i}Cf-;t(b&&%!2UnYPZKO>#sLhQU;vdAS{uu14vU2(Yq{Atz>h-dwT`y-'
            'jnKYFn7Y&M5l{336p}tI}pf58?2J-gH`tl5!$M|LkEE-upc9<tV=2a{yd@w7>R4wyqmy2mkKX)yeSCM#eKE+G?o?_l2a({wc2<=p'
            'c$#3%2n-'
            '|B}qFdIU@)K&2Yaukw8K)u2DTfg+%XnO1uhr8C*krm@P~o6Q<sE}613fCP8k|@9TucX{a=45@OMQ$uc@Qo$08NLEs5&nS>I;=^QJ'
            'D*4*HstqrHCm;5T*ij%X18|-(}9w$orN;5N{#zEpRpT!p-vEtXYtv@ir00^s)OKK$JQ-D!&1#IJoGV>+&2#O2--bhYvb&L=}xR<w'
            '<2(2c9x(MIaF!P@1&uh?~8{jjl`+To&f}lwfJz&EtRt9hM=O>Gi<_M>J~*$HEGY&H{N-'
            '=9_3iX&eNqYK1cnw;eK_?Vt)=03cp3uf$*!ETb>s>MeH{n%jp=l=17Mbj0U<D1;GJ(-'
            '!fEOjWeeA~SqD0xHcNDmb=NlZ^7P=4EaYk&`2z%nVf?N**)a@lj;SAibW%uf(8>Qcjn&Mv-Z@uQgI1umJ4c6g-'
            '^VXAQ<hJ|m2a%FKf?UCeyV3g{z~tXCiVwJ2k@U+YIgYQpA`r}!pk#74cmdQ?bdeY!~QUd+aXMl3-'
            'dO9g5QvJkt^ObL!g3P_3k1Sp}^QI(ZFqbNDx7a5j~n#`TS65PKDo6l{$YY@5se%}|^L5`^|j2b3P1PFJO4paJ;q9(*3D+TH(*~nh'
            'qLTKSw@|WU;Qw{+gbJ8<_CpFA%bOB=`p`^?jru{eZg$my786J9HzSw)_L*`3RJh_}28o-'
            '`(yUG|<>X^?to|`nZKpD|7?|v?jp)i{Fn^$|!zr?a@ZU6P=_RZe|2g%q+<^lov@G*7FN6&7*^G5ITE4{COod<8|IVKN;qS5C>3r'
            '--imh3@ItX#eCcUp8_qJJ)zM^f{G(JK$mw`1Jk$8vJ<1YRPMHM?2{k5GD(K=M>+E$6rF!XC?Gl7)1O(J%`l`kCQ?G$WUm!O^%6&p'
            'mtl#-'
            'Csxw%&X0_Sc^=kE!0}>u@yz?11LgNEhQ2sG?;8?rM>5Z`K7?kHWeuhvaNPmpW>e5*ZT;QkK#jVq~rF={^q1eJI&y(Bf5OM^kLL+z'
            'N*0N7l)PpElC=q%@x4C)78)*`Lggn0UZ>a{}^@$tX)E)K>Y$^}<eFvGII}tLcpB#FLmay1PS8B%)z<^;9UcY<|k=sz)&n7Vg(4<W'
            'IYHg?najH>}<KGx|=kkg3+P6#YYHLx;fjYro%m?h4+8up6K&l7k9LJRr;|pr5<g14WDukKDzZ3U$eQEvT(V<Ry&PDx))!#~*<d2R'
            'T8=z>PL>@H}h+kl6aYS+({ChMVJcm>6V-'
            'S7$)|U$){+!}F*K&nxsobOt|pcbm3I%a@BXX1724868bZ%lT+n@OxU;P1lagFBnL#V<qd$Mpi~!qs&-'
            '}^9vXU)P__ZOln9Y`2CqPr{^Y5fm7nt<mowxQ%45@d6fmLkotnCVcxJ*;D{;`YKo%BDAL`5PBviK)$j9?&Ty<9kKG|8u8)zAp=;p'
            '&S`CaeVlk4o=h;FxrPt2L+KN$MNm(GOxET;GxO@YbRs?6VHqv@@m#r+z4*-*2oaxdGo>W6grNB4SP9xapfTV1GG(SgqV!UuLP5Q-'
            'C{e^f1dIvq;ILPz(Ufzi6%3ZDMZZEQ~$Q3Sbv!NT|SZn?4)wjR>ZtKd8?dPAn{q1jezI=nHMSbT6<YU?X%eQdX1iXSPSaM!KnG3E'
            'x9?{OcY3vGJBg=Z{>m-N^<Sk&aiWJW#!gow5nPjRCQ$#}Q-j=SWlG;Ol#nj5XqG54P0>0KP+W-'
            'zz&pVQ)ccvR<So;zjb+KKYI1}7a2SJHV@#Y}Bol{>Mq(aqsEoaDLMvkD(2E0)#rp-'
            '}g0IK!5V^ZcS$Lx;fvYBCS()_6})?yyt;|ge<i%nN^izuMXa$PIGBPE23UG(c1ZhPik(v12e9J*F9d2E+rBXG+vgUqFF)To2t*7k'
            'WO2&cUcDy^n;l2XEA%Ie@%)fz&B2`0rFloXW(Z(m8R0=H-CIaSj99`LTh7qvnOBGf!4l?of2&Dc-wu?x9o)lstYivy%n1J(sJDL{'
            '4QafXRgG)25jeMW*ldU+iI(cKjY*je49vQOFssV-'
            '9q1@|u5f*FU55sbkgn!eTovWC%o4mz3gu^7VmnR;(6IaiC*M4Bc~v_j5L8Xv>6&aitwZ_C5=04kMLDwW0ilaKhPA38by2s-'
            ')Q&u{uQFo#CjTX-'
            '~QC;DJjuEXF8lI_o)?|u6WqwYK3UD<i>#qF1`_x|u}kj8i3f9B3>PeFXb)|+3MLq})`!19J|XV@F*qivvEV5Pn;=RbTQ&z$B9Y35'
            'ydO(FYpiN2X&))o%FPBst39+S}sR$@R{P7_Xv%ui?Ljvt|XO!kPKFY==#aQXrHtb`Z1@kAb<It96qW+r}q22$wZ{W-'
            'JgLG0@HP;1$&#9i;}ETvTj2>4UT7LcG9)o@v_ZOkpvj?oNe-'
            '}&ebNDIec7#x$gK6@YX>a%1tTqmG__y4{45&Yj~iIl6@ZPEdaXsoz~7g0H}*^=1@tFm~;Byvul33gT2&L6M^d<pMr3wQ_yiAXF_d'
            '&Zn?qoV^Q2F$l84_nuqK^>f%?^`r>1vAn_6Pv$CP!3YYV@i&yw2?CHc%#_B>!7sYny5B6<mUI%%WNhUt!#9=aK#_~Ipom%4Y5Fd5'
            '-bdsU`mVV&oLXOtZOV*0H_Rw9Q4~ggL6^86jn;ws(h-dUD8t(rK&1UPi2no8YDB--'
            'hhG@%iUXGC6{-Uq*mYG`i;Ct6V6DCfM9YENkE`J<?%o_p9Up&am=L(<9p+U`m}@@Kb3Y<-C^OJfqE&(xH%A{7w;9R=9#>}AyY-fy'
            '=B6nqXP{@W*>Du@fqxT!;9D8td~8*?Q0ki$$>S$d|b!jqq<R}RInsQJqj3bbBp73*4lPqv&<yP6ey*B03g&DU}BI5fER!!v6Vy@k'
            'lo25VV|f-We?P`ly_4Txp#9=-'
            'R&VYFzRtd1R)p0xUF~J1GVSY)j!_3_!|hN)h>1zkoOpj?@*btGczasiO1$<#vps}LsL_8a9i)#^z_6r$;EN44~5(KaL|I_O17G!8'
            '@SWZoj9a;qu5?paE?~z7Z(2aet%<gVSZuJasS)B3l;C4Cx3FZy695;e%Vr7M)VLL5plH7E8jnQ&r#rsU}?U;^$slJ_qU$<{?_l|e'
            'zyhN{r(o*ru)j@FTSuZYwpqwOolP1x6@D>1eQL<3c4V*#t~jCHFAVmxY&)Xux3mhP0K+?jCw&$<`NNnP1}&auvXkj!tTRjx&aUkn'
            'sp#1ux^z3?C9vw(EPtHBo92euxOn6;=MLI=70%o1dw77+JLJdrywEp*zAOBzV0`_pD=(vf)6D+scTnC%k&RfL#yeg?xFx5)~>h(U'
            '1-qtE6{lvdE0sVNL+Egdp{1Zq2GTkb@no-'
            '4P)A{cfR3pjcnWArFC(sCT?A~(V(BOc|!y%L(W3|UU%rIT~5ag3UG}l#tO#lGRtfc005NX@OC%UOC?8KJvPo3Xbb-Z-'
            'A2dHMvpngHUU^75+s4qJtnix;xB;u$^^qG`pvilNg$H20bz11XCSn_BqK_B+j(T{GrJMkhN=L9f)W{hw9k}G{=tzEN9cjGfmH^Ts'
            '&cnF%j=zT9tb0j*<Mq&%=Q{duSH`ISPtBYJ~Fb)332D@#hs6yvZiSY)<JJ%#6p|zJ72&hG^#?HtCr!`5(iXY=Q8>@!}R0@T=Mc~s'
            '7K$uv3P|N+wnV~!HP!4APUx(T5{EPzIFKuW(s=y6I;Dcnxd!z-j)LzIs}9Y0s_E%P-'
            'E?}ln#*go@Ll=w5v9kVn4dMedD{GOMl#Y|6;#pk-kCICgo7IkIGiG@qrDL!g*Dvfb<B(1ych|nAN6I!G_3llU6i)%{2+-'
            'K9<Rc`?F*#JV&u8PZ^=`8SRkTJILk&NAkCYk^7B`LlhV~Qc|Tno5KfZ7v8@Jw>sN-ZJ-Gw+)`F#wE3bbt%x+gxjTGm@G`%;s;N$o'
            'Ia!9Cb@?l7qb86b2k*?@`Sw+C^~r9XvT1O<8AB9y_Zunl9oeJ*2=@e+G7!5nF6%;~EvL%lrOTPs&*kf>ejad|^OPzdJiUG8S;+Fj'
            'T;<r6-zjL4q6itgj6)CQWh$omu3G@YMxPdg9bf5~QdAVEoz%PSv}70)Q^$Fx3z-'
            '%}Ps*xj6=vnvY?4+s3W|P)v2LbL0)q^vR6;}}S<?6EjPZS>r@qh6c?Ko3>lj)MKDXeCjMUb3OaBicv~%_'
        ),
    },
}

ENV_DENO_VERSION = "v2.9.6"
ENV_DENO_FILENAME = "deno.exe"
ENV_BROWSER_EDGE_FIRST = True


def _configure_utf8_console():
    for stream_name in ("stdin", "stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8", errors="replace")


def _require_python_311(version=None):
    current = version or (sys.version_info.major, sys.version_info.minor)
    if current < (3, 11):
        raise RuntimeError("需要 Python 3.11 或更高版本。")


def video_output_directory(home=None):
    root = Path.home() if home is None else Path(home)
    return root / "Downloads" / "URL-Extract" / "视频"


def comic_output_directory(home=None):
    root = Path.home() if home is None else Path(home)
    return root / "Downloads" / "URL-Extract" / "漫画"


def core_cache_root(home=None):
    root = Path.home() if home is None else Path(home)
    return root / ".url-extract" / "core"


def _core_spec(name):
    try:
        return CORE_SPECS[name]
    except KeyError as error:
        raise RuntimeError("未知的内嵌核心。") from error


def decode_core_source(name):
    spec = _core_spec(name)
    try:
        compressed = base64.b85decode(spec["payload"].encode("ascii"))
        source = zlib.decompress(compressed)
    except Exception as error:
        raise RuntimeError("内嵌核心载荷损坏，无法解码。") from error
    actual = hashlib.sha256(source).hexdigest()
    if actual != spec["sha256"]:
        raise RuntimeError("内嵌核心完整性校验失败。")
    return source


def _combined_version():
    values = "\n".join(
        "%s:%s" % (name, CORE_SPECS[name]["sha256"])
        for name in sorted(CORE_SPECS)
    )
    return hashlib.sha256(values.encode("ascii")).hexdigest()[:20]


def _file_sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def materialize_core(name, cache_root=None):
    spec = _core_spec(name)
    source = decode_core_source(name)
    root = core_cache_root() if cache_root is None else Path(cache_root)
    version_directory = root / _combined_version()
    version_directory.mkdir(parents=True, exist_ok=True)
    target = version_directory / spec["filename"]
    if target.is_file() and _file_sha256(target) == spec["sha256"]:
        return target.resolve()

    temporary_name = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            prefix=".%s." % spec["filename"],
            suffix=".tmp",
            dir=version_directory,
            delete=False,
        ) as stream:
            temporary_name = stream.name
            stream.write(source)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, target)
        temporary_name = None
    finally:
        if temporary_name is not None:
            Path(temporary_name).unlink(missing_ok=True)
    if _file_sha256(target) != spec["sha256"]:
        target.unlink(missing_ok=True)
        raise RuntimeError("缓存核心完整性校验失败。")
    return target.resolve()


def load_core(name, cache_root=None):
    path = materialize_core(name, cache_root=cache_root)
    path_tag = hashlib.sha256(str(path).encode("utf-8")).hexdigest()[:12]
    module_name = "_url_extract_final_%s_%s_%s" % (
        name,
        _core_spec(name)["sha256"][:12],
        path_tag,
    )
    existing = sys.modules.get(module_name)
    if existing is not None:
        return existing
    module_spec = importlib.util.spec_from_file_location(module_name, path)
    if module_spec is None or module_spec.loader is None:
        raise RuntimeError("无法加载内嵌核心。")
    module = importlib.util.module_from_spec(module_spec)
    sys.modules[module_name] = module
    try:
        module_spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(module_name, None)
        raise
    return module


def classify_text(text, *, video_core, comic_core):
    comic_url = comic_core.extract_comic_url(text)
    if comic_url:
        return "comic", comic_url
    video_url = video_core.extract_supported_url(text)
    if video_url:
        return "video", video_url
    raise RuntimeError(
        "分享文案中没有受支持的链接。支持 B站、抖音、YouTube、X、"
        "Pornhub、MissAV、51吃瓜及 18comic 作品链接。"
    )


def run_from_text(
    text,
    *,
    video_core=None,
    comic_core=None,
    home=None,
    cache_root=None,
    environment_preparer=None,
    video_quality="highest",
):
    if not isinstance(text, str) or not text.strip():
        raise RuntimeError("未输入视频或漫画链接或分享文案。")
    video = video_core if video_core is not None else load_core("video", cache_root)
    comic = comic_core if comic_core is not None else load_core("comic", cache_root)
    kind, url = classify_text(text, video_core=video, comic_core=comic)
    prepare = ensure_complete_environment if environment_preparer is None else environment_preparer
    environment_changed = bool(prepare(video, comic))
    if environment_changed:
        print(
            "首次运行环境已准备完成，请重新运行程序并再次输入链接。",
            file=sys.stderr,
            flush=True,
        )
        return None
    if kind == "comic":
        print("正在提取最高画质漫画并生成 PDF，请勿关闭程序。", file=sys.stderr, flush=True)
        return Path(comic.extract_to_pdf(url, comic_output_directory(home))).resolve()
    if video_quality not in {"highest", "ai_readable"}:
        raise RuntimeError("视频质量配置无效。")
    message = (
        "正在解析并下载 AI 可读最低码率视频，请勿关闭程序。"
        if video_quality == "ai_readable"
        else "正在解析并下载最高码率视频，请勿关闭程序。"
    )
    print(message, file=sys.stderr, flush=True)
    return Path(
        video.download_video(
            url,
            video_output_directory(home),
            media_quality=video_quality,
        )
    ).resolve()


def _diagnostic_message(error):
    message = str(error).strip() or error.__class__.__name__
    return message.replace("\r", " ").replace("\n", " ")[:240]


def _runtime_packages(core):
    runtime = core.runtime_directory(Path(core.__file__))
    packages = core.runtime_packages_directory(runtime)
    if packages.is_dir() and str(packages) not in sys.path:
        sys.path.insert(0, str(packages))
    return runtime, packages


def _dependency_check(core, requirements_name):
    _, packages = _runtime_packages(core)
    requirements = getattr(core, requirements_name)
    missing = core.missing_distributions(requirements, packages)
    if missing:
        return "失败", "缺少：" + "、".join(missing)
    return "正常", "已安装固定版本组件"


def _deno_check(video):
    runtime, _ = _runtime_packages(video)
    executable = runtime / "deno" / "versions" / ENV_DENO_VERSION / ENV_DENO_FILENAME
    if not executable.is_file():
        return "失败", "尚未安装"
    validated = video._validate_deno(executable)
    return "正常", str(validated)


def _ffmpeg_check(video):
    ffmpeg, ffprobe = video.find_ffmpeg_pair()
    return "正常", f"{ffmpeg}；{ffprobe}"


def _browser_check(video):
    runtime, _ = _runtime_packages(video)
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(runtime / "playwright-browsers")
    from playwright.sync_api import sync_playwright

    attempts = (
        ({"channel": "msedge", "headless": True}, {"headless": True})
        if ENV_BROWSER_EDGE_FIRST
        else ({"headless": True},)
    )
    with sync_playwright() as playwright:
        last_error = None
        for options in attempts:
            try:
                browser = playwright.chromium.launch(**options)
                try:
                    return "正常", "浏览器可启动"
                finally:
                    browser.close()
            except Exception as error:
                last_error = error
    raise RuntimeError("浏览器不可启动。") from last_error


def _network_check():
    targets = (
        ("GitHub", "https://github.com/"),
        ("PyPI", "https://pypi.org/simple/"),
        ("X", "https://x.com/robots.txt"),
    )
    failures = []
    for label, url in targets:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "URL-Extract environment check", "Range": "bytes=0-0"},
        )
        try:
            with urllib.request.urlopen(request, timeout=6) as response:
                if getattr(response, "status", 200) >= 500:
                    failures.append(label)
        except (OSError, urllib.error.URLError):
            failures.append(label)
    if failures:
        return "警告", "无法访问：" + "、".join(failures)
    return "正常", "GitHub、PyPI、X 可访问"


def _merged_requirements(video, comic):
    merged = {}
    for requirement in (*video.VIDEO_REQUIREMENTS.values(), *comic.COMIC_REQUIREMENTS.values()):
        name, separator, version = requirement.partition("==")
        if not separator or not name or not version:
            raise RuntimeError("依赖版本配置无效。")
        key = name.casefold().replace("_", "-")
        previous = merged.get(key)
        if previous is not None and previous != requirement:
            raise RuntimeError(f"依赖版本冲突：{name}")
        merged[key] = requirement
    return merged


def ensure_combined_python_dependencies(video, comic, *, run_command=None):
    runtime = video.runtime_directory(Path(video.__file__))
    runtime.mkdir(parents=True, exist_ok=True)
    required = _merged_requirements(video, comic)
    packages = video.runtime_packages_directory(runtime)
    missing = video.missing_distributions(required, packages)
    if not missing:
        if str(packages) not in sys.path:
            sys.path.insert(0, str(packages))
        return packages.resolve(), False

    print("首次运行，正在安装缺失的完整依赖……", file=sys.stderr, flush=True)
    runner = subprocess.run if run_command is None else run_command
    lock_path = runtime.parent / f"{runtime.name}.combined-install.lock"
    with video._exclusive_runtime_lock(lock_path):
        packages = video.runtime_packages_directory(runtime)
        missing = video.missing_distributions(required, packages)
        if not missing:
            if str(packages) not in sys.path:
                sys.path.insert(0, str(packages))
            return packages.resolve(), False

        stage = runtime.parent / f".{runtime.name}.combined-stage-{uuid.uuid4().hex}"
        try:
            if packages.is_dir():
                shutil.copytree(packages, stage)
            else:
                stage.mkdir(parents=True)
            completed = runner(
                video.build_pip_command(Path(sys.executable), stage, missing),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
                shell=False,
            )
            if completed.returncode != 0:
                detail = (completed.stderr or completed.stdout or "").strip()
                raise RuntimeError("缺失依赖安装失败。" + (f" {detail[-500:]}" if detail else ""))
            remaining = video.missing_distributions(required, stage)
            if remaining:
                raise RuntimeError("依赖安装后校验失败：" + "、".join(remaining))
            version_key = hashlib.sha256(
                "\n".join(required.values()).encode("utf-8")
            ).hexdigest()[:16]
            versions = runtime / "versions"
            versions.mkdir(parents=True, exist_ok=True)
            published = versions / f"combined-{version_key}-{uuid.uuid4().hex}"
            os.replace(stage, published)
            pointer_name = getattr(video, "_RUNTIME_POINTER_NAME", "current.txt")
            pointer_temp = runtime / f"{pointer_name}.{uuid.uuid4().hex}.tmp"
            pointer_temp.write_text(published.relative_to(runtime).as_posix(), encoding="utf-8")
            os.replace(pointer_temp, runtime / pointer_name)
            packages = published
        finally:
            if stage.exists():
                shutil.rmtree(stage, ignore_errors=True)
    if str(packages) not in sys.path:
        sys.path.insert(0, str(packages))
    return packages.resolve(), True


def _ensure_browser_runtime(video):
    runtime, _ = _runtime_packages(video)
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(runtime / "playwright-browsers")
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        browser = video._launch_public_browser(playwright)
        try:
            return "浏览器可启动"
        finally:
            browser.close()


def ensure_complete_environment(video, comic):
    print("正在检查并补齐完整运行环境……", file=sys.stderr, flush=True)
    try:
        packages, environment_changed = ensure_combined_python_dependencies(video, comic)
    except Exception as error:
        raise RuntimeError(
            "Python 依赖准备失败：" + _diagnostic_message(error)
            + " 请检查网络代理后重新运行。"
        ) from error
    try:
        deno_status, _ = _deno_check(video)
    except Exception:
        deno_status = "失败"
    environment_changed = environment_changed or deno_status != "正常"
    try:
        deno = video.ensure_deno()
    except Exception as error:
        raise RuntimeError(
            "Deno 准备失败：" + _diagnostic_message(error)
            + " 请检查网络代理后重新运行。"
        ) from error
    try:
        ffmpeg_status, _ = _ffmpeg_check(video)
    except Exception:
        ffmpeg_status = "失败"
    environment_changed = environment_changed or ffmpeg_status != "正常"
    try:
        ffmpeg, ffprobe = video.ensure_ffmpeg()
    except Exception as error:
        raise RuntimeError(
            "FFmpeg 准备失败：" + _diagnostic_message(error)
            + " 请检查网络代理后重新运行。"
        ) from error
    try:
        browser_status, _ = _browser_check(video)
    except Exception:
        browser_status = "失败"
    environment_changed = environment_changed or browser_status != "正常"
    try:
        _ensure_browser_runtime(video)
    except Exception as error:
        raise RuntimeError(
            "Chromium 准备失败：" + _diagnostic_message(error)
            + " 请检查网络代理后重新运行。"
        ) from error
    print(f"依赖路径：{packages}", file=sys.stderr, flush=True)
    print(f"Deno 路径：{deno}", file=sys.stderr, flush=True)
    print(f"FFmpeg 路径：{ffmpeg}；{ffprobe}", file=sys.stderr, flush=True)
    return environment_changed


def environment_is_ready(checks):
    return all(status != "失败" for _, status, _ in checks)


def collect_environment_checks(*, video_core=None, comic_core=None, browser_probe=None, network_probe=None):
    checks = []
    try:
        _require_python_311()
        checks.append(("Python", "正常", f"{platform.python_version()} {platform.machine()}"))
    except Exception as error:
        checks.append(("Python", "失败", _diagnostic_message(error)))

    video = video_core
    comic = comic_core
    try:
        video = video if video is not None else load_core("video")
        comic = comic if comic is not None else load_core("comic")
        checks.append(("内嵌核心", "正常", "视频与漫画核心校验通过"))
    except Exception as error:
        checks.append(("内嵌核心", "失败", _diagnostic_message(error)))

    if video is not None and comic is not None:
        for label, operation in (
            ("视频依赖", lambda: _dependency_check(video, "VIDEO_REQUIREMENTS")),
            ("漫画依赖", lambda: _dependency_check(comic, "COMIC_REQUIREMENTS")),
            ("Deno", lambda: _deno_check(video)),
            ("FFmpeg", lambda: _ffmpeg_check(video)),
            ("Chromium", lambda: (browser_probe or _browser_check)(video)),
        ):
            try:
                status, detail = operation()
            except Exception as error:
                status, detail = "失败", _diagnostic_message(error)
            checks.append((label, status, detail))
    else:
        for label in ("视频依赖", "漫画依赖", "Deno", "FFmpeg", "Chromium"):
            checks.append((label, "失败", "内嵌核心未加载"))

    try:
        status, detail = (network_probe or _network_check)()
    except Exception as error:
        status, detail = "警告", _diagnostic_message(error)
    checks.append(("网络", status, detail))
    return checks, environment_is_ready(checks)


def print_environment_report(checks, ready):
    for name, status, detail in checks:
        print(f"{name}：{status}（{detail}）")
    print("ENV_CHECK_READY" if ready else "ENV_CHECK_INCOMPLETE")


def _self_test():
    _require_python_311()
    video = load_core("video")
    comic = load_core("comic")
    video_route = classify_text(
        "https://www.bilibili.com/video/BV1test",
        video_core=video,
        comic_core=comic,
    )
    comic_route = classify_text(
        "https://18comic.vip/photo/1",
        video_core=video,
        comic_core=comic,
    )
    if video_route != ("video", "https://www.bilibili.com/video/BV1test"):
        raise RuntimeError("视频路由自检失败。")
    if comic_route != ("comic", "https://18comic.vip/photo/1"):
        raise RuntimeError("漫画路由自检失败。")
    if video_output_directory().parts[-2:] != ("URL-Extract", "视频"):
        raise RuntimeError("视频输出目录自检失败。")
    if comic_output_directory().parts[-2:] != ("URL-Extract", "漫画"):
        raise RuntimeError("漫画输出目录自检失败。")


def main(argv=None):
    _configure_utf8_console()
    parser = argparse.ArgumentParser(description="URL-Extract 视频与漫画最终单文件版")
    parser.add_argument("--self-test", action="store_true", help="运行离线单文件自检")
    parser.add_argument("--check-env", action="store_true", help="检查本机运行环境，不下载安装")
    parser.add_argument(
        "--quality",
        choices=("highest", "ai-readable"),
        default="highest",
        help="视频质量：独立运行默认最高码率；AI-readable 保留最高分辨率并降低码率",
    )
    parser.add_argument("text", nargs="?", help="链接或完整分享文案")
    args = parser.parse_args(argv)
    try:
        _require_python_311()
        if args.check_env:
            checks, ready = collect_environment_checks()
            print_environment_report(checks, ready)
            return 0 if ready else 2
        if args.self_test:
            _self_test()
            print("SELF_TEST_OK")
            return 0
        text = (
            args.text
            if isinstance(args.text, str)
            else input("请输入视频或漫画链接或完整分享文案：")
        )
        result = run_from_text(
            text,
            video_quality=args.quality.replace("-", "_"),
        )
        if result is not None:
            print(str(result))
        return 0
    except KeyboardInterrupt:
        print("任务已停止。", file=sys.stderr)
        return 130
    except (EOFError, OSError, RuntimeError, subprocess.SubprocessError) as error:
        message = str(error).strip() or "视频或漫画处理失败。"
        print(message, file=sys.stderr)
        return 2
    except Exception:
        print("视频或漫画处理失败。", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
