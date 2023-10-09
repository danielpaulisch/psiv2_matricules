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

- codi_final: conté el codi en Python que fa tot el procés de la detecció

- Directori actes: directori que conté les actes que hem anat fent per cada sessió. A cada acte es menciona el que s'ha anat fent i acordant en els diferents dies de treball a la universitat.
- 
-Directori codis: Conte varies proves que hem anat fent. Es tracta de un cementi de codis

-scipt.py: arxiu de python que llegeix una imatge i imprimeix la mtricula predita

-scipt_carpeta.py: arxiu de python que llegeix totes les imatges de una carpeta i imprimeix la mstricula predita de cada una de elles.

Base de dades

La nostra base de dades consisteix en unes 29 de cotxes realitzades manualment de les quals dividirem en un train i un test. El train té unes 23  de fotos i el test en conté unes 6 fotos. Els diferents processaments d'imatges i canvis duts a terme per detectar les matrícules es faran sobre el train i a la part de comprovació és veure si aquests canvis també afecta a un grup de test per visualitzar si el nostre model és prou bo per detectar imatges. La base de dades té un nombre d'imatges bastant reduït perquè com que no es tracta de una IA no necessitem un conjunt d'entrenament massiu; i amb un nombre reduït d'imatges amb processament clàssic podem incloure la gran majoria de casos i excepcions que estan en el nostre model d'entrenament.
Comprovem amb el test que no s'està produint el fenomen overfitting amb el conjunt d'entrenament.

Aquestes imatges han estat obtingudes del pàrquing interior de la UAB de l'escola d'enginyeria. Realitzades amb els nostres dispositius mòbils i algunes imatges de la base de dades del professor compartida a través del campus virtual sobre el mateix pàrquing. La il·luminació del pàrquing és suau, ja que és cobert tot i que té espais per on passa la llum solar indirectament.

Tractament d'imatge

Abans de localitzar la matrícula, tractament la imatge amb una sèrie de transformacions geomètriques i morfològiques que permeten que la detecció sigui molt més fàcil i més robusta.
Les operacions que hem emprat han estat les següents:

Binarització: apliquem la binarització, que és el procés de convertir la imatge en blanc o negre segons un llindar, perquè millora el contrast en ressaltar vores i detalls, a més redueix el soroll i les imperfeccions a la imatge, també simplifica el processament i accelera els algorismes de detecció.
Finalment, prepara la imatge per al reconeixement òptic de caràcters (OCR).

Blur: apliquem el blur, perquè és un filtre de desenfocament i per tant ens pot ser molt útil perquè també redueix el soroll a la imatge, eliminant detalls innecessaris que no s'han eliminat amb la binarització, a més elimina els detalls no importants que poden dificultar la detecció de la matrícula i sobretot homogeneïtza la il·luminació.

Otsu: apliquem aquesta tècnica de binarització automàtica i va molt bé per acabar d'eliminar el soroll de la imatge, per facilitar la detecció dels caràcters, ja que millora i ressalta els caràcters de la matrícula.

Opening: apliquem l'operació morfològica d'opening (erosió + dilatació), perquè té molts beneficis, per exemple: elimina el soroll de la imatge, a més uneix els caràcters que es troben separats per alguna imperfecció de la matrícula, també omple els buits, redueix detalls finets i millora la forma dels objectes.

Erosió: apliquem l'erosió per eliminar detalls no desitjats, per refinar les voreres i preparar la detecció acurada dels caràcters.

Dilatació: apliquem la dilatació, ja que ens relata els caràcters, combina els píxels propers per tal que se'ns faciliti la detecció, a més omplim buits i millora la robustesa.

Omplir els buits en blanc: i per acabar apliquem la versió d'imfill de MATLAB a Python, per omplir els buits que es generen en les àrees que ens interessen.

Detecció de voreres

Para detectar les voreres utilitzem la funció findcountourns que ens retorna totes les parts de color blanc que estan envoltades de color negre. Amb aquest procés ens quedem amb els possibles candidats a matrícula, després iterem aquests contorns amb una sèrie de condicions que compleixen les matrícules.
Vam trobar que la majoria d'imatges les podem detectar fàcilment amb la part blava on ens diu que és una matrícula espanyola i per tant ens dona molta informació del que pertany a la matrícula. Definim quin és el contorn correcte dient que el que tingui la part blava a l'interior de les diferents voreres creades, i que sigui la més gran de totes, és la matrícula. A


Rectangle de la matrícula

En definir les voreres no acaben de ser del tot rectangular i la major part de les vegades tenen formes estranyes, que poden tallar parcialment part de la matrícula, tot i que per l'ull humà no suposa cap problema, per un model si els caràcters estan tocant una vorera no poden saber amb certesa de quin caràcter es tracta. Per això ampliem el contorn dibuixant un rectangle que conté a dins tot el contornanterior, fent així que no es talli cap número perquè l'OCR pugui detectar bé els caràcters de la matrícula. Amb el rectangle dibuixat serà la part que retallarem de la imatge en tonalitats de grisos.




OCR

De la imatge resultant obtinguda aplicarem el OCR per fer la identificació de les lletres. És un sistema que consisteix en detectar caracters en imatges i pasar-les en string. Les diferents maneres amb la qual fa això és comparan glifos que té guardats, amb parts de la imatge per vuere sipor trobar o no aquests glifos, en treu le carecteristiques dels glifos i de la imatge i les compara al trobar-ne similituds detecta el caràcter corresponent. Aquest mètode només funciona si la escala i el tipos de font del caraceters són semblants per tan en texts i docments aquest métode funciona molt bé. Els OCRs que hem utilitzat ha estat el pytesseract i el easyOCR. El pytesseract consta de varies configuracions que depenent del tipus d'imatge i com vols detectar necesitaes una configuració o una altre. Té 14 configuracions en total que van de assumeix que només hi ha un bloc de lletres fins a buscar texts esparcits sense cap tipus d'ordre en particular buscant la mallor quantitat de text possible. Nosaltres en hem decantantat per la configuració número 11 que busca la mallor quantitat de text possible. Hem fet això ja que parts de la imatge retallada les pot confondre amb un caracter y només detectar a quella part en concret. Hem decidit agafar tots el carcter que pogui i del text obtingut tractar-lo per aconseguir només la matrícula.

Per facilitar el OCR al trobar carecteritiques hem de fer que les lletres estiguin aliniade amb el ei de les X, ja que el treure les carecteristiques de la imatge la inclinació fa que hi hagi dificultats en detectar les lletres. Per tan detectem la inlcinació de les lletres en el casos on millora la detecció de matricules girem la imatge quedant aliniades amb el eix de les X.


Resultats

A l'hora de veure resultats vam trobar que un problema no era la identificació de lletres de l'OCR sinó la detecció de les matrícules és per això que vam enfocar els nostres esforços a tractar la imatge en diferents punts del nostre pipeline per tal d'aconseguir que les nostres imatges puguin detectar la matrícula i no elements externs al cotxe o parts rectangulars del cotxe que es poden ser detectades com si fossin matrícules.
Els resultats que hem obtingut amb el nostre programa és de 21 sobre 29, és a dir, detecta 21 matrícules de 29 que n'hi ha  ala base de dades. amb el OCR de 

Les comprovaciones que hem fet, a més a més de comparar-ho manualment, hem calculat l'accuracy tant de train com de test, per tal de validar i afirmar que el nostre programa és robust i que no hi ha presència de Tesseract.
L'accuracy del train és d'un 0.813, i l'accuracy de test d'un 0.714.


Tot i això, vam volem fer més comprovacions, en aquest cas hem volgut comprovar els resultats de l'OCR que tenim amb el EasyOCR, perquè aquest és complex per tant sabem que si la diferència que hi ha de resutats no és tant significativa, vol dir que el nostre programa és bastant robut i correcte. 
L'accuracy de train amb EasyOCR és d'un 0.869 i del test és un 0.834. 

Per últim vam fer una matriu d'errors, per comprovar de les matrícules que no s'han detectat, quins son els seus errors més comuns, és a dir, quines lletres son les que el programa no les detecta i si les detecta i s'equivoca quins son aquest caràcter que es solen confondre. 

Conclusió

Podem concloure dient que l'elecció de traiar el OCR Tessearct ha estat molt bona idea, ja que és més o menys igual de robuts que el OCR EasyOCR que és consideret complex, ja que els accuracy ens donen més o menys molt semblants. I encara que el accuracy d'aquest segon és més elevat tarda més, 1.37 min, per tant en comparació amb el del Tesseract que és 5,6 segons, doncs no és massa òptim en el nostre cas. 
En altres paraules el nostre programa balanceja per tal que el resultats siguin el més acurat possible, però a al avegada que no tardi massa, per això hem acabat triant el Tesseract. 
Per altra banda, podem comprovar que la diferència entre els accuracy de train i test del Tesseract no és molts significativa, per tant, podem afirmar que el nostre programa és bastant robust i que no hi ha presència del fenòmen d'overfitting.

Finalment, voliem comentar també un problema que ens ha sorgit a mesura que anavem fent el programa i és que, com nosaltres detectem una zona blava, per detectar la matrícula quan hi ha cotxes amb el mateix blau elèctric que la zona blava de la E d'Espanya, el cotxe no detecta només aquella zona blava i per tant no detecta la matrícula. 
Així doncs, encara que podem afirmar que el nostre codi és robuts a molts casos, quan tenim un cotxe del mateix blau, no detecta bé la matrícula. 













































