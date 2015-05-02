#Laboratoriniai darbai
Čia bus laboratorinių darbų aprašai su nuorodomis į konkrečias kodo vietas ir prezentacijas
##Turinys
 1. [Pirmasis laboratorinis darbas - Rail Fence realizacija](#pirmasis-laboratorinis-darbas)
 2. [Antrasis laboratorinis darbas - Caesar autentifikacija ir autorizacija](#antrasis-laboratorinis-darbas)
 3. [Trečiasis laboratorinis darbas - Paveiksliukų stegonografija paremta prisijungimo sistema](#treciasis-laboratorinis-darbas)
 
##Pirmasis laboratorinis darbas
Šiame darbe realizuotas transpozicinis [Rail Fence](http://en.wikipedia.org/wiki/Rail_fence_cipher) šifras, kurio principas - raidžių išdėstymas zigzagu ir nuskaitymas į vieną žodį eilutė po eilutės.

Realizacija: [Atlikta](L1)
###Užšifravimas
Pavyzdžiui:
Žodis "WE ARE DISCOVERED FLEE AT ONCE"
Sudėjimas zigzagu, kur kas atitinkamaą intervalą yra keičiama teksto rašymo kryptis (aukštyn - žemyn). Šiuo atveju - kas 3.

    W . . . . D I . . . . E R . . . . E E . . . . C E
    . E . . E . . S . . V . . E . . L . . A . . N . .
    . . A R . . . . C O . . . . D F . . . . T O . . .

Užšifruojant tekstą nuskaitoma pirmoji, antroji, ..., n-toji eilutė (priklausomai nuo parinkto intervalo užšifruojant, šiuo atveju - 3):

 1-oji eilutė - `W D I E R E E C E`
 
 2-oji eilutė - `E E S V E L A N`
 
 3-oji eilutė - `A R C O D F T O`

ir paeiliui visos eilutės sudedamos į vieną:

Užšifruotas tekstas - `WDIEREECEEESVELANARCODFTO`

###Iššifravimas

Iššifravimui reikalingas užšifruotas tekstas ir raktas - intervalas kada buvo keičiama kryptis.

Visas principas yra pagrįstas atvirkštiniu būdu, nei buvo užšifruota:
1. Sužinomos eilutės
2. Zigzagu atšifruojamas tekstas

Pirmasis žingsnis turi šiokių tokių svarbių aspektų:
1. Gali egzistuoti "uodega" - paskutinis stulpelis, kuris nėra užpildytas;
2. Uodega svarbi tuo, kad ji gali būti užrašoma tiek iš viršaus, tiek iš apačios - reikia nustatyti kryptį ir raidžių uodegoje kiekį;
3. Žinant kiekį, reikia nustatyti kaip nuskaityti užšifruotą tekstą (jei nuo viršaus rašomos uodegos n raidžių, tai pirmosios n eilučių bus ilgesnės vienu simboliu ir atvirkščiai - iš apačios rašomos uodegos n raidžių, tai paskutinės n eilučių bus vieni simboliu ilgesnės).

##Antrasis laboratorinis darbas
Šiame laboratoriniame darbe realizuota kliento-serverio komunikavimo sistema su cezario šifru.

Cezario šifras yra paremtas individualios raidės perstūmimu. Pavyzdžiui A perstūmiama per 2 vietas angliškame alfabete, būtų A->B->**C**

Ši sistema lygiai tuo pačiu principu tekstą užšifruoja ir atšifruoja kliento ir serverio pusėse.

##Trečiasis laboratorinis darbas
Šiame laboratoriniame darbe realizuota kliento prisijungimo sistema prie serverio naudojantis stegonografija. Tiksliau, prisijungimui pateikiamas prisijungimo vardas ir paveiksliukas, kurio pagalba serveris nustato ar tai tikrai to vartotojo paveiksliukas.

Žinoma, prisijungimui neveiks bet kuris paveiksliukas, nes jame yra paslepiama prisijungimo informacija.

Informacijos slėpimo mechanizmas yra paremtas nedidele deviacija nuo originalių paveiksliuko spalvų. Žinant, kad kiekvienas paveiksliuko pikselis yra paremtas RGB (raudona, žalia ir mėlyna) spalvų variacija, kurioms kiekvienai skiriama po 256 ryškumo reikšmes, turint apibrėžtas taisykles galima nežymiai pakeisti vienos ar kelių spalvų reikšmes. Žmogaus akiai šis pakeitimas yra praktiškai nepastebimas, nes spalvos pokytis per vieną vertė tėra `0,004%` reliatyvinis pokytis.

Šitame laboratoriniame darbe pasirinkau modifikuoti vieną spalva taip, kad nuosekliai skaitant kiekvieno pikselio, kurio mėlyna spalvos reikšmė yra labai žema  (0 - 6 rėžiuose), pridėti binarinę užslėpto teksto vertę (vieną bitą) ir pabaigai pažymėti panaudoti tam tikrą spalvų seką. Atšifruojant žinomi rėžiai ir spalva padės nustatyti tekstą.

###Galimos problemos:
 - Paveiksliukai neturi pakankamai pikselių tam tikram tekstui,
 - Paveiksliukai neturi pakankamai tinkamo rėžio pikselių tam tikram tekstui,
 - Paveiksliukas gali turėti pabaigos pikselių sekas tenai, kur jų neturėtų būti