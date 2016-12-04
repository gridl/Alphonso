from gen_data import DB
from helper import IO, Constant

import datetime
import sys


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
        if not choice:
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


class Analytics:
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

    def get_genre_with_duration(self):
        pass

    def get_genre_with_viewers(self):
        pass

    def get_channel_with_duration(self):
        pass

    def get_channel_with_viewers(self):
        pass

    def get_channel_with_duration_in_prime_time(self):
        pass

    def get_channel_with_viewers_in_prime_time(self):
        pass


def main():
    rdb = ReadDB()
    rdb.load_vwr_data(); rdb.load_chn_data()
    rdb.load_pgm_data(); rdb.load_air_data()
    rdb.load_vship_data()
    choice = 1
    while choice:
        choice, start_time, end_time = Menu.print_menu()
        proc = Analytics(start_time, end_time)
        functions = [sys.exit,
                     proc.get_genre_with_duration,
                     proc.get_genre_with_viewers,
                     proc.get_channel_with_duration,
                     proc.get_channel_with_viewers,
                     proc.get_channel_with_duration_in_prime_time,
                     proc.get_channel_with_viewers_in_prime_time]
        if not choice: functions[choice]("See ya!")
    else: functions[choice]()



if __name__ == "__main__":
    main()
