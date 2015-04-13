#Laboratoriniai darbai
Čia bus laboratorinių darbų aprašai su nuorodomis į konkrečias kodo vietas ir prezentacijas
##Turinys
 1. [Pirmasis laboratorinis darbas - Rail Fence realizacija](#pirmasis-laboratorinis-darbas)
 2. [Antrasis laboratorinis darbas - Caesar autentifikacija ir autorizacija("#antrasis-laboratorinis-darbas)
 
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

```
##Antrasis laboratorinis darbas
