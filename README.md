# Voice Generator web UI
A Multi-speaker, multilingual speech generation tool.

<div align="center">

日本語は[こちら](docs/ja/README.md)

[![Open In Colab](https://img.shields.io/badge/Colab-F9AB00?style=for-the-badge&logo=googlecolab&color=525252)](https://colab.research.google.com/github/log1stics/voice-generator-webui/blob/main/colab.ipynb)

</div>

![](docs/images/Screenshot.png)

## Features

- Speech synthesis for 209 speakers (109 English / 100 Japanese)
- Script generation using LLM
- Accent and phoneme editing functions
- Voice conversion by RVC
- Batch voice conversion by RVC



## Installation and Running

- [Python](https://www.python.org/downloads/windows/) (tested on 3.10.6)
- [CUDA PyTorch](https://pytorch.org/get-started/locally/)


### Windows
- [espeak](docs/dependencies.md#espeak)
- [Build Tools for Visual Studio](docs/dependencies.md#build-tools-for-visual-studio) (Not necessary if Japanese is not generated)

1. download the zip or
`git clone https://github.com/log1stics/voice-generator-webui`

2. run `setup.bat` or `setup.bat en`  
`setup.bat en` avoids installation of pyopenjtalk used for Japanese generation

Run the webui.py file in PowerShell or at the command prompt
```
python webui.py
```

### Linux


Run the webui.py file at a PowerShell or command prompt
```shell
apt-get install espeak # For English Text To Speak

git clone https://github.com/log1stics/voice-generator-webui
chmod +x setup.sh
```
```
setup.sh
```

```shell
# if you do not use Japanese Text To Speak
# you can avoid install pyopenjtalk
setup.sh en
```

## Add RVC model

For example, if you want to handle an RVC trained model named EXAMPLE_MODEL.pth, place it as follows
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
