python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

pip install RPi.GPIO 

cp settings.py.example settings.py
python3 listen_keypress.py