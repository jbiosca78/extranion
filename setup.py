#!/usr/bin/env python3

from setuptools import setup

setup(
	name='nemesisreloaded',
	version='1',
	packages=['nemesisreloaded'],
	install_requires=['pygame'],
	entry_points={
		"console_scripts": [
			"nemesisreloaded = nemesisreloaded.__main__:main"
		]
	}

)
