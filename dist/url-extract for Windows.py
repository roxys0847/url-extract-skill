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
        "sha256": 'dd8fa4485c56c8f2ce94b28921a7ed3020f503c809f95a48988263f92915e8a9',
        "payload": (
            'c-'
            'rlK>v|j4k>GzmMW<(Xgq8vDCebou*h@*2%`ruCNJ_RtF})zsAQ6E8f(CdA&Hd~oj^)IOlu7Kwv2$?}$KFhAc_xW(^5tDN0ww**D{'
            'NJr`{~mSP?EF$=G)9zY;>P%ojP^u)YbR>g=V``UaLpmcC8XMy$g%8UbNe3m)ASZwij<k^}3gfJLN{D+^%@_+FHBZ-'
            't*R)%}xx3T3)@p7qx?;@B2eT)pm2s3&U!+(``p#=+(Ab(70D_G@6}qr`Bx5Lqp<Sd!tou$C3EG-mKT7byh~cYII;E(4}~@S&lcgp'
            'X?93C~ifaa;4lUC%<$%wYq%UDpxA)D3(2ZBW^at^H#aDDW03MM5|uzRGaNB@w+Vt9B=AP$IbQ2QAhsjuC?0Db*-'
            'm(Pd;{{tyZ;Gmko6`+flhvYi!6DwJrIv+pgm*+R-'
            '<=QQWcKM(uX9E#Gx(74iJ78tZ}91Hic6ZMUOFr^ps27VEN1Jufty_37Pcy$kEjYHW74>Y_}y5yk7}R;0cZY2DhQz~js3XBX%VE7A'
            'fu!r;W`1q3U7=<Ky%lH&bLCu$?s<-'
            'POe7JkTkOE}5KI`4|lkvbEV=tua?IFDbUXtNU0<2RbM20g^BdaW}wG!!mfSXh`}T%JA~K0d#+yyTU<{UHzj=dabERrs&C-'
            'rVx@p1-rRQ?%c$jg1#O+xS#zcK2!xy{!I*wOET{v)En}z`PdeWw564nwKiBMfkj{_aJ|Cc4{4flHHE++VcT0jm_?w-'
            'h%aNs}{%QZMzx$tt_(>i#CiGCr8&eM(qalmj^>b7iZ2+&xecC|9W9&ar*r9oDTH8PFSh8{7HN&z*DI-HZnF*JXIWhNVLd`gwZ!*R'
            'jdHNN~IAfHzJCiY45c<%}R4C!eXtxb@_X@R2nbB!pWkWola{POVI<iGX@=suduQAcG|U#%?>prf0at3#fdR$<zOgWyfC*sbACEpn'
            '4g(jo?Z;+rp`~pw0t6!1t5{N?Wow<?EvjNJAH2I!t8Q*?%er>>Bqva%`AjSN=sf&4JV!)9^R;R_}UDg?ySuXpF6kJiZ%+TyR~{H9'
            '&ShVs2oS}aHYA^s5i@%VV_km!}eUmG6e)(VdNqF|IrhLlcS<UwMq>&V3Nf#cwg9faIHKt@lf?db+oWkYfPLdY_#eH{0#KL9|~MUU'
            'V40L?BoPa@kDe2DnC>$pPD#vYIJmbbgVM5K6>h*lTrD^sRzf`qH^`ri3d+cqob!zotzl2M$yR!tL61m6C)>2o|qUJ^=0#Cr|0Gef'
            '=4B4H0yBC(1QaM+hfItiW6eKSg5djY9fS*wbpTlP%tiR#oO!l1my_S^hQrcC&x!d)<)LK<Ll!S51lMOI59R_d1z#GVx;`wiHT_aq'
            '3FTUk+HE;>rpf@{!qDEeyDQt)JSzA8egxB!t}!PQ%{A<^YgRe)Z&@PXD&{Mr=MP)Mywwj8}W{NQ27M^GZfCuU7VVoIU7DXGk13W$'
            '))hz%<MErrZ$m;7SQWl``F6Ek4*Z*mo7c?=<!RtBO`@NyQ9_BW5JNDxH!Euy?7Dm8rIgf*qQk`+^GwT^k?eAQ}}1@!Ys%4<GCsnI'
            'ltfNZmmV_1K)!~&0{~jTElCX8yit>G!LT<0###nVR^tBuvbpc%+BC{;mlcUR{n7A^u?8t!b4MquayhmT74kMJvzBE{OCWeKJ(uKA'
            '0~Hp{=(BUbFPZC(S~zaIa%$gaA|pJ`NER3$44h?!@;A#xOBQP{D|V<(X@8X&nzuXU39jx^7UaTKm6!_!*XXHJ2~nqRc^0u0wIWH`'
            '@H<)vrB;UGvU<o^5V?t3(MAO6PVk_phO7<<mVn;c=(&$W+$pVvhsBwTJfL3S3sI-4S17>H^H$yHZb$p-2CG7nW?4eA=%5Ut8KZ-'
            'R=$2IzT_W!_>t8I9=%lD8t<Nh9xpwrULOx0^&M?Ly?l0d0dVdt(DXCQ;q3gGC!in6u@q;4?a4v8g{d=708XBnnstxk(!r(NrTF+U'
            'noxNUck?4Sf=k6`R=$30H8>s|gU@;R4@<1Uwts|!5?}kGmH0S&%ga)8@!r;2vmPg!D-'
            'thoDR=DBGsi9kd>g>X&dx8xDDy*V)XVcvOwZYidTC8Z*h_1^Dt~t7u^Bqu{E^YI@e?N}9z69>d2PKCRW~+k-'
            '?&`gYBXElY{#AM_Rj9!x28^?0W$R1<1_#A#O(RG`GtR7Tw1<x@yVy2{u+>wg$t)=XU>EdU{8lrkHMj-'
            '=;Qh3w`%ozdH7^;#LGR&h?@rmMn{SxU-'
            'h0udj3^!cj83gae6q_YSp7BqqQe$o#B(?4;IHKyxbGWo#laRzZ`jwMeCQFfp=yTxT|P*^aQkn|0k+10flSVM9t~ShAM)jbZBV3UX'
            'Ek$0x)_@o$^LBjm&3mvD-j)m3{=1tR>%{@~XAnsN!{@a3L;NBQM4(-'
            'WG7g@b{};BiaTsf($+&cMOo<0=)Ntz|@=T<+@h^cD`1R*`<Pa94^7aG&)arfH9bDZfrzt+1(RS)Pg%p3+@llsk*#Wp%LPDTkYC*8'
            '9Lb6j2d3qqY+ih_4-<Q{j#?MVD{SG2I~!*gq4K<*18+HII36kV%U=~i+11@9`WXyjfnNmkP5i!2EA1EcgpPs?2vnCfw=p-'
            'sL$bbKC0Bpi|pRON`_%vhg%!m%K*uI;Fj@-'
            '*o2)NwTa8S3`hoOE(Z{XwMMNIhB?^}8w}K>f#f}2c~bE3EA$rrS<QRc8WofL5<@h{@Uht<v<fBRU-LEZ0zOr0>zy3`8JLBzFDQY3'
            '<op+-'
            'xLMzhDi^V92LNOXey7%{6B|w!&PFG!Rq$8b?6%jVki%&U!AY+HyE@Uv9;YbOg1Tab)pmJf3m#(ry+1tVFB%7ftbC`2WPMPhvp&#3'
            'C%sM=sKJVk1bMGmEUs!T@QEaQOw45xPW%o4?NmN<326d&KHy*TlbQ#7S3k@`YEDo{{V)sB{NOwNwd(U3VQv1H7)4@kY&?nAitZ2s'
            '0X9YLZIWTQHWS?CTHOxeNx6MFYCE?P+dZu4BwdVQV^eYVD-Eoy2K2)oEO1Z*2oHKt!(QmF)obeuKsDIyJf|+|oKPnQ=Ndq_1yzHh'
            'EC;Xx(%lKyH_HIAYFt`wccZ{wq7Gmn?pH++kW)P{i=n_Kg!Zbn4ZyH^EvDjFa%I(lSRvg0JADdn*W%jRU`1g<p+MMk<$7!(Y`9sg'
            'zzrj;M6J#y6d6$qx(Qbl=mU<lb_b3%zOL}Zsbaa)X^YO;HWX0so+0qAt~wxHt6~$yb>Mxf&3YvlAeX)G$LsA{tHTJ-'
            '9wSqYrh19OBoI+W{()*KWeyLNyir*O$5>nIb|OhxY1Bc+a7rblf}OH&_H;SI{ifP0ZbY4&58^LCoX(yf;HhqZZIt2u9vIDRm+Rfg'
            '(GaH<R%sX=_6rNaDw;zw5OD<xYSTbepejf$YOS1VH>$hm%#H^acr^^dU7*8`O=mJWA4K{BLwY}OG^%fkBAlvGqmrY>f&>D>rzHA)'
            '0hmQ#P9juage&L>cMq^-yVIUM0*cQaA2TKo!e`g;a8_7TAcA8Q200O{q1Q3?i#6~8+SllsyY-'
            '<VBGOFm*&>P#Kj7kxf><@>1hHp*aY1d#aTo+zfg;FmD%4^yq;Zq%qZk58plcx1ryC`n$~j^^nrq(xt~>7?2WGGiL=W@=b+KeLG#D'
            'Zq3||O<Xaltg>k&3UR8fOWyIccluYRe>`Mu}=)cfSw-XH(%=BGdDz5ZVBm(L#l>^FxmU-{d!-'
            '{w@I)811}5HuMlNjE_3MlBN_*9_h$P^Q<>?mFOucM&%kb?KF3#(dwyxIB_!GXXuHea;+WF<#${wjzB;e5J(2V!kYjGM8qD*Vt^v9'
            'VDIlSM~)jTKEOPOXcY%kSNsx#$cxjS{%ESwgUX7flNCH7QEYk{qEt%*Lt5nf9H)GH$VOS)=%FCf&cQt5>65)1&a=Z6JX;2hr3o5O'
            'nK*yRfUBFeL+3s3LF@oROS?GE%7>M!YOdCZ&s@kBrrGos|GdN-'
            '1x&PQ>?||M!mUKt{)Y5ZhrW~+u!;0@TC`e*M5BX`kxM8|M>9AE4SWy?(p>&Z+-gXTQ^=;=+5^ia>jCV(p^VT2%LXT+zc$52uKH-'
            'D&)f5Tbgx&E$DlQ*9s(P5vhDXxlSAo#8&JBY_?WTtgei#lJF3J;?cu&Wq2H7=~|=O%we;6@5G7mJgSMJ5-+j@@+Oe+Ely9J4-'
            'WLjoL{<&ohtX}pI`31`(p3;w{O4oyTe~yOWUuwylOhwSz|9pB+P|*{BNKzfaWZ5r=i*k1|Mw_EB^NEa||os;pXSRy!G;{fG2l;^4'
            'aYVu0sK+rDF?64^n`HT!)xb*Z1ScFN2r@nQunM302r5r`cTXiuHBWqZh=_5DgdY$PTy4jV^2oEEZxZs;l*zEjd6~H1UcAm(IL6r^'
            ';J)VK&fJ&QtTf3vxZ21Y^6!;e^d{>}S`!KG=^7*M{q58*0OOUWs;<#Ct+pJ?FmTT?CqNhTtAHTcq9AFGgYtLW(a13PLI~X-'
            'YlvW+^x}>dl={3>Ayh!D|)c@Px1Y$^PE%!tkQTcC!9~&fi!d0sd`-'
            '=pb7iojjVXjs<`fpH=Wz#nprT)*%+RpdhZPg}WTMh;mk|+7*;U{&+$(IyodVz=7vPlf>=f_YjrGz~_!wJRGZx4D$F0Xg9`3#_*qU'
            '{O3XZ=ahBPLV+a?0Qz(ErKD^72LZbPhziLY4V@?aYw|*qPAYC+|KRXHzJ2F~ANJn;1<;9GpM2bV@5i@Zd-'
            'w1+FEA>ijt(j0>9Y?|p{{@}1{GM1z}2kQ(C$5A;zb&32-'
            '_&+`j@~KRVo<qUWSe|$HPCparp9kx8HyM_UA7!T7L7x@85a#nojmm${Uj4kul^sO}-|jzv_sTj4FtM&oCheh>F?HW)dy0(-'
            'gvEA&*BZ3px&CINL~oOn?E!WrLluX?njRn26;3(9g4`1Htka+w8&jihRj9V(>N<UL2_tG2M)QRD1ksWpeb?$f{A0PJK<53uEJjnY'
            'Jb87ooG!08ad3w?&d8+)63ROV?bgez?zn9r*f@!(Z~XZGezJEN_E+A8knZDx>8IJ8GDqEM(-'
            'W3H%9{wxwbKJ2kM7!hy|ZGe$<wJHK#(tXe=*(Ak8hy(S<BSPOK}oCUr|yCCVoXT%1H1c(tRh;(A1wjvDpKu2p8R8f=?gZG93D*M>'
            'nL2;{ff}>cowHI=2EGV4m-OeWTubL{-'
            'xMKa{Ibb(lZeMF32$$^E?pn%}#43pnG|m*{ruS`yQiQRna_Tg<YM?u+?|HmW*sI+}4GsyA8sPdcGL2{ZdJ~0HWm+?CrxnF_xp2lh'
            'jB4wE5+PlVS_PFD-m2)@WK@HC><(4+ZOCgEK~o6qT(^DJ%YnIGQbNpX77>d>BwC>0FYfb~`1=5LFa@qYD{v@k2ZzDv(?p>q-'
            'h2@t+Q|94peIG9yscI!#9iSy&a4te+)xo18n$yy5|y=Ta3v0k%*re0m*e$X&DTyKeiJwcb*Bl@t-D<+s-_-aur3@L$(^GBS?o6Iw'
            'Z`Qf8b|>Gh0V*B2>j?B^Uae$?i?GA&=Le{Q;}s1$4(8BIqi8e*`9S3)Cw2-'
            '%uUFl@HC7!dB>a_hJqY&Z9l1cD||!S9XUpo&msszF2$HZ7z~b|5s^d}tCCDCuo-'
            'x3AUr0D0pdh5Yi(Rc^9Mk2vQexuy52#lO5LN$wY?o6ADzv}!@Z);ddW#?vrHuei7f=UP7r56liU#3`2-dp&1kGq#AKib-'
            '541tl(@en_{9W8x7Uu7ahp~q@9&c~3k={Ob_yk7AoL%Q3kDg=i$6Sk<%OF!-oN$d8@F!!8m`TUKfQkV(sPVAy!DIk;zjxo-'
            '@EnNE4`~f?tS>3BuAWB8NNDg;_n7ppChc%pzCxuYjt1Ni*NWnw6+N0jNCxc1zd2OgsQ;OyD#Gwg~6f`X=AYpyZ^9f#oY2TB{a5Wc'
            '7D*Pw(@XNud}J(*`T)+@=tKdXmj4w4-#q}=z^CsK?^n^jZQ8BxvKwkv%3s-'
            'y57wXe{lQLPj7$zTJPgO{QZ+(?DJL*{CuJk2<}V%rMBY>9&IHs{)S<}MX>ECQ18Z@L}kryTy|MEAXEh<ELh}MbnwtLtU>qQed+MZ'
            'wZDJz(&0P5>%IPV@7k5#NAKVH^`CFQ^}Rd4{V^hcJ~1+FBx3o=-jw42zh>*)o8Z});VGh%c!Q>y?AesgFjAe6e@N=Q$aW7BS-'
            '6x&AbA3lTwvY`Yc<m6d(1A_6PSYBo56GsC}Z)_q`yp-ziZGuZH?m(;A6R4sWpf3Nw@D{#lskcVNhqqUu*lT?$3DXT}Rtwb46ViBB'
            '7WC%56?*Ww)aCMilZ*sz!=TomL9IcR)ku(;>*Wbf6E4t%?*kuySgx^s-'
            '>E1_scmuuhJg79#n&0p~w6af)3Z1<6Q$Gl&U(UvW_x9lXpsEJWKpz@Y}oxndvyd<F-Ck|5T(rBG7x^o=-'
            'dv$KPVpZ3X$7~0$Skuq{1;k)4AK)=}V7Wl>xG84iUPFbO11X8RVH*Yj#s%kWZ<oF&@7xpWv`{0^VCmC@EZz`aG1@r?&8f+fsk%KZ'
            'e>dE7MXjc{bO*$>=RghSE4VxS|XoQTWbmIl{v_k@R@8HyuRSQu79~;|+eGvNiO0-'
            'U8v;!0`Rjd%n_gVKk1=a?@zViOf1;mBh=kkR-'
            'n!LlD{R5DwgB$}FTpwURAv#e&IQSV`aQL5ZfXKXe?WMz?z2AH3`QEjEXQZ(AZ!ZB^<TNp`Ru|OnwMq!vuFskdfDJ*43RJEJKTP|~'
            'iVgbCA78qC{kdB=escJ$*KJiOH>srio`Dmbj-(Al)>A{F0~Lu5D@*ID%IU4rZ4y@u?q`}lQ^<t!{?Qf-xwoHRC$UTK-'
            'H&>&zMZ1!<(*f$Z6SfJ!hAdS7{zx@*vnb3+%jMijUlh82ZO90Mwl4_e<7@Vs9(*<$lMR<doy9C;Mgbna-'
            '?lUu|oTN&*X)a?qD+e=9%Dn6TsBFl#rysSini}_<f;k^*3Sz13mI!^CQy(cT3q1_ARSD4D~E+Ll%Ou4TKsq+VwyU?!5fDy@!kymU'
            'bD&G@T=~0pb7>jhF14L0TgF2)u{Au>rRT(;2%54x`#C@9OOqyseti(IZr1v^bJa4DGl#QXCz0r&{EbjR!XF%@3cw{lZ@o+DFs^hU'
            'jf+sREg&3Hy_-'
            '60}u(ccl_c)oUgRi&9RYxrkevDgH+aP(JjMuB^jV2BlA)kF>=8NbP26d_=K0sp^p;!OS39)AR=yY%t|FQ+VILexrBw6|PI6wY&NG'
            '8;8$bPbk0bMMDqVBk6Bl9KUG=xq8G!fb9j~XI8=Yx)?`;K2Bci|Nbt+oj3k^=a;`tTYxPFS7!TXFdi<9PcyNi+JkZzN$ju*42KW3'
            'Dlvs!(ZV%gQ+H|=5HA3W-'
            'Ug@GyB;*JpQp2RpfNL0awhNUb#@6>#PYAtsVNXshbJ}mvPUO1dxGPWcWg1N^jX1hRUb9AcArPcfsAx|NVATuRTRd8No%QI-dd}a+'
            '2AKVb05%4c4o_EN$Q*JIVLIqkAfx`j1#bwzjSd>M|L2+9T-+rz*C=;$$WgN!Xl}56+-'
            'Z&KH3;u99;m13_4q__vEP&C?=knW(ePIVWUxQ)lAbUho1;t(&(+y0H5aVcxR`U9tWCUYoi-nv%9eg(unmgUg$xA$qNI+&;kv5N8Q'
            'xmq+Lfda@|X^7)R(im@_ODi+B&!j&rOAcUoz5W|cPWu>#w^mV2^mCM)E=BMd7Pg*PbYzK>pBg{ciRyatJV!b|NS(6meUKC$c#blS'
            'W1@2`S|)8UWaWcvsI|K%&NdA!pXz24Oi)Ye(sroBy#7dK#aTDeia?Q78vJ3bg$RRD3YC&~<myH5hr7(oJtcZYYPwF0bg)CQmDXc('
            'Kfq<{R_-'
            '}iA)07d+BU>`aX9@v25>wU5X9T@;FI(1=kaA3lKz`#MHz(PU>ZStx!{34WU!rYoHkm)P4&gK_Of~@)mzf&)hT$)Tfj2p1hD<PW|F'
            'ZKH;kT*2g363~tX6%ySXoOO|*+88z*%gSjv;#hH7vp_eAGTRh7<ONgrA0wf=nuJ*85Py8Ta2nv8=QwG)zIN4*KaSn(Jmoq*6}bYh'
            'NktL#8q~D`zA^cN5>v?e5y9!Xo9aNMoye^eFi74%UId`mc9=VM0dXrxIu0DK8QE<b(IgQSH2;{k9bq;4kp|Y972hBlN=UcMcKWZF'
            'neXymboR0an^<%qMFQrNLI)Uxf|eCR%zDP_V6}et(VtzDGC*&{m5HZHG>qn8<lXef{dvJ`8t}gVIgCvSxf^~N^oh?5?BXV5p}6>i'
            '>4|zBjIe-'
            'J<epq{Cci6tUN~Vc1Q6O17)uz7lW(TlSx^06mi!u#%!>82K$jSeL+hG)pR+9mdxF(d?rh3zNTkr$)sAkgJ@21Z8Wbyas*PIWLco5'
            ')TY@QwFTbW{G#rMTJqxvsTa5$S<Ix0&Jq%u)a&qfn=3YQT%fP{P_pZ$bpFd*u892N0S2$NcC)d?l#8J1<u8h8ydfQA)-'
            'QwN7m<l~6N*<#eJV!4tF)u-T9XV=wH_F{EIhsZ`25_$)biteV`(K;^slR2-6=W?yaznAi$NX=paj2UH%K(aGxNl7wmm!b^plG-'
            'k3GH|o?Zk~yy?ZI(CCTJ0j!C%U^s=fHdr~L0jq(t2+ABnJBRwih+;>f9UcS%@%#ddN~FT;z%RaP<YSHD2Ws6dP@w4}G%QTkL*8%5'
            'Lx4%`W0wAq4^GqamDll(Zs^%8`(__?<2Bea;1+Y48C?5opfbCxYueDcCM>6t3#}wYFQCXo-'
            '`Xskne&B$ichXy?l#sptvTits8a3l1<*7jV^vEBDqAMr51QoTP1i3JDzz9FsIZ2{CWUHLrZ`}wDF`aGMY{+rUOR0J!B+8CU9uQv)'
            'xf(cvJSv21R}dd^^(68N0klK0N{>CT^3VlW01GFq>aWc$kO`ZNT_z3+GK=pA=!$Bp>`Ps4hv*LmAti|2O}CrGe9&tWQ3~1w-'
            'upW&Jv-s?#!3v7Dc>cT3ClRACcJcnvC1vlq>n&PPK5#Vhl+h6qi8%33FMGtgqyfQ*zk*Q^-'
            'Eo2LMn>1CmPsMy81z5Jk4?$cI^6nBv5&XdwRKU$5SN>k6oBdM|vh_xl%mzyFWhe|giCtS3|sDabVtDh()*8)U%OuJ^wGwl-jgOb$'
            '-eMzm4JpkE<cT_k05HDP69@-'
            '$owht82fVpol%S1`mc%G=p{#AJ$DJ90!pdV_Q&lkI@&0(3~Vt#UmV^lMHIRtR_~<XuQS1u!CjPqoe-'
            '+bZl`zbGM`b`J?D5SJTIN@f@xyon3mEl`UE7M5eTz=E%dUnuB7t_NRevk?B|ymLB#p~W=r*bN`2=dLaUHLQ(*4QlT(|5A!lsN^3K'
            'B0-S~1<6SYKuX=6dQMCWsXDdeoE0x3XAz?{e&3nsrG|7r+7*1DvC>1W;kl-TjET_q4*PTg!s1d`iux{UF+k)U6MjRTc%?A9YUqqH'
            'szQvWrHbxy=<tP?(O3$^RTemHNn$W>e{6Lq86!u>VdxRB^kM~K<y;NQ8<4Mw;48K&1H-'
            '9I4jCracH}GSxO!~GzjSOB0#ucEz~dL1dxjonDgk|fNLG^=+6tfdp#>IjGsn9Q4(P)%{hrLW8_C!mAue#OxO}Z4jFv%%Q9&bC=H{'
            '(H#iHinK7scuOmId^0JviO0+w@ZWF#CJ8BuXG$P1&!%;jO+T<T|{*Z^~fpk{0synnpUk?PVI&8qvjQe#N<Ka+Fhy-'
            'a3w1Jjf(ig&Aqor|D#p#(8ZU4l1d^4)gr8L_L`!wmg>Mj)Mm3CG;6EIdp*^^p}8l?=j@6~q5kSlu7bAF%4j@{W0H$NZ!-'
            ';)XdPE;jY)Yx4TfDsgiI4G$ByboI@OVxjFt+DkcAQZsM|55u+*@W9YM3Vw^nI!Xi`NVy@H)*}?GRx*jjc&|a)0Z&Hkh2QGC&biJ|'
            'iKBZUb0v^qIhceBoa2-HhV-tmMv)`$3hl-qd*!zY<b3;GGctHFe&2#tc(r09+7Y*~-'
            '0|am?`I~$;9_oc!N5KQqyh^G`ZvXjs;@D2s>dz0DncX|jc^YZkEkz-y93r%d98^X-(7-'
            'mcgS5)7}$ilzy;SL1A~A3`0#N!#x&3bmJpXBFo;^X2DAwR*R7+%4}k>I^CKa#BF#0j2$z1U11yMeLe%#i$~sfsYsuJ3nkB)>k%!}'
            'B;$ZSfAmxp6)xV=J9-'
            'GZiu9Ol2_Vdb3o2$kgN;y`#P|^}S9wZ7h(AuV6`&Lv5wQ|mOP`ZLloyHbTa>C15#ytNCuoe6*9$2vhWs@W6KrHsUVQ=MTi3gmu5J'
            'r-FJQpS<Cu;<ADo|N&Fz9TQ#u#!^Wb{yMBU@LaOFVL#D`Tt97J%X006#b0#2|xWHL^y9F^uHE+?S^`VB>8{)pa*dl5lO@NAE$a?C'
            '=TUU__Ha4iaah{oq6<hwfd6_W-##U-bj+PN5-'
            'lqMESoFA?wM9#t+C0EugP$^>vr1*xrAH%>kz{lcle5|8Q4)v8Au7Z~P^I2#M{&etQ!*G@_%L7NcZi2tSET6OwsTwL#F{j%54xsKE'
            '$hHt|NGC^itWA*ffYSSH>{VA`t{p@A{U@7-%*Z=Si+h@?J%bKyYDa-'
            '3#VsU>!zAr;0lXbM_9Xoyi<PzM6VDFv%?5EC<&hANbAnAp5+J(wI?Po?UDN~tLa3VXIj5-'
            '2&CIwb!lw|~cZ4ZL`VQ>}v<t}~TfTw-4GVe5r3dsKzk*o@c`FX*}C3(l<MzhmoHa$CK2-'
            '}HlFNo<OO#+7;szaiRuk0aDoP?Wwa5rP34lvY56>c3w`JEsDLnyRKdc>P*w?WyCmz|t2oMN<PDXNpGf2v;39V3!^3>5J(1gmzpxQ'
            '(qr0t@C=wbWkcvZE(ac61E1IBS!~0`H&y*_$IjY&cENF+1(;V$x<^{~uIQMQ{hRHyHDLZ;5>IK!i0K_-'
            'S}#z;qBgZNiaP&y6Nlgz~bKSaH6PIeYO%#6Ne)K+ETqTm0l4Bci~77(bIotpPF8B;LWbhzJg1%A|y5)#k=zMseTsixh2!*V95G21'
            'Ds!!x@Fr_DtpvNLZc`tSs|0Iekm+=Y&M2kT9=}L)x1;&tdcC#H62c2CkrehMi?D3ls^xr$u4~2pr})Jp3ki|4n|!Il^a}YVxa~L@'
            '}9Hu+zZRi3K_A&w6E92i=`&$7OGQ^Tv;K(F-%bR$j1)uy4#|w}D|q%r1mDWW5eSVRE*hisOh&UNwNmIz`-'
            'NiMb5VT=9i>EVQLma1is>GpxSXY(Tt}vefwr`_;45EHi-_W@aryHH((7(yEmWTtpMh07cRu&tc~)T4Q8`Tk{$=rs?}!Hmz@TLEp@'
            'Vbz+n-u}xYg_A_SeWA^`jbTt~(Vo~m>#Gut)OEbEZC6adYTB}?|&@S%?ipB_^1tNRPa(L=B_D!9XAtRU43A3N0=-'
            '!y+gjLdP4)miq(>#+S=g}uP;5K#S9y}y1<xobZ_Mm#QLv)k675-'
            'UWUDX1XcN>mIGOC)c=FD&k+?;inW@ZniULHurjdVtktCr;?X!#~g4i=w{3)D3GdD?6l{h0R!GiL8#j)hWJn6~$|yXMfqV%tQ&iRi'
            'ydM=8tj;HFlv*rWyhkRHT=ipbc(sO=Pi(Le|V&qDP{;m=H+rVUr@5w%ZD%jxr!a@)-cB~$AMS%(-'
            '$TS()gl<>$^4kRpLhGoI5MRwDMEM~8(W=(~x$&cU`)`wx#V@Hbb@Fn4U;t0JP>fb?n=SHo=QpY~*yS!R_KSk9DYe!j4vKL6Zl4}b'
            'i@1j}TOcXMY8}Zh)p|WoN67@|vxA0wcwwgpYEo5BIy`xR;Eg=!n-'
            'E@T9EEv3we#zGB1*S1Hh9Ha}l1a7Pt#>p)V%$yb1Fl~lO|*sBLe5XMC+YnPmR?OMDR`!k3JXoVB7k%>uz$tbzz&E!Q)9Z$4)<GjW'
            'ZMdU9aSg@1e_TH5?mQzr2vqJH|`OMK3qqmK2P?Ik~UbJhPWRk6BgEnr<)emVug2s$%K@{8_o^<-'
            '6*#7=qg^%^B(`fAI3Ccp?VV5+3CHpdEB4gAX9CKta7MiqhwHp6XFf2xE}n47Q%MD*-'
            'maayG?Ts$)+Drjbeaydmzkl&sBF!)g4=PZ8Qtz#m30daPt~UQhRyURv;Nxd&lTbX`xw(uai~7u`;v-LOM(e6k^a#T!-'
            'siPHyTVGj}qgFQj6kA_e~#T-5rzU)YH2ebhS&_p`ft?dE5%q09fve@VLht6R%`a=5rZ4iTm-'
            '=DxW`upKh8dNh{^wwcUY_vQ)#0gPB!$*|K5(d%`5LYSd4Gf~5*wp?#*me(S(=NKqiVX+`C_A#86lX_O}Vg)CKXW1(0WUUV(hEQ#z'
            'Au{YhREv=zBe&05tXlz9G0rFkfJD+5ZSX8sz*%oKD^<N<C90DHBW@QefNG|4745A?Fp>oe!_lY){IOea@#^5tFed4b=nuuW)TD7m'
            'hWQGDR^WA51jmeOY+%Pr-uQ%OS0rXtsX=aAV@|TE<4_|==^f7rs;cp(4am?Eqoqg#&Bf85Q4R{CcAP{`Q8kXbK6r<ePqpR!vo~rP'
            '&KXT&Y1zU9d}fb$qvjb-'
            '25>SUJ|=Ml%m19r1&damY%)O*IIT$7*A;35kDF0IlJSW&vk;@K9Y$4&=A!cDA$MiS^3uvBS$xOPI0hzqQLXbLAs1JO)veUFVQp#E'
            'cnLs5vAV{})}yLe4Gq1FW^p++uB~5>`qxy1vb)8Ig0M>`GfEdm4LdzzzH@?@tWaAlr3V`llUCrW11&JZ^$N1J8-gJl2v1nN-'
            '%j%~APSGeuN&7Uf&sY59f4X_#w|V?jh+l(Ptite)q*0B(MF8Pt8zMNg&?<(R0KceP>w@7C^%f>oIg?&7ePCGfHCl+1P;I$hIaHqE'
            '?vdIRwQ?R%F`N8h6>Qq8{c1#`lmdnJALoNS9<SUyY<N{hEKhOwA-'
            ';>m=C~!c&O%mpERzr9_A9m1;?X56Ayv|VR=sRvIg<MR&L$vl}1sAW@o3iwL$LJot-'
            'G6aMpmJkM7fW4}9D0SP#(!LEl(J(XW)$Ec!u|u}@5(d-'
            'KB|F<7F7=Sv^mdH#onQ#!jvni&G=vPaH|>YB&1;M$Sgh*vqwzWFX+4_+@J2c`{6-'
            '*CtBQj<g3wr{MM8HS9#<JWU50GYZKHo$TT+=#-BTGe+L{w1!1k`WIvB@og%tsC_rkvFhiE3-'
            '77stm8gKl!#lwkoL2i|$1U6`U)i4r?{l@!2^sCKace2q)3V<N(%(ysWtd{G~(a$I^%~@fJq!OSjrf4APeO7@e3R;=Y!;edN6kvCE'
            'NdbyMdc1iUUsl>x-'
            'P+EP$U5}t~v_%Z>QEzGqG21gvbk{1}zPq#Qz1V!G*@qpwNY}6N`1Ix9H3kB4w1!nRQMYIMYgN*tmqaA6Q*CBrK*YSj|{IaWlw|#e'
            'bk6ohqwP8lMhxa7`=dnGwL8w7d@ttp~45e8D8DcUl3WAkM$cSP=l*I@mra+e-'
            '4}6=YD1iVuCWFw&>%8BpWA%PrZHH2~Zc>?le`1tq$_6Xwb)Q=?^9FX@iBTe;f~BRglQ~mmS>%qjxi&b@;E{Dq+g|G9u}eO9C>`^U'
            'xjy=rNSiS1yFXsSkMOU_ToNbC8Cz}4kbnS!pYKxMGvQ5Yctzs<2}@wONJJa<;}N=cfj9q|Cm^%V*_p>?mX`u|Zg{#%iex1tQkIOl'
            'oZ;pdwb{{B&&*gLZXsreMY^TsWJ?Jho-6&LYj`4-'
            'GxY*DZU&ORRphMr!*LFr2Utrw7O)axDY^}eu^{XfSo+)8O0Vkl`C}EO_eF*ao`BSusoB|7M?5xMCM7l;u@F~uHC4Q~wbmrAP(ys9'
            '1}}lCKdzR1Mng}HyH2UkOHeE|-'
            'EV~BHD}xDUuM9BW}L<I_(WhZ_nx}UQqnjR`L#xP?;`=<2Fb`XOzxlzHP{Ql5yXE!X{j{hzq#~aGA&VqYXB}}Gn*UIbVUpc#Mvv>d'
            'U^hd={d^3Wk4-'
            '2z#ljq;Y3@KOvGdn8A6WLP#%jp{Q@zA$w${1ZdzbxkqOgqQ*n8<hVyh!dWL1?4V5iW7GNtM&e4_ls4L*z@q2|8XHia2>gITU()${'
            'l(W3;o8p|S6P=6CbkfMfF&fBIHrpC_@wKVHp9`IPX%(ngE+@;F?SpMWeuq&VNWYG<rIKymNGE#sc6fmP}UqWX@yrAk;87b1pl3&I'
            'G7BOBMD6>Eu$?FQLM95U${c&?RU<`qc`NJZ;K+!i4PDGKk<6g3Gm&E^ZP>Vgm%vv!&QF$9ThT*G?7L@~tXeb3X323-'
            'LhHX1qZpKT=Om8f<4dn?#m%M+0lyggTL`Z4PU>3K1EZ<x<vt1G9QcOz)ct=)HN{P<TEG<o49Ka?{H&`*5-'
            '3*i6flPE20YNHbhK5X1RSJ$yK%~Pl{Qx$rsN)pYDZH?#9i`m{cbR9k`RrDe-cbjcW$AYWTfXyvbyF9;L5=y4Z1ekXA42{mRHGR%y'
            'IXadan0c1a4FE7ygrmSZ$Nhbl(;lLX5IwY4m>%!zHuK&LmR|bAlc+30vja)0RySlHn?-'
            'Zmxl_RdF<pU(tv8WUZ<A>n#SJ0t)I$kpwT9S8cT*i4Pl%`{x*y2P|PZddy5psOKo@6axyPqjw<}i()`?6Qc3Vc1TrVVpvEbNpnxN'
            '6T1u4+S)w6UBN34js=1_-nT?s{HRj7<n3<3cS(3N=NFPs*_O5;B)=ysl{{-'
            '^OLLg6>^pV&qs2u`ef&NfhL!y)@!{U@uMACLAMqXq@3tR>+&Y$%JS4YB7-'
            'kyg_VambEI4R7Tyhgla<UPK;ys#u`rm)pP0b5;o3F}s#|1|y7^7-)#{y<4_Sf*>n#NYn>r@hyHrNTrb-9G&A`Q8s-'
            'HgaWP@8!lG7?C&RTFbP>7(E*YP<W~^J$H6?W@*_cYKDc$UQWsd@r`Lt<Qk<+NeKUc>&82Wul?olmG@w9x8UL5-'
            'f@f$Gab~b7)BILxGL=}TBSa{sF|`XN3vH0!`a32kP@!<!GHFid;Rd8-'
            '&%JXaZiO%HMzlV^>U3(#UNx1gLGXLc7T|Ig*v3=(L@mvF-Uz#=ZrwVylh>pOybH>J$7MnrsVHCPEyfuaNr*kmkY#B*s+<%RO;fYN'
            'mG%MEbU4+NO|0Ab{Gvg0zrs%2YTlE&)U;AfFJZ}gY&{O;nec-;>_s_%hQI;0oF24&Fbf4!u}!IYI;t1wLYv_LyX~HYH)TzHi-'
            'e1@U_eq0YnbNan#njXj4F7a=1yUEFr=Y$^53AGmNW&9*L=a4B{?*{h54_!+1#$EUB>iKv05res1OK{_63-'
            'e+C}%@DLnhvq79I&OA0Zzc_tnYH2#KEhJV<S}#b&s)he!fmFw9Z<LE4JJ9v-'
            ';|3I2XAT*V$SIadt<6*`Tzt%7Nyv;?uVZdDRa@19UkgL$tfdeQQFX)qnEK=(OOSb>vgfDI&P+|(7>~F@vQ7u$=)oo?DH2FRW=Pc;'
            'tF`>}!Zh=UFlhYLg|jpBOr56{er$36!a`x@tRL84V6*wDL8-Z2tY&XcHCI%7U<x?U?&9^Zx79$Cs)-'
            '~fTz%{^Autx+B61|Y%*$1ZKn#nC&?ACpoXkhoZ_$>P7pJGr7iQ+pP4;zMx!a`#A|@hBD3&lO#iSW9`7GL%O|CMxTTw#jYvmi8(gK'
            'tbVg@CLt}QoE5z(7V>NUiex;VWETxQ|))ZE!8XU<}XXFLG464sXyw;_Yn;>x}TL>U;YjwyK)CvgP&XbJ6^gHT|JO>NVJG)Cj*hc_'
            '6nAw{PU%S;&xU;R16;x}}?4hwH(O_8na6`?A%7F4Dr2cM(}A_j+>`~pt-ep};-'
            '>8BHW0<PJc&C1|=fUVW}X^0Dc)}&oFq2nz}Gn~2kIihw`(@TZXu~RMs91c=MmO<vF_WbnH(#-'
            'rEn_%A4=6h~_@%+>>jNKh)RQAMwQ@lRqNzDxIurHPnwy(8aGMwKY1p9{cz&wH<<V5a3PUN$*u0mi#+`*vVaK$d-'
            '{(*cQqTXV}^vsW!(Hyd^E5RB~^6HAo_Zog_3&BI+C8BzzB+%`fM7Lie-'
            'F}ICS$OlywU&&3?k;k)RLBFQLmn_CG8NPF@lIxE<F#t`NeZlmWZ&2zIYGFDo`jvJ5w&LNrCwIW99XZHAs6pbxf)6Q$;l@>du4=YM'
            '7`NU1!PpO<~<&TFmP=*`obk1TC_s$rNe{N(Q6*sPB=5G55dr25fN2isVVB?F5BW_{D~eY{$%*{^4Zyia1od@;EI>S+4(b1m~(4FO'
            'i4<R*XG*>W@qi7qWBc@P7*+j0o<~I+$O6gp$T?Mkhuh<cxW#Ks-KNWlagR`M4ag4V6YJfr&s}$nDQ`4yrEQ(C8m0pBQ@IZ2P^dP)'
            'uA)g*Zhta&O~5NoG5yzAO}&3S)G!(s***@ud?1Dqe&K=LVRSA=FK@dLud>**#wa9CF>&37tfO~zV*AqUtPO>{Y@^QBpYaF7!Vbhg'
            'B>~{eiv!V8F-Y`msZp~#j+}hXq$OWM3{NZ-E-Dx0R)$9%q^K!+5z24PR|A=1)+AS`<xa`_G1gTGbYNWXiW}HvB{H7kG4TL7bWH(K'
            'ZNWU6K2*t+%Vm_bkVJL$+F^Ah=!cD*jlIuUaX%nwiWKd0WdqJgG(onYJbY30&uZ2_OCU!O$nzpQ*X+xi!4YZ@(<E|_?6UNYmBV;M'
            'Hto~JsG80&Q^+8VOD8*#P!KcO_Y*Ua)p3|7wmlsx*9N!W19&@F2jw*5n}ZqPk;(EpVQ>t%vb^i5Tk4+NHR)h0Od#k;a%J<NWchvY'
            'Ynar6=7U}Fd}YP9JGX8bO+<K9;4Iapbo^&$?_?u<}@e@JqY5fbe1${j=Pe?1{5Bi#2*wVo_9+i#xU;;?Mq7C;vK0Lcj#Ol(qp(Xl'
            'XDU=jVgb8jE5@gNr3TiV7i`B>@_q!rwx`YQ%;mg0S=%>or9*oFR<gRNOJ&APhD%O)=XWRc68`;U#`456nQWN4#~Wnlss&KPmkbwq'
            '3PNojzlNiK(7<af>YVh4yLI`j{rIsYz6o>Y|1sM0=K;fSh58(kerXPy1*`0&nN{dvRZY|+iP|quMPN#bwP&V8+oKQ_^|+cw4#3@|'
            '5}t?G$jewKi|IoLGSr1w_d%``}Ae~{hdF)bo=^qw|?`S{_^IHpWpt=N4MYl_N~`{AZ@CJ;1u*?JgWut#=*g4?cyb$>=6<)-'
            '~PjMhyU?yHoCt(`y3n8;gwhJ{Pvf<-'
            '@kJBqbrBM{EkCI#l<|#=1T;sBE6;fk&$26!BFuqie|_w3U!w>({RKjOW|%<JV2efF?IApN!_1~Iij7>7jJu_EJ(hzCTN34PD?RXi'
            '?tB(i2!s`ddLeH@wrmWGE}^IaXt^}F^U`|6Fh@aA(82xK{##P9N=1J9nDE;YrK2PawS3_Z?&Qgtc}x4wmV>GDQ<k10*%;}`t<*uj'
            'oz2l7Q~E>)XzG`6nWhrADx7M&iymflVTa1P%^m-BlIk*OBxB6G|#pNCRsTBVi;zc1SZACjB1m-'
            'B6KE3w|Cu9vZOoArTa52fg_Do%>6~Qks7HK-'
            'L~~D=xc~4galzA6PFlext0)SE$z#Y%!Mp;BL;OC4<@rR_a(xA_K9K2mL_nv681Zn)99>LJ?*-i4R)i6q-'
            'urX<KV8Z`nu_+>ZyUm8Lic!z?@U_#uwdU5WYKQyYBeXgJ-'
            '|ta<432%jq6tS>6tPF*D5cDM^V9tWX~%5K6*#k0FCqvsS<eBAZ7E6oLB>WbvqZf}O<8jk%t)i<dW#-'
            '^teCq=m~uqYS<7cvTRvu7TlvEbZwMUeAO0JJ;fHk4cF!2V67e>O=mHJec9=*xA`BTCeD5aScU3(6Z?Tt*#hGE%S!Kh6^_=hHT8MI'
            '?)vHD(Z6}zU%dN;;d@$HR%iKJb=W(qj@jsqeR>uO&z5Adeq)D>A971mmv+KtuEcDmC91Aqf_;o!r<7Q6;lF%%kP>zHocH`g-'
            ';a9Ig(!ZG$lW~+XP#YPazG;ii+wEWsnPQ;~!dNBLkd#6qDX**hWejA&*g`MKc*61^eOk({mN_{u%d$#kvjfIjYss%TMy<ycHusl$'
            ')Nra^9xrvjBb3GExH0D~t4Wa6`u{`IX<?dG+^50^O$$PpFp)01bQ?Ka4#UL*Qs3zjhd=a~b+BTpJrNcD8+k4y@HccMt!iZcd{>kZ'
            'K4ac9|$Hm<7lQm`fZ*`k+|!)zt2_&*`1_3+V3dooMy0AjuGP0!%L3^wU9=VJNa_Q7;?xhe;v~Qs1LkoKN9^@%q`B%P@~A>R2vjkO'
            'v*U{>Pi2evY<9Bsl_fymjN{+n>L1_{vAUPp)c*ve{?0(YVk8a-'
            'rs@Kk2>rLtRa%HEZIuFl41$KuF2rbM6esNvmmLC(DHyRev9>o({m?ft>CSF15i@wttQ{b&u*c!fF+7?b61B?QZsR(!-'
            'qTc}WT<&0_%MWR$L)6&teTq@+ZK{#qD-xwssmX$%12tjx#WYDd-DZi!JUo}t;tAZ6_mYZvXAkV+vobVPm4#0pZeV@h@?DeM?=9GW'
            'i8GFsHs2Fh+x9uZ7RZ1H|t7t*#F#*G6L!IJT#GP|H8^K!7{Bny3OQXn+9!x17GW>AJgexU(74Z`T*)+%fQK)}fz0vc1+sR9Ud>);'
            'eYnF<Mod~<p<O0r<oA!6@$`Uu9|RRFq1_lW>8c}{W@<6u#9Pv(Sv0d_}o2l#J#6Qex<S%}Tf+EK8rdNrT1=`@5uE6byEAw2v7{J`'
            'c$CbuU?Xx{wA=wumQtV*Y1;t-'
            '^MLf77KnNWIDBdjS++R)lV3!tqs=`B}|<G?|Nz{iC(*L_k=wf0y$&FyNvyg~DRpb9KJ*|*WBDy5Z%cuDwUkI$GPvX%gtqQ{})rC+'
            'y`+t?5sB)el1tWCf>&|`_@)m<XPh4nV|J9>)!nk<v<t4yOVtg)YCCnql7pV5=eEFU*!O4H$&PtMKSO?+2(8(<-'
            'LIfv{kOg3y@w%q+wuf`&nFTxCzdSKYL4i+*+AYwT=25}6szNqCq*=h1e3NZ)Wmi%s~T0p4Lj*3e@cX`lKT1|jA`oswRlV|Y+7_$w'
            ')*^KISm)(l+9h_g{?t<Dlm*gY!A56J#_PJbAY=PcK@As}<!GBq_BtwzrN=ah{P_7i&L4u1#(LPB)%-084S0vfF)I+_`{rB+u-'
            '?xU<d+)j1zkB}XhaY3)LPIB$K}#o%AVYL6u!BRKN<>*ztQ&mEM$Bj&APEs;EgPZA@5>xnIW?r4Eu;U8HDv^~q`HI<kyW2YSJ<a+5'
            'B6ErmC4bGRUQ~h9-)HoW4xC<8W{C+ND%38hVB@J#w=khT73?}MZw-'
            '(mCkMYRfJ>MfM!g5Wq$YU;jiBWR$NA?U`ymg8<A^*MyK2Ht~vec7-'
            'K?HP%zBg>y|NhSdBpV&F;9|BsDf|3Q?;_g`Jn53}v)JMDl3^b`T;e_O5?~0Qmh2z!!o(`u3-'
            '9E2%yW1y_Wblanxpk5A;UrUl}DW(==5lV#`yP@)g2TFQ;ckz7npiwG?uujeg{16T-r1F}T@%bk;nY>B-'
            'C|AO2Xd2hCREM84rtDKotti0Hkgm*$i1E;~HxNT|<8FkHGkJ(Pk^xHy%!D}gTIeHD{Y+wgj!ey>&gIRGKRS?-'
            'K(@Sj>c_8tL3ke?=?T8|Jo@Pl2(bS0w5=j*nPU9mG(|CMj4F4I&e;&ktP8|$J@pUT7=|0_PGO0Z7J02c}4ai8rJIlW&1>)qa!@nM'
            'Vcz0d^<G5e+uKk$l%5J^(?%{7<U>>!Zqs>G-VQ4EcL5wd5vK@u!>LHVpCk;#cXAweZ;qM?wrjrp3d_@W&jt;Nh)gRyb>92th-MVp'
            '=n^yedyAp_s5GfO9uqtPY5;;U;VbAc~%Cjs7bz<1E0X*o%4?RD$iuTPvV(Qs3<bFm+#!ehRK7RB`-'
            'hTgixMcU<eX;la+r8hv)qC&i%@4nS=hbV;>A5qC(=uwLt4L<%{_dJjyc1(rh*xo#Fq5>5F4x|q1~fcfb2uYDu@t!%8_)wRG8nazo'
            'zS~4tnNR|Os<;1P$UQXwDIZ%tMzWYnG3$^HRECxBs1$d<10EkG?O0FLq{S7hkttG@a6aP3F%YOBoNHXSqdPOE>{;X<b{7shN+G^&'
            '<6MHF^PsUc&F1wSiNVOy)$=P)7o85W(8)m8r+Koy21Br5~nn#jSt5(vK=`PrV!~&em|ia8v@cSpj=n3F{{4AS6;Yz<9%aEk%JRnd'
            'D*VU&hXXu=xLnk+4^PjW<?XxP<KsDn2S0cQt6}cMI}4Z0o+h!Uy11M&Y?-iQE8#2N16i<c;TuVJStsMOSu(rkp~ZX-'
            '|Y)Ol;#0zb*2K$QTBOjBs|>PeRFvgfH6FzO@~q5g}`oh3xHgE(rwhubenQpp?pgCZuK>ppy0q6<|SIoidA-ANd{nl<Y!kH#=8l(a'
            '(_dvSmD}}lqO-`!pH57mJSZZ=DHlkpEx5&CdZqMP&tWl_6f!E*Oz*4{;c;O-'
            '^TM44%6TN!XUWriz%nN>6!)1b+cRB>Ta<*BuN1vObFIUa7g3>y(fcv+Dc|_qZqPm3k`_2C^0l=Af@zTlkzp~&efN}<%;7%-'
            'DYs_nz=P+-xp;mmgir;d-(CS!FV*~1t%xO=U_NXM-AaP@edf2G`67*`x}5!pZCtZFcTOyI2jg|hMizygmfcXZ|}7_VL6Jy`5f#QN'
            'oB7*;0QjnMdfpCn?KqJ%b^Tq$<<+W0$Cw^Q`@#)$c6at@G^U1+%2A_()<2zde^_#yNcTrC;ajiO_GFDJA-'
            'p+R+^B6^h~X_iPrCo4TV<N@lc1u6)**UgIoDdj<k39<NW;D>F~_yGdMlUje{-'
            '8adJz>3Qy@otzha{67^D(+Ib1@AXidJmVcOLPT5Yes8aJX3bMk>tzupr{;UypF=E!|WI>eHk52lgbA=)z6Vkodin1VsDoOjMi=2Y'
            'WKu(1<Xb*=DrU)?)877s?SRiIz1?*UcMMX|rWg6#Y{sHlu`mu?ppI!$3Y3{M<$wAIaL@`;z>s|TY;k$qBz4r?lnJek=aF0PI?j>Z'
            '73{atk3OPdf2@0sgBTh^@&3R}IGvZ9yk#-'
            'WHZ;Xgpyj%2uqJS5J2|11)BrO@HD=U!E)WUsTllum?)F5ND8C{{o*qwnQeGP`_X<!BSo;%-'
            'pn;jY;TD<knXDNV{ccVdqq4kFgyUJLwu*r_ei0PD$Te2d(oAj2DD+i0?6~=wB(){#-'
            'gFnP*BE+fzr!o{sI(Uwh5oIuEhfI6G<m|wW5bQUVNn3r7i@Ww}QN6-'
            'qP16BE^iYvO8L5x;OvZpP6)?pxZsiv5QDrfRz@(w$zM`b+YekqnHP56WlFe5*joC!^Kpn<1?9`G5)-'
            '_D~U5_FNA6*<f2?tqDGzIr*UA#ruI7KGjFbIy1-'
            '3CYt!SQa5yw;gfOH=sg;ay=AjW8QImT^I@U%=8B;+kV3zcF@`#h>gr9#!Ts%bO^VTmV0XX^ImLy=o1WM1#a^@d7&Uy#>(_+0oCUS'
            'YwZh|BOVc$Fx+Nj;p8Wae&ojS0)l&$dNeLcB#{BQJw+!`X;k4@{!9+J>4S2{4qS?7HD&A9A;q@v^8a0g10r9^unli(NF+QE_rv5>'
            '5+054q%DE#Rm5W09s?t>|x?_rpc!TGv_ABiKYgDrYP$OW@5e}qN9Vf$Rv<C<#?H{1C<$-'
            'Trxt3&Oei80stXitz`@#?%@@dR5t5QE;<iPhSAhbTa=xp6io28vezJe%)+HfP-TL+i1iWewqWL9Yn4TsA)ZQC$ZOPflVc<wroj!W'
            '3dr&peH`JgdFPFfdmmr5Z#s_qC7YU9!{XLuc+N4SzF64f>;f8?b^$RzCZ#?|-'
            'SQmnMlcBwd(^<9d^^2RcJNkyy9`BwnGs|Ct=INVL9X-'
            '{cU_>smJl`VUoTA0opIe6c0vtiZjR8U?$s;m(vrcMV6M#k_$nm)bm4=woRly`>omxYB1>%J(OBny)Xi$3!F&ntRw<Vp*kOFTd{y6'
            '2t`kYWHubx$VSqKapgH5Zkuo@gI<lr6VYUFdXxLi&GZ%fALz_NHftR&y$Tu?q*?*gyT^*gsqkF&x3#Y<ccjx(ZN}95qDl+6r*S~k'
            '?-`>3Q^5?ye|B$w;+)1eaOI%j(9c#?9FcWKFhKOJN+-Y=taq7@Am8c{i6oSv*m0$MW`a$odSAf_sYnj8Je+F&{-'
            'poa}l3&ZWmMs>|Gpm1XtQI9svx_9KI7}iTx{U9zhbM19OqnSKbNl9DIXQB&A}k~i%oYHFVEruHO4V%A{)1I;ntn{Cm^g4V2q7i?s'
            '(77d^x&{}I7+N^5k_9k;=n(ah??$TDU4L{|K(&W>D$<nseGYZ7s<Q6c>%9;k|TM*Wc{3k|DLzw7rqO5w}pLUGXF*Qpc<ylW$HY<w'
            'X^!>D^Q#!AeD6;0LFjNlo>pXHDij2n^YS~swGUY`^-'
            '+7{BMkM41i3>pOF?J>Cq6Fx$szPNeN}b#@b=Nz>H_igaE5~D?`AlnIfRC!GdP|(8plm|9O6wwA?OzO@9VX^uiL!vw-'
            '~+Y(1IINKe|}v~OT-u+Qw73MC=0b=KEVL|En9X`|#QEsl>~voWyelrhNq1B^i*M=qs@gzO=g0uB+*-'
            'bm+c!<3m$B~0vPM2dkNA@iPasjRi#u93?2-'
            'Sj>L<C44cj5wmNCHfT{#nZCgY<9$frF<Ke4EdhDB@`NKWU{Z^(5PuSQqYixRa8J4j_L8QOWFqv6kzQSeY94@r9sCo+oJKaCw=@ZH'
            'l%a>cR7co1XudiByYBX<|--'
            'O6^HD=EDGOo$m|!me}dM;3JIm$T&?$p%d7QGxxbnpm@BMZ+U28a7D0d2v|8fqKU!^BI&9U}FYnpkM-mlk)*A|tYT&;Hxz!~76{T!'
            'DPFf;|<E>dMFg#+N-'
            'nN<Po|64!``ZQyEYhmp7ynwbhcB~}Xqpq|SI`NwuZed5z(XJWr*tRL%&eHjwvmaN<@2L3q9H_TqMoW%02f3o;l~(WMa(0O{W1mY*'
            '4c(RP_YrpfvOe*+vg@bu*Sd_bx5oN=T_8~aY{YL>)@3R60l)(4`IDyXyG!J*nrfEGl~?SByECi<x-'
            'D7<IUzyh;f~35n&)3PKn~=Qq;nHh39RZWO2PqJWB=MN8~q092&pSB=p6Uq8xMSo@bV{Qee2S)V#+@j5S4rHujodZA>1rHRjATGoM'
            'V}&Jo+BTnfou$7B||4~o_dq0!yo$~758Sob?PTJl#l9yp3%t_i<CSKikYufO!$2H%A@escJ$*EJcg%MVTnNJx_u0);c}`-'
            'I;aZNPMCM}-F4Z%fd&utHB*n_yQx)(l(~G`IozF7WT%g;_gmOB&i9k+?byIR+-'
            'SeOMh1sBCP^UR;KJy?1`zd;RUhAO5=c%c~Gl=J3iN4_|plVPv{xORY+zwMe?p*rxCFiTh1k7Al--'
            '%X^6#Do)%&)V;$}g{zoxD*47RIJ{tr5hTq#s5FvxJ&K&02y5ZR5|Qf+0GPp}?#Z^;ibG|F{CW5DJ3o6D)<KW`<J@x!N`q>oG4Muv'
            'Te#JR>?faZi0h>`nQA<52SsxQLDM4I5y%0JE3QK}3I7DKV>=p8YC7Lknkn`nm!NZ5@J@&MxpPE^dM|trT<81vBlo?Qnuu@QQ3ZmU'
            '7gYqTI%ZO?tL&tQAy<-@R=l8y6QGFPWPf9y)VMP&>YQ5-'
            'l$q(vOfi)7fOG}I<1+#)m2RzG;WfB_VorSHS1*Rpc^ZVneuw1w?kQm~UiXAdX^5z;hGlf^>N8H!m^p(`31qhWaoSg<QJ8e&zyWta'
            '`Ytd$BCouHaZNlH<zxUCeYw-'
            '~Hf7;oIAy`@185%tzuacxbO%FA(05r%i+1yAj=)Hx?tdW10j%fTw~o9H7tWr15sQYgKA1q5Ij}za7H2T~FPt!M65}j#XygVt@kJ#'
            'glP@LZkj<qq1oC?dSKv&T1*a6aU&P{+(hwr2J?nnh6fY3Kl`~xzx4;CJ*)Rcj*1-!;k-'
            'q{#I7&_0JOM|yak&Be*ViSiRe!y;AMeFQSaTAPVEQkp|BYt*!12D;fcFLZAUcDeyt@OD16qt#>QQp>I>_fcp}MeIoDUxjodsIiKr'
            'J9ATzEX7W}?8;l@)kjK724?WR0Z-Q3C<fVr@|TlXE~VQ08<f=npT2?Jr)KTb?;T9WKnz%z;r-'
            'I5%~ETBss;1*hM31fZ&IN8+#(MJbRF3EdMaqGU>RIuTeqWT6pDU9Wr%U5m8n+@sDf7JcDpZq~L0Mly*m$Vt_NMU}wXNBZSaCfltM'
            'XnDuH4OI_EpvrQFE+bYZFKJlw%W?T)F=f(memu3xFapaaRa2BPNePQV_>6W%<5xFJ@u!JNc`3oSS;gqJDktxP3Ks|_qM#E)*k)wa'
            'B+w+UXu+Qs*Ht0Xa#n`~{xg}JyBi|X7tcXOv}lAf|7>}y!s6cTo|*{Zi2@iPVE~bL3{rLUUmJr^8)MnJKhCb+{Ot3?Yabu}>bt!g'
            'AK$$3JTrYjSJ#`L{?L1p94cZDdMZqu(0unW#Tpq(qYFS@%Uts<*gQD<yqDwa=y5`ZBNi(uUa=tM5Kn?#DKdEYK_y%A8n1@OuJXLc'
            ')xI*$B!hMYndjJD+`jKaWW0>^?R@~zSU<S+;+4bK|1{8X-cJt8*P5eaLTCiqcjFZ_o*qp3ZpS@jm{iw<D<vHD6=NS}Z8-'
            'EF!hB(%mWvThI1v~YIEoE;oY6#ryoW9$z+1sh46sm~{dicaIPv@hRb+}EJRuRDFiak+R^A+Uv{v9Kt2Ia;L)Z`IAyH$y)&@}=xA&'
            'V3LD9ZA1u10DojboU{a6SIWtFO4Ro3LhvO{6#LBmu<A*Ic33kr2HJw{+>_Ysv6)0M<qqZ39Zd2ObeJ9v#!Ea?j;%LS%vsMa3byDF'
            'VDJGtlV6b?o(1Ku8LwaOH&Bi`(GYV{&G)_~oa1p<an8HMS)S}&_{?En++5};$NXI2dK(~N&NTG0w5Oa=OZ&P?>Q>So+DhR@stfrc'
            'lf$z3P*sI%MgkHFN0oTMZBJvd*NY=*B24bg7f$py-eZ9b5i8ju-eWwSU!6}m-'
            'CPcq_0BZ+lPws6!1LA$#D(i@naJLh2bbIr~<^d1#@mDm4x_~K{1EAM%V3H2Z?qo*;Ox|)#EM+46TmJC~KfEGE_cL5bAr?xd_3&z+'
            '!Ou3{9n`weOn-OXG&|DR-DZCK`GNMZq1FOQ+h5XWmSf{*(#HoXeL^hAGKCJ&CU1Tnh8$T5}%L0aTmyjVF_JbfHeK#?fEG>(aAR!H'
            'B`FatTqaV%4PXVA<+V^m-'
            'xu^x0)B{^$2uUk_HQ(?o{fn8%TBU<GQi8`DW;$>)Z@GhWcSXLG7Ju&0o08FE!F7!*v{i!%Be4TGLAALDMLi|F;vD(kWE4|o9ZXbE'
            'cuWf)Ks$CR<@l1mYw>0oV&w9&$$&Qbp`(O4mAZ>cZG)NhY?k9qoG|Mqcb@{F9zFP}l`G8GWEB3vJp@6OD>VLP41h}9@s~05sW!0x'
            'ANur&3;F8XUwHIW%5PGR(O*bQqv@;U*lr)LFCvuGARuA-'
            '<bO!G)GtG%)IQMqqM#<RiD*06a#I$}j3FDI44FYykK)#VNXAC68SSzsQv{}aX0u}_RkEP3_8@5$`hnD2dVHz?9eRhqc>^}4EsGc='
            '60D0d4ipJivI3k9Mj2bbxaEwP4InG{+ROsDPl4s8cXs;R)P-65gLUc;*djm+fTb?AoHV+-'
            'kQXV|OCOho7ybyKyZO<Jo)BO%+DXSs@AK#Hym6y<?WMz?y?=Q1+Re{i6YHjyDxI^E0WdV+Citlm2L&AWj@htzYYAxe4P6S)Pdybb'
            '&(F_>Q;TOFpSd_4qL1~GmBLltdPp~(s=2v4!#~4l=?GHMquS0LQ6g%n3GY@C>Oz-'
            ')ffR2`B&PCie}3)u8;BWw#h`<jqS|s#Jsq^}1ViQyW5tJx6aAcVTtgj5{)x%IrJ8~vkzrk7;>|rO8h`-'
            'MT@wR?A;X<HC8k{PTr(S3*C4b{1IU$zEXr>v5oskzyuq<PW<S{4hysQ-Nk2r=l}FZw)hcN&C}20g4ksZBZNxMvy_wM0N!bo0E)(y'
            '_VYW!4!m_>@b-B;rjxa#`ykuh;)CBBEUN$%YVYkGmnPsaa1S3vkB?1hbg{GlWHhCBS6Quj>^xV8ShVr7jB+XA0x9Pl_-'
            'rE6Vv+O|#gfJU|;MZy`6i(&%fCxm);>l@*#Xb?fkRJ_kN-GMVR|ogVcWu?)kA86Llm89g(PXsy-'
            'L$|9{fx`Z?Uk52p9EvgWm%d!<rkur6xL1ya`4O!o5bztNP#UtRQ#OY9`}<-rnNRVjmyZ2xZGHZ)P%iPVt);=4GpR-'
            '%o4MeSBtvp8g3BHI>^1?h}^CraYJQQ+1u!r+i3cXAyrAog-'
            '}4TBM1s3JWI=(7|}9fWvwSPYWhK)5TLper2iw&n|sk|AN8CORC+)%d5@<67e}*mAU_bTWmN{Gw(^ys4{^9ODw1qfQHC1^O?KX11Y'
            'H}tC+bJCZe)0E^5+s`xh3_f5uGk#f>28%Ey$pZ6Txn5w?DYv`|P`}@J@9)L|}ybiC&~cKA>?6bFoP;5of?D;dh+^DNVAyrP<WvP1'
            'BhJqpbrQc92*xCuTzDN@iPk15PF#gsa=_KTyn#tJe=-d<#z=ha(F&k|g%cP_t`%o~Fo>oL-'
            '*>j>7AxV=k%Zm)jEB!)N7P%(@htF*yQDrf3@2kfB8e*d16b58}j7hqZ?LpTuJ6S5&3d>@#`ii#e0s%D|jsdM2RU1vJ<NNt040Q0{'
            '|Y{i_`ntCR-aJqm}a+(EwkHc}O>?0360Fr9^ePQZx_GPi?bXRFnxVLkeW(~Hmscu{JrJ0Q()jVTBmYRLiYurj!5jV(*eATI!IaAy'
            'uqM;HJzg#dX!lkzjCy-'
            '^V;t=Jz7@yY$s<7s$NqM?iyv_|yEU!{_7#Q2bPh2VkC0shQevza2D+A>}U<OnxE`{nJwzQQGBuYC+cv|IoA*{wI;Wg>=zSb>fZO{'
            'O7NC?p3sWI}lF98N;KTB*e>tQq-'
            'V3~7FR6=$jqVN&XJ?r{ac7Zni2#UqBE>}zkF&d_m)Hvo4bATW#*b6jb0T;S9@kjyM^U)tT80ipHjBi&~C3{YDLp#jT4z{*7vLdZO'
            'oxLl649IOUOMhDG&^opuElEcnH5uYjR{UCGQ63h|QblfThELQOQD%sv@or|TXJ1<-K^y~o&(U}DdLxv*dU^i^~*=|u=Bzx-_iUT='
            'b0tazH$gCtbh&Etp9b-'
            '2sA_TEw9KD%7zXc2=cb3n!_P{n!YTj8SD3uppwrPhqccC=zQMqLkI#By8Bmu4+^o@V`OldU>uqb#W7vP%^<`ziWs!>NM#s<fIR@o'
            '0|_qaYvR(=&``#;EmWtVW4Kf-'
            '(gG24tDrrcq4pLl5{Q3cK))dr)dMv5bW*uTt*<Onh*?)_e3bs3*geqhZP62EeV2a{ztvL?_*xB{=|FcuUaOY(}#GmUJ;+w1L)6&x'
            'G89>7qEjSB+KMVE6UN#Ou%nl5dCNI70wD8BOI`|K0p-'
            '09gfPe6#xV1OXtW}0KCKqvu*M@kY(gUf<$z4K!4v*+0X!h}J$essO}+wZ`&2i&>t{Pa1{TY-'
            '4UEeSFr%#UW+VNjH8GYwZg;j)+t=D|UHVNM5eq90y!z21xyVswt@IXhU<7b`JPs<st>;b{nFJ9lCE+$kTat3T=|i_A_v{p8}zV~;'
            'O~rx)j+T$)~73Kyo9AEyeq?{zm0h`0lM+{R|7u+|1)2&w+<!?pi`YA`D9^Z(+^+3ERk5h66tEKZ-Fo?Bj0C%!4qHcmhx6e52o!{n'
            '9LioY!aErh%TxskkC+o_Xnwb3@gzw?JzK<UcR83Mc>zVkb9RcAiC++AA3^#AkhAK?En$Plb!3A^PM?e{~Z!wGppwtp8(Ai^2n%Mx'
            'fe<B$awwk*6<ti5E5@-PR(anhCHlcvR|Z1B#mDmByB%h1kf<8jG!v^JC%6uKx33<s@+v`e%aoxYYuYcZ*4A$g-'
            'p3cH;L$x&Tg<mr&$N|+}fV5;E&L&M7x+mX3?j%(K!8NI?4L?zv2#(mWr*l%TEq#$4gM>D_Sw=2!}|L>ptf<<Xz$0bIRX16Z7Z^>{'
            'iw{CpbDdlqPle<vNrSCYsUCM5Oc$|)CK)tlhcrXyAr>~W*H8D40QvB&+3XG!z+DP#cc8HzYTX5FPo@*Q6S{sENSyQDlA<7X9N(CT'
            'sI;I{BBv{d#&6KI=3#E%v!~sw&L-509T-!x<$KHg4iAeOZ<oo&E2KRDM-RmJW@YdsE587O8$1%e#Fs;1v>@UFD$_QsVAn!34-'
            '=Q;Qx_Q*;`T1ptg*vscFnv~Xaa_iP2>~0ZZEmxqBRQhTO1Pxb<zhi@?@2MX+aNN_Jz841bm@N{5BCo)tz25o1^@KGr9$y5&;0YFr'
            'PY8kAmlx2FtC#lHjq{_*O+6){8uNx@+j~`0Ghvl@)`i~@1H=ThhP8g+2=0#!QVf5@o&$91?mrusdUz0!5#AWfI0l3rDKua4)`8<3'
            'HT#45~4@HXo{RLs4OcEX$n}gNVuu0%)tni;8Mpwvv9JaEUa0$bYWp(esOvFZ20*6((;mI<e5Qu7(<*|xb$%#n|T%`jFoZ~T`#IN7'
            '_KKPdT8#QTM9fhT&tqylW+xBj>WST>Qv67fHoHSyaq`kcUiLSqz#GY$pN_(n3$x9B1xDVEHRlfJUTf%yz=!+@xzZ?T6M0{>H~gWL'
            '>b0Vfh9A~w8Q-mWh@EQg8^hl4r|ARe=<I|!_|jhQI#CBPg-pft6{sv7+3*KcO`Yh2m!=of&|kH^BU-)C}g7i6)K-'
            '0_Ge|_UJ=Ep4T>ml;I&o4ZDHedoA<@;hX2Zt_9;}+ML20pkHrA}(R~y6;j>(S%FLAj>k8A{y8(YQCPLB?bd3QrPBtLMHso#Ni=2B'
            'iFwg>y?d<G8WOZQt;Xe=nZ4FbLjN#K4N3mg4n3#g`kO`{7@zK$okhghSc6s<`H8U`xviBFFKZ-'
            '@~jE#}^+_5o~yDM+(VJ`=66{Dkl4v#ypKMQI{Z-'
            'J)ZjTc8pJ&aiP+F$Pc`_FaBIG1rlE;CR|Z){sKJ;(HF!UKR12stjON6*En_C^<FZVU7U4ME7@1}0Qe;(8vE<tLvV{^(6GWyLJPuf'
            '8oW=~%G{iDknwZwumu7I5(kv_^T4Ig6DbP$M!o9pGwwbeXBQN<P2f{^7>0k3R=%+QZ*Ho7F7R6R6sNH^9n2DqHD&^yl8y_xSj(yu'
            'w1pKxp@yAOAZjZV%tMq6G^FfF)wPz<9AC@+%{V4jB{%m|eWDhgc?;@K0st{Wv6&39|C|2L~S03hBMWwO#Cs1mzvUGRD5qQW1&^pw'
            'IDxa}vLM_VCwlI*evqJ0cjeZ<9U;n%0VlS(%8IOoPWS_VrggR%97=wj`3_FjXyBPGA4v_GdroJ^!YGTCjB5qQP;Z-'
            '9v&QGo@krDQbuzaGeKAoTm4D^TT&|l7Oo}Q~5WvFm`ObRwi*K(_um!9^USw_nAdF9FZ{N-'
            'VZ+SJ^$xBKYQoa+dqJ8Tv$CJ&B5amoD?kHUoMx<U#jJ@MT5zDdL*oyAO6S+s^ps@PhobGj9{40I6rJiQ2a{SoaPvuvV)vq!W@>>s'
            '&)DhqzJ^c_DA*hpNRI>nqY}GgSU)!x7D#*_HW*}(fj@zMz*B^`WQE6k(-'
            '`B$L+?Y0lAKEndap7h~RQZ3wfZdt_PX)&=67+x=V*4#f=L?JT$_PTduKfu(TJ$U2A%`hUrn^NC|?W{|mO11>y'
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
    print("正在解析并下载最高码率视频，请勿关闭程序。", file=sys.stderr, flush=True)
    return Path(video.download_video(url, video_output_directory(home))).resolve()


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
        result = run_from_text(text)
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
