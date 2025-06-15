from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

def get_volume_interface():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))

def set_volume(level):  # level: 0.0 to 1.0
    volume = get_volume_interface()
    volume.SetMasterVolumeLevelScalar(level, None)

def volume_change(step=0.05):
    volume = get_volume_interface()
    current = volume.GetMasterVolumeLevelScalar()
    volume.SetMasterVolumeLevelScalar(min(current + step, 1.0), None)

def toggle_mute():
    volume = get_volume_interface()
    is_muted = volume.GetMute()
    volume.SetMute(not is_muted, None)

