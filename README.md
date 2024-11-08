# BD_Benchmark

BD_Benchmark est un projet destiné au développement de bases de données de référence, fournissant un ensemble d'outils Python pour aider les utilisateurs à générer des bases de données de référence de différentes tailles. Ces outils permettent aux utilisateurs d'obtenir des données valides à partir de la base de données DBLP et de les personnaliser et étendre.

## Objectif du projet

L'objectif de BD_Benchmark est de fournir du code Python aux utilisateurs pour les aider à créer et manipuler des bases de données de référence. Les utilisateurs peuvent générer des bases de données de différentes tailles selon leurs besoins et les utiliser dans divers contextes d'application. Le projet prend également en charge la connexion à l'endpoint DBLP pour effectuer des requêtes sur les données.

## Fonctionnalités

1. **Conversion de jeux de données** : Sélection de jeux de données du réseau académique DBLP, contenant plus de 310 000 nœuds d'identité personnelle. Utilisation de code Python pour convertir ces nœuds en format de fichier CSV.

2. **Filtrage des ID valides** : Connexion à l'endpoint DBLP pour interroger les données, filtrer les ID valides actuellement dans DBLP et les écrire dans un nouveau fichier CSV.

3. **Création de fichiers de données complets** : Lecture des ID de personnes dans les fichiers CSV pour créer un fichier de données complet du réseau DBLP, incluant des informations sur les auteurs, éditeurs, articles, revues, collections de conférences, conférences, éditeurs, etc., et générer des fichiers JSON de nœuds et de liens.

4. **Génération et organisation de fichiers de données** : Génération du nombre requis de fichiers en fonction des paramètres de données dans les fichiers JSON, organisés dans des dossiers par "année-mois-jour". Les utilisateurs peuvent définir le ratio et le contenu de changement pour chaque fichier. Le programme commence à partir d'une date de début et s'arrête après avoir généré le nombre requis de dossiers.

## Installation

Pour installer le projet BD_Benchmark, exécutez la commande suivante :

```sh
pip install bd_dev_benchmark

## Update log
`1.0.0` first release
