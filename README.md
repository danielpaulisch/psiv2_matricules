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


Abans de localitzar la matrícula, tractament la imatge amb una sèrie de transformacions geomètriques i morfològiques que permeten que la detecció sigui molt més fàcil i més robusta.
Les operacions que hem emprat han estat les següents:

Binarització: apliquem la binarització, que és el procés de convertir la imatge en blanc o negre segons un llindar, perquè millora el contrast en ressaltar vores i detalls, a més redueix el soroll i les imperfeccions a la imatge, també simplifica el processament i accelera els algorismes de detecció.
Finalment, prepara la imatge per al reconeixement òptic de caràcters (OCR).

Blur: apliquem el blur, perquè és un filtre de desenfocament i per tant ens pot ser molt útil perquè també redueix el soroll a la imatge, eliminant detalls innecessaris que no s'han eliminat amb la binarització, a més elimina els detalls no importants que poden dificultar la detecció de la matrícula i sobretot homogeneïtza la il·luminació.

Otsu: apliquem aquesta tècnica de binarització automàtica i va molt bé per acabar d'eliminar el soroll de la imatge, per facilitar la detecció dels caràcters, ja que millora i ressalta els caràcters de la matrícula.

Opening: apliquem l'operació morfològica d'opening, perquè té molts beneficis, per exemple: elimina el soroll de la imatge, a més uneix els caràcters que es troben separats per alguna imperfecció de la matrícula, també omple els buits, redueix detalls finets i millora la forma dels objectes.

Erosió: apliquem l'erosió per eliminar detalls no desitjats, per refinar les voreres i preparar la detecció acurada dels caràcters.

Dilatació: apliquem la dilatació, ja que ens relata els caràcters, combina els píxels propers per tal que se'ns faciliti la detecció, a més omplim buits i millora la robustesa.

Omplir els buits en blanc: i per acabar apliquem la versió d'imfill de MATLAB a Python, per omplir els buits que es generen en les àrees que ens interessen.




Detección de voreres

Para detectar les voresres utilitzem la funció findcountourns que ens retorna totes les parts de color balanc que estan envoltades de color negre fent aixì ens quedem amb el possibles candiats a mmatricula després iterme aquests contorns per definir on és la matrícula amb una serie de condicions que compleixen les matrícules al observar els difernts images i resultats, vam torbar que la majoria de imatges podem detectar facilment el la part blava on ens diu que és una matrícula espanyola i per tan ens dona molta informació del que pertany a la matrícula. Definim quin és el contorn correcte dient que el que tingui la part blava al interior dels diferents controns creats a més a més ha de ser el més grans de tots el que tenen parts blaves a dins, aqui agafem el contorn que és la matrícula. Aquest contorn pot tindre més infromació que la matrícula ja que pot detectar algunes part del coche com dins del contron però la part importan es que hi hagi dins la matrícula per poder detectar el números.

Rectangle de la matrícula

Al definir les voreres no acaben de ser del tot rectangular i la majoria de vegades tenen formes extranyes, que poden a tallar parcialment part de la matrícula, tot i que per l'ull huma no suposa cap problema a lhora de veure els números que hi ha en la matrícula, per identificació amb el model com a vegades els números poden tocar els contorns per tan genera probles per saber de quin número o lletra es tracte. Per això ampliem el contron dibuixant un rectangle que conté a dins tot el contor, fent aixì que no es talli cap númeor perquè el OCR pogui detectar bé els caràcters de la matrícula. Amb el rectangle dibuixat serà la part que retallarem de la imatge en tonalitats de grisos. 



























