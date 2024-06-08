import datetime
import inspect

# Niveles de log
NONE = 0
DEBUG = 1
INFO = 2
WARN = 3
ERROR = 4
FATAL = 5
ALL = 6
__levelstr = [ "DEBUG", "INFO ", "WARN ", "ERROR", "FATAL", "#    " ]

def init(file=None, level=INFO):
	global __level, __file
	__file=file
	setlevel(level)

def setlevel(newlvl):
	global level
	if type(newlvl) == int:
		level=newlvl
	if type(newlvl) == str:
		level=NONE
		if newlvl=="DEBUG": level=DEBUG
		if newlvl=="INFO": level=INFO
		if newlvl=="WARN": level=WARN
		if newlvl=="ERROR": level=ERROR
		if newlvl=="FATAL": level=FATAL

def debug(msg):
	_write(DEBUG,msg)

def info(msg):
	_write(INFO,msg)

def warn(msg):
	_write(WARN,msg)

def error(msg):
	_write(ERROR,msg)

def fatal(msg):
	_write(FATAL,msg)

def inside(section=None):

	global __section, __deep

	if section is None:
		# get name of calling function
		finfo = inspect.currentframe().f_back
		section = finfo.f_code.co_name + "()"

	__section.append(section)
	_write(ALL,f"╭╸ {section}")
	__deep+=1

def outside():
	global __section, __deep
	section=__section.pop()
	__deep-=1
	_write(ALL,f"╰╸ {section}")

def outbreak(exception=None):
	global __section, __deep

	if exception is not None:
		error(f"Exception {type(exception).__name__}: {str(exception)}")

	section=__section.pop()
	__deep-=1
	_write(ALL, f"╰× {section}")

# Variables internas
__level=NONE
__file=None
__section=list()
__deep=0

def _write(lvl,msg):
	global __level,__leelstr,__deep,__file

	# Si el nivel de log definido es inferior, salimos
	if lvl>0 and lvl<__level: return

	# Si no hay fichero definido, salimos
	if not __file: return

	# fecha
	time=datetime.datetime.now()
	timestr=time.strftime('%Y-%m-%d %H:%M:%S.%f')[0:23]

	# separador de profundidad
	sepstr="│ "*__deep

	# Juntamos los datos en una línea
	line=f"{timestr} {__levelstr[lvl-1]} - {sepstr}{msg}\n"

	# Escribimos en el log
	f=open(str(__file), "a", encoding="utf8")
	f.write(line)
	f.close()
