import datetime
import json
import os

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.replace(second=0, microsecond=0).isoformat()

        return json.JSONEncoder.default(self, obj)


class IO(object):
    def __init__(self):
        pass

    @staticmethod
    def write_json(ofile, data, append=False):
        """
        Write the json data to file on disk.
        :param ofile:
            The output filename on disk to write data.
        :param data:
            The data to be written.
        :param append:
            The write mode. Default is not append, i.e a new data
            is stored with every write operation.
        :return:
            A list of the ids of the stored json data.
        """
        inserted_ids = [d['_id'] for d in data]
        with open(ofile, mode=('a' if append else 'w') ) as ojsfile:
            json.dump(data, ojsfile, indent=4, cls=JSONEncoder,
                      sort_keys=True, separators=(',', ':'))

        return inserted_ids

    @staticmethod
    def read_json(ifile):
        """
        Read the json data from disk file to memory.
        :param ifile:
            The input filename on disk to read data.
        """
        with open(ifile, mode='r') as ijsfile:
            data = json.load(ijsfile)

        return data

    @staticmethod
    def create_dir(dir_path):
        '''
        Create a directory with the given path.
        param dir_path:
            directory path.
        return:
            directory path or None id mkdir fails.
        '''
        if not os.path.exists(dir_path):
            os.mkdir(dir_path, 0o775)

        return os.path.abspath(dir_path)

    @staticmethod
    def join_dir_file(directory, file_name):
        """
        Return `file_name` path as the child of `directory`.
        """
        return os.path.abspath(os.path.join(directory, file_name))
