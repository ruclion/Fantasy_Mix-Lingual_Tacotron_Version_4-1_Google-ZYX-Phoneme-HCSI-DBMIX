import os
import re
from tqdm import tqdm
from g2p_en import G2p
 

in_path = '/ceph/home/hujk17/TTS.DataBaker.zhcmn.enus.F.DB6.emotion/EN/100001-102000.txt'
out_dir = 'databaker_MIX_Phoneme'

g2p = G2p()


def write_metadata(metadata, out_dir, out_path):
    with open(os.path.join(out_dir, out_path), 'w', encoding='utf-8') as f:
        for m in tqdm(metadata):
            f.write('|'.join([str(x) for x in m]) + '\n')
        print('len:', len(metadata))
    return True


def build_from_path_EN(input_path, use_prosody = False):
    assert use_prosody is False
    content = _read_labels(input_path)
    # databaker EN:
    # 100001    When I found- out about her death% I was shocked%, but not surprised%, she said%.
    #           W EH1 N / AY1 / F AW1 N D / AW1 T / AH0 . B AW1 T / HH ER1 / D EH1 TH / AY1 / W AA1 Z / SH AA1 K T / B AH1 T / N AA1 T / S ER0 . P R AY1 Z D3 / SH IY1 / S EH1 D
    metadata = []
    num = int(len(content)//2)
    for idx in tqdm(range(num)):
        res = _parse_en_prosody_label(content[idx*2], content[idx*2+1], use_prosody)
        if res is not None:
            basename, text = res
            metadata.append([basename, text])
        # break
    return metadata



def _read_labels(input_path):
    # 从多个文件读入, 改为指定一个文件读入, 因此有些冗余
    files = []
    files.append(input_path)
    
    # load from all files
    labels = []
    for item in files:
        with open(item, 'r', encoding='utf-8-sig') as f:
            for line in f:
                line = line.strip()
                if line != '': labels.append(line)
    return labels


def _parse_en_prosody_label(id_text, phoneme_hcsi, use_prosody=False):
    assert use_prosody is False
    id_text = id_text.strip().split()
    sen_id  = id_text[0]
    text = ' '.join(id_text[1:])

    # 开始处理字符串
    # %
    text = re.sub('%', '', text)
    # -
    text = re.sub('-', ' ', text)
    # 有些-会产生多个空格, 只留一个
    _whitespace_re = re.compile(r'\s+')
    text = re.sub(_whitespace_re, ' ', text)

    out = g2p(text)
    mix_out = []
    # 将数字分出来
    # 辅音用11占位, 韵律符号也用11占位
    for x in out:
        if x[-1].isdigit():
            mix_out.append(x[0:-1])
            mix_out.append(str(int(x[-1]) + 7))
        else:
            mix_out.append(x)
            mix_out.append('11')
    print(mix_out)
    # 空格替换为*
    for i, x in enumerate(mix_out):
        if mix_out[i] == ' ':
            mix_out[i] = '*'

    mix_out_str = '_'.join(mix_out)

    # ,号和中文冲突了, 改为^
    mix_out_str = re.sub(',', '^', mix_out_str)
    # .号和中文冲突了, 改为#
    mix_out_str = re.sub('\.', '#', mix_out_str)
    # 其余符号不用管, 不会和中文冲突, 保留, 比如; ? !等
    
    return (sen_id, mix_out_str)




def main():
    os.makedirs(out_dir, exist_ok=True)
    meta = build_from_path_EN(in_path, use_prosody = False)
    finished = write_metadata(meta, out_dir, 'DBMIX_EN_meta_symbol_split.csv.txt')
    print('tag:', finished)
    print('0:', '|'.join(meta[0]))

if __name__ == "__main__":
    main()
