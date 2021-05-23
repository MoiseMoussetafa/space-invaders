# Space Invaders

Il s'agit d'un jeu Space Invaders, en microPython sur la carte électronique STM32F407G-DISC1.  

![image](https://user-images.githubusercontent.com/72506988/119268372-f281ba80-bbf2-11eb-9806-0e0ea20bcd89.png)


## Flasher la carte en uPython (Windows)

- Installer Python3.7 ou plus sur le Microsoft Store
- Télécharger le programme de flashage : https://github.com/micropython/micropython/blob/master/tools/pydfu.py
- Créer un dossier et y placer le programme de flashage

Sous Windows Powershell (en administrateur) :
- Se placer dans le dossier précédement créé
- `.\venv\Scripts\Activate.ps1` Un acronynme (venv) apparait en début de ligne de commande.  
- `pip install pyusb==1.1.1`

Placer un jumper entre VDD et BOOT0 pour activer le mode DFU, puis brancher la carte STM32 par le haut avec un câble mini-USB et par le bas avec un câble micro-USB.

- `python pydfu.py --list` La liste des périphériques en mode DFU apparait.
- `python pydfu.py --upload STM32F4DISC-20210222-v1.14.dfu` Le nom du fichier est à adapter, il suffit de taper `STM32` puis de cliquer sur la touche TAB du clavier pour que le fichier de flashage téléchargé se sélectionne automatiquement.

Une fois le flashage terminé, placer les fichiers **.py** présents dans ce repo dans la carte flashée apparaissant comme une clé USB sur le PC (Remplacer si demandé).

---

## Utilisation
Ce jeu nécessite l'utilisation d'une console en utilisant une connection UART.  
La carte doit également être connectée au PC par ses connecteurs mini et micro USB.

- Télécharger PuTTY
- Ouvrir et configurer PuTTY :  
![image](https://user-images.githubusercontent.com/72506988/119269216-d4b65480-bbf6-11eb-919c-2f88485033ca.png)  
*Remplacer COMX par le COM utilisé par l'UART de la carte, visible depuis le gestionnaire de périphériques*

- Une fois configuré, cliquer sur **OPEN**. Le terminal qui s'ouvre sert d'écran pour le Space Invaders.


## Controles  
- Le vaisseau joueur se déplace en penchant la carte électronique à gauche ou à droite, autour de l'axe Y de l'accéléromètre LIS3DSH présent sur celle-ci (connecteur mini-USB vers l'avant / connecteur mini-USB vers l'arrière). Une LED rouge ou verte s'allume selon la direction de déplacement du vaisseau.
- Le tir s'effectue grâce au bouton poussoir bleu USER présent sur la carte électronique.

![image](https://user-images.githubusercontent.com/72506988/119268551-c3b81400-bbf3-11eb-8312-23051fa8f0ea.png)

Redémarrer une partie en appuyant sur le bouton RESET de la carte*
