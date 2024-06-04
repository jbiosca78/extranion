from setuptools import setup

setup(
	name='extranion',
	version='0.1',
	packages=['extranion'],
	install_requires=['pygame'],
	entry_points={
		#"console_scripts": ["extranion = extranion.__main__:main"]
		"console_scripts": ["extranion = extranion.game:run"]
	}
)
