import time
import reip
import reip.blocks as B
from sensor import SHTC3
from usb_cam import UsbCamGStreamer
from ai import ObjectDetector
from bundles import Bundle
from numpy_io import NumpyWriter
from dummies import BlackHole


DATA_DIR = './data'
MODEL_DIR = '/home/reip/software/reip-pipelines/smart-filter/models'


def sensor_only():
    timestamp = str(time.time())
    # Capture data in an independent process
    # using Task context to prevent data loss
    with reip.Task("Sensor"):
        sensor = SHTC3(name="SHTC3", max_rate=1)

    B.output.Csv(DATA_DIR + "/env/{time}.csv", name="CSV_Writer", headers=["time", "temp", "hum"], max_rows=10)(sensor)


def camera_only(stereo=False, detect=False):
    rate, timestamp = 4, str(time.time())

    with reip.Task("Cam_Task_0"):
        cam_0 = UsbCamGStreamer(name="Cam_0", filename=DATA_DIR + "/video/%d_"+timestamp+".avi", dev=0,
                              bundle=None, rec=True, rate=rate, debug=True, verbose=False)
    if stereo:
        with reip.Task("Cam_Task_1"):
            cam_1 = UsbCamGStreamer(name="Cam_1", filename=DATA_DIR + "/video/%d_"+timestamp+".avi", dev=1,
                                  bundle=None, rec=True, rate=rate, debug=True, verbose=False)

    if detect:
        with reip.Task("Detector_Task"):
            det = ObjectDetector(name="Detector", n_inputs=2 if stereo else 1, labels_dir=MODEL_DIR, max_rate=None, thr=0.1,
                                draw=False, cuda_out=False, zero_copy=False, debug=True, verbose=False)
            det.model = "ssd-mobilenet-v2"

            cam_0.to(det, throughput='large', strategy="latest", index=0)
            if stereo:
                cam_1.to(det, throughput='large', strategy="latest", index=1)

            det_gr = Bundle(name="Detection_Bundle", size=10, meta_only=True)
            det_wr = NumpyWriter(name="Detection_Writer", filename_template=DATA_DIR + "/det/"+timestamp+"_%d")
            det.to(det_gr).to(det_wr).to(BlackHole(name="Black_Hole_Detector"))


def all(stereo=True):
    rate, timestamp = 4, str(time.time())

    # Capture data in an independent process
    # using Task context to prevent data loss
    with reip.Task("Sensor"):
        sensor = SHTC3(name="SHTC3", max_rate=1)

        B.output.Csv(DATA_DIR + "/env/{time}.csv", name="CSV_Writer", headers=["time", "temp", "hum"], max_rows=10)(sensor)

    with reip.Task("Cam_Task_0"):
        cam_0 = UsbCamGStreamer(name="Cam_0", filename=DATA_DIR + "/video/%d_"+timestamp+".avi", dev=0,
                              bundle=None, rec=False, rate=rate, debug=False, verbose=False)

    if stereo:
        with reip.Task("Cam_Task_1"):
            cam_1 = UsbCamGStreamer(name="Cam_1", filename=DATA_DIR + "/video/%d_"+timestamp+".avi", dev=1,
                                  bundle=None, rec=False, rate=rate, debug=False, verbose=False)

    with reip.Task("Detector_Task"):
        det = ObjectDetector(name="Detector", n_inputs=2 if stereo else 1, labels_dir=MODEL_DIR, max_rate=None, thr=0.1,
                            draw=False, cuda_out=False, zero_copy=False, debug=True, verbose=False)
        det.model = "ssd-mobilenet-v2"

        cam_0.to(det, throughput='large', strategy="latest", index=0)
        if stereo:
            cam_1.to(det, throughput='large', strategy="latest", index=1)

        det_gr = Bundle(name="Detection_Bundle", size=10, meta_only=True)
        det_wr = NumpyWriter(name="Detection_Writer", filename_template=DATA_DIR + "/det/"+timestamp+"_%d")
        det.to(det_gr).to(det_wr).to(BlackHole(name="Black_Hole_Detector"))


if __name__ == "__main__":
    import fire
    fire.Fire()

    reip.default_graph().run(duration=60, stats_interval=2)

