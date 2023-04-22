if [ "$1" != "en" ]; then
  pip install pyopenjtalk
fi

cd voice-generator-webui
pip install -r requirements.txt

cd tts/monotonic_align
python setup.py build_ext --inplace