'''
Defines the set of symbols used in text input to the model.

The default is a set of ASCII characters that works well for English or text that has been run
through Unidecode. For other data, you can modify _characters. See TRAINING_DATA.md for details.
'''
# from . import cmudict
symbols_tag = 'MIX_Phoneme_Version'
if True:
    _pad        = '_'
    _eos        = '~'
    _EN_Symbols = ['!', '#', "'", '*', '11', '7', '8', '9', '?', 'AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'B', 'CH', 'D', 'DH', 'EH', 'ER', 'EY', 'F', 'G', 'HH', 'IH', 'IY', 'JH', 'K', 'L', 'M', 'N', 'NG', 'OW', 'OY', 'P', 'R', 'S', 'SH', 'T', 'TH', 'UH', 'UW', 'V', 'W', 'Y', 'Z', 'ZH', '^']
    _CN_Symbols = [' ', ',', '.', '/', '1', '10', '2', '3', '4', '5', '6', 'AY', 'CH', 'EH', 'EY', 'G', 'IY', 'JH', 'K', 'P', 'S', 'UW', 'W', 'Y', 'a', 'ai', 'an', 'ang', 'ao', 'b', 'c', 'ch', 'd', 'e', 'ei', 'en', 'eng', 'er', 'f', 'g', 'h', 'i', 'ia', 'ian', 'iang', 'iao', 'ie', 'in', 'ing', 'io', 'iong', 'iou', 'ix', 'iy', 'j', 'k', 'l', 'm', 'n', 'o', 'ong', 'ou', 'p', 'q', 'r', 'rr', 's', 'sh', 't', 'u', 'ua', 'uai', 'uan', 'uang', 'uei', 'uen', 'ueng', 'uo', 'v', 'van', 've', 'vn', 'x', 'z', 'zh']

    # Prepend "@" to ARPAbet symbols to ensure uniqueness (some are the same as uppercase letters):
    #_arpabet = ['@' + s for s in cmudict.valid_symbols]

    # Export all symbols:
    symbols = [_pad, _eos] + _EN_Symbols + _CN_Symbols

    # 但是tone stress的字符并不查表, 直接字符int转换, 所以不能用len, 而是:tone_stress_symbols_max_no指定不越界
    tone_stress_symbols = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
    tone_stress_symbols_max_no = 15
else:
    _pad        = '_'
    _eos        = '~'
    _characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!\'\"(),-.:;? %/'
    _digits     = '0123456789'
    _cn_prosody = '* $,#%.，。？！‘’：；、（）【】'

    # Prepend "@" to ARPAbet symbols to ensure uniqueness (some are the same as uppercase letters):
    #_arpabet = ['@' + s for s in cmudict.valid_symbols]

    # Export all symbols:
    symbols = [_pad, _eos] + list(_characters) + list(_digits) + list(_cn_prosody)
