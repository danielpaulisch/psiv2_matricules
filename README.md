# PSIV 2 MATRÍCULES

Aquest treball consisteix en detectar i llegir matrícules de cotxes d'Espanya a partir d'una foto. 
La idea és seguir el següent pipeline per detectar les matrícules:

- Adquisició d’una foto
- Tractament de la imatge
- Localització de la matrícula
- Reconeixement a través d'un OCR
- Comprobació de resultats


La distribcuió del GitHub és la següent:
- Directori Imatges: conté les imatges dels cotxes. Aquestes les hem adquirit manualment fent fotos en el pàrquing de cotxes de la universitat. 
A més a més,  les hem adquirit també de la base de dades que tenim al Campus Virtual.

- Script: conté el codi en Python que fa tot el procés de la detecció

-  Directori actes: directori que conté les actes que hem anat fent per cada sessió. A cada acte es menciona el que s'ha anat fent i acordant en els diferents dies de treball a la universitat.


Base de dades

La nostre base de dades consisteix en unes (poner el numero de fotos final) de coches realitzades manualment de les quals dividirem en un train i un test. El train té unes (poner el número fnal de fotos) de fotos i  el test en conté unes 6 fotos. El diferents proceament d'imatges i canvis realitzat per detectar les matrícules es faran sobre el train i a la part de comprobació es veure si aquests canvis també a fecta a un grup de test per visualitzar si el nostre model és suficientment bo per detaectar imatges. La base de dades té un número d'imatges bastant reduït ja que al no tractar-se de IA no necessitem un conjunt d'entranemant massiu  i amb un número reduït d'imatges amb prococessament clàssic podem abarcar la gran majoria de casos i excepcions que están en el nostre model d'entranament. I veure amb el test si funciona per altres imatges per veure que no només funcionen amb les imatges del train. 

Aquestes imtges han estat obtingudes del parking interior de la UAB de l'escola d'enginyeria. Realitzades amb el nostres disposiutius movils i algunes imatges de la base de dades del professor compartida a través del campus virtual sobre el mateix parking. La ilumnació del parking és suau ja que és cobert tot i que tés espais per on pasa la llum solar de manera inderecte.



Tractament d'imatge

Abans de poder detectar la localtizació de la matrícula i fer que la seva detecció sigui molt més reduïda la imatge ha de pasar per una serie de transformacions i tractaments que no només possibiliten obtenir la localització de la mtrícula que sino també ho fan possible. Aquestes transofrmacions eliminen objectes que poden confondre le nostre model amb una matrícula. Les diferents transformacions realitzades són les seguüents:

(cuando esten acabados los tratamainetos explicar los pasos)


Detección de voreres

Para detectar les voresres utilitzem la funció findcountourns que ens retorna totes les parts de color balanc que estan envoltades de color negre fent aixì ens quedem amb el possibles candiats a mmatricula després iterme aquests contorns per definir on és la matrícula amb una serie de condicions que compleixen les matrícules al observar els difernts images i resultats, vam torbar que la majoria de imatges podem detectar facilment el la part blava on ens diu que és una matrícula espanyola i per tan ens dona molta informació del que pertany a la matrícula. Definim quin és el contorn correcte dient que el que tingui la part blava al interior dels diferents controns creats a més a més ha de ser el més grans de tots el que tenen parts blaves a dins, aqui agafem el contorn que és la matrícula. Aquest contorn pot tindre més infromació que la matrícula ja que pot detectar algunes part del coche com dins del contron però la part importan es que hi hagi dins la matrícula per poder detectar el números.

Rectangle de la matrícula

Al definir les voreres no acaben de ser del tot rectangular i la majoria de vegades tenen formes extranyes, que poden a tallar parcialment part de la matrícula, tot i que per l'ull huma no suposa cap problema a lhora de veure els números que hi ha en la matrícula, per identificació amb el model com a vegades els números poden tocar els contorns per tan genera probles per saber de quin número o lletra es tracte. Per això ampliem el contron dibuixant un rectangle que conté a dins tot el contor, fent aixì que no es talli cap númeor perquè el OCR pogui detectar bé els caràcters de la matrícula. Amb el rectangle dibuixat serà la part que retallarem de la imatge en tonalitats de grisos. 

OCR

De la imatge resultant obtinguda aplicarem el OCR per fer la identificació de les lletres. És un sistema que consisteix en detectar caracters en imatges i pasar-les en string. Les diferents maneres amb la qual fa això és comparan glifos que té guardats, amb parts de la imatge per vuere sipor trobar o no aquests glifos. Aquest mètode només funciona si la escala i el tipos de font del caraceters són semblants per tan en texts i docments aquest métode funciona molt bé. Els OCRs que hem utilitzat ha estat el pytesseract i el easyOCR. El pytesseract consta de varies configuracions que depenent del tipus d'imatge i com vols detectar necesitaes una configuració o una altre. Té 14 configuracions en total que van de assumeix que només hi ha un bloc de lletrs fins a buscar texts esparcits sense cap tipus d'ordre en particular buscant la mallor quantitat de text possible. Nosaltres en hem decantantat per la configuració número 11 que busca la mallor quantitat de text possible. Hem fet això ja que parts de la imatge retallada les pot confondre amb un caracter y només detectar a quella part en concret. Hem decidit agafar tots el carcter que pogui i del text obtingut tractar-lo per aconseguir només la matrícula.




























