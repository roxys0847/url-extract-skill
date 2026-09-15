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
        "sha256": '7302885bea84a66d100b20b6f26bd497ee1360ccc2a8e2f8b86c10333c11e361',
        "payload": (
            'c-rl~`+pl(wK)2_|B7MG_nv4{Nq!`8Q-j*;Bu?v7$M&(Ew8b%VWou-'
            'M$db@Ve&G6kTA(zA(u4yol(s;D(q5ns4$xQn_+KuOo&3bVaMxP<y=TuzPEzPSpKs409?k6M+H0@9_ImohKi_P3%B%Ir+p1Nfrgw2'
            '+#*213?ebcu+4ka%s9yJSai`p<l-m`rUR!OK+q>Rsv)PHEP|K^AccXSt^nHJ5sM>CBdSO`YcDn5-'
            '487WB3mW&zjYhLm?$nx%cxXtxYp=J;?Kl#@*P8Wuw8qNFSB(yg1iBP&Hp=ma_LKdA7sbt}Q?8Ud<>Z%cr&gD5Tjffn9mTSTZ^q4r'
            'c-|~`HpFvNmT1+>oochaDSo%*fa49l>A1OeCF;mu-PKmRxu*3L@5;wcwArfG>awBEMms83YK?XIqP8hNcH4EFMLYUdH;Oyf+o;`c'
            'w&lBSts<VkU1L4adH@*Ly6tw<=oHz)#A02RsOR}+vp%&Gt#x6&S&fa(W?hu&Hllc~+=|qfBCT6n6nJFm!puCqVMSU1M;M&=Jda?d'
            '51ri>Oj5j`?nG_Gy1aLx+`<oeZxJWiSmRysIZ|h$68#9j73c9Q6m3=_di-Xy)}V*DRj+l1hK9n$i}Uky3rkby!bj#7mlnN}w>RX$'
            'fBtF>T7~}=*P5Gt-'
            't)J&w~O|>)v*)B&K5pZn%&)6LochpVJ+68*etf&1Te2gdKs)~yym5fs}Vl$=sn0Eo$Xo&pk%jWy!LzmOk<<Fs<&Xh+N{NKdCP7_e'
            '=Eyu$D$46#i`M?^-;S4{pCJ@{KC|^>B;avFHX)(FHKJo$o-'
            'Al`Uc=Fwo$Hyh;6v$J`}$+eQs(lT$uXLi_;5J7p7+QHQMcjm3qscz^4K{l}ckHW8=ls#nA`E09cVQ`ev+(72sE?Gy>&DM6t8&-'
            'BzbrX>LYXthKu)fA5q^CyKDnvgk&q)7rsO^nmS*L5Jci(1G3UHq53&4ar}n(r9sfj9S?r3KuTUE=^yU3g_phXP2fH!r93SQ!p)`C'
            '~E;IYHcejc6K^ID$h-'
            'wpS(D;6rMkSVSei2@axm_AyVFwms7)uCx(aDYaPCn!)H3Hv%}}lZ?>ZK!kKQZUWtd>Q9UZhQ9N8}Za3=9a%I?O)yuG(SFub1L01@'
            'g0RMmVWZ~4PC{e9aLk*Z@aSYxU*6&{}kBmQ1Jy{(sY}Xp&CkyMXdI3KJIq`=A*N_(<nH)Pcj#E4torKB{RLiHwPo5qfJux~~8DAS'
            'c{lKZHeDd`DCsw0!_4LX6Per4nr%#_6KT(aMQ}<WPYp2IYPMtbAJ~Had=Fd&d&J6^QO4Ml9;as8z2Pn42iVqaW#eA_)VdwOC2or0'
            'q;S8Z*T-c1a*6az&5vb{no{CPL7#Ud|SuLMfJ2C#isq+2fW22P^Mn=a+%J-'
            'ifkJcWD?jIc)8#}!gMdK$PC|Ao5R8E~9sg6e{)+(bgz3{^1<KfcW+)OyRaQ2buOH<*QCzfcNjE#+W$33WglK&YBr)Mw0HaZtRHa&'
            'Z8?y<%2{PfHeN2WGWkQR{lT>IGa*B+ekhc91#@}c9GcSc4Emv=_1E60K%S#e=%acbcbkU^}iZLza+v$!ee7wFIA#mDi_?8O<5@5g'
            'ghC~{%1(cN5)+WWo-XQ0P^c(sPtE;rVr+-M#~8w9Gx%>2@THDIrtnVy-(|Ao`%tXcWPxigoRM+y&27QS9Ce0$}-'
            'AotM3^6*3dw({iv3VfK{xw(r^OwYP1(ncH3VdZ4C$HT>?$)$^n&K@6{s0{}X0iV<9#_%JGgNM@ExiG!BIC;t0%JMgcq5SYe{|n2V'
            'efZR<t5mtYwgH47mhJQMkIXCr&QFJvOG^vWXD%*Tt4&~TAA=Gl7?7WPX#Q*8>NY!3<-'
            'z4|_|S^~B)$UDRBOPSJiG~x<*|Y3hiB&&rp`_-P7TRkW?XH{O}6}v%kgFZ*w-'
            'Fhx$mLN#my7l)6nDPht%ui!9%{I?I)Jb&CCPNodcSFb}5{hJNqc~BN?3H3~)&~C^tWO_EEsevy(IKaa`WNoVy$!KSmQO@8WKL5Jz'
            'yi_~i08j;#d8gJbYH5C6jwtFY}K<e<dYzGx*r&ffB})Lgu~x!SD9iROyLI$X{jyZq#_%K_g8FtT%VOEAj(kQ(*U+@n*o_M%>1)e-'
            'jcs;|nQn|^qjPB(vKbnL{*Q{(raexSU%R*9<X8?|p<sc$x#t#7sCPIqg2XZPEaXU+l{dias)|9Euf!tC7qe=aO8UA*+z<4=4YNXY'
            '!fGc(g?!;7$|!^wx?&{XvCLi5|Tdc8b+syO219%IDKg94)?#gVUik0Cw(s<$(KGVnM(oNTq~(PPo-qqWZPsT21XPmFuHN0FJ!1Cx'
            'Ix@*a-'
            'Xt~3Mh>;^Dn(eUU=Xb1mKR9^%N*RF}0Q<Zg91WD=8&|1A5$KFNY3l}@(^=Jxt)!ah2f!r<q2qsudzCY<zYdcZJ>q6l|T&_l5j8(i'
            '%V4&geSG`8G1!M&81AyEyKz<YO-U9+tZ?2W=UIn=ST0LfW5Z-'
            'aP2n*BbJkbHhV5Ygg9<^n6k48}ot~f2YZa}B%u2Y3Zh&^t#Yg=XLV0$BKcx8`9R4v!*tL3#T-'
            'Zp^QYj+#0H*6AC68^W^UC+f)y_y%po`6}j1F!I)H`{DPtapY~z=SvGrK-POZZ}|u+(ip?8MuS`99|cqO0B%Wt{JRk7{+zD<iRx#k'
            'jw|>8jpw#*vV0wn8GW7WPs*!0AW~b)H-39ll`#4KusD*-s6=g1k1lnZ{eSnyoaq(G0876L~{%un=L}CP!j$%U-'
            'K^DQ>C`n$?>0oSqS@r68J~Xe<6yS^{uFK3A=UxK(^p_YMnZ9?Q}nFbi!H%f5pvido2n%oHh}h^ct|M6Rq!Zib5@@8(COwm)AGpA?'
            'Dxv!&CmEaWKfrcWOx12Q@nD0}XV->vVw{EbB;+_lm{hiq-'
            '<3NV3PoTqfYe?*PzF=QEd(CV=My{xv_TdBAt|!z`rc1clTOvk=V>zSCc;KA#cR=8uU{B<9A(lX$J@4j~X=Q`Fufk%wzD!PT$TrCZ'
            'TvxqT&SJGT+rJ*?;i-J@Y+Q*rhy4XmsN^ur!3a8LsX4|-6;p6{;KYisjBHP~f7r|$KfP$vfG8bG%NRfD1|2e1Ot-'
            '3iw=$^fxyTv}>(qrhIG4qzbeS49wzQ{6X<p?oKV_NujYz_5BPrs7y~dBuTPAqWdPeF|>X;@aw9MPWjrK-lx;dTb$VxKXRX4I`{Xt'
            '<DA%8Bq(m0aq001CF$I2aYwquJFXEV!6|4i_Y0L6j1P<B=D}RI3QiCViUzR;C-'
            'sidL<Vim%Zo5YwcRA!wAnVBU6p0dWo_pkZ8dTT(y)khx<z2s4RnHtgUuCk)*6N>L6n{r4mxXPT4nmx)R}jQ|%SkqfX8TX&E3+XV('
            'w#RJXr2%5Z-'
            'VjApjV^={;7h|>zIG>i`Wg@s@h%^?|xxC{lgX&@?46{HrmR!+4W)!lPu$Ab&J8V2Dm&|$}>Gm)GRB7K1&y&pIl)i*^EPSvPU$x&l'
            'L0s-Mu68*ja%px!+5vni36?BBV3)r&VY0n-3#pjNX8IuQDwQG1dE37FH!7&PhoQT!X>lpjR8u$S1Yjn-s`p^&&X(lFZ5k-'
            'd|aPdaDt(tOz*t5R4T({&n3<9k{5o9+NYB3nnxJmX=3;_k!HP8XjjS^4g9I+nF)o%jVo%fCdGgt?r2Wo`6STY(K43Q0nF9blefy#'
            '%q2pb@(s6nP(u7Pk^zf|P>-'
            'ZOvdeezWA5C3)Z)1UNSeXsZ0QwKl$^}&l*|Nhi>I92GhcU2PvO~y&m4G_Cg%Y?@@gEz{b>2<WT2KeAz!c9h9dgYig-*+)Ck3`-'
            '~p3i5WGly7=*EXWfNZ%1(DRHrwFN>ngrP<*%Hkxq<NvHmmeZh+segW`OdAbQCO0|G7*lvQ-$1bI<0KaJ<(++|K@7CYGckuD`-'
            'sjKUe*MPHPd`8W>06*5SejqNN#dkn(SdLRY#iWl*UEw^@7%Gfu#li$sE1tN1H+TLpJJ^gUgu0W1@86DYE^;+=4OA@phlY;e^_OTw'
            'K!a_H&@H`qvFoZ4}Wy)yPqCB|7`F2j}Kn`)4{7BA6$Lu@Xe<WUVZNH(;pw+cvYc0-'
            '=D}C%gsr59YG;*{yA|ouxKJ69VoVt3wLj6)&;hp?;&0*kf24R^8MsGaX1iLu?Mi(Tt2z7JhDQ<L;Q(H4^yq-afqdBjcPN8&E~z6C'
            'r{*2s}z-'
            'ZkwuU<fsAiqYVty`uP^4@;vMW%xkvx<V(*>jde6Ld>&@RD{PKF*e#PZg)4|RfyE!6ZF3jV91BC%JXNfxv)mAY0Xp>m+_otp_SOE_'
            '=KY#7;#g_q3ZvW)7TOYg&1)!FWEgU^a0TObRV@_S)j~~ARVhUuw85t*3VUL_<b1f~_*HMpN5I;jST(l!Q+$=Y`uqm)uh^45m)^E1'
            't0AbO@D-v8f^WvN;Z`y^~Kvy_V&G#<I^>7l5?G}d<Hp{V}UGw^2KQ3Gwu9t174d;0!+EEhkac%XS`;K=JXu=tSd)RD|GF-'
            'nHi75yvz7!}3smz2a^~js0;Mk})w?i>hEKUcnRgA+EzVavgd%Fw6iyB+W`ujS6V}S(tw-KU)Y;|<<XtFvM0G54L!Cw(q5B6J!Slo'
            'hwxTY5Fa^ND$S*>bUP!jp$3DM}}kjMZBo)b+Hw~OCH)HMU2J7V#0tTHmlCq_WKabjc)|2cvG+>ig9wk}#Iu*3mCe~!MCbZu`xU>5'
            '*UA$g;r^Mrp*UTD%u#jSTgIQa8-Za@2@-aEelI&t{P$G!J{eE7;c2fu!nQ4w`?NFh(3eSrFR1#B^>z-k1pX0?WP?-3I((pW>-'
            'Mj_X~1h%MB!HD-Vbfh^R{OR?B7vH<}{xi2ef0ohmn;-'
            't*_RH6GvWHUMkOYs6A<t>@H7Wg7N2Fv_K@5DB2{}Mi%yu@DXnCEc5FQJ8JQ`)taTvqdMgn943@9!e?2Jv*`xU{WB<F{Io;4i^mcQ'
            '6$558CAOU4m{x2f>rNS%o3X7r=l<4?;Iqo+q!jDmFPYqDGz8!ybXEjhmkos9-'
            '?;upIuk{sbyN>N_A=2G>;J^pLo*N+_jlCNz8g#2N73*`G~e!y254OQ4t!vtj^BUeq}Pq?%#6$99*frS(fY&4rOGJ4*H`IBS>1Db-'
            ')1~lz80Xe{0po7*g@IBfANe@0FHb^8uj6gx86AQH!VZaAETC1RnqLdiCHw;kO!{+vjo2`=^#hR_%kZWT>;Y{zgH=uvjRFTFN>le='
            'fyYX^+TKhn_WVd$LQl=zUNpzrbrXV-HXDgH<j761Gr@2`J-'
            'BEql<9)(j?KWy~NPyG;*N2g5JlofrD4Z(OnsKwPD89pmGuB~LTL+W~>2lO6sKoGAMb{>y8q{NVsH$&6Ub_gILSW~*?Xh0=&GnKJV'
            'pg+=SR5kJ0tJ6@kH5s<`>2B{aP?V%Ls2_83`U<O3N7*GivZC^&fft&DKh14wL&583deC~l_=tdioh<hookY)tW|?6aZqGNVL87Xu'
            'hnY4b^`I6z<H=UMTl<Q?NU)S_4tBy;m}C#90kZ?w^6S(uH?|33J@r4Ua>^rNAH+#o&<8|*l>iFAW)l%EMqu!YLLun&lAb^tgE0_x'
            'Y%cILJozeVZ6aR=HxIG<dAFoN!4578`|#3F{*qPK^Sr=#tgz>aQuvjB)V9UWMZDpz*`03F;NT<Cz2Ix;|iKT0E&}IW0leM4oX$(9'
            '!;+8Z3Fq}Y(yUJ6?N82PD-'
            '0)Dj7&@A;5KlI0KsGhPciru=r?3V~rvv12yQz$UvdQ{UyOKCMdeScASjcv@&^rpRieA00*&CC<z0h|A1UD$WWg9(ZNg4-'
            'n{Yt;a_eX-uM+<n-'
            '6~a?!og<Gv4s<7vIB+^zXla_{vMYYd`LN_}wH&oLCvYI&I?b23nsZtkIzBbSG<dPu7cX_+7NN2;q!eN6`gbaGQjxz|y-'
            'f;}(U%q7i9hu?oBYuxG{G@-ii~&1H6e(5SZZa8j?aso>e5w-oYEaLH(M-'
            'qa5gY8~i;moq^NHX)5pE&;i!|3tI91ZKV7%@2Qg>(ftfef~=C<KO?|lV9xdR`&gTq7n%1OaA4y;|m^bC9oBTVZlYP?I=+1#v4Rs&'
            '2L<GSvMe51tlyP@K<#3&@`+;_uhH_;Og~%eDeIk+rRC-`d07y)!s+%-'
            '~QEKZoT>a+rRlSB7Z(HGHoPs`5Ry;U#{1_9fhQA55EOcomyu%XZ&(pp<vKP5hnSE6V5Uz&K88R(cb#&TeqLRcKewh9e(<bE%@iV&'
            'FD*v9TY4mt61H&#%}W4fXBjco$G2*=tPnyfzvB_FFD_#gscn>ghlGo<2KUXYK@E#^31MjTYCj(51k~U<dp`XzDLreE*;0>bP@0?4'
            'Y(EzETAtWI}6l6=hRe<`y`baL=buV^}pSI?KcPi{W{1Td)MA&2nH0D39k?S_Ox0KXj%>!RT<n?JYlD_S>DM}|9RBnmg?or)k>Mf!'
            'xLVPgvO&Q-h<vq-s3;`!^lbyERQigKD1HW>~4lFFf^;jWdE>}<E0E~Gj$}#XI1+e$gu8ycxqHJoE4#3M>IR2aU=$WV-ce*m8@a0w'
            'g@Rgjxn*bDZ4w-'
            'C>!63n6%kaa=swzF^f1RE~YAG%IjJqfazcXwgt&togX1wN~d4`bPkW%uH%WMzeNjg_S+Wnl7TY&liZu0hI^blOo&|No?T$`C<Er!'
            'qK?NL5Aarq^pSv#8<h(iK|~=CywwD`(C%GsRBOZN9u;bp&|9h8;q<K8Hf-0J2MmmiPWR*Y;bXa5sWq3&tL+C%<0n^!U0>;?x*-'
            'OMzEJ892<OAfqAkFEt8IUUA4qYOH8g*K?(9xv;{!^_ebxX-'
            'tF8X?b`k1BD+j;aWl&bRhAt)MLF_W@3k92k;`Y;8+0CfE9)+B@l0)?IF0Pe=?;S9#@Cj2nCl=^~Vmm=fiCH<dKlHL-'
            'XAFKTNad3wCv;A}ZosvTS*FIWkAl-nelvJL{J!jB4mI;apBeRrXi^P(wn6HN82C0mgMG0BaF@H42U211%{Xkcqlsw^_Q?4I+S~Jy'
            'q2)lrcftO?PM&xRoFEBNHz6fwh@oNx%7+}cN;gztYBWSB@I6unV6)Il1EfoJQtfq6zyx+PfaPHS0K|&<U7~7)dh&Q5nuLjdlPLoA'
            'DmY_$4I2&wA4JQQtpqQar>zk%aS>;7S+x-Lrm?Y4*au-oRf*Q9jBo6AUWg78*1gU+YXe|kdH?1D;==85u`v3D;hg<_P=tc`85dk1'
            'U_ad_F|NQ}u-'
            'hExI<7x|@U!=O&p*?<{zt|W_WtX6;AS~18(6DL=W7VtuFskdfDJ*4<%(Pleg_H$VPtRr;rUzdK7DxOCkMZL)n;V5B|M4g44mL}By'
            'AwFo*D|>gOKP5rW?10ET^|hLO@(G5UXisC_<E<_m8$%c<KK6yCf~|z4KA;<+oA{ba>~LZd)kMsxaS<Jx1|e)6wx8b8ZPRiN=uEtU'
            '7|M9!3~H!CwgDOzKy&4K?>e`rb@fmpS%{z8q;AQLNA&-!plkT-l$<78oXk6$xPKT}nvOU@YJyL^FM%YxOr`0|Wi8Ve{i%6-'
            '0uvAM9IJGx_em2*x%L8amLf2WoKp#n0_MWUR0>r!%JM9H9*m2assIbd3Wcx9lVEzUGY$xJCGF$vJR#Ez#R85KpeXc#ukr7U9le5A'
            'C=&QXCz0r&{EbjR!XF%@3ct_3U30Mk8pv5u#7MWx=8I-'
            '|3bdE~fp+mK>?(C`rPibjoPu=QctS|B>AaA9_i*vA|UZU45R9w8Z{Mqm<H#k-'
            'UR%wzS$sf|)_IrsxkY*kCqG%ueanyEl5*Ug9cnTDzN{zkcxay9t{md(kk?!ja5wOyKJ>by?(yivZgTz|WjH?shSb27R2o*8ja-'
            '1||<lTYyalS7x$pFdi<9PqU1r+JkZzN$f}wlToX-c#KC%;G7Rz7hu-gwJ28By~#T^VH2HNrp@ork>|=g%hQn@++&H9kc2H`FS~TW'
            'vnM!pdB+x?OP>|!SH5VO*_{avR^f87U8|613K!GRz$dVkMk87;V`PF5MZ@%-'
            'F#@ud(4(TBi*6`*SLrW_fISI?NTTlos1$6;epu&le3iWMli|q7$coM^h~_3-S}r^QMFA#`lC1`P1a?+Ip<T@s2;+YyQA(-'
            '?vOsHqRsZjJX0?roB2WZDQZZly(WP}jRCQ<#^!uH;I*NFzdK?bYU6Ij;3Pk21YcP&isoEYX^cQeW8k89*7)KYuqmsBR>pi(z2I@M'
            ';Y%3*&;zpL`R?Ts+WlI4WRdRTQ(!HMEDqF8JyhHEY<l-'
            'a12Gmdl*lu>$H@r%7t&1`skOT6<z+<++R<5Hi_rRR3;kMM{Ar#{XV+7<3pM)ZcE;J4htAQ9qnwMLpP0Q=R_N3t<ZZzXma?}+jl!_'
            '@Z4%<B+{kaR1>*!(y#3SL4z8`3IBzHftY~p#wJN)CzV9R{)!W)cs;{U&R6$qzy=91UD_JJast6N0Zsqx}EtWGO8%1M4L+GZRFJBb'
            'xQ92~7OxaENo0K1InLBl)4+tF$PRyb-ybdzWpo453QoKxKMaZmt7{IhTKDH0yofVv9$<n=K!09^Ewg=xHjZ-'
            '>JLcoPK{l1pimSDoP(L7#+U75N&`SLTPsWf25f^$mWf${)Dim=u8ARfS#&Ev$H{i!6{#13ZHx&Y79DCYWHM&TBT%`im?G#ah~tpm'
            ';EmJz5{OSy6s^Pm!fX(bMP;IgT3@)vjBJs!<!<geTO{;qu>aFS^k#aW3e1m^?LTJtuIL9pAo%0_V}O`yHRE4LCvI>&cOmr(K`HUH'
            'b}FHov9s0|e2X?*r~SlfDn)4SikZgX)!U2=OD9r#F)a3ht0=QLz9k%0xAU*~=@om^M+2v$afMtBIM2WQELSs{sz=m1cc)7X?7odU'
            ';J3yiq~gkGy47Ge{BDQVG}Xf!%{Z#fQe~SjZTvZHuEb#aJo9p-'
            'Z+<2UroUra<sQRm?WYm?7D!dz{IJxkN{6SjC38(;dZ63>4RwQtw1+QJHiuu-FX^Z8BOhCS$e0uTq*JA!nuxmL+FKiYOVB))g|MWK'
            'sYXQK6(@WX6psnUqcsACXfmA%P)~T!a)`T0Ck>ZJMf4TkI7VcPauol>9hCiU$tK7N@FWw}pgS^*a3B;`*~3*BfaO7MN5+h6c!6fe'
            'QFV72IKJ?Pg<>nI3^57=KYj(@yC=yLJW4!Vm#@H=%f?jH|>5c$IdvRcn%aiq-'
            '?euK6dH9+{h+pImx`Z$_=evi^028$*fC0`EQ#t!9z$0w}>R*$om}@yz@*oo&xdKJnPX^uv!Vg=ZGPP=9J+F*JJOa{yaoEmU4%wGB'
            'QH=-'
            'y)BEP^tJ(9WTCQAB|#@gfPA9M3PX5Qi%G9{l2~MiE#rI8m*;>BF*UBQ)$!*FxTJ$m5Ah<AN+zKOdZ?MJ}(QD9BLfTHa4STF%vA%Y'
            'f7D73PlRuYzXwimuQ_*W0k1N@BE<6x)d67Jhr9aCX)gdQd*Odb!(J+py-CQ=m%q(i1?_T#!^P9jI)Xct7Z{N9y-'
            'Np;C)+feNc=idv{fWeO@<nuL&po3x9-AEwjBc&-'
            '($skcOa%;u4IQ)C^0&nSe6jp`+TGma|jsA$3+k1A7U?uHR#<B~QSx4cyAha;idZEBMdzJ+8-'
            '9){XA9Jn$NJy!D8ejbcy7|j6D=#YzwiUnJQayd&=!@4tHmRl4)mnr)lwtk4jj@M-R4ku&D?{=z%(-'
            't#HV#l}yYIc~*T4a4ChuxCH8<67vx;_AaN*a({a#nI&;D9KyRY%^<;@lMXX2lBg5B_%T)|*#BGuV6f`@P>i+xy+0Z~gTRQ-'
            'PDvY^5OAK&UjJ+;@-xUw^mvgSWH+J4C;>m?tR$t_d4dlMmw3UKFDSiCs04ULi+TilpxYdjS~>1*L6Cqc%CBAiY7l#>sX-Lk6nK8i'
            '*uwLBHnYV1@LE;^%Tf8}J6OorI)~z3Uf4jMMHRA!6d{i3!O-'
            'WB3>1oOcS;Vu1zi+9|Nmtl}3+k&x@b7uqaDv>Dzxoxjjx8b|Ghk29`^E^9Yzk%0|r@3QC<6!KWfOe92tA{7dflN5lIDq{7Vm=;oX'
            'YR5S%UPR6!Mqj<YGto;8=}|V8@qxxl54DEpnieu9!mMD}r%MwSm%?>at5S<3DjpMF#hrM$FuG!xCSc5^7#&YEu`PoRUw9d-'
            'tw3C5fzy^G2J`k!b4DIPPsd^C5yb#v1!5I?1$2ZUlM|uYY>gQPTbmd%9I))TnACCg*s_25*b0QNEN??R5NPg6dYG;R^a0{rPGI0m'
            'eBOf=SoH23?>gA056ASoHQR2az;Oh?!nNWuxrT6Q0##WBU0hfY7zHX8Qy2FMykBO*Hd+F}72_AMoMR&+ri7n-'
            'G;7S64#v$Tg(iv(Fn0)f%7(%F$2%Zt$c@pgxQ{C}hE(r#IY-{hL`F9-'
            'P1&M&w_=!630fCQ5X00ZcvB|dZP%U@yP7>r)88ir(ixa=%-'
            'zcT*J!6cxXfafLh#aJ_<t8x_D<yYS@mOi$Go*;e!>}#%bXAwwfgimDKcP{xK)dWhl!iL`ewzr()J?lrJO3MxxYdDfwmD2$<PG|ev'
            '3y!OoSv#xgnTFN)-8CGKs}_w?V20Plo@8-|D;0xlU7wqsJ%VN<+bNFsT-'
            'V&Pnnc()ZFDMUH$gwHt%%mER_i^X+%d$l%5JeG6LQ)ryU1Tin8O$B*~DpP2}Qi@Dwf_qz~~3Jh`R-'
            'xOoLzOGuS@i?eek#C`B1cS18M14`*9k8~_t4-'
            'Ya?h=H%L+*;gjw{RsF1QvM82sbMhmXTCrhz7~1iuuYNz}qMpiL0CZXFeV2qci69|?&SX|9sLn2cgEz=DVn1^T{2`DkkJ4YKKz)^B'
            'if<l*=j-=8=VNO_~&!o<-'
            'RkKF1fS4s&E`^D@?o2$kgN;y`#Akz|7?k5UJ)qf?_$~oIX=?XG+8e25M2`^_E^ZX~kR`9oYV8srUO^&1kiCyZ3S)ZFF9&pw|7)il'
            '%xG*U>StHbAfy#2bRA-|!#*mXDqlaP}*}58C;*rx7-YWKgz;LdE7d&rbkU_B;S);-'
            'ThjL)<%TpS#@iwLEx|=8Ixi;>j_n=jFc#Lu|qGc)viL=pua3afA_pZZxfLxrf`hj+*(2zN42*G{kO2m7)N0mzjK;l}SG6CFDL24`'
            '3jgt>azi?`=#AAAMwd&Evh2C7w#vE25_}@tKwUd%b&?W>p$~YwL)~eHA<KlWJ>zBQT&UK_7F}N$nmkToM8mp%-'
            'RGaS5><>6h`Pt2ox0dr>?fMVzuzd!dx~v&Xo3gy_B^LJw<ohy2GFeA!-'
            'm&8cKrX?32=?CD&tB>b>Fk~`2a;Y`r(LK3)P82vk}{PE1t+qt$*3ccXF@vnrk7;|eRUW7DKYdK{&JVzcfixWS($g5L<Qvkibz%k#'
            'QeNq<dVE&alP4TGCQE{G6eNTwim?okVJ_?4%H!1#aCvxCr`o6KDd)HQ3n_ZtO~adqWn$}fbkUCF+J!_w%eef$IDJm7+W#gvdDe>C'
            'hPUwF(SFgKzScSDhqduTi6<8!(!fhi|sWoJ9-'
            'RdN5?>mvpR7s@c#YZy;+LV0;lPD<_@q`Ou9zs|3MX11a~ldgXWUEi{z;fBCOHCPs1Yvri0LF6OO!kZZxqXl;o|%it~lc*^4jY0lN'
            'bVTM;q1l~B$xA_^Of(Y1L@I}jsH;2m6xm*gO(OiE~0ZLUvb6!$&9NU`X6JuP5zkYV_UGYX}>n#?YguvQ~jSte_8`j*_!35iT0VO|'
            '@Dv{7@O!{*J2Nk8QbTp@iGQ>gp^-'
            'JnS5JuMO|K;SUx;la6iaFFD8oFjausV2V)N)(ex20IO0omh~={;XG)MbVw9c3futH*dV4i(Z(OzlxEO2nx#rdNeS|nAwF8hpg2hW'
            'L(Y`RB;?}$*Ts?Sf_})EHRf6w?lm49SdzK6}+dmvu9aHUb6vV*UC~kD2!vzQUA=oW|-'
            'N>2puk()k>3DHbW7VI0I%$Yd?pzv1pCa7j9E*7_g=j1lhDs5d<ML8`h~-!hSbt_Snx-vX2|e576~(P;*GR^%8?tn=;L!Q<g|NWN5'
            '8&T|&FOEl3}ukQRvSz0KjN*Vr?aSB5ZMiZRT7j-sSvCKgsnvpG<t;!N{Q;G9Pv^?)1fk-PekG{Zw-'
            'n%b=D$<Fj4LddMFtY~>px(!Do8CA`g2h73>-'
            '0pQ3duBMLUhWSi%>L!7WjU={PA?OKg?Z(YH_eKlHd{tN=EcGc{Xdwat5hnc?S1W1IyA6+H_>k*iGWgO$}&7gx)pOiX`Vl%$AY3FG'
            '6eyuMMZp7kXFI7(2-IURa5zC!xei(H5F5b`aF^CR<lAWT>C-'
            'RA@9)^(zsD2Jj7)qJnxoe9<2q4)rKr)uj_D4&8^9};1<@0Vbo(sif`MOqJ10N6G!OX&=U{RJGYn}mdf~HTO`OW?NW4-'
            'uy&LjEqj5qySuh9^3s~M%|s#dxDjt%8!AggAW`2Ghznn8XRAqc(<0C2+&kK2^D_O|gn%s=ypDbw*XsqQr8Pz}jvydfwcM?DG(ckb'
            'ZtVlEUmoqhg?vNKPqioM{W6wbNhv9KrjQB?mAxW>bTrtJ$?$;4GyctWcDUcNBiptF&{2hglE9fEAi=c;Rwf~Nc;g<C=);vc>hnb3'
            'V5@`04T<|vvV{3|s)HX%8FO}6vA_(e#X4Q)<65zez1@4-'
            'jCPmqL8*IDhQeap5!Xu$g280P2<(;grPR&OlXq0zlalqB5#GynJ2fl2@1W>{X^;Ad(cQ*Yg0zdQ8FfmZF7`X*P?6o`KvKrBQI12r'
            'xr9olO@?rYD!efj_J_aF5)-U7+e!Low`r0z+4Oy?QB1pI4}=zB#8r1p)g4=L(LIX-'
            '2|AUd;pR08LG5u@1?50&6ENKYF*Gaj^|ETDVWW`hlj4i+OD5@oYj{r5*djAiGlH|+Tf(5o`M;DjXv6sb6>&(8`(H*L?!{1?v0CHk'
            'sJD3T=6db=&Cg!JAT2NcH5sHu-Rtj>ztg?(Ei%QL_sq+P5v`Gxqj?uG`exR;JFg-LImhC+hn;4K-'
            'svaCg+({BxHf#>%k|bqc{L)_sDZMA7Yjo46$3wsI;%R;C<<MKJBqly6*6zIK8UDqwe^NbWeIVJMuv<enyayHP*=r({upT;PpfF1r'
            ';CNV=Vr4~)eBalI{6RdwxI&3u`O58ba4b@53#^WjcULjyY&{Y4xT|{@<<T<AvvNZ4IvWDSDY~gUWbKB&#1-'
            '*cD&@B7}ren#H=c{^;*Z6lWgiZ)Cf{~$D^C7YJ{Z$sSsl{x@w^31-cW<K|!3QQ+StBjicHe-r-'
            '@S+VcM08?|gujV7_QY~emWvj@G=iA3lIm3a!YrGpbqj-'
            '{Z2v_xny%_b8Bfzu$1eO;zDkOLS6BsnpjW?^NNweuAyDR)%9GUTod=@eVJ<R#cKG>(CZUR3M6NXP|xVs$IEEm&JxHC_VHP^_-'
            '8vh}DcRzpKCqgh-|?OxNbNBwImLfPG7=x*4h6B(roqlU>VT~Bj@m@HFUESfPJ5|iiQssk-'
            'B@?r?GwG)C(D2NwXVvSDo3Lpwkc%|E^CxUjk$Q^-NR>mzp8jYR`U{BFTYt@1xkkLkrSz>cKX@zVOki8E-'
            '<xtW|>RdQr<D5TI6rvJ4%!e`XFE+pjMkplB&f}ier`N@l7w%}k$>1K3Lt4VgrHhOAJO;+&o-'
            '+VO@57gRZ(l$B<Rv2thFlzXC=6k|0|Vk|RQ7zbcaZfk&oAN#atoQL6YLAW4+@GnNX!Hkh+(bLC~9pNJKMF*bqbi!*^VMgH3K;P&>'
            'oF<-?sw==y4b!vL}o7|CN%OML&o#j*DqYZhrUzgC*KmKmQTLl{dmj$f)p|U|z{x$Uj&KP%5CsuGJH9TnSarv2VW1-'
            'HO*sXjo{Y(>L7dywt={w)rV5W(J&O@3`R03N@+ZEe$Xp1SAjFYgON2dz%on$U9YtIXjU)YTc+0iNxORTDd{ebXA7e;h%gvjDjkt&'
            '5N!Q2`#uQcp7UpHC};pVocveHCePI*2u&F2Ee?mxdi;BL!8d?{4&8Y#%WDAoJ|bUmZTb;n97&F#`1kMDGq_=k<H~(=O9!kE?=<$6'
            'e-'
            '$LP)ib?in91JL$9qSu?q%A9J><z7|>5Q`ZUr3C`YKakMU@RbC)Z7WBF72!H#@F#X_1Fox?mxBtUT6LE#y$C6<t8C~%59KaHhZH)|'
            '7N;--'
            'P@00l|Sv;<7I{bbWiH?zY@aM;^aMCRWx9c5jjvH=tl>2oymG^#UXpi_w*M#)ftni<MaV!NgZv{dKL5GC#~Njr2B*M`|~I=m;3RUR'
            'XW8_63-9KQ2S>j-J8MaJn2c_A^z1muvk)`f-'
            'VBvw>clnpGFpa8u9KqlYQ$LkbSC}!tg$tZ@7fHL<c){~}JwF3V25pS>v2@c@~igr|-'
            '(zJU)&a}=b@?Zl%ye=O@9^#lr@6^X*mwoWsJmw#Bee^Gr;&j+|f4qzz;a~HXKvxoeL(#?zDcc}j)DC5e79RG7r#MnAEP;`l5pCFy'
            '2kHI{5l+rN3b{znO+P%nw3u`dmaK+M?>HjWW)Rx~ukcZuM^?<t@g}a5W`{+(Zs%l633CNk!g|;6L>dL^1w<zdBz>#MS@DPC960x}'
            'mUJv&CB#y68yI&+m}X((gH}iLica@~W)-'
            'DJT83M)fYjN^nVD4QWHwx;fiav@5m$7Le7w84+N2{=LwutKFM(DL+ydiC4L!9xPfC4Wf`V7-'
            'zH}U~`DKd!Wk#K7+FrbXPXq>Y@2R7W(rlZ^uQkGZ9|`z2NJj8t0wiUV#$Eu9ApY}7OZx!+n~Q-a(o);G2H-+Av$-'
            'KnEzYn&@B?D4m*yUwnx%}z2GsHb{DH$cShN*bQH?k1kl$OJg*j)kuO!%6bl)`GRBU&x;XLG%-'
            'm(~iMHn@vvezK7uE$me(WBcdp&pKR$1i$TtYSGqX@<ax-`kvE-Xk-Mp3b=piJg$(P;6RZ8aEg+vlQ;RALp!YFc#-bQFT#MfbPx-'
            '#yOY9G3Qem=D@`rqdHOB8Hu39y!+$kaKP>h8}o-nW}l*OAe`X5htk6zOO}uA31;e#8C}a;xG{|Q6=-'
            'E{*dn_{X!F<xiN?4Hjcq$xZpKT=+}JGM7iCsPH|76;B;AX2L`WIhU|tA)jC@^w1YHqVSWHXhRzX%!%I+>qFD_1A8o>Nlx6Lz|-'
            '3&K|f!r1p0YNHbhS*I~Rmw|3K%~Pl{Qx$rsN)pYDZIF#9i`m{4<o{A^VzK^oxTn-'
            '%c%JXX3G}<>n1OGgW4@4**0%DX@vYss1G$@cBgt#<C?+2;nIXUd3`8v-hk}XWpU}mn0XUmJMh%#+WI{p4Q-'
            'Gog1niN2yB!H1Pr8FTjvf_UmhxO_Tf{bNCT?fdYxVl=ml`^wtgzFf%fSPYAg>CHH7hM`P(e6Lour;gfCKLL$%#i%gIdYIjZm<i*v'
            'K*NVmju0LgSfgWBO4f&z}PY1zy&gu8~ElVo;E%IOjpXEtV**O)Jd4SGUiWr;%XA$>eG+PnVU!=JqRzX{}*g+QJ*=_9dKWZl$&P%I'
            'H8f+tFeGAvFhMd|{F6os^pM6^KrcxmpOC%8J2PV@FW)b8(kB2pb(u+V-3dCACoWNB%BQPNCd2ZsW-'
            'x`>>h8?^u1)Z<GRPF(Z{%176G^}XI}PcbI`*5^O%z4A*HZXfCP!H3WEe)OV|rV4v6H+I2arXkn5*o9rv=2-'
            '}E0ENd3Q?uu0rWcodqGni_OoOFd5Z{=ldahB*B<}G4hd16nc;&ALFTDqYJA{Y-'
            'dfPENOfpof0%C+{9$9H`(kk`oMa`5Y7?iyt7|tzRfF#<z5B|IN^s5JN|Hiu0h<hr8@5&8!tCwqRs%s%xCuGX3umi*tEYu+*o+gTr'
            'h(StSI%fp><z?$)WfE78>amLp(<Oh;agvILgMI&)xLhE1!j8>6rcxJIO`3|7WNBA|cEl_EW=pO32m~S4gNm?lD6Bng1NcFoHaIUl'
            '9ZoJSEli)exHM(R9AGW;)NGJtUYKk(3DM;Gux1T0hJU%i*#+4o2ARXxGNl&~ISf%$TkWE82!YArI;s+M36nDOoAN_5t_FH^y7n=M'
            'MfZ&-^Fa<{$Uy+P!peO?3Eug+<!|^a#{>UKc*w&;aE#3cajrQ1@a){e)Y-'
            '|!slYaMSvG0CAQdYX{*MLHNJ4v~+@6IMsrr7xfFkS6Ap;WWJf$APMY0DrFEP`haXB*wI$=F-'
            '4;{s`$=`~WZ9q7GWUZNKh^iYt8Pq3-ZQ?uta(rRx-1Ovxy)_W2NGR&SFg;Sw1cgyb2p6e3<H?qun4e-^V#Z-'
            'GdGXxz98<(<g&$s+yEtE%KIaGa7uc14Y8C))oUZxcP|ao49vFWPv<-PZ><vx0rT9%`4C9J_w*`nB2UaY~NHWj7T(Jmbw-GWS1lu^'
            '7KeXQhE-o!hO<pKW&z_&?>)3av%L<fFgy>OxWK#4=Ghjkpv?`ofVetz@388hDZ*1}m5J!+1<R7}W{OPsyW+-'
            '&ikYw`G)B>=kg)@`0=N_9rhq3bU)YM8?UlP)3Q=X`<e{J6(QS|eA(+g9Jb2As0rsrl|fxt2}@%KUt-'
            '&X_gw!2ByySsJnS^9RlEcv4b;TmLL0v71oF<n7#5CmKo9X*KVu*Jy_8Zyge%`ZjbwjEF!6M6H)8;p;XVsVJwsjT_0{T%YuXqJ0)N'
            'HOg|nl@h<GC6elLd(M2QTZnwEU@AiFc#{>7r?;vBVdnCJ&~YXAVJw^RtBe3Y=JLKK^ly6=4oReO}u4k@-'
            '{m+OXt(%)M8<D?6k|+je`?0Z;*K@$~?8W2;_iGFz;#eJwLZ_VR8w^?hdOhd*Z)Y_DmT#gc-'
            '$RU*T@20%rF2%px`!=5`m7VANY8vh5Qf#qX|0=Vn}mz#*W6$uL07Qp8;gDQ-l)g^1Z2JW@v6=C-Z~Z8XV=Ii{E-'
            '@Jm~<J4=5_(ScY{*+iU7xJ=a|lx8FoD)^0NxLs~HVDxcX0Z8qz4&YD!&TsJU@9~vdOJ)>t7vUM*CmiI`Uxk$;3C8jJ@R517Kw!ED'
            'OXDY3hFxFjr9b2hRp<6NbGvBy12!HwXA{PN0T_n@1B~D{xDSHqtz?aYC&a=Kd@JcqV#KSp$PGtO#q(e?xK?{UA{ITM$d+uJ+c|s}'
            '>|3@pFvd-|ZincG2%HGopH8qyA6B_~bA6ozX5k`659mCB8*zqS>Sa|xqP2QCj=jZlHIkbsC!g#L>Jjoi^=1n-'
            '@lm~+7gpzii#X92F8b3#8FN=q9>JDg^SHMnfQkB$WGLL>l2u<p8kLN@j3A2fCwidZ)Zr6L=Vs=^1-'
            'N{`^>8VinLGQaIkzSRoTenrZB9F2b`}{aiccZ$Bmu-'
            '2z%3idZLn$*nqc+^snAfIjRX^PpzDz)F2vBuIMIp0U?X@Iu>#0D@)(J{p;VA1rh11XHQMh7D~#)*LuaV3VK6P6iNKuBQfP5O*`gG'
            'KU!{CdC5x1>ZLLG*+$?gH_{h@GSUGE5@wEn=Yy!x4llgnMQ@~S^Cjfu*w+Fwxe(T*gxTKz3G@LQQRMakZ@`m`Go#7z|k5YfoikfG'
            'BRt1%iTgl2Z^>ayE^@QeSFd(>u#BLRZQj_WCqI!B!sS&VC-'
            'Qzr?vL9Q^lQB^?MQd{CDMG%vdW0?EA!N-#ehAqy7VGA_T&AGwFf_q|6{AWt<n$8J!aMO|{oF*X5Kj((*>Rj)%CS_-cpeFe>tC>ct'
            '+_3vYHOMk3Q7R-$W1jOe?L8Lk5XUhDYMbZNW^FlT-'
            'n=Q<!tSs6@#6YN8FUnyoD+0td|K$C_vhyi0lF5IJTJ3?+OGyaKvBV&l8{mEwDjyZ)Plk0*FyI6C@cWGk|g=fbcHv6eQptv$+Zvt%'
            '?w+AdHBy7Y8k27u{Gnt;f_gIH-'
            'NGbF$*dP;(j-g+dVVRl0whGsj&?qOe5#1@@VTTwnt$m6YDmJ5nv~qP{Yu2Y6=}9ulFBsu(*MEM3-<0OPSjb%ndwYv>e18!TC-'
            'oG6n596$|mW9T2<z;RZjg*0H<dk_Bhv`$eSI%ZR;tQ{RX-Ipt`4n;1f<&ezFNy)<&`1A;_7n;!tTt7SEI{L#|rp(Hid@z$0^i`sB'
            '!L|h1f=#(9Z9#0mCYFiGlpgvR$P*02^>mY<E3Q>{z1?OPlHNt$Mi(SLzL8{dogWLZM=SaliWq>Bo~9(>`sZ8ke$ad7>fy^bdY`_i'
            'zrX#5=Wo6H^x?0c)?ePd@$*}M{pi-4-#L8shtjz~C<Z`5%u`-'
            'LZyX#<=_FqA$p(Yln%?^T(+7Y44jbLypL&`N>fq{2w}10m?{_a9ym0m4weLDqwOlC1j2}gCN>bp9AMU(!X$%#Qv22F9q&T=qdnHF'
            '4(iHB71q;@h8`D@tSZnlWV~%KW_r)7wDO0L1tu5x@(Na^aHe)S+Od{y4l(q5#Moi8W`y`c&Mx4(>dR#(B$pp_}R4^q?62fWY<^b2'
            'y?rH9mn<u)bEhk3=@@6Yq$J#u4nbq!q;Uu{gY6>)BS1$E`ow4ed)hNo0h}h3e%oKUu8)vnIquRZ*SCwKJoKQ0J8zb~A<y#sFmo(2'
            'dj3><j{bCqq+Quej=ZtETyh0e|$p8qQM5YtnPOY>znBASJo9fTB1dbe+F?XEOMr!0)b~~B0psyjGEgFP@Ok84=<*IL(wKTLuG8eL'
            'N%^0TUL@<$+);AIIyH9{~wlsmWm9XEroJME0>S@>AY_J<mBo$E%9|w2J*Vj$=*+|ueGFq!cfw|4+jW4?CEPQv$cHO?sgQv#ha<43'
            '2%jqX(nV=7SF*D3`u1ZN9pimzr5K6*#m-'
            'z%#vsMTkBAdA*==cT*dV^aO#Pz75gU!ZG^SQk=3wXn?ZL4q?!+oMrhJkH+Rgl51f|E%sZBOq^QI`nxFi41pS{&{&@iS(gZN^-'
            'S%imGZ1~`+px3`PdEBaYnMVS(`YzBT%cNe3Ud39mK1qd@NW`QIUO#u_6J_q8vUT-_jss>+^-'
            'p0<8O`K?&f1o}}+%%)9gH&IS+M6bpHz<`5Q8S{QP*JlcbR;Mxw6;Wm#qv58<0%Z4J%(aRRucJLlmDg{(nJPH`xu9%h)*;1v%5{OG'
            '5Hiyq|6to?obAK;?6apMW!;q$wx8aoq^q@lppfgHd-'
            '_@15>y(UOzo?GVh;pdswX70B65io#}V^J%G1jWUF+aA4FA=ErKLU>zuBpC)Wb~)DjX1&YO!|xgZfh5x~`7-'
            '+uXbNOIk$9MA5X3IGj!7=e*J6+_^lyKq#6>0FJzIakL{6gykKK^|6XU@!syOWm_ZfgsgPMQlD%Trek)pm?BNXpfZzeoq~h_Bnk_n'
            'Mr4kIw&IeJA$r5upY3CZqrW(X@?QYqD8%I&>w<k*ttQ5nX*B}i5U)<frv2*41Jk)vG=<_-'
            '}>ttAjCR&^$#~c{T!{wNZbWDeR$)=Tc1CB@X|-'
            'UPp)a4gxP1d%ZE^1a!Kr`Kj}U9BVD(tHEV7RVTMjumk<)Ctz8kxUoF{L(&s@~xpN6j)!zdL<$W;HppY5+m)l_H-al)ty8Lw;VYP~'
            ')25Do%NCbO1;mw!PlUmTz3G*xg;a<1X>ULPMAxpSRns4Z@g_$CXOA#710T9lS9=X}x&9&N5wYF1Y<gUO{NB9^kvRz{BqRASPI>d&'
            'KsIOVkHQ_D|N^mGCjEiv`ngY<W9@can%79p&GfcE?F|1k_(lY_ZjRO-'
            '|9q^;F6~PhY<Y39g9s1TpS7@GzBSc!xpbUllLIXA+L^H)5SJ(i6K!^&+yg+$03m}26gG&?TUM3Xs&FRr7$&^@!h)o9QBe-'
            'T%0qEM{LF9@Fp^|$W2aDzg6u#Uq!0u>n!=-`V#Aw7oMu0Ojw&AW-ujaG61q~t4%JPVZ2oJviKd`xxiLHqdnm2zjI#GrfE7Dw-'
            '*bJ#u(N#{u1}e3w5!RF@B5CcS+0tg2l&#Chao})I;N!xYYd-'
            '1ITDz>B=2o>{US}p*Rk(MM2_t=~;=dSv4u9<O88bu<R<siif_S2~s9(1eTi6hsMmuBUtWCf>P`*(wfO%b_&V{u$^*ef+{hBC~!md'
            'oCF08VjW2eTi+?&yp@j4$j=6==Tmru^k+D&{{cN<^?dL@UfF-'
            '$gWUa^98q~7O6n0tg7Xd=O|a1G3Qia^A2atz|oWPMS~c{0W2j}*2Ox-'
            'I$LPPKqgqa78OeD1KMCFvXoWAgD4`X|q#fiOlMfU^<R>n>v(;rTna$en$)aW2Y7=KY&;N$ztarpO?@kKXTHzl#5|kY|SW&y{4)N-'
            'a<+vV#N{i-InbRGY64@V`j1bE#*2pG*6}4}M?`tM}g1w|@J~%@04uNU??@DT9_y7$L&wTwn)>IF*R9sz_D%l8u<rI6x92##(-'
            '5Y39e>&^a}vTQj5ojK5_BwWPX)NWE2`MpxLQZuj?C)#ZuN@f9A{O&+0wd1RcLJQ^7FbBI0ZaE9&}g+_}`mR2VR!QNo+u1MEZ{XWA'
            'nY(U#9zB0dk>fl#z06#C|%djPKqK!z3MWfSAwO5^9v5YaHDJU3b?sY4XMOckMV$bf++$1<Q4Ixn#N`;*_s0<CdLPYXN1$Gdk)b`%'
            '}2m$cBXMrySCHk#T-'
            '%_dw8VarmOJG0}BtAaAwrqj8mng$4&SV+N3{*paepwgph{<Vz`9)5WyoGT93xRJymZ*QZb25=Fv3KBK5LP2g&UTN*tEs!0GX<R5H'
            '!iXCxP}H!D^GD{)jXr>nvo&1dM}D@gxZDIQZjyY<;&T?4zeWTTtNu4;)b;#X;b#1+9>is;u9AVJ}%l3Mf4lb5^bV=78N9tD$KG@j'
            '6i7l6C-2z&k6kJe*EY3{$Lber=pzh(~TyR%HzJ{&RA?fg7+tR?hOB$l;V@u9RGUs;oW`~Ec$-'
            'YyZ&RQ;5&Tfor7OL%lzRpN1KUw!a7)Df*7C0Z6@sJ=;|Sse<EoO+dthQLJNNfK{D^1Xy7YSl5uo+^{)N+@Tb25LUefJ8n*}e#rGr'
            '-6(Le~*<cFKv^#Q$#=@Ru!nwjs)K~{={lu_k19;GjA8^#eBiv14qAKYE{}@12$1&u7Mn}d@9zTBK=##wl{xfjN?!EI|@0quHzk9R'
            'y-nE+_{^0h@*OSwuTyioVq_K<|=_-<KyuY*R6Ys>>72;JKcGo0wqsz57p#cp~*Bs7>Pb@`v#s+jBi|a?Nqz3V2Mf<_(-'
            'own~stF853V)F{UcF$o-i<eM!B@RzT&#k?W-'
            'VuYMemGeGTy<^kx0S8pI$$B@jZP)`cyOt1T)Q+0tltA(ZvgS;h&UYU!)GS!F{q!qM@wx>9i51`kA)+%vs(v(U+51hS{tHcVjkh@c'
            'o*^DUE64!!a#`NA`vNMmm$<PpHO*fHVsz*VXIH6!GAtXK&tk-&j)Q;Do1Tc32nNA)K-'
            'S+@<?}y1TiRYv5n)R*rV9q3$D|uyJ*IhSNvk6i&vk1Nei>z7iQToI{gt$<nM$j}r;;D}>K@@R0NkFXfgYzy-'
            'v&@ZFIthSFTot<E%8ZWy>d63a>3cF9(a4H&vW0LBPgU~urF3xVD2763_srDw34={DuILW7lXIO}WYL7}}fY+|&Q6|3yLk_^E9$j`'
            '1Is&^7B>D~rRva(+!DNVvAhmYHxd;*dwn(M;iehMG)>?DdA$-Ft<WCXfOjI&Q5rN2Gjd*f%lKYs_$Q#ee2_X~sIx-'
            'X`j>ZWTJFy+`zZL_<{>X0PG!*qw7j}aUaxw-Gk(7d(+n;TY!EQ3u0v^x?*a|TjM*E=a+)9ze-'
            '8C<S?F4S!X_l}ucbM}2vmLl=~?Ry6wUmuJ|Q?7e*LVON}KYY{>-X8yiF-'
            'Z#{>af4n8ufYi%nP&IVS|%FjcM2kCPqj%qP6yJs}q)^7~%_n(Ix5qmD?V{hqkDEu5Iy08(}$=p)C1ljE*BKgl}qF)(g21{|CIxo*'
            '0jOKvU`c;Mcu(zu&ut+Y=}J;#EzOgi||<b7@wZkS+aet+jzB`-'
            '}~RR@m`Shr<;x1%5+7fbAS<@9@WkxpPzD*)wNxdX%CJTax4C=9d+oS&v%59QP#Zr6#rW65c_|x{@saHJUl4WyhjQ`^zZEGB3A+Ay'
            'xRZM%cxOS)UUHQCdGb>6^|Kig;>B_hKuMh75@&Ev_zc3M#{}6;`1=N+||93?A@L>YlMc%v>SZu?&lfoVYKOVem5lgy?Ji*u*nWEC'
            'K&C`|#AnAZI0_n5^OTu73aEoxk<o`-P0Fm-N!O%Qzx;6UR!%Akjj|93jF8MY-ZZMJAj!L9~V$QR3|ISBZF3M!Y-'
            'TExK({Oq0Qc97hjvm<+O)6<us{{+_PMJp)^6h(Owmu0Vk7&OmYc21E2Tu!2w0?eD(D4h;}39=`oq3Si~kXpm5b{o%r{G8QasvSTu'
            '0I;D$cm>Hlui^!FOne;N_zF28~dcnaTVjLJ^)qqnO3M3soPs)fg*x*CLQ($to;YJ7+rOGa@zRSg3yS1oZVUgnLfFOFP$e@g~$$BP'
            '3LzoJfVi>n_i}$FqU|?X<&~aZ;QuVbWNT!-+E@4J&^A%2uIMF>&hp`M}x1?1#;8roNM-c>nFOHppgDfYSg8Q^C-'
            'Xd(AB)fDN1jom21EhuEEx1aq_ROfIDVz%Nt}vRXbl)srid?^dWs}7<$9$?|>?Vsp*>OCo%wv`|P#!rC&J|M><sW+08Y+nfiP_=>b'
            'l!UtVwtj|pT(fZ9u@x?iHy5x8IK)TPtoH5tIMuTB)X6zajxxRr`e(`A@21}Cc)(+mzR3FMTq%haM4ZB=Gr*SVn1kW%C-'
            'b=Ya;17QthIl0NQQx?jYeVrH~!K5`l{i?hOF6#+=C*#pg`BQ4417aB`xlL7*wh20@?bZbWo+kQSK)GN-&n({-'
            'SI;)o`6{+Tor00_~hEn@(253jJ?-dT5Y(RpApjHYhdqU<b9Yl63xy$0!H7JgWQDig#-'
            'fRbpZMPcZ|EYb`?V7fwHqpq7ABl$25ZctS~mdEJh2zSlfuYcV8_?mswaojK2)WjMVH?P2Rjv4jE!X9S_(7?0{i1{%o^+D>E=kSq&'
            'Nr2d+24?A7>4maGFZ0`FDAGfX80&Anwr>h@rN6lA0!5pJz<B?8accIg>&~zpYA|zigf4ZjUQw5p49)~|W#-'
            '4%Ac?XIAFSo1$edcIL3RviVjGXfI{&k7Rs#*@OL(_Rx#YkO<J;w{`i63yNcy#@-'
            ')#+}!np;_8P|=J!5P$%HSLHE2FOLj*4m%G<h#7^^hpZ5tZhNIsBuWb-sJ4+=y)D|4Axl;7~Z-&ZL(9+l;xR`Ay0bu`?vq=joUAN-'
            'uw9XX}c;JLj8ZtW%cf{#ykr%u?A*{_|?xRN5>bZ4lPrOO7cM=`0QPMt@q{+d(XcF#D-'
            'bR9Q^z<a6|B>FS(WcTDHV&v1p!I{cB^jC~=xyB!R_Y5(y!3e1|<ec^YEETPc{^GY`v&ky906A-'
            'Qk100;!@XW3S&W|Q_Gtb)_@V<N@Gftx`HDd|_m>olVWhrPp5G98E{5Na0t{;@>P0|!e1<|U*5b7d>(+t`w+e4$$x$-'
            'BOJ0k3nCBe~CH{hWmVuD9bCz6*J`g*{_3|3mkn8m7%<>O8!)v-'
            ')NmQJf|qm318e#(&U+H#|@|V~UBJ)Y6R$wS)<FpV>*1|BX?O0g&nVGm@GlJsJWtlO<~{DWOz0)_VL!+i>_ui9F0y4l8zUhZQryM_'
            '<bZ%}Sz=Wy8NbjZ<0*r@l5q1Lt!h6LFqygQE2(vz8gTSyJprY-'
            'dd4mm@?9>y|abo~fziVrk>+YlI>!{_TWva$*)YNw3)$*mKGlWc>lgppPS$(nCV7kxKzbz^fUF-fcS%W|oyO-'
            '<Kge(wr=Z6j9|;FwH|V1X`lMJ)T#=QB(J9-'
            'gebgw)mzuBpACK)l(xA!Gb$+3`Hl1qqv2(o6U|mU6muI5_sRWYlqqw8cpvj<TPqpULQ2%VHJ0ghGWJ!(A5G1hDNY9oIYABrq!Thm'
            'u=Db*^@qg7Jbt>{yUsQQrs+^fRfknK=bRAzLi6E=o__haLDWz_^N`6#|pZod~&V#hJUX0P5J7YADG{+UE1YPYZgK0+O%4NQ8`*|S'
            'vqXh)~@W@-$xP^YStSHL2KZ@2Dz0aK^LWLqf=TUhnKKfD=^%5ovy)|ndOrGWIG232`tj8-'
            'V<kFvxhIUM{AnL=vUBVw68sR|Ikh!{I~Rd(QLw)dAX7Fo}~_@K&>If!lIt4RR9;nXyKY6yf;ZLkrutc)CO1wAEsNzMkw8~S`2KT+'
            'ZVwa18>$L84#RXQCmiW^%%c}_fN?6i1AE>sga>F%vfRrQp?UbU3`+X3AU8~KmLq2n%f~p&aSZxA#6A$ibPCtA@dcUB6@;FPA~C1A'
            'b5F_-yD&5{6dq^7qb_0%%w}IS<*@};=<AdBkFjaz+UsKjmbl{dY{>mT4T`=+oW6y$z8`}7P=3L)(oN1H{$Ab8Kzlxk~mtPX*C`=i'
            'eRn@Cq-9^=@b{m^cxS~g*Se3@XJ><fwRkLPe^k}?G*xrGmR02lN@cpbkR(O2HS5-'
            '(6+GRWLTSEM?KaITop990U1T`@9f1HJ1<Te+8&X(I;~CyCboT89S*2$Y|LI<hJ3xZf8Klbt%D!^s`uJ8h<|f%^$!Oxy{#}Z-'
            '3+HzCDK|XMQv=;clyMgye)GYPPOGlXG?`2vpu}DTg;#m2c_UwvH4UUlwok=!E7%`!+CsfJOlJ-eRmm$FD;B)BJ^Np_#+N>Gf3B6n'
            'O|G+zRajd?|gpyXYau3>*0}{J6$cyph|m;P14>Hp2s2k$-'
            'xjJmZ+_*8qeFo=Ul<&w19%Nez18euA@D<EC~|J=m_!$bgHTxYV1QUL0z-poeuN!=ZX6Dp8Y;V7wF@%-'
            'S;wVZa3p*EU?|Y9wT7Y;g)hqX8Z*Vxstpp<F!bfJ4NJS``bgMhUQ_>{oJau%rtgp>ZqiXXu5;#Adv`75Tt)!?bhlQ-'
            'Zl3HP49V-1{D@^DMoft1WI-ZCvi!yl9s~Lk;5)^O)<)}dqo{mt*j-'
            'w^K}^zghv2Q;LPGTk&cgc*fc>~<mC7yoECv;1V7!JbwGlYPLvEE-'
            'm5QRBp#2&<ryHTge1Iqo6z$woX{gR11c24rK!ynKtqErt=4Wn&2=4*jC&uybO3u#_ti76!-eyxU&NwebQ-'
            '3aU@q5By~%GG{TEIc<cV<>IW%&EuzjMEkvX1n-^k`txI+0og*9~Mr30n`9EM`SG-wEs)1LLn0Td4tz?CzdZ8yPan_1lfi{8OoZ;`'
            '(OjSPy;+C0xqw{fKb``6dy_EmqawHNQkMObr^l3|uTsQ=Aod*AWC20Y__fj)@N;3w}6^sYQ0H6N?g{N>^`P!x4SCAF})T0R;&nzg'
            'clT0l<y@U%u1S%GH-EbzX3_+Y}w8cPe}Tmq)W+MxI+=YU$Ee(X?~DqafPU${8CG<{(zoS&PX1v9#EcJjiM(24O1&PW3hfU33?3Eo'
            '2#rO;QT%1J0Sg=WpTW{P&mrYM%y3Gy{`4Wb!L@Evg<P`_C8MQ8-'
            'Gwk0)``PV^Mt|lz11lB&%B?vN4dyPQLJLYYudN=}Amh;ycv0!;g!~aB%%NL93OGPg`o?2xXfn`OlX>8e*i$%?RQoE<~`@5y8)@0?'
            'plwhN+V)R;-lL7&S3j`BU(1{^zGqP$DXp(ie;LnTe3N~r$twRF;nMlsv4H4-'
            '*>YyT8{7jh?yS!Opks5bSkB9I?AvcgPfZij9OC@?-jzMskv1}zYzdhXi?DK=`A0Pbkd%YVU-'
            '@Ne*GuA=p?3<td$a{=jfMO4NDvY1hyiGBaA({50(@I`T5cO@?JUIKjm*eZ`aYBY87Aq-'
            'Uv0MNU0fpW0GOkpEiZ`V!M-7k3b9j#{eFfb~2JHxf@3A`&!Q6vbjv4FQ`vBqxe{lHR)q_|6G|+M0PZ-'
            'bFnxkVvatQV!#w%z%J%;$5j(f;(0;mb+UpVS3#y-s2aOm-dY571m8zY)<A}}m)6dUk3qlpB07oD7dw}Oi?V4*ns@vv067WfIO$P_'
            '<#LLxk2m^@ak^i=Nn!oX2hYmlXhupbPXqQ+LO4f0rSp*j<S#mB-'
            'VWNJQt{=)p!!y)8tRyHH5vZgGM9SX}N8m1}=nWJ`EP^gPpXaYNlmZ+4Nt|Z<Xolr-deiFrc%9<KwGSe4MmJ3V)VXZy5KVUj(c5=_'
            'znNp1K8@xSKZI&s%OuW(U)apfW1p`Y-'
            '3j_?EG78gowO&@^+5slsB|yhk&#V~ery2ilw4xPA7@+h6otaN<#m%^B44=6P0u4_{oxeuxQD>*)AAzY0IY~$MdvLxk*$iJ58lv5{'
            'lM9p`+k7B3H6Sy{%4TtdD%g;io@B(0MiT3oY~iR2f|j8Fqc<=+ch1A?XPce#=<h6)Yp?#{;JMFwSKsp#6Y4?sQ%_?ybzL!KX$PJM'
            '1o@k*fEGDadIA+EH_TOLl*rgV%xtD95@>?k8xg5`(ZCw7DZCK`GNMZq1FOPx#{ANSSf~8l#HoXeL{_@6KCJ&CU2h_g8$T5}%L1mJ'
            'mysbG_Jbgyf-y0eY=euG7bFd5`FatTqaV%4PXVAH6iys_;cRn33yG?SV#T1RR+f0a;aQd?GhaN|RoAOzGX-pV3zN%MkOhs`r8ypY'
            'm2RUgT!PWpId@mAR%xE<4i+mJJr)kyxI$Ysm`E2pfD=@kd%(<_+g5`m{x=zSm)Wxu6||IEiD<i|)so(p@kSY<I`gv05KIZ{ynZoK'
            '1MX(I&TP9j%JBwHn01r8M<IKU9<J9)$>(b_3V;7D!uHA)I`L%;*-'
            'PB<moZqcHn9I4toMiu`SM#|c)VUp)KiYp!%fRp>#H2}Zm+{HBKX-LAYn!Y|C9i~UxwJeeW3M4K}}*4(ROeupk%WdLpFSGGQ$8L#S'
            'sUQjE!I;+F?(o2uzP9z>b|%$%4MxgCqj!2U2hGk;wvd=pFp}b=a7;EMkz@#V*P?Q0!vK3UD?UWo-Q-'
            '?K5IFfUMx_)AQi)2j;upxvBG$7ia7b)~P>WivTSEmb%n((&+9&UZhwreSBx0{R4pR=10$YLV(F=Cmk!j&!4&d`i<W8=MR4N{=v2D'
            'H$QttteaY@bk0hKY|((5;HOF)6mZ--X2a&K<$2aObSb<r`FOZAH#ZYbE}VU2`qEU0Q2`dMOv&=rL#7I;nwvYb{xmGtjvy61ssZH@'
            'C8CC!@J=P6E_C@1$ZWVsVk+;}=htt&j+oI`3_6HCvMu-2v##sjSY&-NR(zm1-'
            'p?z{HPnIRpKvKtY6^x#hOvu@H+QLM00KaFO$=p+40q;~m~z2$&1_&@gU~(=AXgf)D8HdZq?I7?2FLoC{a|Y&3K-'
            'fX{SZl49$6b!tEBlMf%C)~oP;Q}5!0ZAd_rF*Wjl~+PrM@+?;?!~%lc-'
            'V@IHe(!T{~_l8t3hi@YPbTHyeM85y5umg$%fj5uw_2rzIKns#H^<X!wHNcXv^**S3x<wbW%nx80c(|I?&w?iCf*@F-'
            'WVKxN8uh&{AoXYV55r~+bnbRhYeIk4zXDZ^9mK8p)3?4(mwN-mB{P6IT{|Ef}$#VO9X`w>;+4`B=D=~LI3C5bsvNUzdh(#+Ytepn'
            'r;F&Q#iQCbe23vqU4mrI&?ktnc9&c_Mmys25xv><faf>4_vA+h`h6dFZR-'
            ')O;s|8(k4L68p9pqkcL~hlPxS_JD?5%gpZM1*KAi$*KLMWiv5d?)1o~30?jA)q}v(^(DHT|GY2vBvwV;m3t)6bi`(P<y`oDo!dKr'
            '(rkrvMj6vvVLn5UpiZ2Bfy~m7x!D__ZpMY*kT)8wO2w-'
            'd+S<8@em%N3w2Ycy03M5@Wd~^{Fw)E@4VrOCv4Fpp0z7Zfv(cc(?c2_gn$V>U4;}2=@}bNQrzv;}+&(6J8=RhEu}tIt5aiWP3}qs'
            'mYtBGy6tc`!?(#6=+V(gwB=Bw(bO+Ogacxw_CrbC^6UGJ$UX-Jb4`6Ox#G4*f&GXuJL)AB1>|5eHu6lucMB+q@G`HOK1<Dm5Vv+Q'
            'f$WL2rQYRX<$Q!78zi7V6i-i6GI)=8t#7*i=|&yl~%IP<n1r!Om-'
            '^+bB^hmfN~emU>77!N|`{p4}SHpc2ulV8g%z49IA2$`R?0DRkX6#?bg6_7XCR2Co;&~_KTg(R-'
            'cCTcri{_QXAk!sjcpSG{ZHfAaJN92e8A+;HEXUEHQ(;0JOoKIXE3*0L&Bu<N{C1&z$x~#Z0w=&@jX&A6Snkjz)=wGFs3Y(PPz>O1'
            '=?nM%ERA2RaA%GjGjiigaqrcp;D@-'
            '2CjdTYr0rOUPdN7=&nt|NYtF>+diTLqe=TM~EiVkSi3D7bG$vymt;KAzrQ2Vit%`d9esrW@mC3VN&Y!wQ{9w5ET%`#Ulnw?Q3tG&'
            'd_m)Hvo4bgf)y4v$AOch2YfNm&`10U)tT8A<XsZBi&{hI8a*%!7R%_z{*7vLdZOoxLl649IOOMMhDG&^opuElEcnI5uYjR{UCGQ6'
            '3h|QblfThESB;63fbOjor|TXJ1<-'
            'K^n4cz(U}DdLx$oOVyR)%&vuL2BH3HdP#nnd5;%wpLS`kgL9_u&>lnL95z~ql<LJ%w`7K}|dBlWVYZq(-'
            'rRJT*E)&1BHtm4?E|lgyD&KrU2Wp?irNFg=zVQ#ADXnG!76p&w0(=v~+yY5kHR=e(*x<P1GW!AT9@j_7%CEp||4(vY*&&?ek1$_A'
            '%r>KkDR&q>FoLv_r~>DYYJ<_!BgK(G>|bU@as(L@4}nl(bs3*gzHikR62EeVhd*XFvL?_*xB{=`FnSpuOY(}#bK`8rTWjr(70w;I'
            '9>7qEjSE5~MptqpN#Ou%nl5dCNI70wD8BOI`^=-^?3tOfk3vw`V1TgoW@2uqKqvu*2TKx4gUf;r-'
            '+r$5*)!|_VZxxp7vAmt=DTq10e7z3KYbeXRv;d7OM;A?2%{Nx7!=ptOdMBFc#x)od2kS4oYg^`=!e%_t2g6>7@gyJ&JJhw#Yzm6s'
            '%_bye*(fU&t6<Qf7(at>W})#A~TauJhm|X@FPp%nT5H>7N-^#!}-'
            'ajN2mhsd)<u#!Y%<Hx4zLSthPZILaKlJaP5Df8jOnj{J%7PZfY)EfSBUb3sV=SW|tP#iEqlYjT2A^g~;E@FnOi5;%|#U3n7z6ZX|'
            'EkcIsqXZM04BZ~y)!P`Wa7hLFSuZ~qqJ6)+cS?!B&I`v3dX@8SP3(iE&?3A^PM?e{{Y!wGppwtojpAOdjT%@Sxg<B)~Iwk*6<bjW'
            '0j@-'
            'PR(anhCHlcvRAo){fpaduUynZ90zc19bIOQxf>p}e5bMPXn#Xf32&qSfg1wJchTNkt3E8&y)+?L0`1>f&NLj_X_r^W+0eH5_1Qcz'
            'I$wGFLB1cXIwBLYTNB>7={Nr29}0<hL>~QV_6$qnY3E+m#lI;UAy;f`#f~$0f!-'
            'XSXi8Z^@WFhc~|GlyW)t$sH)>(s!KRF6CoEJWfY6pkCT$+#d+j)7Q$@nwT3gDgJaZ1;)_<ZKU`JJH$@yO*rdi&$V@Mt&KvCtf^9&'
            '5akF4r2>#R9aHxQ60GRWX3A9bh0;YS;s7X?Av|U?uI(VZV{gL2L?rrH^8Ng7gS$DX?)H!xc<XVo2W>94<Cx(Vm{#6?>K9;bWyIAT'
            'koOpj@6eet-8|~d+}sib<(-_LpE@VGI4)zt6qXItHn&-'
            'toE%YPC0tSop0Oae_oS%sZ4jB|9x5$gzWje35BK&jFJE5C1^;&6<wEf*PyYKurImnkcH}*3FtF2RHjq{_*O+6){8uNw@(}Pu0GfY'
            '%@(KX)AD=*Kl3)G(si!ad!9PBE?(a{51?mrvsRZm`!5#7-kvaUKB@mL{4)`8<3HT#45~4@HXo{RLx-lybi8WZWNVuu0%o+-'
            'n;8Mpwv$)2hEUa0$cyWGyZeeNaT=>Y`;?kmI<e5Qu7(>8hxb$%#o0&l+jFoZ~T`#IN7_KKPdT8#QTMRrjT&tqylW+xBjs;d0>Qv6'
            '7fHoHSyaq`kcUXG(qz#GY$pP6vn3$x9B1xDVEHRlfJTx&py!?&J@z)-'
            '_yy9G?mHYg>2*ix>B1>jwbcg#N%2*Pp2Ls3qAJ>iv|71jYhpP|2qAEFLpG5E^R>O9SF|Y!f?n>&05dw(G1PP`Y<~7hoQOHF3D^xy'
            '10NBdFy&{TH8<YdVz-'
            'z07+rq}_Ht&nw4gV`cqOwp$7vZEaJr)D>NB2$OhtF~SDKl3BtSd}$?*{zMm<UNn&@~3gIN5+0+mN@7FLLh9z(5N)w!OU#xd4Fihy'
            'Q^9Xmgn2WDK9VG>Q$Q!o(DehfGivo){g?33(frhNGJanuM=pM#oh4{zCLe*%O?xG4h@}HimL{<&AyK%Yj?P=xCqA<Myjhf!fiVrz'
            'v<Rild_*hOK+$uebmBb6qmdW!#W`57g4@Tb4}EF}<4b03ZZHjtlD1b8)i0-'
            'bI<)Jbgh!5Hh%d36+$%o`+=l$!7;IyaA@HnAiH{x8x-qD;6OYa#-eVLD1L&E`EX5DDN?6u@Xe<MCPUgT#b(|Gxb)<=NH`H-'
            '#GmEbFij8`0Y~}&FWG_9@t3Z<JUHtHMpddaw_IG=%{K1w2)`%Ec2R$8SR3S79L!D;^Si1@4vov``K$i)((I8r^7$~kPY_sji29o='
            'XVFMK836D>!%N2cos<C<h1O^yZQNRhcCX&3P47LTc5oJWqKdIfBWSh-Td?gR>jZjA>LddMA`{6Xuun|wmc*u*8Au$y=(9BwYd5c3'
            'y%Zc-'
            '2C{Dprk%{{i+tBACMyv#|B`B4UrEWVb733O@XmT*+htCatU8t=E{IWBKapPkAHCBF=3<LJBTO*4M?0aBUr|u5n7^9aoP3xUf^8QZ'
            '=X8&)f)~2A=mB?hU}ZO&w-}3B7(Fg!h_S`@r!-'
            'c*N#wGhMl8{R8>qZ4OZgsesJrvpY)!2!`Mc!blRc;j%jzUV8~23n$9s8A{Siefzlf4J>UHBZJxs8+Rs#W94&$(8?SjO<nk*fu;P&'
            'wKYE{8zXLk}Gw%KH^WHOmx&5=Z58wJB<jTY93CR_*2H=ok-E-t}>AbXBE?W$mtfxo)y7}P?RsbpA6z>WXBUi{y-'
            '45S!=tw(6tpN5$EH=Uy{zIw4&<q3gVSy_+F9S10gOy{|Jgif;r!(G~!$e)RP9K64$)eW&sNVjg(e7#!O!}try4LQtI(Ezc%^Np*K'
            'X~0pv^GE=CyZI-'
            'rsmFb1AJ+TuOoA&UA{dcxFr*o>?`y2K_)#kgrtgu5@AT;0K*VZ-!SARfNYN~?#6Iwo!Y5kW@I><gJ9_Y0}ih@vH'
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
