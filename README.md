# Projet 13
Eve Craft, l'application pour les joueurs de eve online. Optimisation industrielle, lecture du marché, suivie de l'évolution des prix et détail de la chaîne d'assemblage.  
L'application est accessible depuis l'adresse http://46.101.181.80/.  
  
## 1) Prérequis.
Pour la consultation, un navigateur suffit.  
Pour l'hébergement de l'application, il est nécessaire d'accéder à un terminal et d'installer les prérequis :  
  - git  
  - python 3.8  
  - pipenv  
Une base de données Postgresql doit être créée avant d'aller dans l'installation.  
  
## 2) Installation.
Pour installer l'application:  
  - Clonez le dépôt du projet.  
  - Activez un environnement virtuel dans le dossier téléchargé.  
  - Installez les requirements.  
  - Configurez la constante DATABASES du fichier "evetool/settings/__init__.py" en fonction de la base de données configurée initialement.   
  - Vous pouvez activer les commandes django. (ex: python manage.py migrate)  
   
## 3) Paramétrage.
Des valeurs par défaut ont été choisis pour le system cost index et le market fee. Il est possible d'y avoir accès depuis le fichier config.py.  
  
## 4) Contrôles.
L'application dispose de plusieurs commandes permettant l'interaction entre, les données eve online accessible l'api du jeu et la base de données de l'application. Elles sont activées par, leur nom précédé de "python manage.py". (ex: python manage.py call_market)  
  
call_market : met à jour les prix du marché sur la base de données.  
  
create_db : initialise la base de données en faisant appel aux données actuelles de eve online.  
  
clean_all : suprime TOUTE la base de données.  
