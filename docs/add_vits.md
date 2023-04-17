# Add other VITS model

Here is an example of adding a jsut corpus model.
Trained models and configs, etc should be deployed as follows.

```bash
tts
├── configs
│   └── jsut.json # VITS config
└── models
    ├── jsut.pth # VITS model
    └── jsut_speakers.txt # speakers name list inside model

```

`tts/models/model_list.json`
```json
{
    "en": "vctk",
    "ja": "jsut",
    ...
    "displayed name": "model name"
}
```


Add the following processing based on the symbols used to train VITS.

`text/symbols.py`
```python
jsut_symbols = [
    'a', 'i', 'u', 'e', 'o',
    'I', 'U',
    'k', 'ky', 'g', 'gy',
    's', 'sh', 'z', 'j',
    't', 'ch', 'ts', 'd', 'dy',
    'n', 'ny',
    'h', 'f', 'hy', 'b', 'by', 'v', 'p', 'py',
    'm', 'my',
    'y',
    'r', 'ry',
    'w',
    'N',
    'cl',
    'ty',
     '_', '^', '$', '?',
     '[', ']', '#'
]

jsut_index = {s: i for i, s in enumerate(jsut_symbols)}
```

`text/cleaners.py`
```python
def japanese_cleaners(text):
  phonemes = pyopenjtalk_g2p_prosody(text)
  return phonemes
```

`text/__init__.py`
```python
def text_to_sequence(text, lang):
    ...

  if lang == 'ja':
    clean_text = cleaners.japanese_cleaners(text)
    for symbol in clean_text:
      symbol_id = symbols.jsut_index[symbol]
      sequence += [symbol_id]
```