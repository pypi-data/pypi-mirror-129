from distutils.core import setup
setup(
    name='Telpy',
    packages=['Telpy'],
    version='0.1.4',
    license='MIT',
    description='Telegram API Wrapper',
    author='FishballNoodles',
    author_email='joelkhorxw@gmail.com',
    url='https://github.com/TheReaper62/Telpy',
    download_url='https://github.com/TheReaper62/Telpy/archive/refs/tags/v0.1.tar.gz',
    keywords=['telegram', 'telegram api', 'telegram api wrapper',
              'telegram wrapper', 'telegram bot'],
    install_requires=[
        'requests',
        'regex'
    ],
    package_data = {
        # If any package contains *.py files, include them:
        '': ['*.py'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    long_description="Make Simple Telegram Bots. Open-source. Highly encouraged to user version 3.7 and above so that OrderedDict will work correctly. Expect flaws in order of processing Cases if using Python 3.6 (shouldn;t be too bif og a problem)"
)
