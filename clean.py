persian_alphabet = '۱۲۳۴۵۶۷۸۹۰ٸآابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی'


def create_persian_sub_mapping():
    kaf_alt = 'كڬڬڭګڪ'
    gaf_alt = 'ڲڳ'
    ye_alt = 'ۍېيێئ'
    vav_alt = 'ۅۋۈۉٶۇۆۊؤٶ'
    hamze_alt = 'ٳٱأٲإ'
    he_alt = 'ۃۀہةە'
    r_alt = 'ړڒڕ'
    lam_lat = 'ڵ'
    f_alt = 'ڤڡ'
    mapping = {}
    for k in kaf_alt:
        mapping[k] = 'ک'
    for g in gaf_alt:
        mapping[g] = 'گ'
    for y in ye_alt:
        mapping[y] = 'ی'
    for v in vav_alt:
        mapping[v] = 'و'
    for hz in hamze_alt:
        mapping[hz] = 'ا'
    for h in he_alt:
        mapping[h] = 'ه'
    for r in r_alt:
        mapping[r] = 'ر'
    for l in lam_lat:
        mapping[l] = 'ل'
    for f in f_alt:
        mapping[f] = 'ف'

    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    for i in range(len(persian_digits)):
        mapping[str(i)] = persian_digits[i]
    return mapping

unknown_list = []
def clean(line):
    # remove punctuations
    line = line.strip()
    if len(line) and line[-1] in ':!ء،؛؟»?':
        line = line[:-1]

    mappings = create_persian_sub_mapping()
    new_line = ''
    for ch in line:
        if ch in ':!ء،؛؟><«»()':
            continue
        if ord(ch) == 32 or ch == ' ' or ch == '‌':
            new_line += ' '
            continue
        if ch in mappings.keys():
            new_line += mappings[ch]
        else:
            if ch in persian_alphabet:
                new_line += ch
            else:
                if ord(ch) not in unknown_list:
                    unknown_list.append(ord(ch))
                    return ""
                    # print(line)
                    # print("unknown character: ", ord(ch), ch)
    return new_line

if __name__ == "__main__":
    try:
        with open('persianTestText', 'r') as f:
            history = []
            for line in f:
                new_line = ''
                for word in line.split():
                    new_line = new_line + clean(word) + " "
                history.append(new_line.strip())
        with open("clean_corpus.txt", 'w') as g:
            for l in history:
                g.write(l + "\n")
    except Exception as e:
        with open("clean_corpus.txt", 'w') as g:
            for l in history:
                g.write(l + "\n")
