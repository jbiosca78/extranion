#!/usr/bin/env python3
from setuptools import setup

setup(
	name='extranion',
	version='0.1',
	packages=['extranion'],
	install_requires=[
		'pygame',
		'pyyaml'
	],
	entry_points={
		"console_scripts": ["extranion = extranion.game:main"]
	}
)
