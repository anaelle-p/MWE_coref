#!/bin/bash
# Anaëlle Pierredon et Jianying Liu

# ./lanceur.sh -os phrases/ 
# Dans phrases/ se trouve les fichiers txt à analyser par OFCORS
# La sortie d'OFCORS se trouve dans phrases/ofcors_outputs/

ofcors()
{
    for fichier in `ls $1*.txt`
        do
            echo "--------------------------------------"
            echo $fichier
            ofcors-infer -f -p window $fichier

            new_fichier=(${fichier//\// })
            new_fichier=(${new_fichier[1]//./ })
            echo ${new_fichier[0]}

            mv ./ofcors_outputs/resulting_chains.json ./$1ofcors_outputs/${new_fichier[0]}_resulting_chains.json
            mv ./ofcors_outputs/mentions_detection/mentions_output.json ./$1ofcors_outputs/${new_fichier[0]}_mentions_output.json
            mv ./ofcors_outputs/mentions_detection/tokens.json ./$1ofcors_outputs/${new_fichier[0]}_tokens.json
        done
}

mwecoref()
{
    for fichier in `ls $1*.txt`
        do
            echo "--------------------------------------"
            echo $fichier
            new_fichier=(${fichier//\// })
            new_fichier=(${new_fichier[1]//./ })
            echo ${new_fichier[0]}

            python3 add_mentions_chaine_to_cupt.py ./$1ofcors_outputs/${new_fichier[0]}_mentions_output.json ./$1${new_fichier[0]}annote.config48.cupt ./$1ofcors_outputs/${new_fichier[0]}_resulting_chains.json ./$1mwecoref_outputs/${new_fichier[0]}_mwe_coref.cupt
        done
}

if [ $1 == "-os" ]
then
    mkdir ./$2ofcors_outputs/
    echo "OFCORS"
    ofcors "$2"
    echo "PYTHON"
    mwecoref "$2"
    python3 statistiques.py $2mwecoref_outputs/
elif [ $1 == "-o" ]
then
    mkdir ./$2ofcors_outputs/
    ofcors "$2"
elif [ $1 == "-s" ]
then
    mkdir ./$2mwecoref_outputs/
    mwecoref "$2"
    python3 statistiques.py $2mwecoref_outputs/
else
    echo " Cette option n'existe pas. "
    echo " -o : lance ofcors-infer "
    echo " -s : lance add_mentions_chaine_to_cupt.py et statistiques.py "
    echo " -os : lance ofcors-infer, mwe_coref.py et statistiques.py "
fi