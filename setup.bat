IF "%1"!="en" (
    pip install pyopenjtalk
)

cd voice-generator-webui
pip install -r requirements.txt

cd tts/monotonic_align
python setup.py build_ext --inplace