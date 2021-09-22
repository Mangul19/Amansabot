import os
from gtts import gTTS

language = 'ko'
slow_audio_speed = False
filename = "bot/gtts.mp3"

def reading_from_user():
    audio_created = gTTS(text=user_input, lang=language, slow=slow_audio_speed)
    audio_created.save(filename)

if __name__ == '__main__':
    reading_from_user()