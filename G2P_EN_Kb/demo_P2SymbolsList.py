import os
import re
from tqdm import tqdm


# in
phoneme_in_path = 'databaker_MIX_Phoneme/DBMIX_EN_meta_symbol_split.csv.txt'

# out
symbols_out_path = 'databaker_MIX_Phoneme/DBMIX_EN_symbolsList_symbol_split.csv.txt'


# 100001|W_EH_1_N_*_AY_1_*_F_AW_1_N_D_*_AW_1_T_*_AH_0_B_AW_1_T_*_HH_ER_0_*_D_EH_1_TH_*_AY_1_*_W_AA_1_Z_*_SH_AA_1_K_T_*_^_*_B_AH_1_T_*_N_AA_1_T_*_S_ER_0_P_R_AY_1_Z_D_*_^_*_SH_IY_1_*_S_EH_1_D_*_#
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