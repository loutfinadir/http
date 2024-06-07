# Data import service Errors
https://github.wdf.sap.corp/orca/dataimportservice/blob/master/common/src/main/java/com/sap/orca/dis/common/exceptions/Errors.java

# Public dimension
Importer les données dans une dimension publique ou dans une dimension non-publique se font de manière différentes:
## Pour une dimension non-publique
 - Si lors de l'import, le membre de la dimension n'existe pas celui-ci est créer automatiquement
## Pour une dimension publique
 - Si lors de l'import, le membre de la dimension n'existe pas celui-ci est rejeté et la ligne référencant ce membre n'est pas rajoutée au model. A priori, l'applyout resultant d'une classification ou regression ne peuvent référencer que les membres existant dans la dimension publique. On ne risque pas d'avoir ce genre de problème
 - Si lors de l'import, le membre de la dimension existe la ligne référencant ce membre est rajoutée au model
 



Quand on import les donneés dans une dimension public, il faut que la dimension public contienne tout les données refrencées par la datasource. En d'autres termes on ne peut pas utiliser une seule API, pour l'import des données