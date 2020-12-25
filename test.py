from zh_cn import G2P
g2p = G2P()
sentences=['清华大学人机语音交互实验室！',
           '蒹葭苍苍，白露为霜。',
           '测试一下，code switch。一会儿。',
           '慢着，这是他的东西。']
sentences=[g2p.convert(i) for i in sentences]
print(sentences)

