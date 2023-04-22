cd voice-generator-webui
pip install -r requirements.txt

pip uninstall torchaudio
pip install torch==1.13.1+cu117 --extra-index-url https://download.pytorch.org/whl/cu117

if [ "$1" != "en" ]; then
  pip install pyopenjtalk
fi

cd tts/monotonic_align
python setup.py build_ext --inplace