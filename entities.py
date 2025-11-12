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


class PlayerContext:

    def __init__(self, school: str, description_df: BasketballData, performance_df: BasketballData, record: pd.Series):

        _df = description_df.df
        _df['Height'] = _df['Height'].map(lambda x: height_to_inches(x))

        self.school = school
        self.description = _df
        self.performance = performance_df.df
        self.record = record
        self.df = self.description[['#', 'Height', 'Weight']].join(
            self.performance, how='inner')

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


class Team:

    def __init__(self, context):
        self.context: PlayerContext = context
        self.name: str = context.school
        self.df: pd.DataFrame = context.df
        self.players: list[Player] = context.create_players()
        self.aliases: list[str] = []

        self.games = int(context.record['G'])
        self.wins = int(context.record['W'])
        self.losses = int(context.record['L'])
        self.pct = float(context.record['W-L%'])
        self.srs = float(context.record['SRS'])
        self.sos = float(context.record['SOS'])

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


def height_to_inches(height: str) -> int:
    h = height.split('-')
    return int(h[0]) * 12 + int(h[-1])
