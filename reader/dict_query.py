import sqlite3
from collections import OrderedDict


# Returns whether argument is a Kanji_element, Reading_element or not in the
# dictionary
# 0 = K_element, 1 = R_element, -1 = not in dictionary
def morphene_type(morphene, cursor):
    # tuples = (morphene)
    sql = """
    SELECT CASE WHEN :morphene NOT IN
           (SELECT reb FROM Reading_element WHERE reb = :morphene)
           THEN (SELECT CASE WHEN :morphene NOT IN
                (Select keb FROM Kanji_element WHERE keb=:morphene)
                THEN - 1
                ELSE 0
           END)
           ELSE 1
    END;
    """
    cursor.execute(sql, {'morphene': morphene})
    morphs = {-1: "not_a_word", 0: "keb", 1: "reb"}
    return morphs[cursor.fetchone()[0]]


# Get the correct keb/reb tuples
def get_reb_keb(word, morph_type, cursor):

    # cursor.execute unfortunaly doesn't work with variable table names
    if morph_type == "keb":
        sql = """
        SELECT DISTINCT Ke.ent_seq, keb, ifnull(reb, 0)
        FROM (SELECT keb, ent_seq FROM Kanji_element WHERE keb = :word) AS Ke
        LEFT JOIN Reading_element Re ON Ke.ent_seq = Re.ent_seq
        LEFT JOIN Re_restr ON Re_restr.r_ele_id = Re.r_ele_id
             AND Re_restr.restr = keb;
        """
    else:
        sql = """
        SELECT DISTINCT Re.ent_seq, ifnull(keb, 0), reb
        FROM (SELECT reb, ent_seq, r_ele_id
              FROM Reading_element WHERE reb = :word) AS Re
        LEFT JOIN Kanji_element Ke ON Ke.ent_seq = Re.ent_seq
        LEFT JOIN Re_restr ON Re_restr.r_ele_id = Re.r_ele_id
             AND Re_restr.restr = keb;
        """

    cursor.execute(sql, {"word": word})
    return cursor.fetchall()


# In case the word isn't found
def build_error():
    return {'meta': 404}


# Build an usable definition
def build_def(tuples, cursor):
    ret = {}
    ret['meta'] = 200
    readings = []
    senses = OrderedDict({'-1': {'ident': -1}})
    n_senses = 0
    i = 0
    sense_ids_list = []
    for t in tuples:
        japanese = [t[0], t[1]]
        attr_dict = {'gloss': t[3],
                     'pos': t[4],
                     'misc': t[5],
                     'xref': t[6]}

        if japanese not in readings:
            readings += [japanese]

        sense_id = t[2]
        if sense_id not in sense_ids_list:
            i += 1
            n_senses += 1
            senses[sense_id] = {'gloss': [],
                                'pos': [],
                                'misc': [],
                                'xref': []}
            sense_ids_list.append(sense_id)

        for tag in ['gloss', 'pos', 'misc', 'xref']:
            if attr_dict[tag] not in senses[sense_id][tag]:
                senses[sense_id][tag] += [attr_dict[tag]]

    del senses['-1']
    print("SENSEIDLIST")
    ret['readings'] = readings
    ret['senses'] = senses
    return ret


# Choose apropriate function to call
def build_choice(tuples, cursor):
    if tuples == {'definition': 'Word not found'}:
        return build_error()
    else:
        return build_def(tuples, cursor)


# Query returning all keb/rebe/gloss/pos/misc/nokanji/xref tuples
def select_definitions(word, morph_type, cursor):
    couple = get_reb_keb(word, morph_type, cursor)
    query_tuple = couple[0]
    kebs = []
    rebs = []
    for i in range(0, len(couple)):
        if couple[i][1] != 0:
            kebs += [couple[i][1]]
        if couple[i][2] != 0:
            rebs += [couple[i][2]]

    str_kebs = ""
    str_rebs = ""
    if len(rebs) > 0:
        str_rebs = "AND reb in ({0})".format(', '.join("'" + r + "'" for r in rebs))

    if len(kebs) > 0:
        str_kebs = "AND keb in ({0})".format(', '.join("'" + k + "'" for k in kebs))

    sql = """
    SELECT DISTINCT keb, reb, S.sense_id, gloss, pos, misc, xref
    FROM (SELECT sense_id, ent_seq FROM Sense WHERE ent_seq = :ent_seq) AS S
    LEFT JOIN Stagr Sr ON Sr.sense_id = S.sense_id
    LEFT JOIN Stagk Sk ON Sk.sense_id = S.sense_id
    LEFT JOIN Xref X ON X.sense_id = S.sense_id
    INNER JOIN Gloss G ON G.sense_id = S.sense_id
    LEFT JOIN Misc M ON M.sense_id = S.sense_id
    LEFT JOIN Pos P ON P.sense_id = S.sense_id
    LEFT JOIN Reading_element Re ON S.ent_seq = Re.ent_seq
    LEFT JOIN Kanji_element Ke ON S.ent_seq = Ke.ent_seq
    LEFT JOIN Re_restr ON Re_restr.r_ele_id = Re.r_ele_id
    WHERE CASE WHEN restr IS NOT NULL
        THEN restr = keb
        ELSE 1
    END
    AND CASE WHEN stagr IS NOT NULL
        THEN stagr = reb
        ELSE 1
    END
    """
    sql += str_kebs
    sql += str_rebs
    sql += "ORDER BY k_ele_id, Re.r_ele_id, S.sense_id, gloss, pos, misc;"

    # No user input so hopefuly no sql injection

    cursor.execute(sql, {"ent_seq": query_tuple[0]})
    dict_tuples = cursor.fetchall()
    return dict_tuples


# Returns definitions as an dictionary of the given word
def get_definition(word):
    dict_conn = sqlite3.connect("reader/databases/dict.db",
                                 check_same_thread=False)
    cursor = dict_conn.cursor()
    morph_type = morphene_type(word, cursor)
    ret = {"definition": "Word not found"}
    if morph_type != "not_a_word":
        ret = select_definitions(word, morph_type, cursor)
    return build_choice(ret, cursor)
