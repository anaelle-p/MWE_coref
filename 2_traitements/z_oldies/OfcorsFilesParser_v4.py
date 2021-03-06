# -*- coding: utf-8 -*-
# Jianying Liu et Anaëlle Pierredon
"""
parser et unifier les 3 fichiers sorties de l'OFCORS
"""
import json
import re


class Mention():
    """
    La classe contient tous les infos d'une mention:

    Attributes:
        content (list): liste de ses tokens text
        start (int): indice de son premier token
        end (int): indice de son dernier token
        mid (str): id de mention dans fichier mention_output (commence par 1)
        span (list): liste des indice de tous les tokens dans cette mention
        is_coref (bool): montrer si une mention est dans une chaîne de
            coréférence, False par défaut
        chaine_id (str): id de la chaîne qu'il fait partie
    """
    def __init__(self, content, start, end, mid):
        self.content = content
        self.start = int(start)  # 4
        self.end = int(end)  # 6
        self.mid = mid
        self.span = list(range(self.start, self.end+1))  # [4,5,6]
        self.is_coref = False
        self.chaine_id = ""


class Token():
    """
    La classe d'un token pour la sortie de l'ofcors

    Attributes:
        text (str): texte de ce token
        i_token (str): l'indice de token distribué par OFCORS(debut 0) mais
            unifié au cupt
        is_mention (bool): montre si le token fait partie d'une mention
        ment_list (list): une liste des Mention objets liés à ce token
        ment_coref_list (dict):
            un dictionnaire des dict contenant l'id de mention, l'id de coref
            clé dans le dict: ment_id,   valeur: ment_id, coref_id
    """
    def __init__(self, i_token, text):
        self.text = text
        self.i_token = i_token
        self.is_mention = False
        self.ment_list = []  # Mention object
        self.ment_coref_list = {}  # 0:1; 0:2 ==>  {"1":{ment_id:"1", coref_id:"0"},"2":{ment_id:"2", coref_id:"0"}}


class Mentions():
    """
    Classe sert à initialiser les informatons
    à partir du fichier mentions_output.json de l'ofcors.
    Elle lie les infos des chaînes de coréférences à chaque mention.

    Attributes:
        tokens (dict): un dictionnaire liste tous les tokens
        qui fait partie d'une mention. cupt
            clé: id de token, valeur: liste des id de mention
        mentions (dict): dictionnaire de Mention objet
        ments_omis (dict): dictionnaire de mentions omises dans le résultat
            (à cause de réalignement de phrases),
            respecter la structure du fichier json
    """
    def __init__(self, filepath, ofcors_output):
        """
        Initialiser l'info dans le fichier
        Args:
            filepath (str): chemin vers ce fichier
        """
        self.tokens = {}
        self.mentions = {}
        self.ments_omis = {}  # NEW
        with open(filepath, encoding="utf8") as mentions_file:
            text = mentions_file.read()
        dico_mentions = json.loads(text)

        # transformer en l'indice de token de cupt
        dico_paral = ofcors_output.tokens_i_paral

        # NEW PRINT
        # for i, j in dico_paral.items():
        #     print(i, j)

        for ment in dico_mentions.values():
            try:
                i_start = min([int(i) for i in dico_paral.get(ment["START"])])
                ment["START"] = i_start
                i_end = max([int(i) for i in dico_paral.get(ment["END"])])
                ment["END"] = i_end
            except TypeError:
                ment["START"] = "_"
                ment["END"] = "_"

        for cle, ment in dico_mentions.items():
            # NEW PRINT
            # print(ment["CONTENT"], ment["START"], ment["END"], cle)

            if ment["START"] == "_" or ment["START"] == "_":
                self.ments_omis[cle] = ment
            else:
                mention = Mention(ment["CONTENT"], ment["START"],
                                  ment["END"], cle)  # START & END : int
                self.mentions[mention.mid] = mention
        self.tokens2mentions()   # indice de cupt

    def chainer(self, dico_chaine):
        """
        Ajouter l'info de chaîne de coréférence dans Mention objet
        Args:
            dico_chaine (dict): dict mentions(clé, str)<-->chaine(valeur, str)
        """
        for mention in self.mentions.values():
            mention.chaine_id = dico_chaine.get(mention.mid, "")
            if mention.chaine_id != "":
                mention.is_coref = True

    def tokens2mentions(self):
        """
        Restructuer les infos, remplir dico Mentions.tokens,
        utilisé seulement à l'intérieur
        """
        for mention in self.mentions.values():
            for i_token in mention.span:
                if str(i_token) not in self.tokens.keys():
                    self.tokens[str(i_token)] = [mention.mid]
                else:
                    self.tokens[str(i_token)].append(mention.mid)


class CorefChaines():
    """
    Classe sert à initialiser les informatons
    à partir du fichier resulting_chains.json de l'ofcors.

    Attributes:
        ment_cluster (dict): dictionnaire ayant
            clef: l'id de mention  valeur: l'id de chaine de coréférence
        clusters (dict): prendre la valeur de la clé "clusters" du fichier
    """

    def __init__(self, filepath, file=True):
        """
        Initialiser les infos et les remplir dans l'objet

        Args:
            filepath (str):
                1) chemin vers le fichier resulting_chains,json
                2) le contenu du fichier resulting_chains.json, même structure
                    forme: dict
            file (bool): mettre à False si l'entrée est le contenu
        """
        self.ment_cluster = {}
        self.clusters = {}
        if file:
            with open(filepath, encoding="utf8") as chaines_file:
                text = chaines_file.read()
            dico_json = json.loads(text)
        else:
            dico_json = filepath

        if dico_json["clusters"] != {}:
            self.clusters = dico_json.get("clusters")
            for no_cluster, ments in self.clusters.items():
                for id_mention in ments:
                    self.ment_cluster[id_mention] = no_cluster
            self.has_coref = True
        else:  # TODO: need or not?
            self.has_coref = False


class OfcorsOutput():
    """
    Classe sert à fusionner tous les sortie de l'ofcors.

    Attributes:
        tokens (dict): un dictionnaire des Token objets,
                       clef: id, indice number: cupt
        tokens_i_paral (dict): dictionnaire des indices:
            clé: indice dans tokens ofcors,
            valeur: liste des indices dans tokens cupt
            exemple: {'0': ['0'], '1': ['1'] ... '8': ['7'], '9': ['8', '9']}
    """

    def __init__(self, filepath, cupt_tokens):
        """
        Args:
            filepath (str): chemin vers fichier tokens.json de l'ofcors
            cupt_tokens (dict) : Cupt.tokens
        """
        self.tokens = {}
        with open(filepath, encoding="utf8") as tokens_file:
            text = tokens_file.read()
        dico_json = json.loads(text)
        self.tokenisation_unify(dico_json, cupt_tokens)
        for i, t_form in cupt_tokens.items():  # change to cupt token
            token = Token(i, t_form)
            self.tokens[i] = token

    def merge_result(self, mentions):
        """
        fussionner le résultat de l'ofcors dans cette liste des tokens.
        Args:
            mentions (Mentions): l'objet Mentions contenant l'info de coréf
        """
        for token in self.tokens.values():
            if token.i_token in mentions.tokens.keys():
                token.is_mention = True
                ment_ids = mentions.tokens[token.i_token]
                for ment_id in ment_ids:
                    mention = mentions.mentions[ment_id]
                    token.ment_list.append(mention)
                    token.ment_coref_list[ment_id] = {"ment_id": mention.mid, "coref_id": mention.chaine_id}

    def tokenisation_unify(self, tokens_ofcors, tokens_cupt):
        """
        tokens_ofcors : contenu du json file
        token_cupt: Cupt.tokens
        """
        i = 0
        i_o = 0
        dico_o = {}
        while i < len(tokens_cupt):
            token = tokens_cupt.get(str(i))["token_form"]
            token_mwt = tokens_cupt.get(str(i))["MWT"]
            token_o = tokens_ofcors.get(str(i_o))

            # traiter l'espace dans les chiffres
            token = delete_num_space(token)
            token_o = delete_num_space(token_o)

            try:
                # si le token est seulement retour à la ligne dans OFCORS,
                # on saute ce token dans ofcors
                if token_o == "\n":
                    i_o += 1
                    continue
                # chaine identique
                # elif token == token_o:  ####################################
                if token == token_o:
                    dico_o[str(i_o)] = [str(i)]
                # multi-word token, comme article contracte
                elif token_mwt != []:
                    for i_item, item_mwt in enumerate(token_mwt):
                        if item_mwt.lower() == token_o.lower():
                            dico_o[str(i_o)] = [str(i)]
                            if i_item != len(token_mwt)-1:
                                i_o += 1
                                token_o = tokens_ofcors.get(str(i_o))
                        else:
                            raise Alignementerror(f"Le composant ('{token_o}' et '{item_mwt}') du MWT '{token}' à l'indice {i_o} de l'ofcors ne se décompose pas de la même manière")
                else:
                    if len(token) == len(token_o):
                        raise Alignementerror(f"Chaine de caractere differente (cupt: {token}, ofcors: {token_o})")
                    else:  # longueur differentes
                        if len(token) > len(token_o):
                            while len(token) > len(token_o):
                                dico_o[str(i_o)] = [str(i)]
                                i_o += 1
                                token_o = token_o + delete_num_space(tokens_ofcors.get(str(i_o)))

                            if len(token) != len(token_o) or token != token_o:
                                raise Alignementerror(f"token:{token}(indice: {i})\ttoken_o:{token_o}(indice dans l'ofcors: {i_o})\nChaine de caractere combinee toujours differente")
                            elif token == token_o:
                                dico_o[str(i_o)] = [str(i)]

                        else:  # len(token) < len(token_o)
                            while len(token) < len(token_o):
                                if not dico_o.get(str(i_o)):
                                    dico_o[str(i_o)] = [str(i)]
                                else:
                                    dico_o[str(i_o)].append(str(i))
                                i += 1

                                token = token + delete_num_space(tokens_cupt.get(str(i))["token_form"])

                            if len(token) != len(token_o) or token != token_o:
                                raise Alignementerror(f"token:{token}\ttoken_o:{token_o}\nchaine de caractere combinee toujours differente, ne peut rien faire")
                            elif token == token_o:
                                dico_o[str(i_o)].append(str(i))
                
                # dans la branche try
                i += 1
                i_o += 1

            except Alignementerror as err:
                print(err.msg)
                print("-----Recommencement depuis la phrase suivante-----")
                # trouver le token au début de la phrase suivante (cupt)
                while tokens_cupt.get(str(i))["indice_cupt"] != "1":
                    i += 1
                token = delete_num_space(tokens_cupt.get(str(i))["token_form"])

                # comparer l'un après l'autre le token ofcors avec ce token débutant
                while token != token_o:
                    i_o += 1
                    token_o = delete_num_space(tokens_ofcors.get(str(i_o)))

                print(f"Nouveau début: token ({token}, {i}), token_o ({token_o}, {i_o})")

        # {'0': ['0'], '1': ['1'], '2': ['1'],...'8': ['7'], '9': ['8', '9']}
        self.tokens_i_paral = dico_o


def delete_num_space(string):
    """
    Supprime l'espace dans les nombres.
    """
    if re.match("[0-9 ]+", string):
        string = re.sub(" ", "", string)
    return string


class Alignementerror(Exception):
    """
    Redéfinir une nouvelle erreur pour l'échec d'alignement
    """
    def __init__(self, msg):
        self.msg = msg
