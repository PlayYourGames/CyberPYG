# [BOT] CyberPYG
Ce bot est réalisé pour le serveur Discord Play Your Games (https://discord.gg/wupMD7CsEv).

Il regroupera l'ensemble des fonctionnalités développées au sein du serveur tout en communiquant avec d'autres services extérieurs.

# TODO List

## Système de statistiques
Le bot devra auditionner les différents channels pour en dégager des chiffres et les stocker momentanément en base. Quelques fonctionnalités :
* Calcul de nombre de messages par membre (prévoir une commande pour visualiser dans un embed ou dans un message classique) ;
* Calcul du nombre de messages par salon (idem prévoir une commande pour les visualiser) ;
* Offrir le rôle **Ribs de Porc** (pendant 24h) au membre le plus actif du jour. Rôle retiré au bout des 24h, possibilité de faire une loterie spéciale pour ce rôle ;
* Publication à 0h00 du top 5 des membres les plus actifs du jour dans #taverne .

## Channels de streaming
Le bot pourra également adapter le nom d'un channel vocal dédié au streaming (Streaming 1, Streaming 2 par exemple) en fonction du jeu partagé par le joueur dans le channel. Quelques fonctionnalités :
* Si le joueur commence à streamer tout en jouant à un jeu, alors le nom du channel sera renommé (par exemple : "Rocket League - Jhonny")
* Lorsque le stream s'arrête, que le joueur ne joue plus au jeu ou que le joueur quitte le salon, il devra évidemment reprendre son nom initial (Streaming 1, Streaming 2).
