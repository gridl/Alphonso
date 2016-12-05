from collections import Counter, defaultdict
from gen_data import DB
from helper import IO, Constant

import datetime
import sys

def sdt_to_date(dt): return datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")

class Menu:
    def __init__(self):
        pass

    @staticmethod
    def print_menu():
        print "-"*48
        print "---INSIGHTS---"
        print "1. Most popular Genre (duration wise) for the specified time."
        print "2. Most popular Genre (viewers count wise) for the specified time."
        print "3. Most popular Channel (duration wise) for the specified time."
        print "4. Most popular Channel (viewers count wise) for the specified time."
        print "5. Most popular Channel (duration wise) during prime time(5am-10am, 1pm-3pm, 7pm-10pm)."
        print "6. Most popular Channel (viewers count wise) during prime time(5am-10am, 1pm-3pm, 7pm-10pm)."
        print "0. Exit"
        choice = int(raw_input("Enter the option number for the corresponding insights.\t"))
        if choice in [0, 5, 6]:
            return choice, None, None
        print "-"*48
        print "---TIME---"
        try:
            start_time = datetime.datetime.strptime(raw_input("Enter the start time:\t"), "%Y-%m-%dT%H:%M:%S")
            end_time = datetime.datetime.strptime(raw_input("Enter the end time:\t"), "%Y-%m-%dT%H:%M:%S")
        except ValueError as er:
            print "Invalid datetime format. Please enter ISO8601 format"
            print "Error: ", er

        return choice, start_time, end_time


class ReadDB:
    def __init__(self):
        pass

    def load_vwr_data(self):
        self.vwr_data = IO.read_json(DB.vwr_db_file)

    def load_chn_data(self):
        self.chn_data = IO.read_json(DB.chn_db_file)

    def load_pgm_data(self):
        self.pgm_data = IO.read_json(DB.pgm_db_file)

    def load_air_data(self):
        self.air_data = IO.read_json(DB.air_db_file)

    def load_vship_data(self):
        self.vship_data = IO.read_json(DB.vship_db_file)

chn_id_name = {}
pgm_id_genre_title = {}
def get_chn_id_name(chn_data):
    for chn in chn_data:
        chn_id_name[chn['_id']] = chn['chn_name']

def get_pgm_id_genre_title(pgm_data):
    for pgm in pgm_data:
        pgm_id_genre_title[pgm['_id']] = (pgm['pgm_genres'], pgm['pgm_title'])

class Analytics(ReadDB):


    def __init__(self, start_time=None, end_time=None):
        self.start_time = start_time
        self.end_time = end_time

    def _search_dt(self, start, end, dt_search, prime_search=False):
        """
        Search for a given datetime in viewership data and return its index.
        O(logN)
        """

        while start <= end:
            mid = (start + end)/2
            if prime_search is False:
                if sdt_to_date(self.vship_data[mid]['view_dt']) == dt_search:
                    return mid
                if sdt_to_date(self.vship_data[mid]['view_dt']) > dt_search:
                    end = mid-1
                else:
                    start = mid+1
            else:
                if sdt_to_date(self.vship_data[mid]['view_dt']).time() == dt_search:
                    return mid
                if sdt_to_date(self.vship_data[mid]['view_dt']).time() > dt_search:
                    end = mid-1
                else:
                    start = mid+1

        return end


    def _get_vship_with_duration(self, prime_search=False):
        """
        Filter the viewership data in a specified datetime range.
        :return:
            vwr_count: Total viewer count for specified duration.
            chn_data: The viewer count per channel.
            chn_prog_map: Map of channel_id -> (program_id, duration)
        """
        end_index = self._search_dt(0, len(self.vship_data), self.end_time, prime_search)
        start_index = self._search_dt(0, len(self.vship_data), self.start_time, prime_search)

        req_vship_data = self.vship_data[start_index: end_index+1]
        chn_list = []
        vwr_count = end_index - start_index + 1
        chn_prog_map = defaultdict(list)

        for vship in req_vship_data:
            chn_id = vship['chn_id']; chn_list.append(chn_id)
        chn_data = Counter(chn_list)

        # Map channel_id -> (pgm_id, duration) for airings during specified time
        for air in self.air_data:
            if prime_search:
                if (sdt_to_date(air['start_dt']).time() >= self.start_time and
                    sdt_to_date(air['end_dt']).time() <= self.end_time):
                    duration = sdt_to_date(air['end_dt']) - sdt_to_date(air['start_dt'])
                    chn_prog_map[air['chn_id']].append((air['pgm_id'], duration))
            else:
                if (sdt_to_date(air['start_dt']) >= self.start_time and
                    sdt_to_date(air['end_dt']) <= self.end_time):
                    duration = sdt_to_date(air['end_dt']) - sdt_to_date(air['start_dt'])
                    chn_prog_map[air['chn_id']].append((air['pgm_id'], duration))


        return vwr_count, chn_data, chn_prog_map


    def get_genre_with_duration(self):
        _, _, chn_prog_map = self._get_vship_with_duration()

        genre_map = defaultdict(list)
        for chn in chn_prog_map:
            for prog_data in chn_prog_map[chn]:
                for genre in pgm_id_genre_title[prog_data[0]][0]:
                    genre_map[genre].append(prog_data[-1])

        print {genre: reduce(lambda x,y: x+y, genre_map[genre]) for genre in genre_map}



    def get_genre_with_viewers(self):
        _, chn_data, chn_prog_map = self._get_vship_with_duration()
        genre_list = []
        for chn in chn_prog_map:
            for prog_data in chn_prog_map[chn]:
                for genre in pgm_id_genre_title[prog_data[0]][0]:
                    genre_list.append(genre)

        print Counter(genre_list)


    def get_channel_with_duration(self, prime_search=False):
        """
        Return map of chn_id -> total duration.
        """
        _, _, chn_prog_map = self._get_vship_with_duration(prime_search)

        print {
                 chn_id_name[chn]: reduce(lambda x, y: x+y, [ prog_data[-1]
                                          for prog_data in chn_prog_map[chn] ])
                 for chn in chn_prog_map
               }

    def get_channel_with_viewers(self, prime_search=False):
        """
        Return map of chn_id -> viewer count
        """
        _, chn_data, _ = self._get_vship_with_duration(prime_search)

        for chn_id in chn_data:
            print chn_id_name[chn_id], chn_data[chn_id]


    def get_channel_with_duration_in_prime_time(self):
        print "---PRIME TIME (5am - 10am)---"
        self.start_time = datetime.time(hour=5)
        self.end_time = datetime.time(hour=10)
        self.get_channel_with_duration(True)

        print "---PRIME TIME (1pm - 3pm)---"
        self.start_time = datetime.time(hour=13)
        self.end_time = datetime.time(hour=15)
        self.get_channel_with_duration(True)

        print "---PRIME TIME (7pm - 10pm)---"
        self.start_time = datetime.time(hour=19)
        self.end_time = datetime.time(hour=22)
        self.get_channel_with_duration(True)


    def get_channel_with_viewers_in_prime_time(self):
        print "---PRIME TIME (5am - 10am)---"
        self.start_time = datetime.time(hour=5)
        self.end_time = datetime.time(hour=10)
        self.get_channel_with_viewers(True)

        print "---PRIME TIME (1pm - 3pm)---"
        self.start_time = datetime.time(hour=13)
        self.end_time = datetime.time(hour=15)
        self.get_channel_with_viewers(True)

        print "---PRIME TIME (7pm - 10pm)---"
        self.start_time = datetime.time(hour=19)
        self.end_time = datetime.time(hour=22)
        self.get_channel_with_viewers(True)


def main():
    proc = Analytics()
    proc.load_vwr_data()
    proc.load_chn_data()
    proc.load_pgm_data()
    proc.load_air_data()
    proc.load_vship_data()
    proc.vship_data = sorted(proc.vship_data, key=lambda d: sdt_to_date(d['view_dt']))
    get_chn_id_name(proc.chn_data)
    get_pgm_id_genre_title(proc.pgm_data)
    funct = [sys.exit,
             proc.get_genre_with_duration,
             proc.get_genre_with_viewers,
             proc.get_channel_with_duration,
             proc.get_channel_with_viewers,
             proc.get_channel_with_duration_in_prime_time,
             proc.get_channel_with_viewers_in_prime_time]

    choice = 1

    while choice:
        choice, start_time, end_time = Menu.print_menu()
        if choice > 6:
            print "Invalid Choice"; continue;
        if not choice:
            funct[choice]("See ya!")
        else:
            proc.start_time, proc.end_time = start_time, end_time
            funct[choice]()




if __name__ == "__main__":
    main()
