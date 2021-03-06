import commands
from bottle import *
from lxml import etree
import requests
import ws4py
from sys import argv
import datetime
import psycopg2, psycopg2.extras
import getpass
import os
import socket
from pylxd import Client
client = Client()

uptime = commands.getoutput("uptime -p")

@route('/')
def inicio():
	totalactivos = 0
	totalapagados = 0
	total = 0
	todos = client.containers.all()
	ramtotal = commands.getoutput("free -m | grep Mem: | cut -d' ' -f12")
	lenramtotal = len(ramtotal)
	ramused = commands.getoutput("cat /proc/meminfo | grep MemAvailable")
	ramused = ramused.lstrip("MemAvailable:")
	lenramused = len(ramused)
	ramused = ramused[:lenramused - 3]
	ramused = int(ramused)/1024
	ramused = int(ramtotal)-ramused
	limiteram = int(ramtotal)*70
	limiteram = int(limiteram)/100
	disktotal = commands.getoutput("df -h /dev/sda1 | tr -s ' ' | cut -d ' ' -f2 | tail -1")
	diskused = commands.getoutput("df -h /dev/sda1 | tr -s ' ' | cut -d ' ' -f3 | tail -1")
	lendisktotal = len(disktotal)
	disktotal = disktotal[:lendisktotal - 1]
	limitedisk = int(disktotal)*70
	limitedisk = int(limitedisk)/100
	modelprocessor = commands.getoutput("cat /proc/cpuinfo | grep 'model name' | cut -f2")
	modelprocessor = modelprocessor.lstrip(":")
	for i in todos:
		total = total + 1
		if i.status == "Running":
			totalactivos = totalactivos + 1
		else:
			totalapagados = totalapagados + 1
	return template('resultado.tpl',apagados=totalapagados,activos=totalactivos,ramtotal=ramtotal,ramused=ramused,uptime=uptime,modelprocessor=modelprocessor,limiteram=limiteram,disktotal=disktotal,diskused=diskused,limitedisk=limitedisk,total=total)

@route('/contenedores')
def contenedores():
	todos = client.containers.all()
	lista = []
	img = {}
	contenedor = {}
	lenlista = 0
	for i in todos:
		imagen = commands.getoutput('cat /var/lib/lxd/containers/' + i.name + '/metadata.yaml | grep description | cut -d"(" -f1 | cut -d":" -f2')
		ip = commands.getoutput("lxc list " + i.name + " -c '4' | tail -2 | head -1")
		ip = ip.lstrip("| ")
		ip = ip.rstrip(" |")
		lista.append({"nombre":i.name,"estado":i.status,"alive":i.created_at[0:19].replace("T"," "),"imagen":imagen,"arch":i.architecture,"ip":ip})
		lenlista = lenlista + 1
	return template('contenedores.tpl',lista=lista,lenlista=lenlista,tipo=type(lenlista),uptime=uptime)

@route('/snapshots')
def snapshots():
	todos = client.containers.all()
        lista = []
	lenlista = 0
        for i in todos:
                lista.append(i.name)
		lenlista = lenlista + 1
	return template('formversnapshot.tpl',uptime=uptime,lista=lista,lenlista=lenlista)

@route('/start/<name>',method='get')
def start(name):
	conttostart = client.containers.get(name)
	conttostart.start()
	redirect ('/contenedores')

@route('/stop/<name>',method='get')
def start(name):
        conttostop = client.containers.get(name)
        conttostop.stop()
        redirect ('/contenedores')

@route('/activar/<name>',method='get')
def start(name):
        conttoactivate = client.containers.get(name)
        conttostop.unfreeze()
        redirect ('/contenedores')

@route('/freeze/<name>',method='get')
def start(name):
        conttofreeze = client.containers.get(name)
        conttoactivate.freeze()
        redirect ('/contenedores')

@route('/restart/<name>',method='get',uptime=uptime)
def restart(name):
	conttorestart = client.containers.get(name)
	conttorestart.restart()
	redirect ('/contenedores')

@route('/rename/<name>',method='get')
def rename(name):
	return template('rename.tpl',nombre=name,uptime=uptime)

@route('/rename2/<name>',method='post')
def rename2(name):
	newname = request.forms.get('newname')
	conttorename = client.containers.get(name)
	conttorename.rename(newname,wait=True)
	redirect ('/contenedores')

@route('/renamesnap/<namesnap>/<namecont>',method='get')
def rename(namesnap,namecont):
        return template('renamesnap.tpl',nombresnap=namesnap,nombrecont=namecont,uptime=uptime)

@route('/renamesnap2/<namesnap>/<namecont>',method='post')
def rename2(namesnap,namecont):
        newname = request.forms.get('newname')
        cont = client.containers.get(namecont)
	snaptorename = cont.snapshots.get(namesnap)
        snaptorename.rename(newname,wait=True)
        redirect ('/listsnapshots/' + str(namecont))

@route('/eliminarsnap/<namesnap>/<namecont>',method='get')
def eliminarsnap(namesnap,namecont):
	cont = client.containers.get(namecont)
	snaptodelete = cont.snapshots.get(namesnap)
	snaptodelete.delete(wait=True)
	redirect ('/listsnapshots/' + str(namecont))

@route('/formcrearsnapshot/<name>')
def formcrearsnapshot(name):
	return template('formcrearsnapshot.tpl',name=name,uptime=uptime)

@route('/crearsnapshot/<name>',method='post')
def crearsnapshot(name):
	checkvalue = request.forms.get('check')
	snapname = request.forms.get('nombre')
	container = client.containers.get(name)
	if checkvalue == "on":
		snap = container.snapshots.create(snapname, stateful=True, wait=True)
	else:
		snap = container.snapshots.create(snapname, stateful=False, wait=True)
	redirect ('/listsnapshots/' + str(name))

@route('/intsnap',method='post')
def intsnap():
	name = request.forms.get('opcion')
	redirect ('/listsnapshots/' + str(name))

@route('/listsnapshots/<name>',method='get')
def listsnapshots(name):
	numsnap = commands.getoutput('lxc list | grep '+name+' | cut -d"|" -f7')
	snapshots = commands.getoutput('lxc info '+name+' | tail -n'+numsnap)
	listasnap = []
	lista = []
	linea = snapshots.split("\n")
	if numsnap.strip() == "0":
		sinsnap = "Este contenedor no tiene snapshots"
	else:
		for i in linea:
			listasnap = []
			campos = i.split("(")
			nombre = campos[0]
			creacion = campos[1]
			estado = campos[2]
			creacion = creacion.lstrip("taken at ")
			listasnap.append(nombre.strip())
			listasnap.append(creacion.rstrip(") "))
			listasnap.append(estado.rstrip(") "))
			lista.append(listasnap)
		return template('snapshots.tpl',lista=lista,uptime=uptime,name=name)
	return template('nosnapshots.tpl',sinsnap=sinsnap,uptime=uptime,name=name)

@route('/viewinfocontainer/<name>')
def viewinfocontainer(name):
	info = commands.getoutput("less /var/lib/lxd/containers/" + name + "/metadata.yaml")
	return template('viewinfocontainer.tpl',name=name,uptime=uptime,info=info)

@route('/crearcontenedor')
def crearcontenedor():
	return template('crearcontenedor.tpl',uptime=uptime)

@route('/crearcontenedor2/<dist>/<rel>')
def crearcontenedor2(dist,rel):
	distro = dist
	release = rel
	return template('crearcontenedor2.tpl',distro=distro,release=release,uptime=uptime)

@route('/crearcontenedor3/<distro>/<release>',method='post')
def crearcontenedor3(distro,release):
	name = request.forms.get('nombre')
	container = 'lxc launch images:'+str(distro)+'/'+str(release)+'/amd64 '+str(name)
	os.system(container)
	redirect ('/contenedores')

@route('/eliminarcontenedor/<nombre>',method='get')
def eliminarcontenedor(nombre):
	container = 'lxc delete ' + str(nombre) + ' --force'
	os.system(container)
	redirect ('/contenedores')

@route('/monitor')
def monitor():
	todos = client.containers.all()
        lista = []
        lenlista = 0
        for i in todos:
                lista.append(i.name)
                lenlista = lenlista + 1
	return template('monitor.tpl',uptime=uptime,lista=lista,lenlista=lenlista)

@route('/monitor2',method='post')
def monitor2():
	name = request.forms.get('opcion')
	ip = commands.getoutput('lxc list | grep ' + name + ' | cut -d"|" -f4 | cut -d" " -f2')
	num = [1,2,3,4,5,6,7,8,9]
	lisping = []
	lenlisping = 0
	if ip == "":
		lisping.append("Este contenedor no tiene ip por lo que no se puede realizar el ping hacia el")
		lenlisping = 1
	else:
		for i in num:
			ping = commands.getoutput('ping -c4 ' + str(ip) + '| head -' + str(i) + ' | tail -1')
			lisping.append(ping)
			lenlisping = lenlisping + 1
	return template('monitor2.tpl',uptime=uptime,name=name,lisping=lisping,ip=ip,lenlisping=lenlisping)

@route('/static/<filepath:path>')
def server_static(filepath):
   return static_file(filepath, root='static')

run(host='0.0.0.0',port='8081')
