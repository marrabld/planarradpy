from distutils.core import setup

setup(
    name='planarradpy',
    version='0.0.1',
    packages=['', 'gui', 'log', 'docs', 'tests', 'inputs', 'inputs.iop_files', 'inputs.sky_files', 'inputs.phase_files',
              'inputs.bottom_files', 'inputs.surface_files', 'outputs', 'scripts', 'libplanarradpy'],
    url='https://marrabld.github.io/planarradpy/',
    license='GPL',
    author='Dan Marrable',
    author_email='marrabld+planarradpy@gmail.com',
    description='Tool for batch running PlanarRad across multiple CPUs'
)
