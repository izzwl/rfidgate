python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

#optional
pip install RPi.GPIO or pip install OPi.GPIO
pip install spidev
pip install mfrc522

cp settings.py.example settings.py
python3 listen_keypress.py