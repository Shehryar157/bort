import collections
import ctypes
from sound_lib.external import pybass
from sound_lib.main import bass_call, bass_call_0


class BassConfig(collections.abc.Mapping):
    config_map = {
        '3d_algorithm': pybass.BASS_CONFIG_3DALGORITHM,
        'buffer': pybass.BASS_CONFIG_BUFFER,
        'curve_vol': pybass.BASS_CONFIG_CURVE_VOL,
        'curve_pan': pybass.BASS_CONFIG_CURVE_PAN,
        'dev_buffer': pybass.BASS_CONFIG_DEV_BUFFER,
        'dev_default': pybass.BASS_CONFIG_DEV_DEFAULT,
        'float_dsp': pybass.BASS_CONFIG_FLOATDSP,
        'gvol_music': pybass.BASS_CONFIG_GVOL_MUSIC,
        'gvol_sample': pybass.BASS_CONFIG_GVOL_SAMPLE,
        'gvol_stream': pybass.BASS_CONFIG_GVOL_STREAM,
        'music_virtual': pybass.BASS_CONFIG_MUSIC_VIRTUAL,
        'net_agent': pybass.BASS_CONFIG_NET_AGENT,
        'net_buffer': pybass.BASS_CONFIG_NET_BUFFER,
        'net_passive': pybass.BASS_CONFIG_NET_PASSIVE,
        'net_playlist': pybass.BASS_CONFIG_NET_PLAYLIST,
        'net_prebuf': pybass.BASS_CONFIG_NET_PREBUF,
        'net_proxy': pybass.BASS_CONFIG_NET_PROXY,
        'net_read_timeout': pybass.BASS_CONFIG_NET_READTIMEOUT,
        'net_timeout': pybass.BASS_CONFIG_NET_TIMEOUT,
        'pause_no_play': pybass.BASS_CONFIG_PAUSE_NOPLAY,
        'rec_buffer': pybass.BASS_CONFIG_REC_BUFFER,
        'src': pybass.BASS_CONFIG_SRC,
        'src_sample': pybass.BASS_CONFIG_SRC_SAMPLE,
        'unicode': pybass.BASS_CONFIG_UNICODE,
        'update_period': pybass.BASS_CONFIG_UPDATEPERIOD,
        'update_threads': pybass.BASS_CONFIG_UPDATETHREADS,
        'verify': pybass.BASS_CONFIG_VERIFY,
        'vista_speakers': pybass.BASS_CONFIG_VISTA_SPEAKERS,
    }

    ptr_config = (pybass.BASS_CONFIG_NET_AGENT, pybass.BASS_CONFIG_NET_PROXY)

    def __getitem__(self, key):
        key = self.config_map.get(key, key)
        if key in self.ptr_config:
            return ctypes.string_at(bass_call(pybass.BASS_GetConfigPtr, key))
        return bass_call_0(pybass.BASS_GetConfig, key)

    def __setitem__(self, key, val):
        key = self.config_map.get(key, key)
        if key in self.ptr_config:
            return bass_call(pybass.BASS_SetConfigPtr, key, ctypes.create_string_buffer(val))
        return bass_call(pybass.BASS_SetConfig, key, val)

    def __iter__(self):
        for key in self.config_map.iterkeys():
            yield key

    def __len__(self):
        return len(self.config_map)
