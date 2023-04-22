# Voice Generator web UI
VITS、RVCを用いた多言語、多話者対応のアクセント調整可能な音声生成ツール
<div align="center">

[![Open In Colab](https://img.shields.io/badge/Colab-F9AB00?style=for-the-badge&logo=googlecolab&color=525252)](https://colab.research.google.com/github/log1stics/voice-generator-webui/blob/main/colab.ipynb)

</div>

![](../images/Screenshot.png)

## 機能
- 209人分の音声合成(日本語話者 100人 / 英語話者 109人)
- LLMを用いた台本生成
- アクセントや音素の編集
- RVCによる音声変換
- RVCによるバッチ音声変換



## インストール

- [Python 3.10.6](https://www.python.org/downloads/windows/)
- [CUDA](https://developer.nvidia.com/cuda-toolkit-archive)
すでにインストール済みのケースが多いです。  
初めてAI系のプログラムを動かす場合、`CUDA Toolkit 11.8.0`をDL & インストール
- Build Tools for Visual Studio
詳しくは[こちら](dependencies.md)

### Windows
1. zipをダウンロードするか
`git clone https://github.com/log1stics/voice-generator-webui`

2. `setup.bat`を実行
pyopenjtalkのインストールでエラーになる場合[こちら](dependencies.md)を確認してください

PowerShellやコマンド プロンプトでwebui.pyファイルを実行
```shell
python webui.py
```

### Linux


```shell
git clone https://github.com/log1stics/voice-generator-webui
chmod +x setup.sh
```
```shell
setup.sh
```

```shell
# If you do not use Japanese Text To Speak
# avoid install pyopenjtalk
setup.sh en
```
```shell
# For English Text To Speak
apt-get install espeak
```

## RVCモデルの追加

例えばEXAMPLE_MODEL.pthというRVCの学習モデルを扱いたい場合、以下のようにpthファイルを配置した後、webuiを再起動してください
```bash
vc/
└── models/
    └── EXAMPLE_MODEL/
        ├── EXAMPLE_MODEL.pth # (ファイル名はディレクトリ名と同じにする)
        ├── added.index # なくても可 (名前はadded.index固定)
        └── total_fea.npy # なくても可 (名前はtotal_fea.npy固定)
```


## For developers
Here's how to add code to this repo: [Contributing](docs/add_vits.md)


## Credits

- [VITS](https://github.com/jaywalnut310/vits)
- [Retrieval-based-Voice-Conversion-WebUI](https://github.com/liujing04/Retrieval-based-Voice-Conversion-WebUI)
- [pyopenjtalk](https://github.com/r9y9/pyopenjtalk)

### Dataset
- [JSUT](https://sites.google.com/site/shinnosuketakamichi/publication/jsut)
- [VCTK](https://datashare.ed.ac.uk/handle/10283/2950)
