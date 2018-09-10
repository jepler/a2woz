from passport.wozimage import DiskImage, Track, WozError, raise_if
from passport import a2rchery
import bitarray
import collections

class A2RImage:
    def __init__(self, filename=None, stream=None):
        self.filename = filename
        self.tracks = collections.OrderedDict()
        self.a2r_image = a2rchery.A2RReader(filename, stream)

    def to_bits(self, flux_record):
        """|flux_record| is a dictionary of 'capture_type', 'data_length', 'tick_count', and 'data'"""
        if not flux_record or flux_record["capture_type"] != a2rchery.kCaptureTiming:
            return [], 0
        bits = bitarray.bitarray()
        track_length = 0
        ticks = 0
        flux_total = 0
        fluxxen = flux_record["data"]
        speeds = [(len([1 for i in fluxxen if i%t==0]), t) for t in range(0x1e,0x23)]
        speeds.sort()
        speed = speeds[-1][1]
        for flux_value in fluxxen:
            ticks += flux_value
            if not track_length and ticks > flux_record["tick_count"]:
                track_length = len(bits)
            flux_total += flux_value
            if flux_value == 0xFF:
                continue
            bits.extend([0] * ((flux_total - speed//2) // speed))
            bits.append(1)
            flux_total = 0
        return bits, track_length

    def seek(self, track_num):
        if type(track_num) != float:
            track_num = float(track_num)
        if track_num < 0.0 or \
           track_num > 35.0 or \
           track_num.as_integer_ratio()[1] not in (1,2,4):
            raise WozError("Invalid track %s" % track_num)
        location = int(track_num * 4)
        if not self.tracks.get(location):
            bits, track_length = self.to_bits(self.a2r_image.flux.get(location, [{}])[0])
            self.tracks[location] = Track(bits, len(bits))
        return self.tracks[location]
