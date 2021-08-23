import json
import pickle
import difflib
import pandas as pd
from numpy import mean
import unidecode
from collections import OrderedDict

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

import busquedadesaparecidos.utils.constantes as cfg
from typing import Union


class TargetWords(object):
    entity = ['state', 'prosecuted', 'organization', 'municipios']

    def __init__(self, text: str = None, entity: str = 'state'):

        self.text = text
        self.entity = entity
        self.sentence: Union[list, None] = None
        self.target_list: Union[dict, None] = None
        self.results: Union[dict, None] = None

        if text:
            self.main()

    def filtered_sentence(self):
        self.sentence = filter_sentence(self.text)

    def select_target_list(self):
        if self.entity == 'state':
            self.target_list = read_pickle(cfg.path_states_processed)

        elif self.entity == 'prosecuted':
            self.target_list = read_pickle(cfg.path_prosecuted_processed)

        elif self.entity == 'organization':
            self.target_list = read_pickle(cfg.path_organizations_processed)

        elif self.entity == 'municipios':
            self.target_list = read_pickle(cfg.path_municipios_list_processed)

    def get_matchs(self):

        if self.entity == 'state' or self.entity == 'municipios':
            self.results = get_matches_by_document(self.target_list,
                                                   self.sentence)

        else:
            self.results = search_target_by_document(self.target_list,
                                                     self.sentence)

    def main(self):
        self.filtered_sentence()
        self.select_target_list()
        self.get_matchs()


def to_pickle(obj: object, path: str):
    with open(path, 'wb') as fp:
        pickle.dump(obj, fp, protocol=pickle.HIGHEST_PROTOCOL)


def read_pickle(path: str):
    with open(path, 'rb') as fp:
        obj = pickle.load(fp)

    return obj


def to_json(obj: object, path: str) -> None:
    with open(path, "w") as outfile:
        json.dump(obj, outfile)


def read_json(path: str) -> any:
    """"""
    f = open(path)
    data = json.load(f)
    f.close()

    return data


def read_states() -> pd.DataFrame:
    """"""
    return pd.read_csv(cfg.path_states, encoding='latin1')


def read_transcripts() -> pd.DataFrame:
    """"""
    df = pd.read_csv(cfg.path_transcripts,
                     error_bad_lines=False)
    df = df.loc[df['MetodoTexto'] == 'automatico']
    df.reset_index(drop=True, inplace=True)

    return df


def read_organizations() -> pd.DataFrame:
    """"""
    df = pd.read_csv(cfg.path_organizations,
                     error_bad_lines=False)
    df.reset_index(drop=True, inplace=True)

    return df


def read_prosecuted() -> pd.DataFrame:
    """"""

    df = pd.read_csv(cfg.path_prosecuted,
                     error_bad_lines=False)
    df.reset_index(drop=True, inplace=True)

    return df


def read_municipios():
    """"""
    df = pd.read_csv(cfg.path_municipios,
                     error_bad_lines=False)
    df.reset_index(drop=True, inplace=True)

    return df


def remove_duplicated_letters(word: str):
    """"""
    new_word = ''
    last = ''

    for letter in word:
        if letter == last and letter != 'r':
            continue

        new_word += letter

        last = letter

    return new_word


def filter_sentence(text: str,
                    len_threshold: int = 2,
                    camel_case: bool = False) -> list:
    stop_words = set(stopwords.words('spanish'))
    word_tokens = word_tokenize(unidecode.unidecode(text))
    filtered_sentence = [word for word in word_tokens if not word in
                                                             stop_words]
    cleaned_letters = [remove_duplicated_letters(word) for word
                       in filtered_sentence]

    filtered_by_length = [word for word in cleaned_letters if
                          len(word) > len_threshold]

    camel_case_words = [word.title() if word.isupper() else word
                        for word in filtered_by_length]

    if camel_case:
        camel_case_words = [word.title() for word in camel_case_words]

    return camel_case_words


def closest_word(word: str,
                 correct_list: list) -> Union[str, None]:
    result = difflib.get_close_matches(word, correct_list)

    if result:
        return result[0]


def similarity_score(word: str, best_match: str) -> float:
    return round(difflib.SequenceMatcher(None, word, best_match)
                 .ratio(), 2)


def get_matches_by_document(target_words_list: list,
                            filtered_sentence: str,
                            threshold: float = 0.8) -> Union[dict, None]:
    results_dict = OrderedDict()
    for word in target_words_list:
        best_match = closest_word(word, filtered_sentence)

        if best_match:
            score = similarity_score(word, best_match)

            if score > threshold:
                results_dict[word] = (best_match, score)

    if results_dict:
        return results_dict


def evalute_length_sentence(matches_dict: dict,
                            target_sentence: list):
    matches_len = len(matches_dict)
    target_len = len(target_sentence)

    score = round(matches_len / target_len, 2)

    return score


def evaluate_similarity(matches_dict: dict):
    """"""

    mean_score = mean([matches_dict[key][1] for key in matches_dict])

    return round(mean_score, 2)


def evaluate_total_match(matches_dict: dict,
                         target_sentence: list) -> float:
    score_length = evalute_length_sentence(matches_dict, target_sentence)
    score_similiarity = evaluate_similarity(matches_dict)

    return round(score_length * score_similiarity, 2)


def search_target_by_document(target_dict: dict,
                              filtered_sentence: str):
    total_results = []

    for key in list(target_dict.keys()):
        target_words_list = target_dict[key]
        results_dict = get_matches_by_document(target_words_list, filtered_sentence)
        if results_dict:
            score = evaluate_total_match(results_dict, target_words_list)
            if score > 0.8:
                total_results.append((score, key, target_words_list))

    if total_results:
        return sorted(total_results, reverse=True)

