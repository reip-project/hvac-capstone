import json
import glob
import csv
import time
import os.path
from math import floor

June_1st = 1654056001
One_day = 24*3600

read_from = "/home/vidaviz/hvac_tmp/sensor_6/det/"
save_to = "/home/vidaviz/hvac_tmp/sensor_6_clean/det/"
cam_names = ["left", "right"]  # TODO: Fix later!

def start_file(day_number):
    fname = save_to + 'June_%d.csv' % day_number
    print("New file:", fname)

    csv_wr = csv.writer(open(fname, "w"))
    csv_wr.writerow(["Timestamp", "Camera", "Label", "Confidence", "Top", "Left", "Bottom", "Right"])
    return  csv_wr, day_number

def better_name(name):
    path = os.path.dirname(name)
    basename = os.path.basename(name)
    pos = basename.rfind("_")
    id = int(basename[pos+1:-5])
    new_name = path + "/" + basename[:pos] + "_%06d.json" % id
    # print(name, new_name)
    return new_name

if __name__ == "__main__":
    # print(time.time())
    # exit(0)
    all_files = sorted(glob.glob(read_from + "*.json"))
    print(len(all_files), "files found")

    better_names = [better_name(f) for f in all_files]
    idx = sorted(range(len(better_names)), key=better_names.__getitem__)
    # exit()

    # for i, f in enumerate(better_names[:100]):
    #     print(i, f)

    csv_wr = None
    current_day = 0

    for f_id in idx:
        fname = all_files[f_id]
        data = json.load(open(fname))
        print("Loaded %d:" % f_id, fname)

        for i in range(10):
            det = data["buffer_%d" % i]

            if len(det["objects"]) > 0:
                objs = det["objects"]
                for j in range(len(objs)):
                    obj = objs[j]

                    label, conf = obj["Label"], obj["Confidence"]
                    box = obj["Top"], obj["Left"], obj["Bottom"], obj["Right"]
                    tmp = det["source_meta"]["python_timestamp"]
                    cam = cam_names[det['source_sel']]

                    obj_day = floor(1 + (float(tmp) - June_1st) / One_day)

                    # if label == "Person" and conf > 0.2:
                    if label == "person" and conf > 0.1:
                        # print(f_id, i, j, label, conf)
                        if csv_wr is None or obj_day != current_day:
                            csv_wr, current_day = start_file(obj_day)
                        csv_wr.writerow((tmp, cam, label, conf, *box))
