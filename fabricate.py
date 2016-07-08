
from fabricate import *


def clean():
	run('echo', '"hello world"')
	run('rm', '-rf', 'WurstScript')
	run('rm', '-rf', 'stl.txt')


def build():
	run('./init.sh')


main()
