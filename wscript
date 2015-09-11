#! /usr/bin/env python
# encoding: utf-8

import os
from waflib.TaskGen import feature, after_method

APPNAME = 'kodo-simulations-python'
VERSION = '0.0.0'


def recurse_helper(ctx, name):
    if not ctx.has_dependency_path(name):
        ctx.fatal('Load a tool to find %s as system dependency' % name)
    else:
        p = ctx.dependency_path(name)
        ctx.recurse([p])


def options(opt):

    import waflib.extras.wurf_dependency_bundle as bundle
    import waflib.extras.wurf_dependency_resolve as resolve

    bundle.add_dependency(opt, resolve.ResolveGitMajorVersion(
        name='boost',
        git_repository='github.com/steinwurf/boost.git',
        major_version=1))

    bundle.add_dependency(opt, resolve.ResolveGitMajorVersion(
        name='cpuid',
        git_repository='github.com/steinwurf/cpuid.git',
        major_version=3))

    bundle.add_dependency(opt, resolve.ResolveGitMajorVersion(
        name='fifi',
        git_repository='github.com/steinwurf/fifi.git',
        major_version=20))

    bundle.add_dependency(opt, resolve.ResolveGitMajorVersion(
        name='kodo',
        git_repository='github.com/steinwurf/kodo.git',
        major_version=30))

    bundle.add_dependency(opt, resolve.ResolveGitMajorVersion(
        name='kodo-python',
        git_repository='github.com/steinwurf/kodo-python.git',
        major_version=8))

    bundle.add_dependency(opt, resolve.ResolveGitMajorVersion(
        name='platform',
        git_repository='github.com/steinwurf/platform.git',
        major_version=1))

    bundle.add_dependency(opt, resolve.ResolveGitMajorVersion(
        name='recycle',
        git_repository='github.com/steinwurf/recycle.git',
        major_version=1))

    bundle.add_dependency(opt, resolve.ResolveGitMajorVersion(
        name='meta',
        git_repository='github.com/steinwurf/meta.git',
        major_version=1))

    bundle.add_dependency(opt, resolve.ResolveGitMajorVersion(
        name='sak',
        git_repository='github.com/steinwurf/sak.git',
        major_version=14))

    bundle.add_dependency(opt, resolve.ResolveGitMajorVersion(
        name='waf-tools',
        git_repository='github.com/steinwurf/waf-tools.git',
        major_version=2))

    opt.load("wurf_configure_output")
    opt.load('wurf_dependency_bundle')
    opt.load('wurf_tools')
    opt.load('python')


def configure(conf):

    if conf.is_toplevel():

        conf.load('wurf_dependency_bundle')
        conf.load('wurf_tools')

        conf.load_external_tool('mkspec', 'wurf_cxx_mkspec_tool')
        conf.load_external_tool('runners', 'wurf_runner')
        conf.load_external_tool('install_path', 'wurf_install_path')
        conf.load_external_tool('project_gen', 'wurf_project_generator')

        recurse_helper(conf, 'boost')
        recurse_helper(conf, 'cpuid')
        recurse_helper(conf, 'fifi')
        recurse_helper(conf, 'kodo')
        recurse_helper(conf, 'platform')
        recurse_helper(conf, 'recycle')
        recurse_helper(conf, 'meta')
        recurse_helper(conf, 'sak')
        recurse_helper(conf, 'kodo-python')

    # Ensure that Python is configured properly
    if not conf.env['BUILD_PYTHON']:
        conf.fatal('Python was not configured properly')


def build(bld):

    if bld.is_toplevel():

        bld.load('wurf_dependency_bundle')

        recurse_helper(bld, 'boost')
        recurse_helper(bld, 'cpuid')
        recurse_helper(bld, 'fifi')
        recurse_helper(bld, 'kodo')
        recurse_helper(bld, 'platform')
        recurse_helper(bld, 'recycle')
        recurse_helper(bld, 'meta')
        recurse_helper(bld, 'sak')
        recurse_helper(bld, 'kodo-python')

    # Define a dummy task to force the compilation of the kodo-python library
    bld(features='cxx test',
        use=['kodo-python'])


@feature('test')
@after_method('apply_link')
def test_simulations(self):
    # Only execute the tests within the current project
    if self.path.is_child_of(self.bld.srcnode):
        if self.bld.has_tool_option('run_tests'):
            self.bld.add_post_fun(exec_test_simulations)


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
