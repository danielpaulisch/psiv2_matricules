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



























