# projet_TIPE
 
Projet : TIPE 2022
Thème : Santé Prévention


MCOT :

Application des méthodes de recherche d'isomorphismes de graphes à la comparaison des structures de protéines

Professeur encadrant : Mr Vallaeys, professeur de mathématiques au lycée Faidherbe

Positionnement thématique
INFORMATIQUE, MATHEMATIQUES (Géométrie, Théorie des graphes)

Mots-clés
Mots-clés(français)			  Mots-clés(anglais)
Isomorphisme/automorphisme de graphes	  Graph isomorphism/automorphism
Identification de sous-graphes isomorphes Subgraph isomorphism		
Repliement des protéines		  Protein folding
Modélisation (des protéines)		  (Protein) Modeling

Bibliographie commentée

La comparaison de graphes est un problème d'informatique classique, qui, en plus d'avoir des utilités pratiques, s'avère être un problème théoriquement très intéressant du point de vue informatique.
En effet, c'est l'un des seuls problèmes où l'on ne connaît ni algorithme de résolution en temps polynomial (pour le cas général), ni de preuve qu'il est NP-complet. Une généralisation de ce problème est la recherche
de sous-graphes ismorphes, il a été prouvé qu'il n'existe pas d'algorithmes de résolution en temps polynomial pour celui-ci, il appartient donc aux problèmes de classe NP-complets.

Scott Fortin fait état de l'avancée du problème dans son papier [3], étudiant le travail accompli jusqu'ici, et citant quelques unes des ses applications. Par exemple, ces algorithmes sont utilisés
pour classer les structures des molécules.
Il distingue deux approches : l'une est de directement chercher l'ismorphisme entre les graphes, l'autre est d'utiliser un intermédiaire, une fonction d'étiquetage canonique.
Pour la première, il peut être utile de combiner des invariants de sommets comme le degré d'un sommet, ou de construire l'ismorphisme au fur et à mesure pour un nombre de sommets de plus en plus grands. 
L'avantage est que l'algorithme peut s'arrêter avant son terme si un isomorphisme a été trouvé mais il est difficilement applicable puisque le nombre de possiblités est très élevé et que, s'il faut déterminer que les graphes
ne sont justement pas isomorphes, on parcourt toutes les possibilités.
Pour l'autre, la méthode est plus applicable, c'est d'ailleurs celle utilisée en pratique. Il faut déterminer une manière efficace et canonique d'étiqueter les graphes. C'est ainsi que McKay [4] propose un algorithme efficace "nauty", utilisant ce procédé. Il prouve que son étiquetage
est le même pour toute paire de graphes isomorphes. Il est ainsi le premier à résoudre le problème pour un graphe non-trivial d'une centaine de sommets.

Récemment, Lazlo Babai a proposé le meilleur algorithme répondant au problème, de complexité quasi-polynomiale (O(ln(n)^c)), ce qui correspont à une avancée majeure dans le domaine.

En ce qui concerne le problème des sous-graphes ismorphes, Eppstein [1] propose de résoudre le problème d'isomorphisme de sous-graphes pour les graphes planaires en temps linéaire.
Il se base sur une technique de partition du graphe planaire en morceaux de petite taille, une méthode de type "diviser pour régner". 
Finalement, ces concepts peuvent être appliqués à la mesure de similarité de deux graphes [2]. Ce qui aidera à mesurer la similarité de deux protéines.

Problématique retenue
Il s'agit de comparer les structures de protéines lorsqu'elles ont formé leurs liasons et se sont formées dans l'espace, et déterminer leur proximité tant sur la forme que sur la position.
Un outil de comparraison permettrait de mesurer la précision des prédictions informatiques d'un modèle, par rapport à un modèle référent dont la structure
a été déterminée par une méthode longue et coûteuse (par rayons X par exemple).

Objectifs
Je me propose:
	- d'étudier des modèles simples, une suitre de points sans ramifications par exemple, et déterminer leur proximité par différentes méthodes
	- de me familiariser avec la structure des protéines et le format pdb, 
	- de proposer des moyens de comparer des proteines (graphes), en commençant par écrire un algorithme naïf de détection d'isomorphismes de graphes, améliorer en utilisant des invariances entre les sommets.
	- d'étudier la méthode McKay [4] et les concepts présentés.
	- d'adapter ces concepts à la recherche du plus grand sous-graphe isomorphe.
	- d'établir un indice de comparaison, en fonction de la ressemblance de structure et de position des atomes dans l'espace

Bibliographie
[1] Subgraph Isomorphism in Planar Graphs and Related Problems, David Eppstein, 1999
[2] Measuring the similarity of labeled graphs, Pierre-Antoine Champin, Christine Solnon, 2003
[3] The Graph Isomorphism Problem, Scott Fortin, 1996
[4] B. McKay. Practical graph isomorphism. Congressus Numerantium, 1981


Note : le code est ici tel qu'il a été utilisé pour la présentation, veuillez excuser tout manque de mise en forme