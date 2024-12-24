import machine
from modules import settings
try:
    from utime import sleep
except ModuleNotFoundError:
    from time import sleep
from modules.logging import *
# import uasyncio as asyncio


class BuzzerMelody:
    """
    Plays a melody. Example usage::

        from modules.BuzzerMelody import BuzzerMelody
        player = BuzzerMelody()
        res = await player.playsong_async("cantinaband")
    """
    tones = {
        "B0": 31, "C1": 33, "CS1": 35, "D1": 37, "DS1": 39, "E1": 41, "F1": 44, "FS1": 46, "G1": 49, "GS1": 52,
        "A1": 55, "AS1": 58, "B1": 62, "C2": 65, "CS2": 69, "D2": 73, "DS2": 78, "E2": 82, "F2": 87, "FS2": 93,
        "G2": 98, "GS2": 104, "A2": 110, "AS2": 117, "B2": 123, "C3": 131, "CS3": 139, "D3": 147, "DS3": 156,
        "E3": 165, "F3": 175, "FS3": 185, "G3": 196, "GS3": 208, "A3": 220, "AS3": 233, "B3": 247, "C4": 262,
        "CS4": 277, "D4": 294, "DS4": 311, "E4": 330, "F4": 349, "FS4": 370, "G4": 392, "GS4": 415, "A4": 440,
        "AS4": 466, "B4": 494, "C5": 523, "CS5": 554, "D5": 587, "DS5": 622, "E5": 659, "F5": 698, "FS5": 740,
        "G5": 784, "GS5": 831, "A5": 880, "AS5": 932, "B5": 988, "C6": 1047, "CS6": 1109, "D6": 1175, "DS6": 1245,
        "E6": 1319, "F6": 1397, "FS6": 1480, "G6": 1568, "GS6": 1661, "A6": 1760, "AS6": 1865, "B6": 1976, "C7": 2093,
        "CS7": 2217, "D7": 2349, "DS7": 2489, "E7": 2637, "F7": 2794, "FS7": 2960, "G7": 3136, "GS7": 3322, "A7": 3520,
        "AS7": 3729, "B7": 3951, "C8": 4186, "CS8": 4435, "D8": 4699, "DS8": 4978, "F#1": 46, "G#1": 51, "A#1": 56, "C#2": 70, "D#2": 74, "F#2": 92, "G#2": 103, "A#2": 112,
        "C#3": 139, "D#3": 149, "F#3": 185, "G#3": 207, "A#3": 224, "C#4": 277, "D#4": 297, "F#4": 370,
        "G#4": 415, "A#4": 448, "C#5": 554, "D#5": 594, "F#5": 740, "G#5": 831, "A#5": 896, "C#6": 1109,
        "D#6": 1188, "F#6": 1480, "G#6": 1661, "A#6": 1792, "C#7": 2217, "D#7": 2376, "F#7": 2960, "G#7": 3322,
        "A#7": 3584, "C#8": 4435, "D#8": 4752, "F#8": 5920, "G#8": 6645, "A#8": 7168
    }

    """Stores songs in RTTTL notation.
    - d = duration
    - o = octave
    - b = BPM"""
    # Melodies from https://www.convertyourtone.com/ringtones3.html
    songs = {
        "Cantinaband": "Cantina:d=4, o=5, b=250:8a, 8p, 8d6, 8p, 8a, 8p, 8d6, 8p, 8a, 8d6, 8p, 8a, 8p, 8g#, a, 8a, 8g#, 8a, g, 8f#, 8g, 8f#, f., 8d., 16p, p., 8a, 8p, 8d6, 8p, 8a, 8p, 8d6, 8p, 8a, 8d6, 8p, 8a, 8p, 8g#, 8a, 8p, 8g, 8p, g., 8f#, 8g, 8p, 8c6, a#, a, g",
        "Pinkpanther": "PinkPanther:d=4, o=5, b=160:8d#, 8e, 2p, 8f#, 8g, 2p, 8d#, 8e, 16p, 8f#, 8g, 16p, 8c6, 8b, 16p, 8d#, 8e, 16p, 8b, 2a#, 2p, 16a, 16g, 16e, 16d, 2e",
        "StarWars": "SWEnd:d=4, o=5, b=225:2c, 1f, 2g., 8g#, 8a#, 1g#, 2c., c, 2f., g, g#, c, 8g#., 8c., 8c6, 1a#., 2c, 2f., g, g#., 8f, c.6, 8g#, 1f6, 2f, 8g#., 8g., 8f, 2c6, 8c.6, 8g#., 8f, 2c, 8c., 8c., 8c, 2f, 8f., 8f., 8f, 2f",
        "AxelF": "AxelF:d=4, o=5, b=160:f#, 8a., 8f#, 16f#, 8a#, 8f#, 8e, f#, 8c.6, 8f#, 16f#, 8d6, 8c#6, 8a, 8f#, 8c#6, 8f#6, 16f#, 8e, 16e, 8c#, 8g#, f#.",
        "BarbieGirl": "Barbie girl:d=4, o=5, b=125:8g#, 8e, 8g#, 8c#6, a, p, 8f#, 8d#, 8f#, 8b, g#, 8f#, 8e, p, 8e, 8c#, f#, c#, p, 8f#, 8e, g#, f#",
        "Deutschland": "Deutschlandlied:d=4, o=5, b=160:2g, 8a, b, a, c6, b, 8a, 8f#, g, e6, d6, c6, b, a, 8b, 8g, 2d6, 2g, 8a, b, a, c6, b, 8a, 8f#, g, e6, d6, c6, b, a, 8b, 8g, 2d6, a, b, 8a, 8f#, d, c6, b, 8a, 8f#, d, d6, c6, 2b, 8b, c#6, 8c#6, 8d6, 2d6, 2g6, 8f#6, 8f#6, 8e6, d6, 2e6, 8d6, 8d6, 8c6, b, 2a, 16b, 16c6, 8d6, 8e6, 8c6, 8a, 2g, 8b, 8a, 2g",
        "FinalCoundown": "The Final Countdown:d=4, o=5, b=125:p, 8p, 16b, 16a, b, e, p, 8p, 16c6, 16b, 8c6, 8b, a, p, 8p, 16c6, 16b, c6, e, p, 8p, 16a, 16g, 8a, 8g, 8f#, 8a, g., 16f#, 16g, a., 16g, 16a, 8b, 8a, 8g, 8f#, e, c6, 2b., 16b, 16c6, 16b, 16a, 1b",
        "HappyBirthday": "HappyBirthday:d=4, o=5, b=125:8g., 16g, a, g, c6, 2b, 8g., 16g, a, g, d6, 2c6, 8g., 16g, g6, e6, c6, b, a, 8f6., 16f6, e6, c6, d6, 2c6, 8g., 16g, a, g, c6, 2b, 8g., 16g, a, g, d6, 2c6, 8g., 16g, g6, e6, c6, b, a, 8f6., 16f6, e6, c6, d6, 2c6",
        "LastChristmas": "Last Christmas:d=4,o=5,b=112:16d6,e6,8p,e6,8d6,8p,8a,8e6,8e6,8f#6,d.6,8b,8b,8e6,8e6,f#6,d.6,8b,8c#6,8d6,8c#6,2b.,16e6,f#6,8p,e.6,8p,8b,8f#6,8g6,8f#6,2e6,8d6,8c#6,8d6,8c#6,c#6,8d6,8p,8c#6,8p,2a,16d6,e6,8p,e6,8d6,8p,8a,8e6,8e6,8f#6,d.6,8b,8b,8e6,8e6,f#6,d.6,8b,8c#6,8d6,8c#6,2b.,16e6,f#6,8p,e.6,8p,8b,8f#6,8g6,8f#6,2e6,8d6,8c#6,8d6,8c#6,c#6,8d6,8p,8c#6,8p,a",
        "Beep": "Beep:d=4,o=6,b=100:48c,24p,48c,p,48c,24p,48c,p,48c,24p,48c,p,48c,24p,48c,p,48c,24p,48c,p,48c,24p,48c,p,48c,24p,48c,p,48c,24p,48c,p,48c,24p,48c,p,48c,24p,48c,p,48c,24p,48c,p",
        "BeepShort": "BeepShort:d=4,o=6,b=100:48c,24p,48c,p"
    }

    def __init__(self) -> None:
        self.buzzer = machine.PWM(machine.Pin(settings.config.get("buzzer.pin", 16)))

    def _playtone(self, frequency, duration: int):
        self.buzzer.duty_u16(1000)
        self.buzzer.freq(frequency)
        sleep(duration / 1000)  # we need ms

    def _bequiet(self, duration: int):
        self.buzzer.duty_u16(0)
        sleep(duration / 1000)  # we need ms

    async def playsong_async(self, song: str):
        self._playsong(song)

    def _playsong(self, song):
        """Plays the song from the Songs library.

        Args:
            song (Song): The selected sing in RTTTL notation
        """
        matching_songs = [value for key, value in self.songs.items() if key.lower() == song.lower()]
        if matching_songs:
            melody_rtttl = matching_songs[0]
        else:
            log_warning(f"Melody '{song}' not found in player.songs, playing default.")
            melody_rtttl = self.songs['Beep']

        song_info = melody_rtttl.split(":")
        # Check if there are enough elements in the song_info list
        if len(song_info) >= 3:
            bpm = int(song_info[1].split(",")[2].split("=")[1])
            tact = int(song_info[1].split(",")[0].split("=")[1])
            notes = song_info[2].split(",")
            octave = song_info[1].split(",")[1].split("=")[1]
            log_info(f"Playing song {song_info[0]}.")

            # Calculate the duration of a quarter note in milliseconds
            quarter_note_duration = 60000 / bpm

            try:
                for note in notes:
                    try:
                        note = note[1:] if str(note).startswith(" ") else note  # remove empty space if there is one
                        # Extract the duration and note
                        if "." in note and len(note) == 2:
                            duration_str = str(tact)
                            note_value = note[0]
                        elif "." in note and "#" in note and len(note) == 4:
                            duration_str = str(int(int(note[0]) * 1.5))
                            note_value = note[1:3]
                        elif "." in note and "#" in note and len(note) == 3:
                            duration_str = str(int(int(tact) * 1.5))
                            note_value = note[0:2]
                        elif (len(note)) == 4 and note[2] == ".":
                            duration_str = str(int(int(note[0]) * 1.5))
                            note_value = note[1] + note[3]
                        elif len(note) == 3 and note[1] == ".":
                            duration_str = str(tact)
                            note_value = note[0] + note[2]
                        elif "." in note and len(note) > 2:
                            duration_str = str(int(int(note[0]) * 1.5))
                            note_value = note[1]
                        elif len(note) == 1:
                            duration_str = str(tact)
                            note_value = note
                        elif len(note) == 2 and "#" in note:
                            duration_str = str(tact)
                            note_value = note
                        elif note[:2].isdigit():
                            duration_str = note[:2]
                            note_value = note[2:]
                        elif "#" in note and not note[0].isdigit():
                            duration_str = str(tact)
                            note_value = note
                        elif note[1].isdigit() and len(note) == 2:
                            duration_str = str(tact)
                            note_value = note
                        else:
                            duration_str, note_value = note[0], note[1:]
                        duration = int(duration_str)

                        # Convert note duration to milliseconds
                        note_duration = int(quarter_note_duration / (duration / tact))

                        if note_value == "p":
                            log_info("Note: PAUSE \tFrequency: 0     Duration:", note_duration)
                            self._bequiet(note_duration)
                        else:
                            if len(note_value) == 1:
                                note_value += octave
                            if "#" in note_value and len(note_value) == 2:
                                note_value += octave
                            note_key = str(note_value).upper()
                            note_frequency = self.tones.get(note_key)
                            if "." in duration_str:
                                # Handle dotted notes
                                note_duration *= 1.5
                            log_info("Note:", note_key, "\tFrequency:", note_frequency, ("\t") if int(note_frequency) < 1000 else (""), "Duration:", note_duration)
                            self._playtone(note_frequency, note_duration)
                    except Exception as fail:
                        log_error("Failed playing", note)
                log_info(green_text("Finished playing song."))
            except Exception as ex:
                log_error("Failed playing note.", ex)
            finally:
                self._bequiet(1)
        else:
            log_error("Invalid song format")


# if __name__ == "__main__":
#     async def main():
#         player = BuzzerMelody()
#         await player.playsong_async("Cantinaband")

#     asyncio.run(main())
