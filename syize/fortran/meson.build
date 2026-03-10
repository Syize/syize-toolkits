# Install Python sources
py3.install_sources(
    [
        '__init__.py',
        'formatter.py',
    ],
    subdir: 'syize/fortran'
)

# Variables to build extensions
netcdf_dep = dependency('netcdf-fortran', required : true)

# include path
fortran_include = include_directories('/usr/include', 'palm/src')

# PALM source files
src_dir = meson.current_source_dir() / 'palm/src'

palm_sources = files(
    join_paths(src_dir, 'kinds.f90'),
    join_paths(src_dir, 'control_parameters.f90'),
    join_paths(src_dir, 'indices.f90'),
    join_paths(src_dir, 'pegrid.f90'),
    join_paths(src_dir, 'arrays_3d.f90'),
    join_paths(src_dir, 'basic_constants_and_equations_mod.f90'),
    join_paths(src_dir, 'boundary_settings_mod.f90'),
    join_paths(src_dir, 'exchange_horiz_mod.f90'),
    join_paths(src_dir, 'general_utilities.f90'),
    join_paths(src_dir, 'grid_variables.f90'),
    join_paths(src_dir, 'nc_input.f90'),
    join_paths(src_dir, 'topo.f90'),
)

# wrapper file
wrapper_source = files(join_paths(src_dir, 'palm.f90'))

# build PALM source to static library
palm_lib = static_library(
    'palmcore',
    palm_sources,
    include_directories: fortran_include,
    dependencies: netcdf_dep,
    install: false
)

# generate wrapper using f2py
palm_pyf = custom_target(
    'palm_pyf',
    input: wrapper_source,
    output: 'palm.pyf',
    command: [
        py3, '-m', 'numpy.f2py',
        '@INPUT@',
        '-m', 'palm',
        '-h', meson.current_build_dir() / 'palm.pyf'
    ]
)

palm_f2py_wrapper = custom_target(
    'palmcore',
    input: [palm_pyf, wrapper_source],
    output: ['palmmodule.c', 'palm-f2pywrappers2.f90'],
    command: [
        py3, '-m', 'numpy.f2py',
        '@INPUT@',
        '-m', 'palm',
        '--lower', '--build-dir', meson.current_build_dir()
    ]
)

# dependencies needed to build python extension.
py_dep = py3.dependency()

include_dir_numpy = run_command(
    py3,
    ['-c', 'import os; os.chdir(".."); import numpy; print(numpy.get_include())'],
    check : true
).stdout().strip()

include_dir_f2py = run_command(
    py3,
    ['-c', 'import os; os.chdir(".."); import numpy.f2py; print(numpy.f2py.get_include())'],
    check : true
).stdout().strip()

include_numpy = include_directories(include_dir_numpy, include_dir_f2py)

# build python extension
py3.extension_module(
    'palm',
    [
        wrapper_source,
        palm_f2py_wrapper,
        include_dir_f2py / 'fortranobject.c'
    ],
    include_directories: include_numpy,
    dependencies: py_dep,
    link_with: palm_lib,    # link palm static library
    install: true,
    install_dir: join_paths(py3.get_install_dir(), 'syize/fortran/palm')
)

# Install palm submodule Python interface files
py3.install_sources(
    [
        'palm/py/__init__.py',
    ],
    subdir: 'syize/fortran/palm',
)
