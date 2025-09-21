# -*- coding: utf-8 -*-

import json
import math
import os
import platform
import random
import re
import sys
import time

from collections import OrderedDict
from io import StringIO
import requests

import numpy as np
from scipy import optimize

from ELATE import elastic

__author__ = "Romain Gaillac and François-Xavier Coudert"
__version__ = "2025.08.26"
__license__ = "MIT"


def removeHTMLTags(s):
    """Remove HTML tags, notably for use as page title"""
    return re.sub('<[^<]+?>', '', s)


def finishWebPage(outbuffer):
    """ Write the footer and finish the page """

    print('<div id="footer" class="content">')
    print('Code version: ' + __version__ + ' (running on Python ' + platform.python_version() + ')<br/>')
    print('<script type="text/javascript">var endTime = %.12g;' % time.perf_counter())
    print('document.write("Execution time: " + (endTime-startTime).toFixed(3) + " seconds<br/>");')
    print('if(typeof isOrtho !== \'undefined\') document.write("Specific (faster) code for orthorhombic case was used.");')
    print('</script></div>')
    print('</div>')
    print('</body></html>')
    return outbuffer.getvalue()


def writeHeader(outbuffer, title="Elastic Tensor Analysis"):
    """ Write the header of the HTML page """

    print("""
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
    <html>
    <head>
        <title>%s</title>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <link rel="stylesheet" type="text/css" href="/default.css" />
        <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/jsxgraph@1.8.0/distrib/jsxgraph.css" />
        <script src="https://cdn.jsdelivr.net/npm/jsxgraph@1.8.0/distrib/jsxgraphcore.js"></script>
        <script src="https://cdn.plot.ly/plotly-2.30.0.min.js" charset="utf-8"></script>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
        </head>
    """ % (title))


# printTitle writes the introduction of Elate
def printTitle(outbuffer, title="Elastic Tensor Analysis"):
    writeHeader(outbuffer, title)
    print("""
        <body>

        <div class="content">
        <h1><a href="/elate">ELATE: Elastic tensor analysis</a></h1>

        <p>Welcome to ELATE, the online tool for analysis of elastic tensors, developed by <b>Romain Gaillac</b> and <b><a
        href="https://coudert.name/fx.html" target="_blank" rel="noreferrer">François-Xavier Coudert</a></b> at <a
        href="https://coudert.name/" target="_blank" rel="noreferrer">CNRS / Chimie ParisTech</a>. <br/> If you use the
        software in published results (paper, conference, etc.), please cite the <a
        href="https://doi.org/10.1088/0953-8984/28/27/275201" target="_blank" rel="noreferrer">corresponding paper</a>
        (<em>J. Phys. Condens. Matter</em>, 2016, 28, 275201) and give the website URL.</p>

        <p>ELATE is <a href="https://github.com/fxcoudert/elate" target="_blank" rel="noreferrer">open source software</a>.
        Any queries or comments are welcome at
    <script type="text/javascript">
    //<![CDATA[
    var c_="";for(var o5=0;o5<411;o5++)c_+=String.fromCharCode(("s%oz65j5>oJ.~~vs!Kt00}.~|}{\\"$s~%}!s0Kv#\\"wv<s!~tjjK{j5wo#zH}<j5s!z~qo6s~=u=i:00ikk>97a6!#|w<u!t{}vQ!o}Qsr?6F8G9:B8D9>@?7>a9!#|w<u!t{}vQ!o}QsrB67Dj59}qr$!s8#vq{wsw~;!oAA\\"wA#qsj5v!<~sozsq=6=A:u00970i0<ikk>a9!#|w<u!t{}vQ!o}QsrA69DDD>:E\\'7@<7s!z~qo6sjj==8:uN070j59j5jj.0|}}{\\"$}s#$0Kv#\\"wv<s!Ktj5jjj5jjL0\\'t14>O>>DBqI$}sr#!14>>>>BDqIwvw{sO~;!o\\"ws#vq14>>B>ID!t=JLo<j5s!z~qo6sO=u=0:705<!s~zoqs6=6<76<7=u:02@2?07<\\"$p\\"#!6?77".charCodeAt(o5)-(14)+0x3f)%(2*6+83)+64-32);document.write(eval(c_))
    //]]>
    </script>
        </p>
    """)


# 3D plot functions
################################################################################################

def write3DPlotData(dataX, dataY, dataZ, dataR, n, opacity=1.0):

    showcont = "true"
    if (opacity != 1.0):
        showcont = "false"
    if (n == 1):
        js = OrderedDict([
            ("x", dataX),
            ("y", dataY),
            ("z", dataZ),
            ("text", dataR),
            ("showscale", "false"),
            ("colorscale", "[[\'0\',\'rgb(22,136,51)\'],[\'0.125\',\'rgb(61,153,85)\'],[\'0.25\',\'rgb(121,178,136)\'],[\'0.375\',\'rgb(181,204,187)\'],[\'0.5\',\'rgb(195,230,200)\'],[\'0.625\',\'rgb(181,204,187)\'],[\'0.75\',\'rgb(121,178,136)\'],[\'0.875\',\'rgb(61,153,85)\'],[\'1\',\'rgb(22,136,51)\']]"),
            ("zsmooth", "'fast'"),
            ("type", "'surface'"),
            ("hoverinfo", "'text'"),
            ("opacity", opacity),
            ("contours", "{x :{ show:"+showcont+", color: 'rgb(192,192,192)'},y :{ show:"+showcont+", color: 'rgb(192,192,192)'},z :{ show:"+showcont+", color: 'rgb(192,192,192)'}}")
        ])

    if (n == 2):
        js = OrderedDict([
            ("x", dataX),
            ("y", dataY),
            ("z", dataZ),
            ("text", dataR),
            ("showscale", "false"),
            ("colorscale", "[[\'0\',\'rgb(180,4,38)\'],[\'0.125\',\'rgb(222,96,77)\'],[\'0.25\',\'rgb(244,154,123)\'],[\'0.375\',\'rgb(245,196,173)\'],[\'0.5\',\'rgb(246,216,201)\'],[\'0.625\',\'rgb(245,196,173)\'],[\'0.75\',\'rgb(244,154,123)\'],[\'0.875\',\'rgb(222,96,77)\'],[\'1\',\'rgb(180,4,38)\']]"),
            ("zsmooth", "'fast'"),
            ("type", "'surface'"),
            ("hoverinfo", "'text'"),
            ("opacity", opacity),
            ("contours", "{x :{ show:"+showcont+", color: 'rgb(192,192,192)'},y :{ show:"+showcont+", color: 'rgb(192,192,192)'},z :{ show:"+showcont+", color: 'rgb(192,192,192)'}}")
        ])

    if (n == 3):
        js = OrderedDict([
            ("x", dataX),
            ("y", dataY),
            ("z", dataZ),
            ("text", dataR),
            ("showscale", "false"),
            ("colorscale", "[[\'0\',\'rgb(59,76,192)\'],[\'0.125\',\'rgb(98,130,234)\'],[\'0.25\',\'rgb(141,176,254)\'],[\'0.375\',\'rgb(184,208,249)\'],[\'0.5\',\'rgb(207,223,250)\'],[\'0.625\',\'rgb(184,208,249)\'],[\'0.75\',\'rgb(141,176,254)\'],[\'0.875\',\'rgb(98,130,234)\'],[\'1\',\'rgb(59,76,192)\']]"),
            ("zsmooth", "'fast'"),
            ("type", "'surface'"),
            ("hoverinfo", "'text'"),
            ("opacity", opacity),
            ("contours", "{x :{ show:"+showcont+", color: 'rgb(192,192,192)'},y :{ show:"+showcont+", color: 'rgb(192,192,192)'},z :{ show:"+showcont+", color: 'rgb(192,192,192)'}}")
        ])

    print(json.dumps(js, indent=3).replace('\"', '') + ";")


def make3DPlot(func, legend='', width=600, height=600, npoints=200):

    str1 = legend.split("\'")[0]
    str2 = legend.split("\'")[1]

    u = np.linspace(0, np.pi, npoints)
    v = np.linspace(0, 2*np.pi, 2*npoints)
    r = np.zeros(len(u)*len(v))

    dataX = [[0.0 for i in range(len(v))] for j in range(len(u))]
    dataY = [[0.0 for i in range(len(v))] for j in range(len(u))]
    dataZ = [[0.0 for i in range(len(v))] for j in range(len(u))]
    dataR = [["0.0" for i in range(len(v))] for j in range(len(u))]

    count = 0
    for cu in range(len(u)):
        for cv in range(len(v)):
            r_tmp = func(u[cu], v[cv])
            z = r_tmp * np.cos(u[cu])
            x = r_tmp * np.sin(u[cu]) * np.cos(v[cv])
            y = r_tmp * np.sin(u[cu]) * np.sin(v[cv])
            dataX[cu][cv] = x
            dataY[cu][cv] = y
            dataZ[cu][cv] = z
            dataR[cu][cv] = "'E = "+str(float(int(10*r_tmp))/10.0)+" GPa, "+"\u03B8 = "+str(float(int(10*u[cu]*180/np.pi))/10.0)+"\u00B0, "+"\u03c6 = "+str(float(int(10*v[cv]*180/np.pi))/10.0)+"\u00B0'"
            count = count+1

    i = random.randint(0, 100000)
    print('<div class="plot3D">')
    print('<div id="box%d" style="width: %dpx; height: %dpx; display:block;"></div>' % (i, width, height))
    print('</div>')
    print('<script type="text/javascript">')
    print("var trace =")
    write3DPlotData(dataX, dataY, dataZ, dataR, 1)
    print("var data = [trace]")
    print("var layout =")
    layout = {"title": "\'"+str1+"\\"+"\'"+str2+"\'", "width": "650", "height": "700", "autosize": "false", "autorange": "true", "margin": "{l: 65, r: 50, b: 65, t: 90}"}
    print(json.dumps(layout, indent=3).replace('\\\\', '\\').replace('\"', '') + ";")
    print("Plotly.newPlot('box%d',data,layout);" % (i))
    print('</script>')


def make3DPlotPosNeg(func, legend='', width=600, height=600, npoints=200):

  u = np.linspace(0, np.pi, npoints)
  v = np.linspace(0, 2*np.pi, 2*npoints)

  dataX1 = [[0.0 for i in range(len(v))] for j in range(len(u))]
  dataY1 = [[0.0 for i in range(len(v))] for j in range(len(u))]
  dataZ1 = [[0.0 for i in range(len(v))] for j in range(len(u))]
  dataR1 = [["0.0" for i in range(len(v))] for j in range(len(u))]

  count = 0
  for cu in range(len(u)):
    for cv in range(len(v)):
      r_tmp = max(0, func(u[cu], v[cv]))
      z = r_tmp * np.cos(u[cu])
      x = r_tmp * np.sin(u[cu]) * np.cos(v[cv])
      y = r_tmp * np.sin(u[cu]) * np.sin(v[cv])
      dataX1[cu][cv] = x
      dataY1[cu][cv] = y
      dataZ1[cu][cv] = z
      dataR1[cu][cv] = "'"+"\u03B2 = "+str(float(int(10*r_tmp))/10.0)+" TPa'"+"+'-1'.sup()+"+"', \u03B8 = "+str(float(int(10*u[cu]*180/np.pi))/10.0)+"\u00B0, "+"\u03c6 = "+str(float(int(10*v[cv]*180/np.pi))/10.0)+"\u00B0'"
      count = count+1

  dataX2 = [[0.0 for i in range(len(v))] for j in range(len(u))]
  dataY2 = [[0.0 for i in range(len(v))] for j in range(len(u))]
  dataZ2 = [[0.0 for i in range(len(v))] for j in range(len(u))]
  dataR2 = [["0.0" for i in range(len(v))] for j in range(len(u))]

  count = 0
  for cu in range(len(u)):
    for cv in range(len(v)):
      r_tmp = max(0, -func(u[cu], v[cv]))
      z = r_tmp * np.cos(u[cu])
      x = r_tmp * np.sin(u[cu]) * np.cos(v[cv])
      y = r_tmp * np.sin(u[cu]) * np.sin(v[cv])
      dataX2[cu][cv] = x
      dataY2[cu][cv] = y
      dataZ2[cu][cv] = z
      dataR2[cu][cv] = "'"+"\u03B2 = -"+str(float(int(10*r_tmp))/10.0)+" TPa'"+"+'-1'.sup()+"+"', \u03B8 = "+str(float(int(10*u[cu]*180/np.pi))/10.0)+"\u00B0, "+"\u03c6 = "+str(float(int(10*v[cv]*180/np.pi))/10.0)+"\u00B0'"
      count = count+1

  i = random.randint(0, 100000)
  print('<div class="plot3D">')
  print('<div id="box%d" style="width: %dpx; height: %dpx; display:block;"></div>' % (i, width, height))
  print('</div>')
  print('<script type="text/javascript">')
  print("var trace1 =")
  write3DPlotData(dataX1, dataY1, dataZ1, dataR1, 1)
  print("var trace2 =")
  write3DPlotData(dataX2, dataY2, dataZ2, dataR2, 2)
  print("var data = [trace1, trace2]")
  print("var layout =")
  layout = {"title": "\'"+legend+"\'", "width": "650", "height": "700", "autosize": "false", "autorange": "true", "margin": "{l: 65, r: 50, b: 65, t: 90}"}
  print(json.dumps(layout, indent=3).replace('\\\\', '\\').replace('\"', '') + ";")
  print("Plotly.newPlot('box%d',data,layout);" % (i))
  print('</script>')


def make3DPlot2(func, legend='', width=600, height=600, npoints=50):

  u = np.linspace(0, np.pi, npoints)
  v = np.linspace(0, np.pi, npoints)
  w = [v[i]+np.pi for i in range(1,len(v))]
  v = np.append(v, w)

  dataX1 = [[0.0 for i in range(len(v))] for j in range(len(u))]
  dataY1 = [[0.0 for i in range(len(v))] for j in range(len(u))]
  dataZ1 = [[0.0 for i in range(len(v))] for j in range(len(u))]
  dataR1 = [["0.0" for i in range(len(v))] for j in range(len(u))]

  dataX2 = [[0.0 for i in range(len(v))] for j in range(len(u))]
  dataY2 = [[0.0 for i in range(len(v))] for j in range(len(u))]
  dataZ2 = [[0.0 for i in range(len(v))] for j in range(len(u))]
  dataR2 = [["0.0" for i in range(len(v))] for j in range(len(u))]

  count = 0
  r = [0.0,0.0,np.pi/2.0,np.pi/2.0]
  for cu in range(len(u)):
    for cv in range(len(v)):

      r = func(u[cu],v[cv],r[2],r[3])
      z = np.cos(u[cu])
      x = np.sin(u[cu]) * np.cos(v[cv])
      y = np.sin(u[cu]) * np.sin(v[cv])

      r1_tmp = r[0]
      z1 = r1_tmp * z
      x1 = r1_tmp * x
      y1 = r1_tmp * y
      dataX1[cu][cv] = x1
      dataY1[cu][cv] = y1
      dataZ1[cu][cv] = z1
      dataR1[cu][cv] = "'"+"G'"+"+'min'.sub()+"+"' = "+str(float(int(10*r1_tmp))/10.0)+"GPa, "+"\u03B8 = "+str(float(int(10*u[cu]*180/np.pi))/10.0)+"\u00B0, "+"\u03c6 = "+str(float(int(10*v[cv]*180/np.pi))/10.0)+"\u00B0'"

      r2_tmp = r[1]
      z2 = r2_tmp * z
      x2 = r2_tmp * x
      y2 = r2_tmp * y
      dataX2[cu][cv] = x2
      dataY2[cu][cv] = y2
      dataZ2[cu][cv] = z2
      dataR2[cu][cv] = "'"+"G'"+"+'max'.sub()+"+"' = "+str(float(int(10*r1_tmp))/10.0)+"GPa, "+"\u03B8 = "+str(float(int(10*u[cu]*180/np.pi))/10.0)+"\u00B0, "+"\u03c6 = "+str(float(int(10*v[cv]*180/np.pi))/10.0)+"\u00B0'"
      count = count+1

  i = random.randint(0, 100000)
  print('<div class="plot3D">')
  print('<div id="box%d" style="width: %dpx; height: %dpx; display:block;"></div>' % (i, width, height))
  print('</div>')
  print('<script type="text/javascript">')
  print("var trace1 =")
  write3DPlotData(dataX1, dataY1, dataZ1, dataR1, 1)
  print("var trace2 =")
  write3DPlotData(dataX2, dataY2, dataZ2, dataR2, 3, 0.5)
  print("var data = [trace1, trace2]")
  print("var layout =")
  layout = {"title": "\'"+legend+"\'", "width":"650", "height":"700" , "autosize":"false", "autorange":"true", "margin": "{l: 65, r: 50, b: 65, t: 90}"}
  print(json.dumps(layout, indent=3).replace('\\\\','\\').replace('\"','') + ";")
  print("Plotly.newPlot('box%d',data,layout);" % (i))
  print('</script>')


def make3DPlot3(func, legend='', width=600, height=600, npoints=50):

  str1 = legend.split("\'")[0]
  str2 = legend.split("\'")[1]

  u = np.linspace(0, np.pi, npoints)
  v = np.linspace(0, np.pi, npoints)
  w = [v[i]+np.pi for i in range(1,len(v))]
  v = np.append(v, w)

  dataX1 = [[0.0 for i in range(len(v))] for j in range(len(u))]
  dataY1 = [[0.0 for i in range(len(v))] for j in range(len(u))]
  dataZ1 = [[0.0 for i in range(len(v))] for j in range(len(u))]
  dataR1 = [["0.0" for i in range(len(v))] for j in range(len(u))]

  dataX2 = [[0.0 for i in range(len(v))] for j in range(len(u))]
  dataY2 = [[0.0 for i in range(len(v))] for j in range(len(u))]
  dataZ2 = [[0.0 for i in range(len(v))] for j in range(len(u))]
  dataR2 = [["0.0" for i in range(len(v))] for j in range(len(u))]

  dataX3 = [[0.0 for i in range(len(v))] for j in range(len(u))]
  dataY3 = [[0.0 for i in range(len(v))] for j in range(len(u))]
  dataZ3 = [[0.0 for i in range(len(v))] for j in range(len(u))]
  dataR3 = [["0.0" for i in range(len(v))] for j in range(len(u))]

  count = 0
  r = [0.0, 0.0, 0.0, np.pi/2.0, np.pi/2.0]
  ruv = [[r for i in range(len(u))] for j in range(len(v))]
  for cu in range(len(u)):
    for cv in range(len(v)):
       ruv[cv][cu] = func(u[cu],v[cv],r[3],r[4])

  for cu in range(len(u)):
    for cv in range(len(v)):

      z = np.cos(u[cu])
      x = np.sin(u[cu]) * np.cos(v[cv])
      y = np.sin(u[cu]) * np.sin(v[cv])

      r = ruv[cv][cu]
      r1_tmp = r[0]
      dataX1[cu][cv] = r1_tmp * x
      dataY1[cu][cv] = r1_tmp * y
      dataZ1[cu][cv] = r1_tmp * z
      dataR1[cu][cv] = "'"+"\u03BD'"+"+'min'.sub()+"+"' = "+str(float(int(100*r1_tmp))/100.0)+", "+"\u03B8 = "+str(float(int(100*u[cu]*180/np.pi))/100.0)+"\u00B0, "+"\u03c6 = "+str(float(int(100*v[cv]*180/np.pi))/100.0)+"\u00B0'"

      r2_tmp = r[1]
      dataX2[cu][cv] = r2_tmp * x
      dataY2[cu][cv] = r2_tmp * y
      dataZ2[cu][cv] = r2_tmp * z
      dataR2[cu][cv] = "'"+"\u03BD'"+"+'min'.sub()+"+"' = "+str(float(int(100*r2_tmp))/100.0)+", "+"\u03B8 = "+str(float(int(100*u[cu]*180/np.pi))/100.0)+"\u00B0, "+"\u03c6 = "+str(float(int(100*v[cv]*180/np.pi))/100.0)+"\u00B0'"

      r3_tmp = r[2]
      dataX3[cu][cv] = r3_tmp * x
      dataY3[cu][cv] = r3_tmp * y
      dataZ3[cu][cv] = r3_tmp * z
      dataR3[cu][cv] = "'"+"\u03BD'"+"+'max'.sub()+"+"' = "+str(float(int(100*r3_tmp))/100.0)+", "+"\u03B8 = "+str(float(int(100*u[cu]*180/np.pi))/100.0)+"\u00B0, "+"\u03c6 = "+str(float(int(100*v[cv]*180/np.pi))/100.0)+"\u00B0'"
      count = count+1

  i = random.randint(0, 100000)
  print('<div class="plot3D">')
  print('<div id="box%d" style="width: %dpx; height: %dpx; display:block;"></div>' % (i, width, height))
  print('</div>')
  print('<script type="text/javascript">')
  print("var trace1 =")
  write3DPlotData(dataX1, dataY1, dataZ1, dataR1, 2, 0.5)
  print("var trace2 =")
  write3DPlotData(dataX2, dataY2, dataZ2, dataR2, 1, 1.0)
  print("var trace3 =")
  write3DPlotData(dataX3, dataY3, dataZ3, dataR3, 3, 0.5)
  print("var data = [trace1, trace2, trace3]")
  print("var layout =")
  layout = {"title": "\'"+str1+"\\"+"\'"+str2+"\'", "width":"650", "height":"700" , "autosize":"false", "autorange":"true", "margin": "{l: 65, r: 50, b: 65, t: 90}"}
  print(json.dumps(layout, indent=3).replace('\\\\','\\').replace('\"','') + ";")
  print("Plotly.newPlot('box%d',data,layout);" % (i))
  print('</script>')




# Polar plot functions
################################################################################################

def writePolarPlotData(dataX, dataY, suffix):
    """Write data for a polar plot, taking care of the center of inversion"""

    print("var dataX" + suffix + " = [")
    print((len(dataX) * "%.5f,") % tuple(dataX))
    print(((len(dataX)-1) * "%.5f," + "%.5f") % tuple(-dataX))
    print("];")
    print("var dataY" + suffix + " = [")
    print((len(dataX) * "%.5f,") % tuple(dataY))
    print(((len(dataX)-1) * "%.5f," + "%.5f") % tuple(-dataY))
    print("];")



def makePolarPlot(func, maxrad, legend='', p='xy', width=300, height=300, npoints=90, color='#009010', linewidth=2):

    i = random.randint(0, 100000)
    print('<div class="plot">')
    print('<div id="box%d" class="jxgbox" style="width: %dpx; height: %dpx; display:inline-block;"></div>' % (i, width, height))
    print('<br />%s</div>' % legend)
    print('<script type="text/javascript">')
    print('var b = JXG.JSXGraph.initBoard(\'box%d\', {boundingbox: [-%f, %f, %f, -%f], axis:true, showcopyright: 0});'
          % (i, maxrad, maxrad, maxrad, maxrad))

    u = np.linspace(0, np.pi, npoints)
    r = list(map(func, u))
    if (p == "xy"):
        x = r * np.cos(u)
        y = r * np.sin(u)
    else:
        y = r * np.cos(u)
        x = r * np.sin(u)

    writePolarPlotData (x, y, "")
    print("b.create('curve', [dataX,dataY], {strokeColor:'%s', strokeWidth: %d});" % (color, linewidth))
    print('</script>')

def makePolarPlotPosNeg(func, maxrad, legend='', p='xy', width=300, height=300, npoints=90, linewidth=2):
    i = random.randint(0, 100000)
    print('<div class="plot">')
    print('<div id="box%d" class="jxgbox" style="width: %dpx; height: %dpx; display:inline-block;"></div>' % (i, width, height))
    print('<br />%s</div>' % legend)
    print('<script type="text/javascript">')
    print('var b = JXG.JSXGraph.initBoard(\'box%d\', {boundingbox: [-%f, %f, %f, -%f], axis:true, showcopyright: 0});'
          % (i, maxrad, maxrad, maxrad, maxrad))

    u = np.linspace(0, np.pi, npoints)
    r = list(map(lambda x: max(0, func(x)), u))
    if (p == "xy"):
        x1 = r * np.cos(u)
        y1 = r * np.sin(u)
    else:
        y1 = r * np.cos(u)
        x1 = r * np.sin(u)
    r = list(map(lambda x: max(0, -func(x)), u))
    if (p == "xy"):
        x2 = r * np.cos(u)
        y2 = r * np.sin(u)
    else:
        y2 = r * np.cos(u)
        x2 = r * np.sin(u)

    writePolarPlotData (x1, y1, "1")
    writePolarPlotData (x2, y2, "2")
    print("b.create('curve', [dataX1,dataY1], {strokeColor:'green', strokeWidth: %d});" % (linewidth))
    print("b.create('curve', [dataX2,dataY2], {strokeColor:'red', strokeWidth: %d});" % (linewidth))
    print('</script>')

def makePolarPlot2(func, maxrad, legend='', p='xy', width=300, height=300, npoints=61, linewidth=2):
    i = random.randint(0, 100000)
    print('<div class="plot">')
    print('<div id="box%d" class="jxgbox" style="width: %dpx; height: %dpx; display:inline-block;"></div>' % (i, width, height))
    print('<br />%s</div>' % legend)
    print('<script type="text/javascript">')
    print('var b = JXG.JSXGraph.initBoard(\'box%d\', {boundingbox: [-%f, %f, %f, -%f], axis:true, showcopyright: 0});'
          % (i, maxrad, maxrad, maxrad, maxrad))

    u = np.linspace(0, np.pi, npoints)
    r = list(map(func, u))

    if (p == "xy"):
        x1 = np.array([ ir[0] * np.cos(iu) for ir, iu in zip(r,u) ])
        y1 = np.array([ ir[0] * np.sin(iu) for ir, iu in zip(r,u) ])
        x2 = np.array([ ir[1] * np.cos(iu) for ir, iu in zip(r,u) ])
        y2 = np.array([ ir[1] * np.sin(iu) for ir, iu in zip(r,u) ])
    else:
        y1 = np.array([ ir[0] * np.cos(iu) for ir, iu in zip(r,u) ])
        x1 = np.array([ ir[0] * np.sin(iu) for ir, iu in zip(r,u) ])
        y2 = np.array([ ir[1] * np.cos(iu) for ir, iu in zip(r,u) ])
        x2 = np.array([ ir[1] * np.sin(iu) for ir, iu in zip(r,u) ])

    writePolarPlotData (x1, y1, "1")
    writePolarPlotData (x2, y2, "2")
    print("b.create('curve', [dataX1,dataY1], {strokeColor:'green', strokeWidth: %d});" % (linewidth))
    print("b.create('curve', [dataX2,dataY2], {strokeColor:'blue', strokeWidth: %d});" % (linewidth))
    print('</script>')

def makePolarPlot3(func, maxrad, legend='', p='xy', width=300, height=300, npoints=61, linewidth=2):
    i = random.randint(0, 100000)
    print('<div class="plot">')
    print('<div id="box%d" class="jxgbox" style="width: %dpx; height: %dpx; display:inline-block;"></div>' % (i, width, height))
    print('<br />%s</div>' % legend)
    print('<script type="text/javascript">')
    print('var b = JXG.JSXGraph.initBoard(\'box%d\', {boundingbox: [-%f, %f, %f, -%f], axis:true, showcopyright: 0});'
          % (i, maxrad, maxrad, maxrad, maxrad))

    u = np.linspace(0, np.pi, npoints)
    r = list(map(func, u))

    if (p == "xy"):
        x1 = np.array([ ir[0] * np.cos(iu) for ir, iu in zip(r,u) ])
        y1 = np.array([ ir[0] * np.sin(iu) for ir, iu in zip(r,u) ])
        x2 = np.array([ ir[1] * np.cos(iu) for ir, iu in zip(r,u) ])
        y2 = np.array([ ir[1] * np.sin(iu) for ir, iu in zip(r,u) ])
        x3 = np.array([ ir[2] * np.cos(iu) for ir, iu in zip(r,u) ])
        y3 = np.array([ ir[2] * np.sin(iu) for ir, iu in zip(r,u) ])
    else:
        y1 = np.array([ ir[0] * np.cos(iu) for ir, iu in zip(r,u) ])
        x1 = np.array([ ir[0] * np.sin(iu) for ir, iu in zip(r,u) ])
        y2 = np.array([ ir[1] * np.cos(iu) for ir, iu in zip(r,u) ])
        x2 = np.array([ ir[1] * np.sin(iu) for ir, iu in zip(r,u) ])
        y3 = np.array([ ir[2] * np.cos(iu) for ir, iu in zip(r,u) ])
        x3 = np.array([ ir[2] * np.sin(iu) for ir, iu in zip(r,u) ])

    writePolarPlotData (x1, y1, "1")
    writePolarPlotData (x2, y2, "2")
    writePolarPlotData (x3, y3, "3")
    print("b.create('curve', [dataX1,dataY1], {strokeColor:'red', strokeWidth: %d});" % (linewidth))
    print("b.create('curve', [dataX2,dataY2], {strokeColor:'green', strokeWidth: %d});" % (linewidth))
    print("b.create('curve', [dataX3,dataY3], {strokeColor:'blue', strokeWidth: %d});" % (linewidth))
    print('</script>')


################################################################################################


# Materials Project URL
urlBase = 'https://api.materialsproject.org'


def queryMaterials(query, mapiKey):
    """Return a list of material IDs for a given query string"""

    # If the query is a material ID, return it
    if query[0:3] == "mp-":
        return 1, [query]

    # We accept either a chemical system or a formula
    if '-' in query:
        query = 'chemsys=' + query
    else:
        query = 'formula=' + query

    try:
        r = requests.get(f'{urlBase}/materials/summary/?{query}&deprecated=false&_fields=has_props,material_id,formula_pretty',
                         headers={'X-API-KEY': mapiKey, 'accept': 'application/json'}, timeout=4)
        resp = r.json()
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 0, []

    if 'meta' not in resp or resp['meta']['total_doc'] == 0:
        return 0, []

    # Return the total number of hits, and the first page of results
    return resp['meta']['total_doc'], resp['data']


def queryElasticity(mat, mapiKey):
    """Return elastic properties for a given material ID, using so-called 'new API'"""

    try:
        r = requests.get(f'{urlBase}/materials/elasticity/?material_ids={mat}&&_fields=elastic_tensor,material_id,formula_pretty',
                         headers={'X-API-KEY': mapiKey, 'accept': 'application/json'}, timeout=4)
        resp = r.json()
    except Exception as e:
        print(str(e), file=sys.stderr)
        return None


    if resp["meta"]["total_doc"] == 0:
        return None
    if resp["meta"]["total_doc"] > 1:
        raise(Exception("Multiple results returned"))

    return resp["data"][0]



def ELATE_MaterialsProject(query, mapiKey):
  """Call ELATE with a query from the Materials Project"""

  # If we were directly given a material ID, or there is a simple match
  nres, materials = queryMaterials(query, mapiKey)
  if len(materials) == 1:
    r = queryElasticity(query, mapiKey)

    if r and 'elastic_tensor' in r:
      tensor = r["elastic_tensor"]["ieee_format"]
      return ELATE(tensor, '%s (Materials Project id <a href="%s%s" target="_blank">%s</a>)' % (r["formula_pretty"], "https://www.materialsproject.org/materials/", r["material_id"], r["material_id"]))

  # Otherwise, run the MP query, list the matches and let the user choose
  sys.stdout = outbuffer = StringIO()
  printTitle(outbuffer, "ELATE: Elastic tensor analysis")
  print('<h2>Query from the Materials Project database</h2>')

  # Either there was no match, or a single match with no elastic data
  if len(materials) <= 1:
    print("""<p>
            Your query for <tt style="background-color: #e0e0e0;">%s</tt> from the <a href="https://materialsproject.org"
            target="_blank" rel="noreferrer">Materials Project</a> database has returned a total of zero result.
            Or is it zero results? In any case, we are very sorry.</p>

            <p>If you wish, you can try another query here:
            <form name="elastic" action="/elate/mp" method="get">
              <input type="text" name="query" style="font-family:sans-serif; width: 20em;">
              <input type="submit" style="font-size: 100%%; color: #b02020;" value="Submit query">
            </form>
            or go back to our <a href="/elate">main page</a>.
            </p>""" % (query))
    return finishWebPage(outbuffer)


  print("""<p>Your query for <tt style="background-color: #e0e0e0;">%s</tt> from the <a
           href="https://materialsproject.org" target="_blank" rel="noreferrer">Materials Project</a> database
           has returned %d results.""" % (query, nres))

  if len(materials) < nres:
    print(f'Below is a table of the {len(materials)} first matches.')

  print("<table><tr><th>Identifier</th><th>Formula</th><th>Elastic data</th></tr>")
  for mat in materials:
    mid = mat['material_id']
    print('<tr><td><a href="https://www.materialsproject.org/materials/%s" target="_blank" rel="noreferrer">%s</a></td><td>%s</td>' % (mid, mid, mat["formula_pretty"]))
    if mat['has_props'].get('elasticity'):
      print('<td>Elastic data available, <a href="/elate/mp?%s" target="_blank" rel="noreferrer">perform analysis</a></td></tr>' % (mid))
    else:
      print('<td>No elastic data available</td></tr>')
  print("</table>")

  return finishWebPage(outbuffer)


def ELATE(matrix, sysname):
    """
    ELATE is the main function, interprets the matrix for 2D or 3D material,
    and dispatches the work to specialized functions.
    """

    # Redirect output to out string buffer
    sys.stdout = outbuffer = StringIO()

    # Start timing
    print('<script type="text/javascript">var startTime = %.12g</script>' % time.perf_counter())
    sysname_sanitized = removeHTMLTags(sysname).strip()
    printTitle(outbuffer, "Elastic analysis of " + sysname_sanitized)

    try:
        # First try to interpret as a 3D matrix
        elas = elastic.Elastic(matrix)
    except TypeError as e:
        try:
            elas = elastic.Elastic2D(matrix)
        except ValueError as e:
            print('<div class="error">Invalid stiffness matrix: ')
            print(e.args[0])
            if matrix:
                print('<pre>' + str(matrix) + '</pre>')
            print('</div>')
            print('<input action="action" type="button" value="Go back" onclick="window.history.go(-1); return false;" />')
            return finishWebPage(outbuffer)
    except ValueError as e:
        print('<div class="error">Invalid stiffness matrix: ')
        print(e.args[0])
        if matrix:
            print('<pre>' + str(matrix) + '</pre>')
        print('</div>')
        print('<input action="action" type="button" value="Go back" onclick="window.history.go(-1); return false;" />')
        return finishWebPage(outbuffer)

    if elas.is2D():
        return ELATE_main_2D(elas, matrix, sysname, outbuffer)
    else:
        return ELATE_main_3D(elas, matrix, sysname, outbuffer)


def ELATE_main_2D(elas, matrix, sysname, outbuffer):
    """Performs the calculations and plots properties for 2D materials"""

    print('<h2>Summary of the properties (2D material)</h2>')

    displayname = " of " + sysname if len(sysname) else ""
    print('<h3>Input: stiffness matrix (coefficients in N/m)%s</h3>' % (displayname))
    print('<pre>')
    for i in range(3):
        print(("   " + 3 * "%7.5g  ") % tuple(elas.CVoigt[i]))
    print('</pre>')

    print('''<h3>Eigenvalues of the stiffness matrix</h3>
    <table><tr>
    <th>&lambda;<sub>1</sub></th>
    <th>&lambda;<sub>2</sub></th>
    <th>&lambda;<sub>3</sub></th>
    </tr><tr>''')
    eigenval = elas.eigenvalues()
    print((3 * '<td>%7.5g N/m</td>') % tuple(eigenval))
    print('</tr></table>')

    if eigenval[0] <= 0:
        print('<div class="error">Stiffness matrix is not definite positive, crystal is mechanically unstable<br/>')
        print('No further analysis will be performed.</div>')
        return finishWebPage(outbuffer)

    def findMin(func):
        # We prefer the brute() function to minimize_scalar(), which only does local optimization
        # But our functions are one-dimensional, which brute() does not accept, so make a wrapper
        res = optimize.brute(lambda x: func(x[0]), ((0, np.pi),), Ns=100, full_output=True, finish=optimize.fmin)
        return (res[0][0], res[1])

    def findMax(func):
        # We prefer the brute() function to minimize_scalar(), which only does local optimization
        # But our functions are one-dimensional, which brute() does not accept, so make a wrapper
        res = optimize.brute(lambda x: -func(x[0]), ((0, np.pi),), Ns=100, full_output=True, finish=optimize.fmin)
        return (res[0][0], -res[1])

    minE = findMin(elas.Young)
    maxE = findMax(elas.Young)
    minG = findMin(elas.shear)
    maxG = findMax(elas.shear)
    minNu = findMin(elas.Poisson)
    maxNu = findMax(elas.Poisson)

    print("""<h3>Variations of the elastic moduli</h3>
                <table>
                <tr><td></td><th colspan="2">Young's modulus</th>
                <th colspan="2">Shear modulus</th>
                <th colspan="2">Poisson's ratio</th></tr>
                <tr><td></td><th><em>E</em><sub>min</sub></th><th><em>E</em><sub>max</sub></th>
                <th><em>G</em><sub>min</sub></th><th><em>G</em><sub>max</sub></th>
                <th>&nu;<sub>min</sub></th><th>&nu;<sub>max</sub></th><th></th></tr>""")

    print(('<tr><td>Value</td><td>%8.5g N/m</td><td>%8.5g N/m</td>'
           + '<td>%8.5g N/m</td><td>%8.5g N/m</td>'
           + '<td>%.5g</td><td>%.5g</td><td>Value</td></tr>') % (minE[1], maxE[1], minG[1], maxG[1], minNu[1], maxNu[1]))

    anisE = '%8.4g' % (maxE[1] / minE[1])
    anisG = '%8.4g' % (maxG[1] / minG[1])
    anisNu = ('%8.4f' % (maxNu[1] / minNu[1])) if minNu[1] * maxNu[1] > 0 else "&infin;"
    print(('<tr><td>Anisotropy</td>' + 3 * '<td colspan="2">%s</td>'
           + '<td>Anisotropy</td></tr>') % (anisE, anisG, anisNu))

    print('<tr><td>Angle</td>')
    print('<td>%.2f°</td>' % (minE[0] * 180 / np.pi))
    print('<td>%.2f°</td>' % (maxE[0] * 180 / np.pi))
    print('<td>%.2f°</td>' % (minG[0] * 180 / np.pi))
    print('<td>%.2f°</td>' % (maxG[0] * 180 / np.pi))
    print('<td>%.2f°</td>' % (minNu[0] * 180 / np.pi))
    print('<td>%.2f°</td>' % (maxNu[0] * 180 / np.pi))
    print('<td>Axis</td></tr></table>')

    print("<h2>Spatial dependence of Young's modulus</h2>")
    m = 1.2 * maxE[1]
    makePolarPlot(elas.Young, m, "Young's modulus", width=500, height=500, npoints=180)

    print("<h2>Spatial dependence of shear modulus</h2>")
    m = 1.2 * maxG[1]
    makePolarPlot(elas.shear, m, "Shear modulus", width=500, height=500, npoints=180)

    print("<h2>Spatial dependence of Poisson's ratio</h2>")
    m = 1.2 * max(abs(maxNu[1]), abs(minNu[1]))
    makePolarPlotPosNeg(elas.Poisson, m, "Poisson's ratio", width=500, height=500, npoints=180)

    return finishWebPage(outbuffer)


def ELATE_main_3D(elas, matrix, sysname, outbuffer):
    """Performs the calculations and plots properties for 3D materials"""

    if elas.isOrthorhombic():
        elas = elastic.ElasticOrtho(elas)
        print('<script type="text/javascript">var isOrtho = 1;</script>')

    print('<h2>Summary of the properties (3D material)</h2>')

    print('<h3>Input: stiffness matrix (coefficients in GPa) of %s</h3>' % (sysname))
    print('<pre>')
    for i in range(6):
        print(("   " + 6 * "%7.5g  ") % tuple(elas.CVoigt[i]))
    print('</pre>')

    avg = elas.averages()
    print('<h3>Average properties</h3>')

    print("<table><tr><th>Averaging scheme</th><th>Bulk modulus</th><th>Young's modulus</th><th>Shear modulus</th><th>Poisson's ratio</th></tr>")
    print(('<tr><td>Voigt</td><td><em>K</em><sub>V</sub> = %7.5g GPa</td><td><em>E</em><sub>V</sub> = %7.5g GPa</td>'
           + '<td><em>G</em><sub>V</sub> = %7.5g GPa</td><td><em>&nu;</em><sub>V</sub> = %.5g</td></tr>') % tuple(avg[0]))
    print(('<tr><td>Reuss</td><td><em>K</em><sub>R</sub> = %7.5g GPa</td><td><em>E</em><sub>R</sub> = %7.5g GPa</td>'
           + '<td><em>G</em><sub>R</sub> = %7.5g GPa</td><td><em>&nu;</em><sub>R</sub> = %.5g</td></tr>') % tuple(avg[1]))
    print(('<tr><td>Hill</td><td><em>K</em><sub>H</sub> = %7.5g GPa</td><td><em>E</em><sub>H</sub> = %7.5g GPa</td>'
           + '<td><em>G</em><sub>H</sub> = %7.5g GPa</td><td><em>&nu;</em><sub>H</sub> = %.5g</td></tr>') % tuple(avg[2]))
    print('</table>')

    print('''<h3>Eigenvalues of the stiffness matrix</h3>
    <table><tr>
    <th>&lambda;<sub>1</sub></th>
    <th>&lambda;<sub>2</sub></th>
    <th>&lambda;<sub>3</sub></th>
    <th>&lambda;<sub>4</sub></th>
    <th>&lambda;<sub>5</sub></th>
    <th>&lambda;<sub>6</sub></th>
    </tr><tr>''')
    eigenval = elas.eigenvalues()
    print((6 * '<td>%7.5g GPa</td>') % tuple(eigenval))
    print('</tr></table>')

    if eigenval[0] <= 0:
        print('<div class="error">Stiffness matrix is not definite positive, crystal is mechanically unstable<br/>')
        print('No further analysis will be performed.</div>')
        return finishWebPage(outbuffer)

    minE = elastic.minimize(elas.Young, 2)
    maxE = elastic.maximize(elas.Young, 2)
    minLC = elastic.minimize(elas.LC, 2)
    maxLC = elastic.maximize(elas.LC, 2)
    minG = elastic.minimize(elas.shear, 3)
    maxG = elastic.maximize(elas.shear, 3)
    minNu = elastic.minimize(elas.Poisson, 3)
    maxNu = elastic.maximize(elas.Poisson, 3)

    print("""<h3>Variations of the elastic moduli</h3>
                <table>
                <tr><td></td><th colspan="2">Young\'s modulus</th><th colspan="2">Linear compressibility</th>
                <th colspan="2">Shear modulus</th><th colspan="2">Poisson\'s ratio</th><th></th></tr>
                <td></td><th><em>E</em><sub>min</sub></th><th><em>E</em><sub>max</sub></th>
                <th>&beta;<sub>min</sub></th><th>&beta;<sub>max</sub></th><th><em>G</em><sub>min</sub></th><th><em>G</em><sub>max</sub></th>
                <th>&nu;<sub>min</sub></th><th>&nu;<sub>max</sub></th><th></th></tr>""")

    print(('<tr><td>Value</td><td>%8.5g GPa</td><td>%8.5g GPa</td>'
           + '<td>%8.5g TPa<sup>&ndash;1</sup></td><td>%8.5g TPa<sup>&ndash;1</sup></td>'
           + '<td>%8.5g GPa</td><td>%8.5g GPa</td>'
           + '<td>%.5g</td><td>%.5g</td><td>Value</td></tr>') % (minE[1], maxE[1], minLC[1], maxLC[1], minG[1], maxG[1], minNu[1], maxNu[1]))

    anisE = '%8.4g' % (maxE[1] / minE[1])
    anisLC = ('%8.4f' % (maxLC[1] / minLC[1])) if minLC[1] > 0 else "&infin;"
    anisG = '%8.4g' % (maxG[1] / minG[1])
    anisNu = ('%8.4f' % (maxNu[1] / minNu[1])) if minNu[1] * maxNu[1] > 0 else "&infin;"
    print(('<tr><td>Anisotropy</td>' + 4 * '<td colspan="2">%s</td>' + '<td>Anisotropy</td></tr>') % (anisE, anisLC, anisG, anisNu))

    print('<tr><td>Axis</td>')
    print('<td>%.4f<br />%.4f<br />%.4f</td>' % tuple(elastic.dirVec(*minE[0])))
    print('<td>%.4f<br />%.4f<br />%.4f</td>' % tuple(elastic.dirVec(*maxE[0])))
    print('<td>%.4f<br />%.4f<br />%.4f</td>' % tuple(elastic.dirVec(*minLC[0])))
    print('<td>%.4f<br />%.4f<br />%.4f</td>' % tuple(elastic.dirVec(*maxLC[0])))
    print('<td>%.4f<br />%.4f<br />%.4f</td>' % tuple(elastic.dirVec1(*minG[0])))
    print('<td>%.4f<br />%.4f<br />%.4f</td>' % tuple(elastic.dirVec1(*maxG[0])))
    print('<td>%.4f<br />%.4f<br />%.4f</td>' % tuple(elastic.dirVec1(*minNu[0])))
    print('<td>%.4f<br />%.4f<br />%.4f</td>' % tuple(elastic.dirVec1(*maxNu[0])))
    print('<td>Axis</td></tr>')

    print('<tr><td></td><td></td><td></td><td></td><td></td>')
    print('<td>%.4f<br />%.4f<br />%.4f</td>' % tuple(elastic.dirVec2(*minG[0])))
    print('<td>%.4f<br />%.4f<br />%.4f</td>' % tuple(elastic.dirVec2(*maxG[0])))
    print('<td>%.4f<br />%.4f<br />%.4f</td>' % tuple(elastic.dirVec2(*minNu[0])))
    print('<td>%.4f<br />%.4f<br />%.4f</td>' % tuple(elastic.dirVec2(*maxNu[0])))
    print('<td>Second axis</td></tr></table>')

    print("<h2>Spatial dependence of Young's modulus</h2>")
    print("""<form id="elastic" action="/wait3D" method="post" target="_blank">
                <textarea name="matrix" style="display: none;">%s</textarea>
                <textarea name="sysname" style="display: none;">%s</textarea>
                <textarea name="job" style="display: none;">%s</textarea>
                <br /><input type="submit" style="font-size: 100%%; color: #b02020;" value="Visualize in 3D">
            </form>""" % (matrix, sysname, "young"))
    m = 1.2 * maxE[1]
    makePolarPlot(lambda x: elas.Young([np.pi / 2, x]), m, "Young's modulus in (xy) plane", "xy")
    makePolarPlot(lambda x: elas.Young([x, 0]), m, "Young's modulus in (xz) plane", "xz")
    makePolarPlot(lambda x: elas.Young([x, np.pi / 2]), m, "Young's modulus in (yz) plane", "yz")

    print("<h2>Spatial dependence of linear compressibility</h2>")
    print("""<form id="elastic" action="/wait3D" method="post" target="_blank">
                <textarea name="matrix" style="display: none;">%s</textarea>
                <textarea name="sysname" style="display: none;">%s</textarea>
                <textarea name="job" style="display: none;">%s</textarea>
                <br /><input type="submit" style="font-size: 100%%; color: #b02020;" value="Visualize in 3D">
            </form>""" % (matrix, sysname, "lc"))
    m = 1.2 * max(maxLC[1], abs(minLC[1]))
    makePolarPlotPosNeg(lambda x: elas.LC([np.pi / 2, x]), m, "linear compressibility in (xy) plane", "xy")
    makePolarPlotPosNeg(lambda x: elas.LC([x, 0]), m, "linear compressibility in (xz) plane", "xz")
    makePolarPlotPosNeg(lambda x: elas.LC([x, np.pi / 2]), m, "linear compressibility in (yz) plane", "yz")

    print("<h2>Spatial dependence of shear modulus</h2>")
    print("""<form id="elastic" action="/wait3D" method="post" target="_blank">
                <textarea name="matrix" style="display: none;">%s</textarea>
                <textarea name="sysname" style="display: none;">%s</textarea>
                <textarea name="job" style="display: none;">%s</textarea>
                <br /><input type="submit" style="font-size: 100%%; color: #b02020;" value="Visualize in 3D">
            </form>""" % (matrix, sysname, "shear"))
    m = 1.2 * maxG[1]
    makePolarPlot2(lambda x: elas.shear2D([np.pi / 2, x]), m, "Shear modulus in (xy) plane", "xy")
    makePolarPlot2(lambda x: elas.shear2D([x, 0]), m, "Shear modulus in (xz) plane", "xz")
    makePolarPlot2(lambda x: elas.shear2D([x, np.pi / 2]), m, "Shear modulus in (yz) plane", "yz")

    print("<h2>Spatial dependence of Poisson's ratio</h2>")
    print("""<form id="elastic" action="/wait3D" method="post" target="_blank">
                <textarea name="matrix" style="display: none;">%s</textarea>
                <textarea name="sysname" style="display: none;">%s</textarea>
                <textarea name="job" style="display: none;">%s</textarea>
                <br /><input type="submit" style="font-size: 100%%; color: #b02020;" value="Visualize in 3D">
            </form>""" % (matrix, sysname, "poisson"))
    m = 1.2 * max(abs(maxNu[1]), abs(minNu[1]))
    makePolarPlot3(lambda x: elas.Poisson2D([np.pi / 2, x]), m, "Poisson's ratio in (xy) plane", "xy")
    makePolarPlot3(lambda x: elas.Poisson2D([x, 0]), m, "Poisson's ratio in (xz) plane", "xz")
    makePolarPlot3(lambda x: elas.Poisson2D([x, np.pi / 2]), m, "Poisson's ratio in (yz) plane", "yz")

    print("</div>")
    return finishWebPage(outbuffer)


def wait3D(matrix, sysname, job):
    """Display a waiting page while we calculate a 3D plot"""

    sys.stdout = outbuffer = StringIO()
    writeHeader(outbuffer, "Young 3D for " + removeHTMLTags(sysname))

    print("""
    <div class="content">
    <img src="/loading.gif" alt="[loading]" />
    <p>Please wait while your 3D graph is loading… (it can take from 15 seconds up to a minute)</p>
    """)

    # Pass arguments
    print("""
    <form id="elastic" action="/plot3D" method="post" style="display: none;">
        <textarea name="matrix">%s</textarea>
        <textarea name="sysname">%s</textarea>
        <textarea name="job">%s</textarea>
        <input type="submit" value="">
    </form>""" % (matrix, sysname, job))

    # Reload immediately
    print("""
    <script type="text/javascript">
        window.onload = function(){
        setTimeout(function () {
            document.getElementById("elastic").submit();
                }, 100);
            };
    </script>""")

    return finishWebPage(outbuffer)


def plot3D(matrix, sysname, job):
    """Display a 3D plot"""

    # Dispatch to the specific function depending on type
    functions = {'young': YOUNG3D, 'lc': LC3D, 'shear': SHEAR3D, 'poisson': POISSON3D}
    return functions[job](matrix, sysname)


# ELATE : basic usage of the tool, only 2D plots
# YOUNG3D : visualize Young's modulus in 3D
# LC3D : visualize Linear compressiblity in 3D
# SHEAR3D : visualize Shear modulus in 3D
# POISSON3D : visualize Poisson ratio in 3D
################################################################################################


def YOUNG3D(matrix, sysname):

    sys.stdout = outbuffer = StringIO()
    writeHeader(outbuffer, "Young 3D for " + removeHTMLTags(sysname))

    # Start timing
    print('<script type="text/javascript">var startTime = %.12g</script>' % time.perf_counter())
    print('<div class="content">')

    print("<h1> 3D Visualization of Young's modulus </h1>")
    elas = elastic.Elastic(matrix)
    if elas.isOrthorhombic():
        elas = elastic.ElasticOrtho(elas)
        print('<script type="text/javascript">var isOrtho = 1;</script>')

    make3DPlot(lambda x, y: elas.Young_2(x, y), "Young's modulus")

    print('<h3>Input: stiffness matrix (coefficients in GPa) of %s</h3>' % (sysname))
    print('<pre>')
    for i in range(6):
        print(("   " + 6 * "%7.5g  ") % tuple(elas.CVoigt[i]))
    print('</pre></div>')
    return finishWebPage(outbuffer)


def LC3D(matrix, sysname):

    sys.stdout = outbuffer = StringIO()
    writeHeader(outbuffer, "LC 3D for " + removeHTMLTags(sysname))

    # Start timing
    print('<script type="text/javascript">var startTime = %.12g</script>' % time.perf_counter())
    print('<div class="content">')

    print("<h1> 3D Visualization of Linear compressiblity </h1>")
    elas = elastic.Elastic(matrix)
    if elas.isOrthorhombic():
        elas = elastic.ElasticOrtho(elas)
        print('<script type="text/javascript">var isOrtho = 1;</script>')

    make3DPlotPosNeg(lambda x, y: elas.LC_2(x, y), "Linear compressiblity")

    print('<h3>Input: stiffness matrix (coefficients in GPa) of %s</h3>' % (sysname))
    print('<pre>')
    for i in range(6):
        print(("   " + 6 * "%7.5g  ") % tuple(elas.CVoigt[i]))
    print('</pre></div>')
    return finishWebPage(outbuffer)


def SHEAR3D(matrix, sysname):

    sys.stdout = outbuffer = StringIO()
    writeHeader(outbuffer, "Shear 3D for " + removeHTMLTags(sysname))

    # Start timing
    print('<script type="text/javascript">var startTime = %.12g</script>' % time.perf_counter())
    print('<div class="content">')

    print("<h1> 3D Visualization of Shear modulus </h1>")
    elas = elastic.Elastic(matrix)
    if elas.isOrthorhombic():
        elas = elastic.ElasticOrtho(elas)
        print('<script type="text/javascript">var isOrtho = 1;</script>')

    make3DPlot2(lambda x, y, g1, g2: elas.shear3D(x, y, g1, g2), "Shear modulus")

    print('<h3>Input: stiffness matrix (coefficients in GPa) of %s</h3>' % (sysname))
    print('<pre>')
    for i in range(6):
        print(("   " + 6 * "%7.5g  ") % tuple(elas.CVoigt[i]))
    print('</pre></div>')
    return finishWebPage(outbuffer)


def POISSON3D(matrix, sysname):

    sys.stdout = outbuffer = StringIO()
    writeHeader(outbuffer, "Poisson 3D for " + removeHTMLTags(sysname))

    # Start timing
    print('<script type="text/javascript">var startTime = %.12g</script>' % time.perf_counter())
    print('<div class="content">')

    print("<h1> 3D Visualization of Poisson's ratio </h1>")
    elas = elastic.Elastic(matrix)
    if elas.isOrthorhombic():
        elas = elastic.ElasticOrtho(elas)
        print('<script type="text/javascript">var isOrtho = 1;</script>')

    make3DPlot3(lambda x, y, g1, g2: elas.Poisson3D(x, y, g1, g2), "Poisson's ratio")

    print('<h3>Input: stiffness matrix (coefficients in GPa) of %s</h3>' % (sysname))
    print('<pre>')
    for i in range(6):
        print(("   " + 6 * "%7.5g  ") % tuple(elas.CVoigt[i]))
    print('</pre></div>')
    return finishWebPage(outbuffer)
