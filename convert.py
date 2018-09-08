#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import codecs
import argparse
import collections


def parse_key(s_key):
    pattern = r" *{.*} *$"
    comp = re.compile(pattern)
    s_class_list = comp.findall(s_key)
    s_class = u""
    if len(s_class_list) == 0:
        return (s_key, u'-')
    else:
        s_word = s_key
        for c in s_class_list:
            s_word = s_word.replace(c, '')
            s_class += re.sub(r"} *$", "", re.sub(r"^ *{", "", c))
    return (s_word, s_class)


class DictEntry(object):
    class_order = {
            u'^-$': 0,
            u'^語源($|[- ・].*)': 1,
            u'^名($|[- ・].*)': 2,
            u'^代($|[- ・].*)': 3,
            u'^動($|[- ・].*)': 4,
            u'^自他動($|[- ・].*)': 5,
            u'^他動($|[- ・].*)': 6,
            u'^自動($|[- ・].*)': 7,
            u'^形($|[- ・].*)': 8,
            u'^副($|[- ・].*)': 9,
            u'^助動($|[- ・].*)': 10,
            u'^前($|[- ・].*)': 11,
            u'^助($|[- ・].*)': 12,
            u'^接続($|[- ・].*)': 13,
            u'^接頭($|[- ・].*)': 14,
            u'^接尾($|[- ・].*)': 15,
            u'^間($|[- ・].*)': 16,
            u'^句動($|[- ・].*)': 17,
            u'^句他動($|[- ・].*)': 18,
            u'^句自動($|[- ・].*)': 19,
            u'^略($|[- ・].*)': 20,
            u'^人名($|[- ・].*)': 21,
            u'^地名($|[- ・].*)': 22,
            u'^組織($|[- ・].*)': 23,
            }

    def __init__(self, s_word):
        self.word = s_word
        self._contents = []

    def add_content(self, s_class, s_value):
        s_class_order = None
        for class_regex in self.class_order:
            if re.match(class_regex, s_class):
                s_class_order = self.class_order[class_regex]
        if s_class_order is None:
            s_class_order = 100
        self._contents.append({"class": s_class, "value": s_value, "class_order": s_class_order})

    def _sort_contents(self):
        self._contents = sorted(self._contents, key=lambda x: x["class_order"])

    def to_unicode(self):
        ret_str = self.word
        ret_str += u'\t'
        self._sort_contents()
        for con in self._contents:
            if con["class"] != u"-":
                ret_str += u'【%s】' % con["class"]
            ret_str += con["value"] + u"\\n"
        ret_str += u"\n"
        return ret_str


def make_word_index(in_f):
    word_index = {}
    pos = 0
    for s in in_f:
        if s[0] == u'■':
            s = s[1:]
        s = s.replace(u'\\', u'\\\\')
        try:
            s_key, s_value = s.split(u' : ', 1)
        except Exception:
            continue
        s_word, s_class = parse_key(s_key)
        if s_word in word_index:
            word_index[s_word].append(pos)
        else:
            word_index[s_word] = [pos]
        pos = in_f.tell()
    word_index_order = collections.OrderedDict(sorted(word_index.items()))
    return word_index_order


def convert_file(sorted_file, output_file, encode):
    with codecs.open(sorted_file, 'r', encode) as in_f:
        word_index_order = make_word_index(in_f)
        with codecs.open(output_file, 'w', 'utf8') as out_f:
            # make dict data
            eiji_entry = None
            for word_key, word_pos_list in word_index_order.items():
                eiji_entry = DictEntry(word_key)
                for word_pos in word_pos_list:
                    in_f.seek(word_pos)
                    s = in_f.readline()
                    if s[0] == u'■':
                        s = s[1:]
                    s = s.replace(u'\\', u'\\\\')
                    s_key, s_value = s.split(u' : ', 1)
                    s_word, s_class = parse_key(s_key)
                    s_value = s_value.replace(u'\n', u'').replace(u'\r', u'').replace(u'■', u'\\n')
                    eiji_entry.add_content(s_class, s_value)
                out_f.write(eiji_entry.to_unicode())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input',
                        action='store',
                        required=True,
                        help='Input original dictionary file')
    parser.add_argument('-o', '--output',
                        action='store',
                        required=True,
                        help='Output converted tab format dictionary file')
    parser.add_argument('-e', '--encode',
                        action='store',
                        default='cp932',
                        help='Character encode of input file (default: "cp932")')
    args = parser.parse_args()
    convert_file(args.input, args.output, args.encode)


if __name__ == '__main__':
    main()
