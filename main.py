# Master : Omid Amir Ghiasvand 1400 (qiau.992)
# Student : Fatemeh Afshar
# Project : Persian Text Cleaner

import sys
import codecs
import textwrap
import argparse
from re import sub
from os import getcwd, path
from collections import defaultdict
from operator import itemgetter


class PersianTextCleaner(object):
    __lineCounter = 0
    __CHUNK_SIZE = 1024  # It could be 4096 or 256 or whatever
    __persian_alphabet = '۱۲۳۴۵۶۷۸۹۰ٸآابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی'
    __unknown_list = []
    __begin_sub_word = ["نا", "با", "می"]  # Compares only one or two or three letters from the beginning of the word. if you want any else just add another slicing compare in if statement
    __end_sub_word = ["های", "انه", "ها", "ان", "ای"]  # Compares only one or two or three letters from the end of the word. if you want any else just add another slicing compare in if statement
    __skip_word = {"با": ["باشه", "باشد", "بازنده"], "ان": ["فراوان", "توان", "زمان", "پایان", "زبان"], "انه": ["رایانه"], "ای": ["برای"]}  # Words that are special and you want to stay the unchanged
    __replacements = list()

    def __init__(self) -> None:
        self.__fileDirectory: str = ""
        self.__fileHandle = None

    @property
    def file_directory(self) -> str:
        """
        Playing the role of getter
        :return:
        """
        return self.__fileDirectory

    @file_directory.setter
    def file_directory(self, newFileDirectory: str) -> None:
        """
        setter function and Check the format if it is forgotten
        :param newFileDirectory: str
        :return: None
        """
        str_file = str(newFileDirectory)
        if path.isfile(str_file):
            self.__fileDirectory = str_file
        elif path.isfile(str_file + ".txt"):
            self.__fileDirectory = str_file + ".txt"
        elif path.isfile(str_file[:-4]):
            self.__fileDirectory = str_file[:-4]
        else:
            print(f"Please enter a valid location and file name using setter or main args\n{getcwd()}")
            quit()

    @file_directory.deleter
    def file_directory(self) -> None:
        del self.__fileDirectory

    def get_args(self) -> None:
        """
        The argparse was preferred to the sys.argv
        You can use the help: python main.py --help
        :return: None
        """
        if len(sys.argv) > 1:
            parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent("""
            To run the program:
            python pythonfile.py textfile.txt
            1) make sure your terminal support unicode utf-8 for presenting persian words
            2) Please enter a valid file location and name according to your operating system
            """))
            parser.add_argument('mainText', type=str, help="A Persian text file.")
            temp = parser.parse_args()
            self.file_directory = str(temp.mainText)

    def file_open(self) -> None:
        """
        Trying to open the received file as read mode and assign it to a private value
        :return: None
        """
        try:
            self.__fileHandle = codecs.open(self.__fileDirectory, mode='r', encoding="utf-8")
        except(OSError, IOError) as e:
            print("Could not open file " + self.__fileDirectory)
            print(f"{e}")  # {type(e)}
            print(f"Please enter a valid location and file name using setter or main args\n{getcwd()}")
            quit()

    @staticmethod
    def each_chunk(stream, separator='.') -> None:
        """
        Reading based on buffer size and separate by separator
        :param stream: IOBase
        :param separator: The word separator
        :return: None
        """
        buffer = ''
        while True:  # until EOF
            chunk = stream.read(PersianTextCleaner.__CHUNK_SIZE)
            if not chunk:  # EOF?
                yield buffer
                break
            buffer += chunk
            while True:  # until no separator is found
                try:
                    part, buffer = buffer.split(separator, 1)
                except ValueError:
                    break
                else:
                    yield part

    def persian_cleaner(self) -> None:
        """
        create and opening file as write mode and Writing after separating and cleaning
        Cleaning and presenting section by section
        :return: None
        """
        # PersianTextCleaner.__lineCounter = len(self.__fileHandle.readlines())
        # for PersianTextCleaner.__lineCounter, text in enumerate(self.__fileHandle.readlines(), 1):
        #     buffer = text
        #     print(f"{PersianTextCleaner.__lineCounter}, {text}")
        halfSpace = ['\u200F', '\u2028', '\u200c']  # half space is index[2]
        show_list = []
        new_line = ''
        open("CLean_" + self.__fileHandle.name, 'w').close()
        for chunk in self.each_chunk(stream=self.__fileHandle, separator='.'):
            PersianTextCleaner.__lineCounter += 1
            with open("CLean_" + self.__fileHandle.name, 'a') as nf:
                for word in chunk.split():
                    word = sub(r'[٪=/«»)(}{\]\[!?:.،؛,><_\-]', ' ', word)  # If you want to delete the English letters or apply any changes, just the regex. like a-zA-z
                    new_line = new_line + PersianTextCleaner.clean(word) + " "
                    show_list.append(PersianTextCleaner.clean(word) + " ")
                # tmp = new_line.split()
                # temp = halfSpace[2].join(temp)
                nf.write(new_line.strip() + "\n")
                new_line = ''
                if show_list:
                    show_list = [x.strip(' ') for x in show_list]
                    show_list[:] = [x for x in show_list if x]
                    # print(show_list)
                    PersianTextCleaner.tokenizer(show_list)
                del show_list[:]

        print(f"{self.__fileHandle.name} file have {PersianTextCleaner.__lineCounter} lines")
        print(f"Clean_{self.__fileHandle.name} is new and clean file in same directory")

    @staticmethod
    def create_persian_sub_mapping():
        """
        creating persian letters and numbers map
        :return: list
        """
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
        for ll in lam_lat:
            mapping[ll] = 'ل'
        for f in f_alt:
            mapping[f] = 'ف'

        persian_digits = '۰۱۲۳۴۵۶۷۸۹'
        for i in range(len(persian_digits)):
            mapping[str(i)] = persian_digits[i]
        return mapping

    @staticmethod
    def clean(line) -> str:
        """
        remove punctuations
        :param line: str
        :return: str
        """
        line = line.strip()
        if len(line) and line[-1] in ':!ء،؛؟»?':
            line = line[:-1]

        mappings = PersianTextCleaner.create_persian_sub_mapping()
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
                if ch in PersianTextCleaner.__persian_alphabet:
                    new_line += ch
                else:
                    if ord(ch) not in PersianTextCleaner.__unknown_list:
                        PersianTextCleaner.__unknown_list.append(ord(ch))
                        return ""
                        # print(line)
                        # print("unknown character: ", ord(ch), ch)
        return new_line

    @staticmethod
    def tokenizer(chunk_list) -> None:
        """
        tokenizer, Based on slicing strings and replace them
        :param chunk_list: list
        :return: None
        """
        for w in range(len(chunk_list)):
            for n in range(len(PersianTextCleaner.__begin_sub_word)):
                if chunk_list[w][0:2] == PersianTextCleaner.__begin_sub_word[n] or chunk_list[w][:1] == PersianTextCleaner.__begin_sub_word[n] or chunk_list[w][:3] == PersianTextCleaner.__begin_sub_word[n]:
                    list_of_keys = [key for key, list_of_values in PersianTextCleaner.__skip_word.items() if chunk_list[w] in list_of_values]
                    if PersianTextCleaner.__begin_sub_word[n] in PersianTextCleaner.__skip_word and list_of_keys:
                        pass
                    else:
                        PersianTextCleaner.__replacements.append([chunk_list[w].partition(PersianTextCleaner.__begin_sub_word[n]), w])
                        break
            for n in range(len(PersianTextCleaner.__end_sub_word)):
                if chunk_list[w][-2:] == PersianTextCleaner.__end_sub_word[n] or chunk_list[w][-1:] == PersianTextCleaner.__end_sub_word[n] or chunk_list[w][-3:] == PersianTextCleaner.__end_sub_word[n]:
                    list_of_keys = [key for key, list_of_values in PersianTextCleaner.__skip_word.items() if chunk_list[w] in list_of_values]
                    if PersianTextCleaner.__end_sub_word[n] in PersianTextCleaner.__skip_word and list_of_keys:
                        pass
                    else:
                        PersianTextCleaner.__replacements.append([chunk_list[w].rpartition(PersianTextCleaner.__end_sub_word[n]), w])
                        break

        temp = []
        for k, v in PersianTextCleaner.__replacements:
            temp.append(v)

        def list_duplicates(seq):
            tally = defaultdict(list)
            for i, item in enumerate(seq):
                tally[item].append(i)
            return ((key, locs) for key, locs in tally.items() if len(locs) > 1)

        dup_ls = []
        for dup in sorted(list_duplicates(temp)):
            dup_ls.append(dup)
        dup_ls.sort(key=itemgetter(0))

        fixed_ls = []
        for fx in range(len(dup_ls)):
            fixed_word = PersianTextCleaner.__replacements[dup_ls[fx][1][0]][0]
            fixed_ls.append(
                [[fixed_word[1], fixed_word[2].strip(PersianTextCleaner.__replacements[dup_ls[fx][1][1]][0][1]),
                  PersianTextCleaner.__replacements[dup_ls[fx][1][1]][0][1]],
                 PersianTextCleaner.__replacements[dup_ls[fx][1][0]][1]])

        r = 0
        for rm in range(len(dup_ls)):
            del PersianTextCleaner.__replacements[int(dup_ls[rm][1][0])]
            del PersianTextCleaner.__replacements[int(dup_ls[rm][1][0])]
            r += 2
            try:
                dup_ls[rm + 1][1][0] -= r
                dup_ls[rm + 1][1][1] -= r
            except IndexError:
                pass

        for rp in range(len(fixed_ls)):
            PersianTextCleaner.__replacements.insert(dup_ls[rp][1][0], fixed_ls[rp])

        for rpi in range(len(PersianTextCleaner.__replacements)):
            temp_ls = list(PersianTextCleaner.__replacements[rpi][0])
            if temp_ls:
                temp_ls = [x.strip(' ') for x in temp_ls]
                temp_ls[:] = [x for x in temp_ls if x]
            chunk_list.pop((PersianTextCleaner.__replacements[rpi][1]))
            chunk_list.insert(PersianTextCleaner.__replacements[rpi][1], temp_ls)

        print(chunk_list)
        PersianTextCleaner.__replacements = list()

    def __str__(self) -> str:
        """
        Prints readable format
        :return: str
        """
        print("__str__")
        # current_dir = re.split(r' |/|\\', getcwd())
        return f"file directory: {self.__fileDirectory}"

    def __repr__(self) -> str:
        """
        prints the official format
        :return: str(repr)
        """
        print("__repr__")
        return f"file directory: {str(self.__fileDirectory)}"

    def __del__(self) -> None:
        """
        The finalizer was preferred to the with statement :
        def __enter__(self):
            return self.fileHandle

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.fileHandle.close()
        """
        if isinstance(self.__fileHandle, codecs.StreamReaderWriter) and not self.__fileHandle.closed:
            self.__fileHandle.close()
            print("file closed")


if __name__ == '__main__':
    obj = PersianTextCleaner()
    obj.get_args()
    # obj.file_directory = "test.txt"
    obj.file_open()
    obj.persian_cleaner()
    del obj
