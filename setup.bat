cd voice-generator-webui
pip install -r requirements.txt

pip uninstall torchaudio
pip install torch==1.13.1+cu117 --extra-index-url https://download.pytorch.org/whl/cu117

IF "%1"!="en" (
    pip install pyopenjtalk
)

cd tts/monotonic_align
python setup.py build_ext --inplace