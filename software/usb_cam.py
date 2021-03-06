import reip
import time
import cv2
import numpy as np
from bundles import BundleCam
from cv_utils import ImageConvert, ImageDisplay
from gstreamer import *


class UsbCamOpenCV(BundleCam):
    # global_time = None  # Global timestamp
    pixel_format = "BGR"  # Supported pixel formats: RGB
    res = (1944, 2592)  # Supported resolutions: (1944, 2592), (1080, 1920), (720, 1280)
    fps = 15  # Supported max fps: 15, 30, 30
    dev = 0  # Camera device ID
    filename = "%d_{time}.avi"
    cam = None  # Actual camera handle

    gst_str = "v4l2src device=/dev/video%d ! image/jpeg,width=%d,height=%d,framerate=%d/1 ! jpegdec ! " + \
	          "queue max-size-buffers=1000 leaky=no ! videoconvert ! video/x-raw,format=BGR ! appsink"

    def init(self):
        assert(self.pixel_format in ["BGR"])

        self.gst_str = self.gst_str % (self.dev, self.res[1], self.res[0], self.fps)

        if self.debug:
            print("\ngst_str:\n", self.gst_str, "\n")

        self.cam = cv2.VideoCapture(self.gst_str, cv2.CAP_GSTREAMER)

        super().init()

    # Implements BundleCam.get_buffer()
    def get_buffer(self):
        ret_val, img = self.cam.read()
        t = time.time()
        img = img[:, :, ::-1]

        if not self.bundle:  # copy required by pyarrow because negative strides are not supported
            img = img.copy() # bundles make a copy by default

        if ret_val:
            return img, {"python_timestamp" : t,
                         "resolution": self.res,
                         "fps": self.fps,
                         "pixel_format" : self.pixel_format}
        else:
            return None, {}

    # Provided by BundleCam
    # def process(self, *xs, meta=None):
    #     ...

    def finish(self):
        if self.cam:
            self.cam.release()

        super().finish()


class UsbCamGStreamer(BundleCam):
    # global_time = None  # Global timestamp
    pixel_format = "I420"  # Supported pixel formats: RGB
    res = (1944, 2592)  # Supported resolutions: (1944, 2592), (1080, 1920), (720, 1280)
    fps = 15  # Supported max fps: 15, 30, 30
    rate = 5  # Decoding / appsink rate
    dev = 0  # Camera device ID
    max_duration = 3  # Max file duration, sec
    max_size = 300  # Max file size, MB
    gst_started = False  # Delay pipeline start until all blocks loaded
    rec = True  # Do record the original data stream
    gst = None  # GStreamer pipeline

    gst_str = "v4l2src device=/dev/video%d ! image/jpeg,width=%d,height=%d,framerate=%d/1 ! jpegdec ! " + \
	          "queue max-size-buffers=1000 leaky=no ! videoconvert ! video/x-raw,format=BGR ! appsink"

    def init(self):
        assert(self.pixel_format in ["I420"])
        self.tot_samples, self.tot_overrun, self.tot_filenames, self.count, self.t0 = 0, 0, 0, 0, time.time()
        self.new_filename = "Default"

        GStreamer.init()
        self.gst = GStreamer(debug=self.debug)
        g = self.gst

        self.fname = self.filename % self.dev
        if self.rec:
            reip.util.ensure_dir(self.fname)
        self.fname = self.fname[:-4] + "_%d" + self.fname[-4:]

        # if self.rec:
        g.add("v4l2src", "source").set_property("device", "/dev/video%d" % self.dev)
        g.add("capsfilter", "src_caps").set_property("caps", g.from_string("image/jpeg,width=%d,height=%d,framerate=%d/1" % (self.res[1], self.res[0], self.fps)))
        g.add("tee", "tee").set_property("name", "t")
        g.add("queue", "queue_f")
        g.add("avimux", "mux")
        # self.fname = self.filename.format(**{"time": time.time()}) % self.dev

        f = g.add("multifilesink", "filesink")
        f.set_property("location", self.fname)
        f.set_property("post-messages", True)
        f.set_property("next-file", 4)  # Use max-file-size property
        f.set_property("max-file-size", int(self.max_size * 1e+6))
        # Duration limit doesn't work for some reason
        # f.set_property("next-file", 5)  # Use max-file-duration property
        # f.set_property("max-file-duration", self.max_duration * 1e+9)
        # f.connect("filesink", self.new_file, f)

        q = g.add("queue", "queue_a")#.set_property("leaky", "downstream")
        q.set_property("max-size-buffers", 3)
        q.set_property("leaky", "downstream")
        q.connect("overrun", self.overrun, q)

        r = g.add("videorate", "rate")
        r.set_property("max-rate", self.rate)
        r.set_property("skip-to-first", True)
        r.set_property("drop-only", True)
        g.add("jpegdec", "decode")
        # g.add("videoconvert", "convert")
        # g.add("capsfilter", "sink_caps").set_property("caps", g.from_string("video/x-raw,format=RGB"))
        
        s = g.add("appsink", "sink")#.set_property("emit-signals", True)

        s.set_property("emit-signals", True)  # eos is not processed otherwise
        s.set_property("max-buffers", 2)  # protection from memory overflow
        s.set_property("drop", False)  # if python is too slow with pulling the samples (or let queue do that)
        s.connect("new-sample", self.new_sample, s)
        # g.sink.connect("new-sample", just_pull, g.sink)
        # g.sink.connect("new-sample", pull_copy, g.sink)

        g.link(["source", "src_caps", "tee"])
        if self.rec:
            g.link(["tee", "queue_f", "mux", "filesink"])
        g.link(["tee", "queue_a", "rate", "decode", "sink"])
        #else:
        #    g.add("v4l2src", "src").set_property("device", "/dev/video%d" % self.dev)
        #    g.add("capsfilter", "caps").set_property("caps", g.from_string("image/jpeg,width=%d,height=%d,framerate=%d/1" % (self.res[1], self.res[0], self.fps)))
        #    q = g.add("queue", "q")
        #    g.add("jpegdec", "decode")
        #    s = g.add("appsink", "sink")

        #    # g.src.set_property("num-buffers", 150)
        #    # print("\n\tname", g.src.get_property("device-name"))

        #    q.set_property("max-size-buffers", 3)
        #    q.set_property("leaky", "no")
        #    q.connect("overrun", self.overrun, q)

        #    s.set_property("emit-signals", True)  # eos is not processed otherwise
        #    s.set_property("max-buffers", 1)  # protection from memory overflow
        #    s.set_property("drop", False)  # if python is too slow with pulling the samples
        #    s.connect("new-sample", self.new_sample, s)

        #    g.link()
        # self.gst_str = self.gst_str % (self.dev, self.res[1], self.res[0], self.fps)

        # if self.debug:
        #     print("\ngst_str:\n", self.gst_str, "\n")

        # self.cam = cv2.VideoCapture(self.gst_str, cv2.CAP_GSTREAMER)

        super().init()

        # self.gst.start()

    def new_file(self, sink, data):
        # global tot_samples, t0
        # sink.emit("try-pull-sample", 1e+6)
        self.tot_filenames += 1
        self.new_filename = "?"

        if self.debug and self.verbose:
            print("Filename_%d:" % self.dev, self.tot_filenames, self.new_filename, time.time() - self.t0)

        return Gst.FlowReturn.OK

    def new_sample(self, sink, data):
        # global tot_samples, t0
        # sink.emit("try-pull-sample", 1e+6)
        self.tot_samples += 1

        if self.debug and self.verbose:
            print("Sample_%d:" % self.dev, self.tot_samples, time.time() - self.t0)

        return Gst.FlowReturn.OK

    def overrun(self, queue, data):
        # global tot_overrun, t0
        self.tot_overrun += 1

        if self.debug:
            print("\nOverrun_%d:" % self.dev, self.tot_overrun, time.time() - self.t0)

        return Gst.FlowReturn.OK

    # Implements BundleCam.get_buffer()
    def get_buffer(self):
        if not self.gst_started:
            self.gst.start()
            self.gst_started = True

        # sample = self.gst.sink.try_pull_sample(1e+6)
        # sample = self.gst.sink.try_pull_sample(1e+9 / self.fps)
        sample = None
        while not sample:
            sample = self.gst.sink.try_pull_sample(1e+9 / self.fps / 10)
        t = time.time()
        gt = None

        if sample:
            self.count += 1
            img, gt, fmt = GStreamer.unpack_sample(sample, debug=self.verbose)

            if self.debug and self.verbose:
                print("Pulled_%d:" % self.dev, self.count, gt / 1.e+9, "at", time.time() - self.t0)

            w, h, ch, fmt = fmt
            assert(fmt == "I420")
            # img = img[: img.shape[0] * 2 // 3].reshape((h, w))
        else:
            img = None

        # ret_val, img = self.cam.read()
        
        # img = img[:, :, ::-1]

        # if not self.bundle:  # copy required by pyarrow because negative strides are not supported
        #     img = img.copy() # bundles make a copy by default

        if img is not None:
            return img, {"python_timestamp" : t,
                         "gstreamer_timestamp" : gt / 1.e+9,
                         "resolution": self.res,
                         "file_template": self.fname,
                         "file_index": self.gst.multifilesink_index,
                         "fps": self.fps,
                         "pixel_format" : self.pixel_format}
        else:
            return None, {}

    # Provided by BundleCam
    # def process(self, *xs, meta=None):
    #     ...

    def finish(self):
        if self.gst and self.gst_started:
            self.gst.stop(timeout=3)

        if self.debug or True:
            print("\nCamera_%d:\n\tPulled - %d, Lost - %d" % (self.dev, self.tot_samples, self.tot_overrun))

        super().finish()


if __name__ == '__main__':
    from dummies import BlackHole

    # c = BuiltinCamOpenCV(name="BuiltinCam", bundle=None, zero_copy=True, debug=True, verbose=True)
    # c.to(BlackHole(name="Black_Hole", debug=False))

    # reip.default_graph().run(duration=5)

    # c = UsbCamOpenCV(name="UsbCam", bundle=None, zero_copy=True, debug=True, verbose=False)
    c = UsbCamGStreamer(name="UsbCam", bundle=None, zero_copy=True, debug=True, verbose=False)
    c.to(BlackHole(name="Black_Hole", debug=False))
    # d = ImageDisplay(name="Display", make_bgr=False)
    # c.to(d, strategy="latest").to(BlackHole(name="Black_Hole", debug=False))

    reip.default_graph().run(duration=15)
