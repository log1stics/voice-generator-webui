# Add other VITS model

Here is an example of adding a jvs corpus model.
Trained models and configs, etc should be deployed as follows.

```bash
tts
├── configs
│   └── jvs.json # VITS config
└── models
    ├── jvs.pth # VITS model
    └── jvs_speakers.txt # speakers name list inside model

```

`tts/models/model_list.json`
```json
{
    "en": "vctk",
    "ja": "jvs",
    ...
    "displayed name": "model name"
}
```


Add the following processing based on the symbols used to train VITS.

`text/symbols.py`
```python
jvs_symbols = [
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

jvs_index = {s: i for i, s in enumerate(jvs_symbols)}
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
      symbol_id = symbols.jvs_index[symbol]
      sequence += [symbol_id]
```