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
  
- Directori codis: Conte varies proves que hem anat fent. Es tracta de un cementiri de codis

- scipt.py: arxiu de python que llegeix una imatge i imprimeix la matricula predita, hem fet aquest codi per tal que pugueu fer una prova amb qualsevol imatge que vulgueu.
Però només una.

- scipt_carpeta.py: arxiu de python que llegeix totes les imatges de una carpeta i imprimeix la matricula predita de cada una de elles. Hem fet aquest codi, per tal que, pugueu executar el codi amb el conjunt d'imatges que vulgueu. 

- Detecció matrícules: la presentació del repte 1. 

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

ClearBorder: amb aquesta funció eliminavem les voreres, per tal d¡eliminar tot el soroll possible i que sigui molt més fàcil detectar les àrees màximes. 

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

De la imatge resultant obtinguda aplicarem l'OCR per fer la identificació de les lletres. És un sistema que consisteix a detectar caràcters en imatges i passar-les en string. Les diferents maneres amb la qual fa això es comparen glifs que té guardats, amb parts de la imatge per veure si pot trobar o no aquests glifs, en treu les característiques dels glifs i de la imatge i les compara en trobar-ne similituds detecta el caràcter corresponent. Aquest mètode només funciona si l'escala i el tipus de font dels caràcters són semblants, per tant, en texts i documents aquest mètode funciona molt bé. Els OCR que hem utilitzat ha estat el Pytesseract i l'easyOCR. El Pytesseract consta de diverses configuracions que depenent del tipus d'imatge i com vols detectar necessites una configuració o un altre. Té 14 configuracions en total que van assumint que només hi ha un bloc de lletres fins a buscar texts escampats sense cap mena d'ordre en particular buscant la quantitat més gran de text possible. Nosaltres ens hem decantat per la configuració número 11 que busca la quantitat més gran de text possible. Hem fet això, parts de la imatge retallada les pot confondre amb un caràcter i només detectar aquella part en concret. Hem decidit agafar tots els caràcters que pugui del text obtingut itractar-lo per aconseguir només la matrícula.

Per facilitar l'OCR en trobar característiques hem de fer que les lletres estiguin alineades amb l'eix de les X, ja que treure les característiques de la imatge inclinada fa que hi hagi dificultats en detectar les lletres. Per tant, detectem la inclinació de les lletres en els casos on es pugui millorar la detecció de matrícules i girem la imatge quedant alineades amb l'eix de les X.

Resultats

A l'hora de veure resultats vam trobar que un problema no era la identificació de lletres de l'OCR sinó la detecció de les matrícules és per això que vam enfocar els nostres esforços a tractar la imatge en diferents punts del nostre pipeline per tal d'aconseguir que les nostres imatges puguin detectar la matrícula i no elements externs al cotxe o parts rectangulars del cotxe que es poden ser detectades com si fossin matrícules. Els resultats que hem assolit amb el nostre programa és de 21 sobre 29, és a dir, detecta 21 matrícules de 29 que n'hi ha a la base de dades.

Les comprovacions que hem fet, a més a més de comparar-ho manualment, hem calculat l'accuracy tant de train com de test, per tal de validar i afirmar que el nostre programa és robust i que no hi ha presència de Tesseract. L'accuracy del train és d'un 0.813, i l'accuracy de test d'un 0.714.

Tot i això, vam voler fer més comprovacions, en aquest cas hem volgut comprovar els resultats de l'OCR que tenim amb el EasyOCR, perquè aquest és complex, per tant, sabem que si la diferència que hi ha de resultats no és tan significativa, vol dir que el nostre programa és bastant robust i correcte. L'accuracy de train amb EasyOCR és d'un 0.869 i del test és un 0.834.

Finalment, vam fer una matriu d'errors, per comprovar de les matrícules que no s'han detectat, quins són els seus errors més comuns, és a dir, quines lletres són les que el programa no les detecta i si les detecta i s'equivoca quins són aquest caràcter que se solen confondre. Això és degut que al haver-hi tants caràcters no es pot obervar bé la matriu de confuió i no és pràctic. Per tant vam decidir només viualitzar en la matriu aquelles lletres que es confonen amb unes altres. Al veure la matriu no veiem cap tipus de patrò on el qual podem afirmar que un caràcter es confon amb un altre.



Conclusió

Podem concloure dient que l'elecció de triar l'OCR Tessearct ha estat molt bona idea, ja que és més o menys igual de robust que l'OCR EasyOCR que és considerat complex, perquè els accuracy ens donen més o menys molt semblants. I encara que l'accuracy d'aquest segon és més elevat tarda més, 1,37 min, per tant, en comparació amb el del Tesseract que és 5,6 segons, no és massa òptim pel nostre cas. En altres paraules el nostre programa balanceja, per tal que els resultats siguin el més acurat possible, però a la vegada que no tardi massa, per això hem acabat triant el Tesseract. Per altra banda, podem comprovar que la diferència entre els accuracy de train i test del Tesseract no és molta significativa, així doncs, podem afirmar que el nostre programa és bastant robust i que no hi ha presència del fenomen d'overfitting.

Finalment, volíem comentar també un problema que ens ha sorgit a mesura que anàvem fent el programa i és que, com nosaltres detectem una zona blava, per detectar la matrícula quan hi ha cotxes amb el mateix blau elèctric que la zona blava de la E d'Espanya, el cotxe no detecta només aquella zona blava i, per tant, no detecta la matrícula. Així doncs, encara que podem afirmar que el nostre codi és robust a molts casos, quan tenim un cotxe del mateix blau, no detecta bé la matrícula.

Millores

Com a millores i observacions del nostre treball a futur s'ha de tenir en compte que les imatges en rebut un tractament previ segons el tipus de pàrquing que era. És a dir que el fet de ser un pàrquing cobert on la llum i altres factors visuals poden variar amb un pàrquing descobert. La part prèvia de tractament d'imatge s'hauria de revisar en implementar el model en pàrquings descoberts. També en veure que els cotxes blaus amb una tonalitat semblant al color que identifica el país de la matrícula, s'oposa un problema de detecció de matrícula tot i que no hi ha molts cotxes d'aquest color. Es pot desenvolupar al projecte amb datasets de cotxes blaus per tractar aquest problema.








































