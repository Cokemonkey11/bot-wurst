
from invoke import task

@task
def clean(ctx):
	ctx.run('rm -rf WurstScript/')
	ctx.run('rm -rf stl.txt')

@task
def build(ctx):
	ctx.run('./init.sh')
