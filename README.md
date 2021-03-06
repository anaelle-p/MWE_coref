# MWE_coref

Ce dépôt sert à collecter les travaux réalisés pour étudier les expressions polylexicales et la coréférence.

## Sujet

Ce dépôt a été créé dans le cadre d'un stage dont l'objectif est de vérifer de manière expérimentale l'hypothèse selon laquelle les composants individuels d'une expression polylexicale sont rarement susceptibles d'appartenir à des chaînes de coréférences.

**Expressions polylexicales** : Termes complexes composés de plusieurs mots tels que "blanc d'œuf", "mémoire vive", "prendre une pause", "prendre le temps", "retourner sa veste" ou "prendre le taureau par les cornes" etc. Elles présentent des comportements linguistiques irréguliers et notamment la non-compositionnalité sémantique, qui signifie que le sens global de l'expression n'est pas déductible de manière régulière à partir des sens des composants et des liens syntaxiques qui les relient.  
**Chaînes de coréférence** : Procédé linguistique dans lequel plusieurs éléments d'un discours réfèrent à un même élément du discours.

Exemple : "Il a retourné sa veste et l'a suspendue dans l'armoire."   Ici le groupe nominal _la veste_ est ce que l'on appelle une **mention**, c'est-à-dire un élément qui réfère d'une entité du monde du discours (la veste qui appartient à la personne décrite dans l'énoncé). De même, le pronom _l'_ est lui-même une mention qui réfère à cette même entité du discours. On dit alors que _sa veste_ et _l'_ sont **coréférents**, c'est-à-dire qu'ils désignent la même entité.

Dans l'exemple précédent, la coréférence entre le pronom et _sa veste_ n'est possible que parce que nous ne sommes pas en présence de l'expression polylexicale "retourner sa veste" ("changer d'opinion"). Si la phrase "Il a retourné sa veste" avait été une EP, la non-compositionnalité de celle-ci aurait empêché de rendre le composant _sa veste_ accessible à une coréférence. C'est ce type de restriction que nous souhaitons étudier au cours de ce stage.

Pour vérifier cette hypothèse, nous avons à disposition un outil pour l'annotation en expressions polylexicales ([Seen2seen](https://gitlab.com/cpasquer/st_2020)) et un outil pour la résolution de coréférences ([OFCORS](https://gitlab.com/Stanoy/ofcors/-/tree/master), qui utilise [DECOFRE](https://github.com/LoicGrobol/decofre) pour la reconnaissance de mentions). Les entrées et les sorties diffèrent d'un outil à l'autre.

## Installation des outils

Pour pouvoir utiliser notre dépôt, il faut installer Seen2seen et OFCORS. Il est conseillé d'utiliser un environnement virtuel.

### Installation de Seen2seen
Pour plus de détails, référez-vous au README de Seen2seen : [Lien vers Seen2seen](https://gitlab.com/cpasquer/st_2020).
* Clonez le dépôt de Seen2seen: `git clone https://gitlab.com/cpasquer/st_2020 Seen2Seen`
* Clonez ce dépôt : `git clone https://github.com/anaelle-p/MWE_coref`
* Supprimez l'ancien code et l'ancien fichier config : `rm Seen2Seen/CODE/seen2seen.py Seen2Seen/config.cfg`
* Copiez-collez le nouveau code : `cp MWE_coref/seen2seen/seen2seen.py Seen2Seen/CODE/seen2seen.py`
* Copiez-collez le nouveau fichier config : `cp MWE_coref/seen2seen/config.cfg Seen2Seen/config.cfg`
* Ajoutez le script de conversion udpipe : `cp MWE_coref/seen2seen/udpipe_annote.py Seen2Seen/CODE/udpipe_annote.py`
* Téléchargez le modèle utilisé par le script de conversion : [french-gsd-ud-2.5-191206.udpipe](https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3131)
* Créez un répertoire `model_udpipe` : `mkdir Seen2Seen/CODE/model_udpipe/`
* Déplacez le modèle dans ce répertoire  
Vous pouvez maintenant utiliser Seen2seen pour l'annotation ! Le lancement est expliqué plus bas.

### Installation d'OFCORS
Pour plus de détails, référez-vous au README d'OFCORS : [Lien vers OFCORS](https://gitlab.com/Stanoy/ofcors/-/tree/master).
* Clonez le dépôt d'OFCORS : `git clone https://gitlab.com/Stanoy/ofcors.git`
* Installez flit si besoin : `pip install flit`
* Rendez-vous dans le répertoire ofcors : `cd ofcors`
* `pip install -r requirements.txt`
* `flit build --format wheel`
* `pip install dist/ofcors-X.Y.Z-py3-none-any.whl`
* Téléchargez les modèles d'OFCORS : [models.zip](https://gitlab.com/Stanoy/ofcors/-/releases/)
* Déplacez le dossier `models` dans `ofcors/models`
* N'oubliez pas d'installer les modèles de Spacy (`python -m spacy download fr_core_news_lg`) et de Stanza (`python3`, `import stanza`, `stanza.download('fr')`)  
Ofcors est installé!
* Si vous n'avez pas cloné notre dépôt : sortez du dépôt d'OFCORS et `git clone https://github.com/anaelle-p/MWE_coref`  
Vous pouvez maintenant utiliser OFCORS dans notre dépôt! Le lancement est expliqué plus bas.

## Choix de corpus
### Première expérience : sous-corpus de PARSEME
Pour traiter correctement la coréférence, il est nécessaire de connaître les frontières de textes dans un corpus. En effet, la coréférence ne peut être traitée qu'à l'intérieur d'une même unité discursive.  
Le [corpus PARSEME](https://gitlab.com/parseme/parseme_corpus_fr) est annoté en expressions polylexicales mais les frontières des textes ne sont pas annotées. Ce corpus contient quatre sous-corpus (SEQUOIA, GSD, PARTUT et PUD) et il n'est possible de retrouver l'ordre des phrases que pour un seul sous-corpus : [SEQUOIA](https://lindat.mff.cuni.cz/dépôt/xmlui/handle/11234/1-3429).  
Nous avons donc isolé les différents documents présents dans le corpus SEQUOIA pour lesquels les phrases se suivent selon l'ordre du document initial :
* 2 rapports de l'agence européenne du médicament pour la partie EMEA (\~ 1 000 phrases en tout)
* 19 articles Wikipédia sur des affaires sociale ou politiques pour la partie frwiki (\~ 1 000 phrases en tout)
* 36 articles de journaux courts avec des thèmes variés pour la partie annodisER (\~ 500 phrases en tout)  

Ce corpus étant annoté manuellement en expressions polylexicales, les erreurs d'annotation ne peuvent venir que des chaînes de coréférence.  

### Deuxième expérience : Est Républicain
Dans un deuxième temps, l'expérience se réalise sur le [corpus Est Républicain](http://redac.univ-tlse2.fr/corpus/estRepublicain.html), un recueil des articles paru en 1999, 2002 et les deux premiers mois de 2003 sur le journal régional Est Républicain. Considérant la taille énorme de corpus, pour l'instant, nous limitons notre test sur les 100 premiers articles ayant plus de 300 mots de l'année 2003 (\~ 3 000 phrases en tout).  

Ce corpus étant composé de fichiers texte brut, les erreurs d'annotation peuvent venir des chaînes de coréférence ou des expressions polylexicales. 

### Troisième expérience : ANCOR
Enfin, nous avons réalisé notre expérience sur le corpus ANCOR (téléchargé depuis le [lien donné par DECOFRE](https://sharedocs.huma-num.fr/wl/?id=omxQyO3MkOgUgfEVwOlBygZZHYAocTDt)). C'est un corpus d'oral transcrit composé de 4 sous-corpus :
* ESLO_ANCOR : des entretiens divisés en sous dialogues thématiques cohérents (\~ 25 000 phrases en tout).
* ESLO_CO2 : trois entretiens complets (\~ 2 500 phrases en tout).
* OTG : des dialogues interactifs entre des individus et le personnel d’accueil de l’office de tourisme de Grenoble (\~ 2 800 phrases en tout).
* UBS : des dialogues interactifs par téléphone recueillis auprès du standard téléphonique d’une université (\~ 700 phrases en tout).

Ce corpus étant annoté manuellement en chaînes de coréférence, les erreurs d'annotation ne peuvent venir que des expressions polylexicales. 

## Structure du dépôt

```
|-- MWE_coref
    |-- .gitignore
    |-- README.md
    |-- presentation_MWE_coref.pdf
    |-- seen2seen
    |   |-- udpipe_annote.py
    |   |-- seen2seen.py
    |   |-- config.cfg
    |-- 1_corpus
    |   |-- SEQUOIA
    |   |   |-- annodisER
    |   |   |-- emea
    |   |   |-- frwiki
    |   |   |-- z_corpus_initial
    |   |   |-- z_fichiers_intermediaires
    |   |   |-- EMFR_corpus_split.py
    |   |   |-- EMFR_txt_from_conllu.py
    |   |   |-- ER_get_texte.py
    |   |   |-- ER_get_date_title.py
    |   |   |-- get_mwe_from_cupt.py
    |   |   |-- MWE_decompte_*.json
    |   |-- EST_REPUBLICAIN
    |   |   |-- TXT2003
    |   |   |-- TXT2003_len300_articles
    |   |   |-- extract_text_er.py
    |   |-- ANCOR
    |   |   |-- ESLO_ANCOR
    |   |   |-- ESLO_CO2
    |   |   |-- OTG
    |   |   |-- UBS
    |-- 2_traitements
    |   |-- CuptParser.py
    |   |-- OfcorsFilesParser.py
    |   |-- merge_s2s_ofcors.py
    |   |-- statistiques.py
    |   |-- lanceur.sh
    |   |-- ANCOR
    |   |-- blabla
    |   |-- ER2003
    |   |-- SEQUOIA
    |   |-- z_oldies
    |-- 3_resultats
    |   |-- visualisations.ipynb
    |   |-- visualisations_jyliu.ipynb
    |   |-- sequoia_frwiki_050721.json
    |   |-- sequoia_frwiki_050721_validation.json
    |-- |-- ...
    |   4_compositionnalite
    |   |-- extract_vrai_exemple.py
    |   |-- extract_faux_exemple.py
    |   |-- degre_to_annotations.py
    |   |-- consignes_annotation.pdf
    |   |-- test_compositionnalite_resultats.xlsx
    |   |-- ...
    |   |-- resultats_croisements
    |   |   |-- ...
    |   |-- resultats_mwes
    |   |   |-- ...

```

## Processus de travail

1. Modification du script de Seen2seen, pour qu'il puisse faire seulement l'étape d'annotation;

    - Script `seen2seen/udpipe_annote.py` pour transformer un fichier txt en `cupt.blind`;
    - Modification du script `seen2seen/seen2seen.py` en créant un mode "annotation_ONLY" qui permet de ne faire que l'annotation sans refaire l'entraînement. Ce mode est à spécifier dans le fichier de config (`seen2seen/config.cfg`) avec "annotation_ONLY = True".


2. Utilisation du corpus SEQUOIA dans PARSEME, séparation des sous-corpus EMEA, frwiki et annodis.er selon les articles;

    - Lien pour télécharger le [corpus](https://lindat.mff.cuni.cz/dépôt/xmlui/handle/11234/1-3429)
    - Sélection manuelle des parties "emea" et "frwiki" dans le fichier `1_corpus/SEQUOIA/z_fichiers_intermediaires/sequoia-ud.conllu` (puisqu'il est ordonné) pour créer deux fichiers `1_corpus/SEQUOIA/z_fichiers_intermediaires/emea.conllu` et `1_corpus/SEQUOIA/z_fichiers_intermediaires/frwiki.conllu`
    - Utilisation du script `1_corpus/SEQUOIA/EMFR_txt_from_conllu.py` pour extraire d'abord le texte brut et les sent_id des phrases qu'il contient dans les fichiers `1_corpus/SEQUOIA/z_fichiers_intermediaires/emea_textbrut.txt` et `SEQUOIA/z_fichiers_intermediaires/frwiki_textbrut.txt`
    - Division manuelle du corpus en articles, avec l'annotation "## DEBUT DOC" et "## FIN DOC" dans `1_corpus/SEQUOIA/z_fichiers_intermediaires/emea_textbrut_annote.txt` et `1_corpus/SEQUOIA/z_fichiers_intermediaires/frwiki_textbrut_annote.txt`
    - À partir du contenu du fichier cupt, utilisation de `1_corpus/SEQUOIA/EMFR_corpus_split.py` pour former le fichier `cupt` et `txt` de chaque article selon le sent_id choisi et le source_sent_id dans le fichier cupt (téléchargement de cupt de [PARSEME](https://gitlab.com/parseme/parseme_corpus_fr)), un article par fichier
    - Répertoire obtenus : `1_corpus/SEQUOIA/emea/` et `1_corpus/SEQUOIA/frwiki` à recopier dans `2_traitements/SEQUOIA/emea` et `2_traitements/SEQUOIA/frwiki`. Ils contiennent les fichiers `*.cupt` et `*.txt`.
    - Pour le sous-corpus annodis.er, utiliser le script `ER_get_texte.py` pour obtenir le répertoire de corpus `1_corpus/SEQUOIA/annodisER` à recopier dans `2_traitements/SEQUOIA/annodisER`. Il contient les fichiers `*.cupt` et `*.txt`.
    - **N'oubliez pas de l'annoter avec OFCORS avant la fusion des résultats.**

3. Utilisation du corpus Est Républicain, séparation des articles en fichiers;
    - [Téléchargement](http://redac.univ-tlse2.fr/corpus/estRepublicain.html) et décompression du corpus dans le répertoire `1_corpus/EST_REPUBLICAIN`
    - Lancement du script `1_corpus/EST_REPUBLICAIN/extract_text_er.py` dans `1_corpus/EST_REPUBLICAIN` avec `python extract_texte_er.py <rep_corpus> <taille_min_article>`
    - Le répertoire des articles est `1_corpus/EST_REPUBLICAIN/<rep_corpus>_len<taille>_articles`, et dans lequel chaque article est nommé comme `<date>_<indice_article>.txt`
    - **N'oubliez pas de l'annoter avec Seen2seen et OFCORS avant la fusion des résultats.**

4. Utilisation du corpus ANCOR, conversion des fichiers TEI en fichiers txt;
    - [Téléchargement](https://sharedocs.huma-num.fr/wl/?id=omxQyO3MkOgUgfEVwOlBygZZHYAocTDt) et décompression du corpus dans le répertoire `1_corpus/ANCOR/`. Supprimez les fichiers `1_corpus/ANCOR/*-syntax.tei` et séparez les sous-corpus en différents sous-dossiers.
    - Lancement du script `1_corpus/ANCOR/ancor.py` sur les 4 sous-corpus (`ANCOR/ESLO_ANCOR` `ANCOR/ESLO_CO2` `ANCOR/OTG` et `ANCOR/UBS`) depuis `1_corpus/ANCOR/` avec `python ancor.py <rep_corpus>`
    - Vous pouvez ensuite recopier chaque sous-corpus (`1_corpus/ANCOR/<sous-corpus>`) dans le répertoire `2_traitements/ANCOR/<sous-corpus>` sans les fichiers TEI (ils ne seront pas utiles pour les traitements).
    - **N'oubliez pas de l'annoter avec Seen2seen avant la fusion des résultats.**

5. Fusion du résultat de OFCORS et de celui de Seen2seen au format cupt : ajout de 2 colonnes : la colonne des mentions et celle des chaînes de coréférences;

    - Format : colonne des mentions : id de mentions séparés par `;`  
               colonnes des coréférences : `id_de_chaînes:id_de_mention`, séparés par `;`  
               Exemple :

        ```
        ...
        1   Le  le  DET _   Definite=Def|Gender=Masc|Number=Sing|PronType=Art   2   det _   _   *   31  1:31
        2   trajet  trajet  NOUN    _   Gender=Masc|Number=Sing 4   nsubj   _   _   *   31  1:31
        3   ne  ne  ADV _   Polarity=Neg    4   advmod  _   _   *   *   *
        4   dure    durer   VERB    _   Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin   0   root    _   _   *   *   *
        5   que que ADV _   _   7   advmod  _   _   *   *   *
        6   20  20  NUM _   _   7   nummod  _   _   *   32  *
        7   minutes minute  NOUN    _   Gender=Fem|Number=Plur  4   obj _   _   *   32  *
        8   !   !   PUNCT   _   _   4   punct   _   _   *   *   *
        ...
        ```
    Ici, La mention n°31 est "Le trajet" et la mention n°32 est "20 minutes".
    La chaîne n°1 contient (entre autres) la mention 31. La mention 32 n'appartient à aucune chaîne de coréférence.
    - Scripts pour les fusionner : `2_traitements/CuptParser.py`, `2_traitements/OfcorsFilesParser.py` et `2_traitements/merge_s2s_ofcors.py`
    - Script pour lancer tout :`2_traitements/lanceur.sh`
    - Script pour étudier le résultat :  `2_traitements/statistiques.py`
    - Répertoire de test : `2_traitements/blabla/`
    - Répertoire d'expériences : `2_traitements/SEQUOIA/annodisER/`, `2_traitements/SEQUOIA/emea/`, `2_traitements/SEQUOIA/frwiki/`, `2_traitements/ER2003/ER2003_len300_1-100/`, `2_traitements/ANCOR/ESLO_ANCOR/`, `2_traitements/ANCOR/ESLO_CO2/`, `2_traitements/ANCOR/OTG/` et `2_traitements/ANCOR/UBS/`
    - Anciens scripts : `2_traitements/z_oldies/`

## Utilisation

### Lancement de Seen2seen en version Train et Test
Si vous n'avez jamais lancé Seen2seen vous pouvez commencer par lancer l'entrainement et le test. Attention, c'est assez long.  
Vous aurez besoin du fichier `test.cupt`. Si vous ne l'avez pas, téléchargez-le [ici](https://gitlab.com/parseme/sharedtask-data/-/tree/master/1.2/) et déplacez-le dans le répertoire `Seen2Seen/INPUT/FR/`.  
Le mode annotation_ONLY doit être désactivé (`annotation_ONLY = False` ligne 13 du fichier `Seen2Seen/config.cfg`)  
Vous devez vous trouver dans `Seen2Seen/CODE/`.  

    python3 seen2seen.py

À la fin du traitement, la meilleure configuration de filtres pour le français est mise à jour automatiquement dans le fichier `Seen2Seen/config.cfg`.

### Lancement de Seen2seen en version annotation_ONLY
Le répertoire du corpus à analyser doit se trouver dans `Seen2seen/INPUT/FR/`.  
Les fichiers du corpus sont donc dans `Seen2seen/INPUT/FR/<nom_repertoire_corpus>/`  
Ils doivent être soit au format .cupt soit au format .txt.  
Le mode annotation_ONLY doit être activé (`annotation_ONLY = True` ligne 13 du fichier `Seen2Seen/config.cfg`)  
Vous devez vous trouver dans `Seen2Seen/CODE/`.  

    python3 seen2seen.py <nom_repertoire_corpus>

OU

    python3 seen2seen.py Seen2seen/INPUT/FR/<nom_repertoire_corpus>/

Dans les deux cas seul le nom du répertoire sera pris en compte.
Les résultats de l'annotation se trouvent dans `Seen2Seen/OUTPUT_seen/ANNOTATIONS/FR/<nom_repertoire_corpus>/` et se terminent par`_annote.config48.cupt`.

### Lancement d'OFCORS et de la fusion:
Vous devez vous trouvez dans `MWE_coref/2_traitements/`.  

    ./lanceur.sh -os blabla/
  
Cette commande lance tout le processus sur les fichiers contenus dans le répertoire `2_traitements/blabla/`. Ce répertoire doit contenir les fichiers textes et les fichiers cupt annotés en MWEs (passés dans Seen2seen) du corpus.
Les fichiers textes sont d'abord passés dans OFCORS et les fichiers résultats (`<nom>_resulting_chains.json`, `<nom>_mentions_output.json` et `<nom>_token.json`) sont créés dans `2_traitements/blabla/ofcors_outputs`. Ensuite, le script `2_traitements/merge_s2s_ofcors.py` est appelé pour créer les fichiers cupt avec les deux colonnes supplémentaires dans le dossier `2_traitements/blabla/mwecoref_outputs` à partir des sorties d'OFCORS et des fichiers cupt. Enfin, le script `2_traitements/statistiques.py` affiche les résultats dans le terminal.  
OFCORS est lancé avec le tokenizer stanza, en mode fenêtre (taille de 8).


    ./lanceur.sh -o blabla/

Cette commande ne lance que la partie OFCORS.  
OFCORS est lancé avec le tokenizer stanza, en mode fenêtre (taille de 8).


    ./lanceur.sh -s blabla/

Cette commande ne lance que les scripts `2_traitements/merge_s2s_ofcors.py` et `2_traitements/statistiques.py`. Elle nécessite que les fichiers résultats de OFCORS sur les fichiers de `2_traitements/blabla/` se trouvent dans `2_traitements/blabla/ofcors_outputs`.


## Résultats  
Légendes des exemples:  
- [mentions]  
- **expressions**  

### Fichier de sortie
```
        "FICHIER": "emea_2_mwe_coref.cupt",
        "PHRASE": "Aclasta ne doit être utilisé, chez les patients souffrant de la maladie osseuse de Paget, que par un médecin expérimenté dans le traitement de cette maladie.",
        "TOKENS": "['souffrant', 'de', 'maladie']",
        "LEMMES": [
            "souffrir",
            "de",
            "maladie"
        ],
        "COREF": "['*', '*', '58:131']",
        "CAS": "{'131': 4}",
        "CHAINE(S)": {
            "58": "{'131': ['la', 'maladie', 'osseuse', 'de', 'Paget'], '135': ['cette', 'maladie'], '138': ['une', 'maladie'], '139': ['qui']}"
        }
```
Les différentes expressions polylexicales faisant parties d'une chaîne de coréférence sont regroupées par type (VID, LVC.full ...). Pour chaque type sont ensuite affichées les informations sur les expressions polylexicales comme ci-dessus.
* FICHIER :  le fichier où se trouve l'expression.
* PHRASE :  La phrase où se trouve l'expression.
* INFOS : 
    - Les tokens qui composent l'expression.
    - Les lemmes des tokens qui composent l'expression.
    - Pour chaque token : son appartenance ou non à une chaîne de coréférence. Si `*` alors il n'appartient pas à une chaîne, sinon `indice de chaine : indice de mention`. Dans l'exemple ci-dessus, "maladie" correspond à la mention 131 et fait partie de la chaîne de coréférence 68.
    - Le cas correspondant pour chaque mention. (CAS 1 : expression incluse dans mention, CAS 2 : la mention et l'expression sont identiques, CAS 3 : mention incluse dans l'expression et CAS 4 : chevauchement)
* CHAINE(S) : Pour chaque chaîne à laquelle l'expression appartient, on affiche l'ensemble des mentions de la chaîne. Dans l'exemple ci-dessus une seule chaîne a été trouvée, on affiche donc uniquement la chaîne 58 qui contient les mentions 131 ("la maladie osseuse de Paget"), 135 ("cette maladie"), 138 ("une maladie") et 139 ("qui").

### Annotation de validation
Pour examiner les croisements des expressions polylexicales et des chaînes de coréférence, nous annotons trois aspects : *VALIDATION*, *DEGRE DE COMPOSITIONNALITE* et *SOURCE D'ERREUR*.

- **"VALIDATION"**
    - 5 valeurs possibles : "vrai", "faux", "non concerné", "discutable" et "répétitions".
    - **"vrai"** : L'exemple est utilisable pour notre hypothèse, c'est-à-dire que le composant détecté dans l'expression polylexicale se trouve dans une vraie chaîne de coréférence (interprétation humaine), quelle que soit la performance du système.  
    Par exemple, nous mettons "vrai" pour cette phrase : _"Pour la fin de l'année et après avoir distribué les colis aux anciens, M. Didier Louis, lors de son allocution, a fait tout d'abord [une rétrospective des **travaux**] [qui] ont été **accomplis** dans la commune."_ . Le composant "travaux" dans "accomplir travaux" est vraiment coréférent avec "qui", même si la mention détectée "une rétrospective des travaux" est fausse.
    - **"faux"** : Cas contraire du précédent, l'exemple est trouvé à cause des erreurs du système.  
    Par exemple, nous mettons "faux" pour cette phrase : _"Après plusieurs mois, [la Chine] **met** [**une sourdine**] à ses objections et le ministère français des Affaires étrangères lève son veto."_
    - **"non concerné"** : Souvent attribué à un exemple de cas 1 (expression polylexicale inclue dans la mention détectée), qui ne fait pas partie de notre analyse.  
    Par exemple, nous mettons "non concerné" pour cette phrase : _"[De nombreux patients **atteints** d'**ostéoporose**] n'ont aucun symptôme, mais [ils] présentent néanmoins un risque de fracture osseuse car l'ostéoporose a fragilisé leurs os."_ car on s'intéresse seulement à la reprise des composants d'une expression.
    - **"discutable"** : L'exemple peut être vrai ou faux selon l'interprétation humaine.  
    Par exemple, dans la phrase _"- Créé par la Fédération nationale qui perpétue le souvenir de l'homme d'Etat meusien qui fut ministre de la Guerre et l'initiateur d'un système de défense qui **porte** [son **nom**], le prix [André-Maginot] récompense des travaux liés au civisme et au devoir de mémoire."_ , la coréférence entre les deux mentions "son nom" et "André-Maginot" est difficile à déterminer, puisque le dernier est le nom du prix et non le nom de la personne.
    - **"répétitions"** : Répétitions simples à cause des disfluences ou réutilisations des expressions complètes dans le texte (courant dans le corpus oral ANCOR).  
    Par exemple nous mettons "répétitions" pour ces phrases : _"cinq kilomètres d' ici ? ah non je crois que si j' **ai** [**le temps**] j' irai la voir" "oui mais vous préférez vous déplacer plutôt oui si j' ai [le temps] j' aime mieux j' aime mieux aller aller les voir"_ et _"je **ferais** [un **détour**] pour aller à Chambord je ferais [un détour] vous voyez ça c' est c' est c' est c' est sans doute dans mon tempérament vous comprenez ça c' est c' est c' est personnel ça"_

- **"DEGRE DE COMPOSITIONNALITE"**
    - Cette valeur n'est renseignée que pour les exemples vrais. 3 valeurs sont possibles : "faible", "moyen" ou "fort".
    - Nous nous sommes inspirées de l'article [_Unsupervised Compositionality Prediction of Nominal Compounds_](https://hal-univ-tln.archives-ouvertes.fr/hal-02318196/) (Cordeiro et al. 2019) pour créer un test de compositionnalité adapté aux expressions polylexicales verbales. Vous pouvez retrouver ce test et les annotations dans le dossier `4_compositionnalite/`. Les expressions ont été annotées par 4 annotateurs indépendants.

- **"SOURCE D'ERREUR"**
    - Les erreurs peuvent venir de deux côtés : l'expression polylexicale ou la chaîne de coréférence. Nous les définissons avec 5 sources d'erreurs : 
    - **"MWE incorrecte"** : l'expression détectée n'est pas une vraie expression polylexicale malgré les lemmes corrects.
    - **"MWE littérale"** : un sous-cas de l'erreur précédente, l'expression détectée demande une lecture littérale dans ce contexte.  
    eg. _"Nous travaillons en accord avec les organisateurs et proposons à chaque personne qui s'apprête à reprendre le volant de souffler dans le ballon pour voir où **il en est**."_
    - **"MWE type incorrect"** : L'expression détectée est correcte, mais elle est classée dans une catégorie incorrecte.
    - **"chaîne incorrecte"** : Aucune des mentions de la chaîne n'est coréférente avec la mention de l'expression.
    - **"mention incorrecte"** : La mention utilisée dans la chaîne détectée est incorrecte, mais la chaîne serait correcte si la mention prenait en compte plus ou moins de mots.  
    eg. _"Pour la fin de l'année et après avoir distribué les colis aux anciens, M. Didier Louis, lors de son allocution, a fait tout d'abord [une rétrospective des **travaux**] [qui] ont été **accomplis** dans la commune."_, la chaîne serait correcte si on changeait "une rétrospective des **travaux**" par "des **travaux**"  

L'annotation a été réalisée lors de réunions, les annotateurs n'étaient donc pas indépendants des autres. Il y avait entre 2 et 7 annotateurs. Les phrases étaient lues et vérifiées puis les annotateurs discutaient entre eux de la validité ou non des exemples.

### Nombres des croisements
| Type | Nombre de croisements vrais | Nombre de EPV détectés |
| --- | --------- | --------- |
| VID | 29 | 5266 |
| LVC.full | 245 | 1726 |
| LVC.cause | 1 | 18 |
| IRV | 1 | 996 |
| MVC | 0 | 41 |
| TOTAL | 276 | 8047 |


### Quelques exemples corrects

-  Dès la fin de la guerre, la veuve de Théophile Maupas, soutenue par la Ligue des droits de l'Homme contactée dès le mois d'avril 1915, entama [un combat] pour la réhabilitation de son époux et des autres caporaux fusillés de Souain ; [**combat**] contre les institutions, **mené** sans relâche, qui dura près de deux décennies et qui, en dehors de son activité d'institutrice, l'occupa à plein temps. (FRWIKI)
- Aclasta ne doit être utilisé, chez les patients **souffrant de** [la **maladie** osseuse de Paget], que par un médecin expérimenté dans le traitement de [cette maladie]. (EMEA)
- Dans le cas où vous avez **eu** récemment [une **fracture** de hanche], il est recommandé qu'Aclasta soit administré 2 semaines ou plus après réparation de [votre fracture]. (EMEA)
- Il est utilisé en conjonction avec de l'aspirine et du clopidogel (médicaments contribuant à prévenir les caillots sanguins) chez les patients sur le point de **subir** [un **traitement**] pour leur SCA, comme un [traitement médicamenteux], subissant une angioplastie ou [un pontage coronarien]. (EMEA)
- Pour la fin de l'année et après avoir distribué les colis aux anciens, M. Didier Louis, lors de son allocution, a fait tout d'abord une rétrospective [des **travaux**] [qui] ont été **accomplis** dans la commune. (Est Républicain)
- Une course entamée à l'aube, 3 h 35, pour se terminer presque deux heures plus tard à l'hôtel de police... où sa cliente a avoué [le meurtre de l'homme] qui lui offrait l'hospitalité. [Un **crime**] **commis** une semaine plus tôt, dans un studio de la résidence Lemire. (Est Républicain)
- D'ores et déjà, Guy Rolland se demande « si l'année prochaine nous n'allons pas **mener** [des **actions** plus ciblées] comme [celles] que nous menons en direction des boîtes de nuit. (Est Républicain)
- j' aimerais vous **poser** [une **dernière question**] mais alors vous n' êtes pas obligée d' [y] répondre est -ce qu' il y a un parti politique qui représente bien vos opinions" (ESLO_ANCOR)
- à peu près pour la même raison mais seulement c' était moins développé dans mon temps enfin c' était [une impression] à moi j' **ai** [l' **impression**] que c' était moins développé que maintenant (ESLO_CO2)