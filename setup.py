from distutils.core import setup

setup(
    name='ReExpose',
    version='0.1.0',
    packages=['reexpose',],
    license='Apache License v2.0',
    long_description=open('README.md').read(),
    install_requires=[
        'flask',
        'gevent',
        'requests',
        'pyyaml'
    ],
    extras_require={
        'dev': [
            'pylint'
        ]
    },
    scripts=['bin/reexpose']
)
