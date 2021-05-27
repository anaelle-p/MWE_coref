# -*- coding: utf-8 -*-
# Anaëlle Pierredon et Jianying Liu

"""
Production de statistiques sur la totalité des MWEs des différents fichiers.
Args:
    Répertoire où se trouvent les cupt+
"""

import glob
import argparse

# -------------------------- CLASSES --------------------------


class ExprPoly():
    """
    Expressions polylexicales.

    Attributs:
        identifiant (int): Identifiant de la MWE dans la phrase (commence à 1)
        type_mwe (str): Type de la MWE (LVC.full, VID...)
        texte (str): Texte de la phrase où se trouve la MWE
        tokens (liste de str): Liste des tokens composant la MWE
        coref (liste de str): Appartenance ou non à une chaîne de coréférence
                              pour chaque token ("*" = pas dans une chaîne)
        schema_mwe (liste de str): Liste représentant les tokens de la phrase
                                - "*": ce token n'appartient pas à une MWE
                                - indice: ce token appartient à une MWE
        schema_mention (dict): représente les tokens de la phrase
                    - "*": token n'appartient pas à une mention de la chaine
                    - indice: token appartient à une mention de la chaine
                    Avec en clé la mention concernée
        cas (dict): Les différents cas possible de débordement ou d'inclusion
                   d'une mention dans une MWE avec en clé la mention concernée
        chaines (liste de dict): Les chaines de coreférences de la MWE
    """
    def __init__(self, identifiant, type_mwe, texte, tokens, coref):
        # Définis immédiatement
        self.identifiant = identifiant  # 1 ou 2 (par phrase)
        self.type_mwe = type_mwe  # LVC.full
        self.texte = texte  # Merci de me donner l'occasion de...
        self.tokens = [tokens]  # ['me', 'donner']
        self.coref = [coref]  # ['*', '3']

        # Définis plus tard
        self.schema_mwe = []  # ["*", "*", "1", "1", "*", "*", "*", "*", ...]
        self.schema_mention = {}  # {18: ["*", "*", "*", "18", "*", ...]}
        self.cas = {}  # {18: "1"}
        self.chaines = []

    def append_schemas(self, schema_mwe, schema_mention):
        """
        Ajoute des attributs schema_mwe, schema_mention et cas à partir des
        attributs déjà existants (identifiant et coref).
        """

        # Schema MWE
        for indice in schema_mwe:
            liste_indices = [elt.split(":")[0] for elt in indice.split(";")]
            if str(self.identifiant) not in liste_indices:
                # Ce n'est pas la MWE qu'on est en train de définir
                self.schema_mwe.append("*")
            else:
                self.schema_mwe.append('1')

        # Mentions
        coref = []
        for elt in self.coref:
            if elt != "*":
                coref.extend(elt.split(";"))
        coref = list({elt.split(':')[1] for elt in coref if elt != "*"})

        if len(set(coref)) > 0:  # tout sauf ["*", "*"]
            for ment_cor in coref:
                self.schema_mention[ment_cor] = []
                for ment_sch in schema_mention:
                    if ment_cor in ment_sch.split(';'):
                        self.schema_mention[ment_cor].append(ment_cor)
                    else:
                        self.schema_mention[ment_cor].append("*")
                self.cas[ment_cor] = self.determiner_cas(ment_cor)

    def append_chaine(self, dico_coref):
        """
        Ajoute l'attribut chaines.

        Args:
            dico_coref (dict): Toutes les chaînes du répertoire
        """
        for corefs in self.coref:
            if corefs != "*":
                for coref in corefs.split(";"):
                    id_coref = coref.split(":")[0]
                    if dico_coref[id_coref] not in self.chaines:
                        self.chaines.append(dico_coref[id_coref])

    def determiner_cas(self, ment):
        """
        Détermine le cas selon le chevauchement ou d'inclusion
        d'une mention dans une MWE.

        Args:
            ment (str), l'identifiant de la mention à étudier
        Returns:
            cas (int), le cas correspondant aux schémas de la mention et
                       de la MWE:
        - CAS 1 -> La mention déborde de la MWE
        - CAS 2 -> La mention et la MWE sont identiques
        - CAS 3 -> La mention correspond à une partie de la MWE
        - CAS 4 -> MWE   =   se(1) faire(1) des(*) soucis(1)
                   MENTION = se(*) faire(*) des(1) soucis(1)
        """
        # Récupérer indices de fin et de début
        ind_mentions = span_schema(self.schema_mention[ment])[0]
        ind_mwes = span_schema(self.schema_mwe)

        # Comparaisons
        liste_cas = []
        for morceau_mwe in ind_mwes:
            debut_mwe, fin_mwe = morceau_mwe
            debut_ment, fin_ment = ind_mentions
            # DÉBORDEMENTS DE LA MENTION
            # MWE:[*, 1, 1]MENT:[1, 1, 1] || MWE:[1, 1, *, 1]MENT:[*, *, 1, 1]
            if debut_mwe > debut_ment and fin_mwe == fin_ment:
                if len(liste_cas) > 0:  # La MWE est en plusieurs parties
                    cas = 4
                else:
                    cas = 1
            # MWE:[1, 1, *]MENT:[1, 1, 1]
            elif debut_mwe == debut_ment and fin_mwe < fin_ment:
                cas = 1
            # MWE:[*, 1, 1]MENT:[1, 1, *] || MWE:[1, *, 1, 1]MENT:[*, 1, 1, *]
            elif fin_mwe > fin_ment >= debut_mwe > debut_ment:
                if len(liste_cas) > 0:  # La MWE est en plusieurs parties
                    cas = 4
                else:
                    cas = 1
            # MWE:[1, 1, *]MENT:[*, 1, 1]
            elif debut_mwe < debut_ment <= fin_mwe < fin_ment:
                cas = 1
            # MWE:[*, 1, *]MENT:[1, 1, 1] || MWE:[1, *, 1, *]MENT:[*, 1, 1, 1]
            elif debut_mwe > debut_ment and fin_mwe < fin_ment:
                if len(liste_cas) > 0:  # La MWE est en plusieurs parties
                    cas = 4
                else:
                    cas = 1

            # SCHÉMAS IDENTIQUES
            # MWE:[1, 1, 1]MENT:[1, 1, 1]
            elif debut_mwe == debut_ment and fin_mwe == fin_ment:
                cas = 2

            # INCLUSION D'UNE MENTION PLUS PETITE
            # MWE:[1, 1, 1]MENT:[*, 1, 1]
            elif debut_mwe < debut_ment and fin_mwe == fin_ment:
                cas = 3
            # MWE:[1, 1, 1]MENT:[1, 1, *]
            elif debut_mwe == debut_ment and fin_mwe > fin_ment:
                cas = 3
            # MWE:[1, 1, 1]MENT:[*, 1, *]
            elif debut_mwe < debut_ment and fin_mwe > fin_ment:
                cas = 3

            else:
                cas = "*"
            liste_cas.append(cas)

        # On prend le dernier cas trouvé s'il y en a un
        if cas == "*":
            for element in liste_cas:
                if element != "*":
                    cas = element

        # Vérifications
        # print(ind_mentions)
        # print(ind_mwes)
        # print(f"LISTE : {liste_cas}")
        # print(f"CAS : {cas}")

        return cas


class TypeExpr():
    """
    Liste d'expressions polylexicales par type.

    Attributs:
        type_mwe (str): Type des MWEs (LVC.full, VID...)
        mwes (liste de ExprPoly): La liste des MWEs de ce type
    """
    def __init__(self, type_mwe):
        self.type_mwe = type_mwe
        self.mwes = []


class Repertoire():
    """
    Informations globales sur tous les fichiers du répertoire donné.

    Attributs:
        repertoire (str): le nom du répertoire
        liste_phrases (liste de str): liste des phrases de tous les fichiers
        liste_mwes (liste de ExprPoly): liste des MWEs de tous les fichiers
        chaines (dict): liste des chaines de coréférence de tous les fichiers
        liste_type (liste de TypeExpr): liste des MWEs par type
    """

    def __init__(self, repertoire):
        self.repertoire = repertoire
        self.liste_phrases = self.lecture()

        coref = {}
        self.liste_mwes = []
        for phrase in self.liste_phrases:
            mwes, coref = phrase_mwe(phrase, coref)
            self.liste_mwes.extend(mwes)

        self.chaines = coref
        self.liste_type = complet_type(self.liste_mwes)

    def lecture(self):
        """
        Lecture des fichiers.

        Returns:
            liste_phrases (liste de str), la liste des phrases de tous les
            fichiers du répertoire.
        """
        liste_phrases = []
        for fichier in glob.glob(f"{self.repertoire}*"):
            with open(fichier, 'r') as entree:
                sortie = entree.read().split('\n\n')
            liste_phrases.extend(sortie)
        return liste_phrases


# ----------------------- FONCTIONS (CONSTRUCTION) -----------------------


def phrase_mwe(phrase, dico_coref):
    """
    Liste des MWEs par phrases

    Args:
        phrase (str), les lignes de la phrase
        dico_coref (dict), les chaînes de coréférence trouvées dans les
                           phrases précédentes
    Returns:
        liste_expoly (liste de ExprPoly), la liste des MWEs de la phrase
        dico_coref (dict), complété par les nouvelles chaînes éventuelles
    """
    liste_expoly = []
    schema_mwe = []
    schema_mention = []

    for ligne in phrase.split('\n'):
        if ligne.startswith('# text'):
            texte = ligne.split(' = ')[1]
        if ligne.startswith("#") or ligne.strip() == "":
            continue
        ligne = ligne.strip().split('\t')
        mwes = ligne[10]
        mention = ligne[11]
        corefs = ligne[12]
        schema_mwe.append(mwes)
        schema_mention.append(mention)
        if mwes != "*":
            for mwe in mwes.split(';'):
                infos = mwe.split(':')
                id_mwe = int(infos[0])
                if len(infos) == 2:
                    expoly = ExprPoly(id_mwe, infos[1], texte, ligne[1],
                                      ligne[12])
                    liste_expoly.append(expoly)
                else:
                    for expoly in liste_expoly:
                        if expoly.identifiant == id_mwe:
                            expoly.tokens.append(ligne[1])
                            expoly.coref.append(ligne[12])
        if corefs != "*":
            for coref in corefs.split(';'):
                coref_id, coref_mention = coref.split(':')
                if coref_id not in dico_coref:
                    dico_coref[coref_id] = {}
                if coref_mention not in dico_coref[coref_id]:
                    dico_coref[coref_id][coref_mention] = []
                dico_coref[coref_id][coref_mention].append(ligne[1])

    for expoly in liste_expoly:
        expoly.append_schemas(schema_mwe, schema_mention)

    return liste_expoly, dico_coref


def complet_type(liste_expoly):
    """
    Args:
        liste_expoly (liste de ExprPoly), la liste des MWEs de la phrase
    Returns:
        liste_typexp (liste de TypeExpr), la liste des types existants et les
                    expressions polylexicales qui correspondent à ce type.
    """
    liste_typexp = list(set(expoly.type_mwe for expoly in liste_expoly))
    liste_typexp = [TypeExpr(type_mwe) for type_mwe in liste_typexp]

    for expoly in liste_expoly:
        for type_item in liste_typexp:
            if type_item.type_mwe == expoly.type_mwe:
                type_item.mwes.append(expoly)
    return liste_typexp


def span_schema(schema):
    """
    Récupère les identifiant de début et de fin des éléments d'un schéma.

    Args:
        schema(liste de str)
    Returns:
        liste_ind (liste de liste de int): les identifiants de début et de fin
        pour chaque partie
        ex: [*, 1, 1, *] -> [[1,2]]
            [1, *, 1, 1] -> [[0,0], [2,3]]
    """
    encours = False
    liste_ind = []
    for indice, element in enumerate(schema):
        if element != "*" and not encours:
            # L'élément vient de commencer
            encours = True
            debut = indice
        elif element == "*" and encours:
            # l'élément vient de se finir
            encours = False
            fin = indice - 1
            liste_ind.append([debut, fin])

    return liste_ind


# ----------------------- FONCTIONS (AFFICHAGE) -----------------------


def affichage_infos(liste_typexp):
    """
    Affiche les tokens, la coref et le cas par MWE classées selon leur type.
    """
    print("-"*50)
    for typexp in liste_typexp:
        print(typexp.type_mwe)
        for expoly in typexp.mwes:
            print(f"tokens : {expoly.tokens}, coref : {expoly.coref}")


def affichage_stats_globales(liste_typexp):
    """
    Affiche le nombre de MWEs par type et le nombre de MWEs total.
    """
    print("-"*50)
    total = 0
    for typexp in liste_typexp:
        print(f"{typexp.type_mwe} : {len(typexp.mwes)}")
        total += len(typexp.mwes)
    print(f"TOTAL : {total}")


def affichage_stats_coref(liste_typexp):
    """
    Affiche le nombre de MWEs faisant partie d'une chaîne de coréférence par
    type et total, ainsi que les information sur ces MWEs (texte, tokens,
    coref, cas et chaines).
    """
    print("-"*50)
    total = 0
    nb_coref_total = 0
    for typexp in liste_typexp:
        print(typexp.type_mwe)
        total += len(typexp.mwes)
        nb_coref = 0
        for expoly in typexp.mwes:
            coref = len([el for el in expoly.coref if el != "*"])
            if coref > 0:
                nb_coref += 1
                nb_coref_total += 1
                print(f"\tTEXTE : {expoly.texte}")
                print(f"\tINFOS : tokens : {expoly.tokens}, "
                      f"coref : {expoly.coref}, cas : {expoly.cas}")
                print("\tCHAÎNE(S) : ")
                for chaine in expoly.chaines:
                    print(f"\t   -{chaine}")
                print("\n")
        print(f"==========>{nb_coref}/{len(typexp.mwes)}\n\n")
    print(f"TOTAL\n==========>{nb_coref_total}/{total}\n")


# --------------------------- MAIN ---------------------------


def main():
    """
    Créer une liste d'expressions polylexicales par type et afficher des
    statistiques.
    """
    parser = argparse.ArgumentParser(description="fichier")
    parser.add_argument("rep", help="répertoire des cupt+")
    args = parser.parse_args()

    repertoire = Repertoire(args.rep)

    for expoly in repertoire.liste_mwes:
        ExprPoly.append_chaine(expoly, repertoire.chaines)

    affichage_infos(repertoire.liste_type)
    affichage_stats_globales(repertoire.liste_type)
    affichage_stats_coref(repertoire.liste_type)


if __name__ == "__main__":
    main()
