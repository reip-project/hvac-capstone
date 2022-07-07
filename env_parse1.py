import glob
import csv
import time
import os.path
from math import floor


June_1st = 1654056001
One_day = 24*3600

read_from = "/home/vidaviz/hvac_tmp/sensor_5/env/"
save_to = "/home/vidaviz/hvac_tmp/sensor_5_clean/env/"


def start_file(day_number):
    fname = save_to + 'June_%d.csv' % day_number
    print("New file:", fname)
    csv_wr = csv.writer(open(fname, "w"))
    csv_wr.writerow(["Timestamp", "Temp", "Hum"])
    return csv_wr, day_number

if __name__ == "__main__":
    # print(time.time())
    # exit(0)
    all_files = sorted(glob.glob(read_from + "*.csv"))
    print(len(all_files), "files found")

   # better_names = [better_name(f) for f in all_files]
    #idx = sorted(range(len(better_names)), key=better_names.__getitem__)
    # exit()

    # for i, f in enumerate(better_names[:100]):
    #     print(i, f)

    csv_wr = None
    current_day = 0

    for f_id in range(len(all_files)):
        fname = all_files[f_id]
        reader = csv.reader(open(fname))
        i = 0
        print("Loaded %d:" % f_id, fname)
        for row in reader:
            # print(row)
            if i == 0:
                i = 1
                continue
            tmp = float(row[0])
            obj_day = floor(1 + (tmp - June_1st) / One_day)
            if csv_wr is None or obj_day != current_day:
                csv_wr, current_day = start_file(obj_day)
            csv_wr.writerow([tmp, row[1], row[2]])