
import pickle
import openpyxl as xl

from entities import *
from constants import TEAMS_DATA

with open(TEAMS_DATA, 'rb') as f:
    teams = pickle.load(f)

wb = xl.load_workbook('resources/blank_bracket.xlsx', data_only=True)
sheet = wb['Teams']

east = {
    1 : sheet['C2'].value,
    16: sheet['C3'].value,
    8 : sheet['C4'].value,
    9 : sheet['C5'].value,
    5 : sheet['C6'].value,
    12: sheet['C7'].value,
    4 : sheet['C8'].value,
    13: sheet['C9'].value,
    6 : sheet['C10'].value,
    11: sheet['C11'].value,
    3 : sheet['C12'].value,
    14: sheet['C13'].value,
    7 : sheet['C14'].value,
    10: sheet['C15'].value,
    2 : sheet['C16'].value,
    15: sheet['C17'].value,
}

midwest = {
    1 : sheet['C18'].value,
    16: sheet['C19'].value,
    8 : sheet['C20'].value,
    9 : sheet['C21'].value,
    5 : sheet['C22'].value,
    12: sheet['C23'].value,
    4 : sheet['C24'].value,
    13: sheet['C25'].value,
    6 : sheet['C26'].value,
    11: sheet['C27'].value,
    3 : sheet['C28'].value,
    14: sheet['C29'].value,
    7 : sheet['C30'].value,
    10: sheet['C31'].value,
    2 : sheet['C32'].value,
    15: sheet['C33'].value,
}

south = {
    1 : sheet['C34'].value,
    16: sheet['C35'].value,
    8 : sheet['C36'].value,
    9 : sheet['C37'].value,
    5 : sheet['C38'].value,
    12: sheet['C39'].value,
    4 : sheet['C40'].value,
    13: sheet['C41'].value,
    6 : sheet['C42'].value,
    11: sheet['C43'].value,
    3 : sheet['C44'].value,
    14: sheet['C45'].value,
    7 : sheet['C46'].value,
    10: sheet['C47'].value,
    2 : sheet['C48'].value,
    15: sheet['C49'].value,
}

west = {
    1 : sheet['C50'].value,
    16: sheet['C51'].value,
    8 : sheet['C52'].value,
    9 : sheet['C53'].value,
    5 : sheet['C54'].value,
    12: sheet['C55'].value,
    4 : sheet['C56'].value,
    13: sheet['C57'].value,
    6 : sheet['C58'].value,
    11: sheet['C59'].value,
    3 : sheet['C60'].value,
    14: sheet['C61'].value,
    7 : sheet['C62'].value,
    10: sheet['C63'].value,
    2 : sheet['C64'].value,
    15: sheet['C65'].value,
}

first_round_order = [
    (1, 16),
    (8, 9),
    (5, 12),
    (4, 13),
    (6, 11),
    (3, 14),
    (7, 10),
    (2, 15)
]