#!/usr/bin/env python3

import glob
import jinja2
import os
import yaml

from jinja2 import Template
from distutils.dir_util import copy_tree

latex = jinja2.Environment(
    block_start_string='\\jblock{',
    block_end_string='}',
    variable_start_string='\\jvar{',
    variable_end_string='}',
    comment_start_string='\\#{',
    comment_end_string='}',
    line_statement_prefix='%%',
    line_comment_prefix='%#',
    trim_blocks=True,
    autoescape=False,
    loader=jinja2.FileSystemLoader(os.path.abspath('.'))
)


for config in glob.glob('src/config_*.yaml'):
    lang = config.split('_')[1].split('.yaml')[0]
    config_lang = None
    with open(config, 'r') as config_fd:
        try:
            config_lang = yaml.safe_load(config_fd)
        except yaml.YAMLError as e:
            print(e)

    if config_lang is None:
        print('unable to parse {}'.format(config))
        continue

    for template in glob.glob('src/template_*.tex'):
        name = template.split('_')[1].split('.tex')[0]
        latex.get_template(template).stream(config_lang).dump(
            '{}/templates/{}_{}.tex'.format(os.environ['BUILD_DIR'],  name, lang))

    if os.path.isdir('src/assets'):
        copy_tree('src/assets', '{}/templates'.format(os.environ['BUILD_DIR']))
