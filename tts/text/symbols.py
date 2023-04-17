""" from https://github.com/keithito/tacotron """

'''
Defines the set of symbols used in text input to the model.
'''
_pad        = '_'
_punctuation = ';:,.!?¡¿—…"«»“” '
_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
_letters_ipa = "ɑɐɒæɓʙβɔɕçɗɖðʤəɘɚɛɜɝɞɟʄɡɠɢʛɦɧħɥʜɨɪʝɭɬɫɮʟɱɯɰŋɳɲɴøɵɸθœɶʘɹɺɾɻʀʁɽʂʃʈʧʉʊʋⱱʌɣɤʍχʎʏʑʐʒʔʡʕʢǀǁǂǃˈˌːˑʼʴʰʱʲʷˠˤ˞↓↑→↗↘'̩'ᵻ"


# Export all symbols:
vctk_symbols = [_pad] + list(_punctuation) + list(_letters) + list(_letters_ipa)

# Special symbol ids for train
# SPACE_ID = vctk_symbols.index(" ")

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

vctk_index = {s: i for i, s in enumerate(vctk_symbols)}
jsut_index = {s: i for i, s in enumerate(jsut_symbols)}
