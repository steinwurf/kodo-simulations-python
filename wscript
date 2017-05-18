#! /usr/bin/env python
# encoding: utf-8

import os

APPNAME = 'kodo-simulations-python'
VERSION = '1.0.0'


def options(opt):

    opt.load('python')


def build(bld):

    # Define a dummy task to force the compilation of the kodo-python library
    bld(features='cxx test',
        use=['kodo-python'])

    if bld.is_toplevel():
        if bld.has_tool_option('run_tests'):
            bld.add_post_fun(exec_test_simulations)


def exec_test_simulations(bld):
    python = bld.env['PYTHON'][0]
    env = dict(os.environ)
    kodo_ext = bld.get_tgen_by_name('kodo-python').link_task.outputs[0]
    env['PYTHONPATH'] = kodo_ext.parent.abspath()

    # First, run the unit tests in the 'test' folder (the unittest module
    # automatically discovers all files matching the 'test*.py' pattern)
    if os.path.exists('test'):
        cwd = 'test'
        bld.cmd_and_log('"{0}" -m unittest discover\n'.format(python),
                        cwd=cwd, env=env)

    # Then run the examples in the 'examples' folder
    if os.path.exists('examples'):
        cwd = 'examples'
        for f in sorted(os.listdir('examples')):
            if f.endswith('.py'):
                bld.cmd_and_log(
                    '"{0}" {1}\n'.format(python, f), cwd=cwd, env=env)
