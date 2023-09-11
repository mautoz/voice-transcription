# Voice Transcription

Do you want to transcribe voice messages on Telegram? This is a simple code to transcript voice messages sent to Telegram. I speak Brazilian Portuguese, but it's easy to change the language.

## Dependencies

### Pip

- SpeechRecognization
- pydub
- python-telegram-bot==13.7 (I had problems with new versions)
- ffmpeg

### apt-get
 - ffmpeg
 
$ rpm --import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro 

$ rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-5.el7.nux.noarch.rpm
Install the FFmpeg and FFmpeg development packages.

$ yum install ffmpeg ffmpeg-devel -y


