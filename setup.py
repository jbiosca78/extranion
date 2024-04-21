#!/usr/bin/env python3

from setuptools import setup

setup(
	name='Nemesis Reloaded',
	version='1',
	packages=['nemesis_reloaded'],
	install_requires=['pygame'],
	entry_points={
		"console_scripts": [
			"nemesis_reloaded = nemesis_reloaded.__main__:main"
			]
	}

)
