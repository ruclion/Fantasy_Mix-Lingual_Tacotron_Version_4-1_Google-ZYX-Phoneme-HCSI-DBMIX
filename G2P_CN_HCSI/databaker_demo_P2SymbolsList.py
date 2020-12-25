import os
import re
from tqdm import tqdm


# in
phoneme_in_path = 'databaker_MIX_Phoneme/DBMIX_CN_metaProsody_symbol_split.csv.txt'

# out
symbols_out_path = 'databaker_MIX_Phoneme/DBMIX_CN_symbolsList_symbol_split.csv.txt'


# 000001|n_a_4_x_ie_1_ _zh_uang_1_j_ia_5_ _t_ian_2_van_2_ _/_ _z_ai_4_ _g_uo_6_g_uo_3_ _ian_6_l_i_6_ _/_ _g_an_3_j_ve_2_ _t_ai_4_q_in_1_q_ie_4_l_e_5_.
def main():
    f = open(phoneme_in_path, 'r', encoding='utf-8-sig')
    a = f.readlines()
    a = [i.strip() for i in a]

    symbolsList = []
    for s in a:
        s = s.split('|')[1]
        # print('s is:', s)
        s = s.split('_')
        symbolsList.extend(s)
    symbolsList = list(set(symbolsList))
    symbolsList.sort()
    print(symbolsList)
    f = open(symbols_out_path, 'w')
    print(symbolsList, file=f)



if __name__ == '__main__':
    main()