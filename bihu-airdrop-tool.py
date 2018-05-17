#!/usr/bin/python

import hashlib
from collections import OrderedDict

# block hash 比特币未来的某个区块号，币乎官方会在空投开始前公布
block_hash = bytes.fromhex('0000000000000000003729bfa376e4148ee0643ce834053d885af5699440d6d3')
# total lottery num 总共有多少人参与了此次活动
total_lottery = 100000

#函数 1
#基本的算法就是用 10 种哈希算法不停的哈希，每一种算法用了约 4000 万次，也就是 4 亿次的哈希，最后算出这个幸运数字（保证了幸运数字的不可预测性）
def lucky_num_from_block_hash(h):
    hash_names = ['md5', 'md4', 'whirlpool', 'RIPEMD160', 'DSA', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512']
    print(str(len(hash_names)) + ": " + str(hash_names))

    repeat = 10000 * 400 * 20
    r = h
    for i in range(repeat):
        if i % 100000 == 0:
            print(str(i) + ":...")
        for n in hash_names:
            h = hashlib.new(n)
            h.update(r)
            r = h.digest()

    return r

#函数 2
#此方法最核心的算法就是score ＝ hash( luck_num + 奖券号) ％ base
def score_for_each_lottery(lucky_num, lottery_id):
    # print(result_hash.hex())
    # 这一段意思就是用幸运数字和你的 ID 再进行一次哈希，由于幸运数字是不可预测的，所以每个人的分数也是不可预测的
    h = hashlib.sha256()
    h.update(lucky_num)
    h.update(bytes(lottery_id))

    #base就是一个最高分吧，把多于这个分的都对取余数
    base = 10**11
    score = int(h.hexdigest(), 16) % base
    return score

#函数 3
#最核心算法，给每个用户打个分
def compute_airdrop_reward():
    r = {}
    #用币乎官方公布的比特币未来的某个区块号，计算一个幸运数字
    #具体计算方法见函数 1
    lucky_num = lucky_num_from_block_hash(block_hash)

    for lottery_id in range(total_lottery):
        #对每一个 ID 都算一个得分，具体得分方法为函数 2
        s = score_for_each_lottery(lucky_num, lottery_id)
        r[lottery_id] = s
    return r


#计算每一个用户的得分，计算方法见函数 3
reward_map = compute_airdrop_reward()
#排个序
reward_sorted = OrderedDict(sorted(reward_map.items(), key=lambda t: t[1], reverse = True))
#结果输出
print("=======================Rewards================================")
for item in reward_sorted:
    print(str(item) + ": " + str(reward_map[item]))
