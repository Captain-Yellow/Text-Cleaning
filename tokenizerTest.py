from copy import copy
from collections import defaultdict
from operator import itemgetter


testList = ["کاربردهای", "رقابت", "دوستانه", "به", "صورت", "ناجوانمردانه", "با", "نتیجه", "3-1", "به", "نفع", "تیم", "همیشه", "بازنده", "در", "زمین", "ای", "نامناسب", "خاتمه", "یافت"]
# testList = ["دوست"]
testTemp = copy(testList)

begin_sub_word = ["نا", "با"]
end_sub_word = ["های", "انه", "ها", "ان", "ای"]
skip_word = {"با": ["باشه"]}
list_of_words = ['One', 'Two', 'Three', 'Four', 'Five']
replacements = list()

for w in range(len(testList)):
    print("w :", testList[w])
    for n in range(len(begin_sub_word)):
        if testList[w][0:2] == begin_sub_word[n]:
            list_of_keys = [key for key, list_of_values in skip_word.items() if testList[w] in list_of_values]
            if begin_sub_word[n] in skip_word and list_of_keys:
                pass
            else:
                replacements.append([testList[w].partition(begin_sub_word[n]), w])
                print(testList[w])
                break
    for n in range(len(end_sub_word)):
        if testList[w][-2:] == end_sub_word[n] or testList[w][-1:] == end_sub_word[n] or testList[w][-3:] == end_sub_word[n]:
            list_of_keys = [key for key, list_of_values in skip_word.items() if testList[w] in list_of_values]
            if end_sub_word[n] in skip_word and list_of_keys:
                pass
            else:
                replacements.append([testList[w].rpartition(end_sub_word[n]), w])
                print(testList[w])
                break
            # break


print(replacements)


temp = []
for k, v in replacements:
    temp.append(v)

print(temp)




def list_duplicates(seq):
    tally = defaultdict(list)
    for i, item in enumerate(seq):
        tally[item].append(i)
    return ((key, locs) for key, locs in tally.items() if len(locs) > 1)
dup_ls = []
for dup in sorted(list_duplicates(temp)):
    dup_ls.append(dup)
dup_ls.sort(key=itemgetter(1))
print("dup_ls: ", dup_ls)





fixed_ls = []
for fx in range(len(dup_ls)):
    fixed_word = replacements[dup_ls[fx][1][0]][0]
    print(fixed_word)
    print("r    " , replacements[dup_ls[fx][1][0]][1])
    fixed_ls.append([[fixed_word[1], fixed_word[2].strip(replacements[dup_ls[fx][1][1]][0][1]), replacements[dup_ls[fx][1][1]][0][1]], replacements[dup_ls[fx][1][0]][1]])

print("fixed_ls: ", fixed_ls)
print(dup_ls)




# sort indexes for mines
# sub all index's after herself from 2
print(len(replacements))
r = 0
for rm in range(len(dup_ls)):
    del replacements[int(dup_ls[rm][1][0])]
    del replacements[int(dup_ls[rm][1][0])]
    r += 2
    try:
        dup_ls[rm + 1][1][0] -= r
        dup_ls[rm + 1][1][1] -= r
    except IndexError:
        pass





for rp in range(len(fixed_ls)):
    replacements.insert(dup_ls[rp][1][0], fixed_ls[rp])



print(list(replacements))
for rpi in range(len(replacements)):
    temp_ls = list(replacements[rpi][0])
    if temp_ls:
        temp_ls = [x.strip(' ') for x in temp_ls]
        temp_ls[:] = [x for x in temp_ls if x]
    testList.pop((replacements[rpi][1]))
    testList.insert(replacements[rpi][1], temp_ls)





dup_ls = []
temp = []
fixed_ls = []
print(testList)
# print(replacements)
