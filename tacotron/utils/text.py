import re

from . import cleaners
from .symbols import symbols
from .symbols import symbols_tag


assert symbols_tag == 'MIX_Phoneme_Version'


# Mappings from symbol to numeric ID and vice versa:
_symbol_to_id = {s: i for i, s in enumerate(symbols)}
_id_to_symbol = {i: s for i, s in enumerate(symbols)}

# Regular expression matching text enclosed in curly braces:
_curly_re = re.compile(r'(.*?)\{(.+?)\}(.*)')


def text_to_sequence(text, cleaner_names):
  '''Converts a string of text to a sequence of IDs corresponding to the symbols in the text.

    The text can optionally have ARPAbet sequences enclosed in curly braces embedded
    in it. For example, "Turn left on {HH AW1 S S T AH0 N} Street."

    Args:
      text: string to convert to a sequence
      cleaner_names: names of the cleaner functions to run the text through

    Returns:
      List of integers corresponding to the symbols in the text
  '''
  sequence = []

  # Check for curly braces and treat their contents as ARPAbet:
  while len(text):
    m = _curly_re.match(text)
    if not m:
      sequence += _symbols_to_sequence(_clean_text(text, cleaner_names))
      break
    sequence += _symbols_to_sequence(_clean_text(m.group(1), cleaner_names))
    sequence += _arpabet_to_sequence(m.group(2))
    text = m.group(3)

  # Append EOS token
  sequence.append(_symbol_to_id['~'])
  return sequence


def text_to_sequence_MIX_Phoneme_Version(text, cleaner_names):
  '''Converts a string of text to a sequence of IDs corresponding to the symbols in the text.

    The text can optionally have ARPAbet sequences enclosed in curly braces embedded
    in it. For example, "Turn left on {HH AW1 S S T AH0 N} Street."

    Args:
      text: string to convert to a sequence
      cleaner_names: names of the cleaner functions to run the text through

    Returns:
      List of integers corresponding to the symbols in the text
  '''
  assert len(cleaner_names) == 1 and cleaner_names[0] == 'MIX_Phoneme_cleaners'

  # uo_3_ _10_sh_10_en_1_sh_10_ang_4_ _10_f_10_en_1_uen_2_ _10_m_10_ei_2_iou_3_._10
  sequence_id_suffix = text.split('_')
  sequence_txt = []
  digital_tone_stress = []
  # 拆分为两个数字List
  for i, ch in enumerate(sequence_id_suffix):
    if i % 2 == 0:
      sequence_txt.append(_symbol_to_id[ch])
    else:
      assert ch.isdigit() is True
      digital_tone_stress.append(int(ch))

  # Append EOS token
  sequence_txt.append(_symbol_to_id['~'])
  digital_tone_stress.append(digital_tone_stress[-1])

  assert len(sequence_txt) == len(digital_tone_stress)
  return (sequence_txt, digital_tone_stress)


def sequence_to_text(sequence):
  '''Converts a sequence of IDs back to a string'''
  result = ''
  for symbol_id in sequence:
    if symbol_id in _id_to_symbol:
      s = _id_to_symbol[symbol_id]
      # Enclose ARPAbet back in curly braces:
      if len(s) > 1 and s[0] == '@':
        s = '{%s}' % s[1:]
      result += s
  return result.replace('}{', ' ')


def _clean_text(text, cleaner_names):
  for name in cleaner_names:
    cleaner = getattr(cleaners, name)
    if not cleaner:
      raise Exception('Unknown cleaner: %s' % name)
    text = cleaner(text)
  return text


def _symbols_to_sequence(symbols):
  return [_symbol_to_id[s] for s in symbols if _should_keep_symbol(s)]


def _arpabet_to_sequence(text):
  return _symbols_to_sequence(['@' + s for s in text.split()])


def _should_keep_symbol(s):
  return s in _symbol_to_id and s is not '_' and s is not '~'
