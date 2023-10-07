# PSIV 2 MATRÍCULES


Aquest treball consisteix a detectar i llegir matrícules de cotxes d'Espanya a partir d'una foto.
La idea és seguir el següent pipeline per detectar les matrícules:

- Adquisició d'una foto
- Tractament de la imatge
- Localització de la matrícula
- Reconeixement a través d'un OCR
- Comprovació dels resultats.

La distribució del GitHub és la següent:
- Directori Imatges: conté les imatges dels cotxes. Aquestes les hem adquirit manualment fent fotos en el pàrquing de cotxes de la universitat.
A més a més, les hem adquirit també de la base de dades que tenim al Campus Virtual.

- Script: conté el codi en Python que fa tot el procés de la detecció

- Directori actes: directori que conté les actes que hem anat fent per cada sessió. A cada acte es menciona el que s'ha anat fent i acordant en els diferents dies de treball a la universitat.

Base de dades

La nostra base de dades consisteix en unes (n imatges) de cotxes realitzades manualment de les quals dividirem en un train i un test. El train té unes (n imatges) de fotos i el test en conté unes 6 fotos. Els diferents processaments d'imatges i canvis duts a terme per detectar les matrícules es faran sobre el train i a la part de comprovació és veure si aquests canvis també afecta a un grup de test per visualitzar si el nostre model és prou bo per detectar imatges. La base de dades té un nombre d'imatges bastant reduït perquè com que no es tracta de una IA no necessitem un conjunt d'entrenament massiu; i amb un nombre reduït d'imatges amb processament clàssic podem incloure la gran majoria de casos i excepcions que estan en el nostre model d'entrenament.
Comprovem amb el test que no s'està produint el fenomen overfitting amb el conjunt d'entrenament.

Aquestes imatges han estat obtingudes del pàrquing interior de la UAB de l'escola d'enginyeria. Realitzades amb els nostres dispositius mòbils i algunes imatges de la base de dades del professor compartida a través del campus virtual sobre el mateix pàrquing. La il·luminació del pàrquing és suau, ja que és cobert tot i que té espais per on passa la llum solar indirectament.

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

Detecció de voreres

Para detectar les voreres utilitzem la funció findcountourns que ens retorna totes les parts de color blanc que estan envoltades de color negre. Amb aquest procés ens quedem amb els possibles candidats a matrícula, després iterem aquests contorns amb una sèrie de condicions que compleixen les matrícules.
Vam trobar que la majoria d'imatges les podem detectar fàcilment amb la part blava on ens diu que és una matrícula espanyola i per tant ens dona molta informació del que pertany a la matrícula. Definim quin és el contorn correcte dient que el que tingui la part blava a l'interior de les diferents voreres creades, i que sigui la més gran de totes, és la matrícula. A


Rectangle de la matrícula

En definir les voreres no acaben de ser del tot rectangular i la major part de les vegades tenen formes estranyes, que poden tallar parcialment part de la matrícula, tot i que per l'ull humà no suposa cap problema, per un model si els caràcters estan tocant una vorera no poden saber amb certesa de quin caràcter es tracta. Per això ampliem el contorn dibuixant un rectangle que conté a dins tot el contornanterior, fent així que no es talli cap número perquè l'OCR pugui detectar bé els caràcters de la matrícula. Amb el rectangle dibuixat serà la part que retallarem de la imatge en tonalitats de grisos.






























