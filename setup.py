from setuptools import setup
from distutils.command.install import INSTALL_SCHEMES

for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

setup(
    name='MPC-HC-MultiStart',
    version='1.1.1',
    packages=['mpc'],
    data_files=[('', ['config.json', 'movies_template.json'])],
    include_package_data=True,
    license='MIT',
    author='Cazacu Sergiu',
    author_email='cazacu.serjio@gmail.com',
    description='A project that handles multiple synchronized instances of MPC-HC.'
)
