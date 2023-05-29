from .exceptions import ImpossibleTitlesError, InvalidYearCupError, NegativeTitlesError
from datetime import datetime


def data_processing(cup_squad_infos):
    titles = cup_squad_infos["titles"]

    if titles < 0:
        raise NegativeTitlesError("titles cannot be negative")

    first_cup_string = cup_squad_infos["first_cup"]
    first_cup_date = datetime.strptime(first_cup_string, "%Y-%m-%d")

    first_cup_year = int(first_cup_date.strftime("%Y"))

    last_cup_year = 2022
    cup_participations = ((last_cup_year - first_cup_year) / 4) + 1

    if first_cup_year < 1930 or (first_cup_year - 1930) % 4 != 0:
        raise InvalidYearCupError("there was no world cup this year")

    if titles > cup_participations:
        raise ImpossibleTitlesError("impossible to have more titles than disputed cups")
