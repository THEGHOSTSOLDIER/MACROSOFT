# MACROSOFT
[![C++](https://img.shields.io/badge/language-Python-%23f34b7d.svg?style=plastic)](https://en.wikipedia.org/wiki/C%2B%2B) 
[![Linux](https://img.shields.io/badge/platform-Linux-0078d7.svg?style=plastic)](https://en.wikipedia.org/wiki/Linux)
[![x64](https://img.shields.io/badge/arch-x64-red.svg?style=plastic)](https://en.wikipedia.org/wiki/X86-64) 

Ce projet de cybersécurité a pour but de créer un [ransomware](https://en.wikipedia.org/wiki/Ransomware) qui va chiffrer tous les fichiers `.txt` d'un utilisateur cible (extension modifiable), envoie la clé de chiffrement sur le serveur distant de l'attaquant, ainsi qu'une copie des données de la victime afin de pouvoir négocier efficacement si elle a réalisée un backup.
Le nom `Macrosoft` s'inspire d'une dérivée du nom de la société [Microsoft](https://en.wikipedia.org/wiki/Microsoft) présente dans le célèbre jeu de hacking [Hacknet](https://en.wikipedia.org/wiki/Hacknet).

## Installation

### Prérequis
Ce projet nécessite a été développé pour un système Linux, ce qui veut dire que tous les systèmes d'exploitaion de cette famille sont compatibles. Il est cependant vivement conseillé d'utiliser [Ubuntu](https://en.wikipedia.org/wiki/Ubuntu). Les instructions dans cette documentation ont été réalisées pour ce dernier.

L'installation de [Docker](https://en.wikipedia.org/wiki/Docker_(software)) est nécessaire pour pouvoir utiliser correctement les scripts, et surtout, de manière sécurisée.
Ci dessous la commande à entrer dans un terminal pour l'installer :

```bash
sudo apt install docker-compose
```

### Avertissement et clause de non-responsabilité
*<span style="color:red">Pour des raisons de sécurité, le ransomware ne pourra qu'être executé à partir des fichier [bash](https://en.wikipedia.org/wiki/Bash_\(Unix_shell\)) prévus à cet effet.</span>*
*<span style="color:red">Les fichiers `.py` ne doivent jamais être exécutés directement, vous maniez des scripts dangereux.</span>*

*<span style="color:red">L'auteur ne sera tenu responsable en cas de dommages matériels ou logiciels liés la mauvaise utilisation de ce programme !</span>*

### Installation des conteneurs docker

Pour installer les conteneurs docker, il suffit de se placer dans le dossier `MACROSOFT` et d'exécuter le script `build.sh` avec la commande suivante :

```bash
sudo ./build.sh
```

## Utilisation

### Lancement du serveur

Pour lancer le serveur de l'attaquant, il suffit de se placer dans le dossier `MACROSOFT` et d'exécuter le script `run_cnc.sh` avec la commande suivante :

```bash
sudo ./run_cnc.sh
```

### Lancement du ransomware

Pour lancer le ransomware, il suffit de se placer dans le dossier `MACROSOFT` et d'exécuter le script `run_ransomware.sh` avec la commande suivante :

```bash
sudo ./run_ransomware.sh
```

### Alternative : Lancement du ransomware avec le point de vue de la victime

Pour lancer le ransomware avec le point de vue de la victime, il suffit de se placer dans le dossier `MACROSOFT` et d'exécuter le script `exec_target.sh` avec la commande suivante :

```bash
sudo ./exec_target.sh
```

Déplacer-vous alors jusqu'au fichier `/root/ransomware/ransomware.py` et exécutez-le avec les commandes suivantes :

```bash
cd /root/ransomware
python3 ransomware.py
```

## Réponses aux questions

### Q1 : Quelle est le nom de l'algorithme de chiffrement ? Est-il robuste et pourquoi ?

Il s'agit d'un chiffrement de type [XOR cipher](https://en.wikipedia.org/wiki/XOR_cipher). L'algorithme consiste à appliquer un masque (clé) à un message pour le chiffrer, et à appliquer le même masque (clé) à un message chiffré pour le déchiffrer. L'opération XOR est une opération logique qui renvoie 1 si les deux bits sont différents, et 0 si les deux bits sont identiques (voir schémas ci-dessous).

Chiffrement :

| Texte clair | Clé | Texte chiffré |
|:-----------:|:---:|:-------------:|
|      0      |  0  |       0       |
|      0      |  1  |       1       |
|      1      |  0  |       1       |
|      1      |  1  |       0       |

Déchiffrement :

| Texte chiffré | Clé | Texte clair |
|:-------------:|:---:|:-----------:|
|       0       |  0  |      0      |
|       1       |  1  |      0      |
|       1       |  0  |      1      |
|       0       |  1  |      1      |

Cependant, il n'est pas du tout robuste, car il est possible de le casser en utilisant une attaque à [texte clair connu](https://en.wikipedia.org/wiki/Known-plaintext_attack). En effet, si on connait le texte clair et le texte chiffré, il est possible de retrouver la clé en appliquant l'opération XOR entre les deux (voir schéma ci-dessous).

| Texte chiffré | Texte clair | Clé |
|:-------------:|:-----------:|:---:|
|       0       |      0      |  0  |
|       1       |      0      |  1  |
|       1       |      1      |  0  |
|       0       |      1      |  1  |

 C'est pourquoi il est nécessaire de générer une clé en se basant sur l'aléatoire et non sur l'algorithme de chiffrement. Le XOR est donc à proscrire.

### Q2 : Pourquoi ne pas hacher le sel et la clef directement ? Et avec un hmac ?

En effet, il est possible de hacher le sel et la clé directement, mais cela ne résoud pas le problème de la robustesse du chiffrement. En effet, si on connait le hash de la clé et du sel, il est possible de retrouver la clé et le sel en utilisant une attaque de [collision](https://en.wikipedia.org/wiki/Collision_attack). Le hmac permet de résoudre le problème en hachant le sel puis en dérivant le hash à partir de la clé. La sortie est également plus longue que le hash de la clé et du sel, ce qui permet de rendre l'attaque de collision plus difficile.

## Q3 : Pourquoi il est préférable de vérifier qu'un fichier token.bin n'est pas déjà présent ?

Si un fichier token.bin est déjà présent, cela signifie que le ransomware a déjà été exécuté sur la machine. Il est donc inutile de le réexécuter, car il n'y a plus de fichiers à chiffrer et cela risquerait de rechiffrer des fichiers déjà chiffrés, ce qui pourrait entraîner des problèmes. Au passage, le précédent token sera écrasé. Retrouver la bonne clé correspondant au bon token ne serait pas chose aisée.

## Q4 : Comment vérifier que la clef la bonne ?

Il suffit de dériver la clé et le sel, on obtiendra alors un nouveau token. Si le token obtenu est le même que le token initial, alors la clé est la bonne.

## B1 : Expliquez ce que vous faites et pourquoi ?

Nous allons tout simplement créer une fonction leak_files() dans le fichier ransomware.py et post_leak() dans le fichier cnc.py. La fonction leak_files() va parcourir et envoyer les fichiers trouvés à la fonction post_leak() du serveur. La fonction post_leak() va alors récupérer les fichiers et les stocker sur le serveur de l'attaquant.

## B2 : Expliquez comment le casser et écrivez un script pour récupérer la clef à partir d’un fichier chiffré et d’un fichier clair.
On créer un script avec la même tactique que dans `Q1`. Il suffit de récupérer le fichier chiffré et le fichier clair, puis de faire l'opération XOR avec le script `xor_cipher_attack.py` pour retrouver la clé. Ensuite, on va déchiffrer le fichier chiffré avec la clé trouvée via le script `xor_file_unlocker.py` pour retrouver le fichier clair.

## B3 : quelle(s) option(s) vous est(sont) offerte(s) fiable(s) par la bibliothèque cryptographie ?
On va implémenter la méthode AES-CBC. AES est un algorithme de chiffrement symétrique qui utilise des clés de 128, 192 ou 256 bits. CBC est un mode de fonctionnement qui permet de chiffrer des données en blocs de 128 bits. Il est robuste et fiable.

## B4 : Quelle ligne de commande vous faut-il avec pyinstaller pour créer le binaire ?
```bash
pyinstaller --onefile ransomware.py
```
--onefile permet de créer un seul fichier exécutable.

## B5 : Où se trouve le binaire créer ?
Le binaire se trouve dans le dossier `/dist`.

<a href="https://imgur.com/Tso2t0M"><img src="https://i.imgur.com/Tso2t0M.jpg" title="source: imgur.com" /></a>