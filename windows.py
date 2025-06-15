from ctypes import cast, POINTER

from comtypes import CLSCTX_ALL, CoInitialize, CoUninitialize
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


def get_volume_interface():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))


def set_volume(level):  # level: 0.0 to 1.0
    volume = get_volume_interface()
    volume.SetMasterVolumeLevelScalar(level, None)


def volume_change(step=0.05):
    CoInitialize()
    try:
        volume = get_volume_interface()
        current = volume.GetMasterVolumeLevelScalar()
        if step > 0:
            volume.SetMasterVolumeLevelScalar(min(current + step, 1.0), None)
        else:
            volume.SetMasterVolumeLevelScalar(min(current + step, 0.0), None)

    finally:
        CoUninitialize()


def toggle_mute():
    volume = get_volume_interface()
    is_muted = volume.GetMute()
    volume.SetMute(not is_muted, None)
