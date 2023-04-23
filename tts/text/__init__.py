""" from https://github.com/keithito/tacotron """
from . import cleaners
# from text.symbols import symbols
from . import symbols

# symbols = symbols.jsut_symbols

# Mappings from symbol to numeric ID and vice versa:
# _symbol_to_id = {s: i for i, s in enumerate(symbols)}
# _id_to_symbol = {i: s for i, s in enumerate(symbols)}


def text_to_sequence(text, lang, cleaned):
  '''Converts a string of text to a sequence of IDs corresponding to the symbols in the text.
    Args:
      text: string to convert to a sequence
      cleaner_names: names of the cleaner functions to run the text through
    Returns:
      List of integers corresponding to the symbols in the text
  '''

  sequence = []
  
  # clean_text = _clean_text(text, cleaner_names)
  if lang == 'ja':
    if cleaned:
      clean_text = text.split(' ')
    else:
      clean_text = cleaners.japanese_cleaners(text)
    for symbol in clean_text:
      symbol_id = symbols.jsut_index[symbol]
      sequence += [symbol_id]
  else:
    if cleaned:
      clean_text = text.split(' ')
    else:
      clean_text = cleaners.english_cleaners2(text)
    # print(cleaned,clean_text,text)
    for symbol in clean_text:
      symbol_id = symbols.vctk_index[symbol]
      sequence += [symbol_id]

  return clean_text, sequence


# def cleaned_text_to_sequence(cleaned_text):
#   '''Converts a string of text to a sequence of IDs corresponding to the symbols in the text.
#     Args:
#       text: string to convert to a sequence
#     Returns:
#       List of integers corresponding to the symbols in the text
#   '''
#   sequence = [_symbol_to_id[symbol] for symbol in cleaned_text]
#   return sequence


# def sequence_to_text(sequence):
#   '''Converts a sequence of IDs back to a string'''
#   result = ''
#   for symbol_id in sequence:
#     s = _id_to_symbol[symbol_id]
#     result += s
#   return result


# def _clean_text(text, cleaner_names):
#   for name in cleaner_names:
#     cleaner = getattr(cleaners, name)
#     if not cleaner:
#       raise Exception('Unknown cleaner: %s' % name)
#     text = cleaner(text)
#   return text
