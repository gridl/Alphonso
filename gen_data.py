from helper import Model, IO, Constant

import datetime
import json
import os
import random
import time

dir_path = IO.create_dir('data')
class DB:
    dpath = dir_path
    vwr_db_file = IO.join_dir_file(dpath, Constant.VWR_DB_FILE)
    chn_db_file = IO.join_dir_file(dpath, Constant.CHN_DB_FILE)
    pgm_db_file = IO.join_dir_file(dpath, Constant.PGM_DB_FILE)
    air_db_file = IO.join_dir_file(dpath, Constant.AIR_DB_FILE)
    vship_db_file = IO.join_dir_file(dpath, Constant.VSHIP_DB_FILE)

    def __init__(self):
        pass

    def gen_and_store_vwr_collection(self, vwr_count=1000):
        """
        Generate distinct viewers and store as json file on disk.
        :param vwr_count:
            A count of the distinct viewers to be generated. Default is 1000.
        :return:
            A list of ids for the distinct viewers generated.
        """
        return IO.write_json(DB.vwr_db_file,
                             [Model.Viewer().__dict__
                              for _ in range(vwr_count)])


    def gen_and_store_chn_collection(self):
        """
        Generate 25 distinct channels and store as json file on disk.
        :return:
            A list of ids for the distinct channels generated.
        """
        return IO.write_json(DB.chn_db_file,
                             [Model.Channel(chn_name).__dict__
                              for chn_name in Constant.TV_CHANNELS])

    def gen_and_store_pgm_collection(self):
        """
        Generate 22 distinct programs and store as json file on disk.
        :return:
            A list of ids for the distinct programs generated.
        """
        return IO.write_json(DB.pgm_db_file,
                             [Model.Program(pgm[-1], *pgm[:-1]).__dict__
                              for pgm in Constant.PROGRAMS])

    def gen_and_store_air_collection(self, chn_ids, pgm_ids):
        end_dt = Model.TODAY + datetime.timedelta(hours=30*24) # 1 Month airing
        delta = datetime.timedelta(hours=1)
        airs = []
        for chn in chn_ids:
            start_dt = Model.TODAY
            while start_dt + delta <= end_dt:
                airs.append(Model.Airing(chn,
                                         random.sample(pgm_ids, 1)[0],
                                         start_dt, start_dt+delta).__dict__)

                start_dt += delta

        return IO.write_json(DB.air_db_file, airs)

    def gen_and_store_vship_collection(self, vwr_ids, chn_ids):
        return IO.write_json(DB.vship_db_file,
                             [Model.Viewership(vwr_id,
                                               random.sample(chn_ids, 1)[0]).__dict__
                              for vwr_id in vwr_ids])


def main():
    start = time.time()
    db = DB()
    vwr_ids = db.gen_and_store_vwr_collection(1000)
    chn_ids = db.gen_and_store_chn_collection()
    pgm_ids = db.gen_and_store_pgm_collection()
    air_ids = db.gen_and_store_air_collection(chn_ids, pgm_ids)
    vship_ids = db.gen_and_store_vship_collection(vwr_ids, chn_ids)
    print ("Generated {vwr_ids} distinct viewer records, "
          "{chn_ids} distinct channel records, \n"
          "{pgm_ids} distinct program records, and "
          "{air_ids} distinct airing records, ".format(vwr_ids=len(vwr_ids),
                                                       chn_ids=len(chn_ids),
                                                       pgm_ids=len(pgm_ids),
                                                       air_ids=len(air_ids)))
    print "Time taken {time} seconds".format(time=time.time()-start)


if __name__ == "__main__":
    main()
