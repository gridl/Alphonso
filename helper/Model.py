from faker import Faker
from random import randint, sample

from Constant import TV_CHANNELS, PROGRAMS, AIR_TOTAL_HR, TODAY

import datetime
import uuid

test_data = Faker()
# test_data.seed(4321) # uncomment for test purpose


class Viewer:
    def __init__(self, vwr_name=None):
        self._id = str(uuid.uuid1())
        self.vwr_name = test_data.name() if vwr_name is None else vwr_name

    @property
    def vwr_id(self):
        return self._id


class Channel:
    def __init__(self, chn_name=None):
        self._id = str(uuid.uuid1())
        self.chn_name = (sample(TV_CHANNELS, 1)[0]
                         if chn_name is None else chn_name)

    @property
    def chn_id(self):
        return self._id


class Program:
    def __init__(self, pgm_title=None, *pgm_genres):
        self._id = str(uuid.uuid1())
        if pgm_title is None:
            pgm = sample(PROGRAMS, 1)[0]
            pgm_title = pgm[-1]
            pgm_genres = list(pgm[:-1])

        self.pgm_title = pgm_title
        self.pgm_genres = list(pgm_genres)

    @property
    def pgm_id(self):
        return self._id


class Airing:
    def __init__(self, chn_id, pgm_id, start_dt, end_dt):
        self._id = str(uuid.uuid1())
        self.chn_id = chn_id
        self.pgm_id = pgm_id
        self.start_dt = start_dt
        self.end_dt = end_dt

    @property
    def air_id(self):
        return self._id


class Viewership:
    def __init__(self, vwr_id, chn_id, view_dt=None):
        self._id = str(uuid.uuid1())
        self.vwr_id = vwr_id
        self.chn_id = chn_id
        self.view_dt = test_data.date_time_between_dates(
                        datetime_start=TODAY,
                        datetime_end=TODAY+datetime.timedelta(hours=AIR_TOTAL_HR-1))
    @property
    def vship_id(self):
        return self._id


def main():
    vwr = Viewer()
    chn = Channel()
    pgm = Program()
    air = Airing(chn.chn_id, pgm.pgm_id)
    vship = Viewership(vwr.vwr_id, chn.chn_id)
    print vwr.__dict__
    print chn.__dict__
    print pgm.__dict__
    print air.__dict__
    print vship.__dict__
    print [Viewer().__dict__ for _ in range(5)]


if __name__ == "__main__":
    main()
