import bgtsound
from speech import speak
from os import getcwd
from os.path import join
from random import uniform
class soundsystem:
    _instance = None
    # this is a singleton, meaning it will only create 1 instance and if you try to create another it'll return the first instance.
    @staticmethod
    def get_instance():
        if soundsystem._instance is None:
            soundsystem()
        return soundsystem._instance
    def __init__(self):
        self.unmanaged_sounds = []
        if soundsystem._instance is not None:
            self = soundsystem._instance
        else:
            soundsystem._instance = self
        self.active_sounds=[]
        self.music=None
        self.ambience = None

    def play(self, file, pitch = None, pan = None, volume = None, tag = None, blocking = False, looping = False, log=True, source_object=None):
        sound=bgtsound.sound()
        file=f'{getcwd()}/sounds/{file}'
        sound.stream(file)
        if log and not blocking and source_object is not None:
            self.active_sounds.append((sound, source_object))
        if pitch:
            sound.pitch=pitch
        if source_object is None:
            if volume is not None:
                sound.volume = volume
            if pan is not None:
                sound.pan = pan
            self.unmanaged_sounds.append(sound)
        if blocking:
            sound.play_wait()
        else:
            if not looping:
                sound.play()
            else:
                sound.play_looped()
        return sound

    def set_music(self, musicfile, volume = 50):
        if not self.music is None:
            self.music.stop()
        self.music = self.play(musicfile, looping=True, volume = volume)

    def set_ambience(self, amb):
        if not self.ambience is None:
            self.ambience.stop()
        self.ambience = self.play(amb, volume=-15, looping=True)

    def stop_sounds(self):
        for sound_obj, _ in self.active_sounds:
            sound_obj.stop()
            sound_obj.close()
        self.active_sounds.clear()
        for sound_obj, _ in self.unmanaged_sounds:
            sound_obj.stop()
            sound_obj.close()
        self.unmanaged_sounds.clear()

    def stop_music(self):
        if  self.music:
            self.music.stop()

    def stop_music_and_ambience(self):
        if self.music is not None:
            self.music.stop()
        if self.ambience is not None:
            self.ambience.stop()
        self.music = None
        self.ambience = None

    def reset_audio_system(self):
        self.stop_sounds()
        self.stop_music_and_ambience()

    def destroy(self):
        self.reset_audio_system()
    def update_spatial_audio(self, listener_x, listener_y, channels=10, volchange=10):
        sounds_to_remove = []
        for sound_object, source_game_object in self.active_sounds:
            if sound_object.playing:
                source_x = source_game_object.x
                source_y = source_game_object.y
                pan, volume = bgtsound.sound.pan_sound(listener_x, listener_y, source_x, source_y, channels=9, volchange=25)
                sound_object.pan = pan
                sound_object.volume = volume
            else:
                sounds_to_remove.append((sound_object, source_game_object))
                sound_object.close()
        for item in sounds_to_remove:
            if item in self.active_sounds:
                self.active_sounds.remove(item)
        self.cleanup()
    def cleanup(self):
        sounds_to_remove = [sound_obj for sound_obj in self.unmanaged_sounds if not sound_obj.playing]
        for sound_obj in sounds_to_remove:
            sound_obj.stop()
            sound_obj.close()
            self.unmanaged_sounds.remove(sound_obj)