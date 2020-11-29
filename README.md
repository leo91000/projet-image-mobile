# Projet Image Mobile - Léo Coletta

Le projet consiste à développer une application de recherche à partir d’image depuis un smartphone. Il s’agit d’un type d’application déjà très utilisé dans le monde du mobile. L’objectif de ce projet et de mettre en application toutes les connaissances apprises en cours lors des enseignements à distance .
-   Service REST
-   Application Android
-   Traitement d’images

La réalisation de cette application comporte deux partie bien distinct. D’une part, on a le développement de l’application mobile, que nous avons appelé FashionistApp, permettant de prendre de photos ou d’en sélectionner une depuis les librairies. D’autre part, une partie serveur qui prend en charge toutes la parties recherche d’image similaire.

  

Les technologies utilisées sont les suivantes :
-   Pour la partie serveur : Python + Django + OpenCV + Keras
-   Pour la partie client : Quasar Framework  

Nous allons décomposer notre rapport en deux parties. Tout d’abord, nous allons étudier la partie serveur et l’API REST, puis, dans un second temps nous allons comprendre le fonctionnement de la partie cliente et de l’application Android.


# Partie serveur : API REST

## Structure du service

Le service développé à tenu compte de la philosophie de conception REST qui consiste à permettre simplement la manipulation de ressources.

Chaque recherche et résultat sera associé sous la forme d’une ressource exposée en utilisant le format JSON, permettant ainsi de formuler clairement les recherches d’images.

Chaque interaction d’un client avec le serveur REST pour une recherche d’image comporte les étapes suivantes :

  

-   Le client choisis d’envoyer une requête HTTP avec le verbe HTTP “POST” dans laquelle est contenue l’image fournis par l’utilisateur. A partir de la réception de la requête, le serveur exécute une recherche d’image similaires. Ensuite, les résultats sont stockés dans une base de donnée de manière à ne pas avoir à effectuer le calcul plusieurs (calcul assez coûteux). Le serveur termine avec l’envoie d’une réponse au client qui contient l’ID correspondant à la ressource matérialisant le résultat.
    

![](https://lh5.googleusercontent.com/bbB816yTlXvxvr1XnFDphi67oXYayZUhS1D4Yycp9reglrHW7wQSDPNej_fu6PANz511y-F1wkhyCiKDmm-gr47-QF5WQYEK9Yj3aThpTfF_-VcCb0NphbMzsDK8MY0u6BNdkikN)
*Capture d’écran de la requête POST “/img_searches” sur POSTMAN*

-   Une fois la requête effectuée, on peut effectuer une requête HTTP GET sur la ressource afin de récupérer ses informations. Le résultat de la recherche contient l’URL des 5 images les plus similaire à l’image original et dont le score est supérieur à 0.
    

![Requête GET “/img_searches/4039” sur POSTMAN](https://lh6.googleusercontent.com/udnh-8AOyFvNHZ0dTbwibqC2-8T4-Z0N7-01Bq0yOGw_77LHZY36V00si9cj3PWOWLnns5XFNkN-81Th7O5RwXHLzsLcinyAgz-OvEqYEL72rtWsLEgBC0ZVtYLRR6bJsk_KAotX)
*Requête GET “/img_searches/4039” sur POSTMAN*

## Algorithme de recherche
L'algorithme employé pour la recherche d’image similaire se base sur les connaissances vu en cours. Il se base d’une part sur du machine learning (réseau neuronale convolutif) afin de transformer les images en vecteur. D’autre part, il utilise un algorithme d’indexation qui va permettre d’évaluer la distance entre ces vecteurs.

### Le réseau neuronale convolutif

Dans le domaine du deep learning, un réseau neuronal convolutif (CNN ou ConvNet) est une classe de réseaux neuronaux profonds, le plus souvent appliqué à l'analyse de l'imagerie visuelle. Ils ont des applications dans la reconnaissance d'images et de vidéos, les systèmes de recommandation, la classification d'images, l'analyse d'images médicales, le traitement du langage naturel et les séries temporelles financières.

  

Afin de simplifier le développement de la partie serveur, nous avons décidé d’adapter un modèle pré entraîné. De cette manière, nous évitons également d’utiliser des ordinateurs très puissant nécessaire à l’apprentissage automatique de réseau neuronaux.

  

Parmis les modèles pré entraînés existants, nous avons choisis de prendre le CNN appelé VGG. VGG est un réseau neuronale convolutif proposé par Karen Simonyan et Andrew Zisserman de “Oxford Robotics Institue” durant l’année 2014. Il a été dans plusieurs compétition de reconnaissance d’image et a obtenu une précision de 92,7%.C’est également l’un des plus grosse base de données d’image disponible aujourd’hui, contenant approximativement 14 million d’image labelisé par des humains.

  

![Architecture de VGG 16](https://lh6.googleusercontent.com/o7MX5QcReuuLkf9K0mEphAInA_cG8mdpwxlWlGvIOXqLzvfRVEeoXthioh1sfndwvTmbCE2BndngvCiESPJa1rNioRC5jkWBGzuk_Q2ADdvvRDREO_hrrbqrZdbY-GezVrQOH0_A)
*Architecture de VGG 16*

### **Indexation des images**

Pour indexer la base de donnée d’image donnée par l’exercice, nous transformons toutes les photos en vecteurs.

Grâce au réseau neuronal, nous recevons une liste de mot et leur score. Notre algorithme d’indexation élimine tout de suite les mots ayant un score très faible (inférieur à 0.001), cela nous permet d’économiser de la place en base de donnée.

A partir de cela, lorsqu’une recherche est effectuée, nous transformons l’image recherché en vecteur et nous effectuons la distance de manhattan par rapport à toutes les autres images. Nous gardons dans les résultats seulement les 5 plus gros ayant un score supérieur à 0.

De plus, un point d'API est prévu pour ajouter des images à la base de donnée.

### Relevance feedback

Un appel d'api permet client peut noter les résultats de la recherche. Ces résultats pourront être utilisés plus tard pour améliorer la qualité de la recherche.

# Partie Client : application native iOS/Android

L’application mobile, qui permet à l’utilisateur de communiquer avec la partie serveur, a été réalisée en **Vue (Javascript)** avec le framework **Quasar Framework**, et permet de créer des applications 100% natives et multiplateformes (iOS, Android, Windows 10, etc) en se basant essentiellement sur une partie commune du code, et sur peu de code propre à chaque plateforme. Nous allons montrer comment nous avons réalisé une application **Android** et **iOS**, et comment nous l’avons testée sur Android Studio.

## Architecture de l'application

Les applications Vue se basent sur le principe des composants, c’est-à-dire une partie graphique et une partie code, les 2 étant liées par défaut (dans un fichier .vue, une partie html, une partie css et une partie script). L’interface commune a été réalisée en HTML, avec des composants fournis par défault.
  

![](https://i.imgur.com/Rszyj2v.png)

Un exemple de la structure d'un fichier .vue d’éléments visuels (label, images) dans ImageSearchView.vue  

![](https://i.imgur.com/lddpToc.png)


![](https://i.imgur.com/Rszyj2v.png)

L’envoi du fichier en StreamPart qui s’effectue de manière assez simple et modulaire.

  

Le response récupéré à partir de la requête permet d’obtenir un ID : cet ID représente le calcul effectué côté serveur, et en lançant une requête GET avec cet ID, l’application récupère le JSON avec les 5 photos plus similaires, avec leur emplacement sur le serveur ainsi que leur similarité. L’étape finale consiste à mettre en forme le JSON et afficher les images reçues.

  

![](https://lh4.googleusercontent.com/c0Xr4SoOXUeGzZjlq1sAXJJIj2sj0bcl_WTlVodNj52yG-f7uvYgYa_55WbqJuVLK3hpeQ09MNkWtIUe8rbtT6mZ5eJOTX2nUR45SXl-KlncZHsI05oK-diPR9TkN07N1LrlLsEu)

Avec un foreach, chaque résultat de requête est mis dans une classe Result qui inclut les champs adaptés, ce qui facilite sa gestion et son affichage dans un tableau.

# Bilan et conclusion

Ce projet nous a permis d’appliquer toutes nos connaissances sur le CNN mais aussi sur les services REST, sur le langage Python et sur le développement mobile.  
  
Concernant l’application, nous avons décidé de passer à “un niveau supérieur” en essayant de tester nos compétences en termes de développement mobile. Nous avons choisi une technologie, Xamarin, que nous n’avons pas abordé pendant les cours et par conséquent il nous était difficile d’obtenir des conseils de la part des enseignants. Il était primordial pour nous donc de savoir s’auto-documenter, mais cela a été facilité relativement par notre expérience précédente dans ce framework.

  

Nous avons été satisfaits de pouvoir rendre un travail où nous avons appliqué toute notre expérience à l’IMT mais aussi tout ce que l’on a appris à partir de nos projets personnels.