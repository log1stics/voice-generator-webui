# Voice Generator web UI
A Multi-speaker, multilingual speech generation tool.

<div align="center">

日本語は[こちら](docs/ja/README.md)

[![Open In Colab](https://img.shields.io/badge/Colab-F9AB00?style=for-the-badge&logo=googlecolab&color=525252)](https://colab.research.google.com/github/log1stics/voice-generator-webui/blob/main/colab.ipynb)

</div>

![](docs/images/Screenshot.png)

## Features

- Speech synthesis for 209 speakers (100 Japanese / 109 English)
- Script generation using LLM
- Accent and phoneme editing functions
- Voice conversion by RVC
- Batch voice conversion by RVC



## Installation and Running
Tested Environment
- Ubuntu 22
- Python 3.10.6
- CUDA 11.7

Install CUDA PyTorch
```shell
pip install torch==1.13.1+cu117 --extra-index-url https://download.pytorch.org/whl/cu117
```
```shell
git clone https://github.com/log1stics/voice-generator-webui
```

```shell
cd voice-generator-webui
pip install -r requirements.txt
cd tts/monotonic_align
python setup.py build_ext --inplace

apt-get install espeak
```
Run
```shell
cd ../../ # Go to webui.py location
python webui.py
```

## Add RVC model

For example, if you want to handle an RVC training model called EXAMPLE_MODEL.pth, place it as follows
```bash
vc/
└── models/
    └── EXAMPLE_MODEL/
        ├── EXAMPLE_MODEL.pth # file name should be the same as the directory name
        ├── added.index # not necessary (name is fixed to added.index)
        └── total_fea.npy # not necessary (name is fixed to added.index)
```



## Contributing
Here's how to add code to this repo: [Contributing](docs/add_vits.md)


## Credits

- [VITS](https://github.com/jaywalnut310/vits)
- [Retrieval-based-Voice-Conversion-WebUI](https://github.com/liujing04/Retrieval-based-Voice-Conversion-WebUI)
- [pyopenjtalk](https://github.com/r9y9/pyopenjtalk)

### Dataset
- [JSUT](https://sites.google.com/site/shinnosuketakamichi/publication/jsut)
- [VCTK](https://datashare.ed.ac.uk/handle/10283/2950)
