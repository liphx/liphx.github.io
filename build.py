#!/usr/bin/env python3

import os
import time
import json
import string

docs_dir = os.path.abspath("./docs")

def execute_cmd(cmd):
    print("execute:", cmd)
    os.system(cmd)

def mkdir(dir):
    if not os.path.exists(dir):
        execute_cmd("mkdir -p {}".format(dir))

def md2html(md_file, html_file):
    cmd = 'pandoc -f markdown -t html -c /css/common.css -s --quiet'
    mkdir(os.path.dirname(html_file))
    execute_cmd('{} {} -o {}'.format(cmd, md_file, html_file))

def get_file_modify_time(path):
    if not os.path.exists(path):
        return None
    return time.localtime(os.path.getmtime(path))

def list_files(path, end):
    ret = []
    for file in os.listdir(path):
        p = os.path.join(path, file)
        if os.path.isfile(p) and p.endswith(end):
            ret.append(p)
        elif os.path.isdir(p):
            if os.path.abspath(p) != docs_dir:
                ret += list_files(p, end)
    return ret

def gen_html():
    md_files = list_files('.', '.md')
    html_files = []
    for md_file in md_files:
        html_file = os.path.join(docs_dir, md_file[0:-2] + 'html')
        t1 = get_file_modify_time(md_file)
        t2 = get_file_modify_time(html_file)
        if t2 == None or t1 > t2: # html file doesn't exist or md file is newer than html file
            print('update {} ...'.format(html_file), 'modify_time is ' + time.strftime('%F %T', t1))
            md2html(md_file, html_file)
            print('done.')

def make_docs():
    mkdir(docs_dir)
    docs_files = []
    suffix = ['.html', '.js', '.css', '.jpg', '.ico', 'CNAME', '.pdf']
    for i in suffix:
        files = list_files('.', i)
        docs_files += files

    for file in docs_files:
        new_file = os.path.join(docs_dir, file)
        t1 = get_file_modify_time(file)
        t2 = get_file_modify_time(new_file)
        if t2 == None or t1 > t2:
            mkdir(os.path.dirname(new_file))
            execute_cmd('cp {} {}'.format(file, new_file))

def clean_docs():
    execute_cmd('rm -rf docs/*')

if __name__ == '__main__':
    make_docs()
    gen_html()
