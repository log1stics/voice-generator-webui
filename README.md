# Voice Generator web UI
日本語は[こちら](docs/README_ja.md)
A Multi-speaker, multilingual speech generation tool.

![](screenshot.png)

## Features

- Speech synthesis for 209 speakers (100 Japanese / 109 English)
- Accent and phoneme editing functions
- Voice conversion by RVC
- RVC model creation with a few clicks using the Colab environment
- Batch voice conversion by RVC



## Installation and Running
[Python 3.10.6](https://www.python.org/downloads/windows/)

```
git clone https://github.com/log1stics/voice-generator-webui
```

```
cd voice-generator-webui
pip install requirement.txt
python3 webui.py
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
- [JSUT](https://sites.google.com/site/shinnosuketakamichi/publication/jsut)
- [VCTK](https://datashare.ed.ac.uk/handle/10283/2950)
