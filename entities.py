from data.school_alt_names import alt_names

import pandas as pd
from dataclasses import dataclass


class Player:

    def __init__(self, name, number, position,
                 height, weight, stats):

        self.name: str = name
        self.jersey_number: str = number
        self.position: str = position
        self.height: int = height
        self.weight: int = weight
        self.stats: dict = stats

    def __repr__(self):
        return f"<Player: {self.name} (#{self.jersey_number})>"


class BasketballData():

    def __init__(self, df):
        self.df = df.set_index('Player')
        self.df.fillna(0)


class PlayerContext:

    def __init__(self, 
                 school: str, 
                 description_df: BasketballData, 
                 performance_df: BasketballData, 
                 record: pd.Series,
                 schedule: pd.DataFrame,
                 schedule_team: pd.DataFrame,
                 schedule_opp: pd.DataFrame,
                 pace: float
        ):

        _df = description_df.df
        _df['Height'] = _df['Height'].map(lambda x: height_to_inches(x))

        self.school = school
        self.description = _df
        self.performance = performance_df.df
        self.record = record
        self.schedule = schedule
        self.schedule_team = schedule_team       
        self.schedule_opp = schedule_opp
        self.pace = pace

        self.df = self.description[['#', 'Height', 'Weight']].join(
            self.performance, how='inner')
        self.df.fillna(0)

    def __repr__(self):
        return f"<School: {self.school} contains {self.num_players()} players>"

    def create_player(self, who: str) -> Player:

        d = self.description.loc[who]
        p = self.performance.loc[who]

        return Player(
            name=who,
            number=d['#'],
            position=d['Pos'],
            height=d['Height'],
            weight=d['Weight'],
            stats=p.to_dict()
        )

    def get_players(self) -> list[str]:
        return list(self.df.index)

    def num_players(self) -> int:
        return len(self.get_players())

    def create_players(self) -> list[Player]:
        return [self.create_player(p) for p in self.get_players()]

_SHARED = ['Opp_Name', 'Tm', 'Opp_Score']
_COLS = ['FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF']
_O_COLS = ['o' + col for col in _COLS]

class Team:

    def __init__(self, context):
        self.context: PlayerContext = context
        self.name: str = context.school
        self.df: pd.DataFrame = context.df
        self.players: list[Player] = context.create_players()
        self.aliases: list[str] = alt_names.get(self.name)

        self.games = int(context.record['G'])
        self.wins = int(context.record['W'])
        self.losses = int(context.record['L'])
        self.pct = float(context.record['W-L%'])
        self.srs = float(context.record['SRS'])
        self.sos = float(context.record['SOS'])
        self.pace = float(context.pace)

        self.schedule = context.schedule
        self.schedule_team = context.schedule_team       
        self.schedule_opp = context.schedule_opp
        self.causal_df = self.create_causal_df()       
        self.seed = None

        self.df.fillna(0)
        self.causal_df.fillna(0)

    def __repr__(self):
        return f"<Team: {self.name} Record: {self.wins}-{self.losses}>"

    def add_alias(self, alias):
        if type(alias) == list:
            for a in alias:
                self.aliases.append(a)

        elif type(alias) == str:
            self.aliases.append(alias)

        else:
            raise TypeError("Alias must be a string")
        

    def create_causal_df(self):
        df1 = self.schedule_team[_SHARED + _COLS]
        df2 = self.schedule_opp[_SHARED + _COLS]
        rename_map = dict(zip(_COLS, _O_COLS))
        df2 = df2.rename(columns=rename_map)
        _df = pd.merge(df1, df2, on=_SHARED, how='inner')
        _df.insert(loc=0, column='Team', value=self.name)
        return _df


def height_to_inches(height: str) -> int:
    h = height.split('-')
    return int(h[0]) * 12 + int(h[-1])
