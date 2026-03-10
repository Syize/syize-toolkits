project(
    'syize',
    ['c', 'fortran'],
    version: '1.2.17',
    license: 'GPL-3.0-or-later',
    meson_version: '>=0.64.0',
    default_options: ['warning_level=2'],
)

add_languages('fortran')

py3 = import('python').find_installation(pure: false)

subdir('syize')
