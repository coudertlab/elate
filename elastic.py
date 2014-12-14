# -*- coding: utf-8 -*-

import sys, math, random
from cStringIO import StringIO
import IPython.utils.timing
import numpy as np
import numpy.linalg as la
from scipy import optimize


def finishWebPage(outbuffer):
  print '<div id="footer">'
  print '<script type="text/javascript">var endTime = %g;' % IPython.utils.timing.clock()
  print 'document.write("Execution time: " + (endTime-startTime).toFixed(3) + " seconds<br/>");' 
  print 'if(isOrtho) document.write("Specific (faster) code for orthorhombic case was used.");'
  print '</script></div>'

  print """
  <script type="text/javascript">
  document.getElementById("wait").hidden = true;
  </script>
  </body></html>"""

  return outbuffer.getvalue()


def writePolarPlotData(dataX, dataY, suffix):
  """Write data for a polar plot, taking care of the center of inversion"""
  print "var dataX" + suffix + " = ["
  print (len(dataX) * "%.5f,") % tuple(dataX)
  print ((len(dataX)-1) * "%.5f," + "%.5f") % tuple(-dataX)
  print "];"
  print "var dataY" + suffix + " = ["
  print (len(dataX) * "%.5f,") % tuple(dataY)
  print ((len(dataX)-1) * "%.5f," + "%.5f") % tuple(-dataY)
  print "];"


def makePolarPlot(func, maxrad, legend = '', width = 300, height = 300, npoints = 90, color = '#009010', linewidth = 2):

  i = random.randint(0, 100000)
  print '<div class="plot">'
  print '<div id="box%d" class="jxgbox" style="width: %dpx; height: %dpx; display:inline-block;"></div>' % (i, width, height)
  print '<br />%s</div>' % legend
  print '<script type="text/javascript">'
  print ('var b = JXG.JSXGraph.initBoard(\'box%d\', {boundingbox: [-%f, %f, %f, -%f], axis:true, showcopyright: 0});'
         % (i, maxrad, maxrad, maxrad, maxrad))

  u = np.linspace(0, np.pi, npoints)
  r = map(func, u)
  x = r * np.cos(u)
  y = r * np.sin(u)

  writePolarPlotData (x, y, "")
  print "b.create('curve', [dataX,dataY], {strokeColor:'%s', strokeWidth: %d});" % (color, linewidth)
  print '</script>'

def makePolarPlotPosNeg(func, maxrad, legend = '', width = 300, height = 300, npoints = 90, linewidth = 2):
  i = random.randint(0, 100000)
  print '<div class="plot">'
  print '<div id="box%d" class="jxgbox" style="width: %dpx; height: %dpx; display:inline-block;"></div>' % (i, width, height)
  print '<br />%s</div>' % legend
  print '<script type="text/javascript">'
  print ('var b = JXG.JSXGraph.initBoard(\'box%d\', {boundingbox: [-%f, %f, %f, -%f], axis:true, showcopyright: 0});'
         % (i, maxrad, maxrad, maxrad, maxrad))

  u = np.linspace(0, np.pi, npoints)
  r = map(lambda x: max(0, func(x)), u)
  x1 = r * np.cos(u)
  y1 = r * np.sin(u)
  r = map(lambda x: max(0, -func(x)), u)
  x2 = r * np.cos(u)
  y2 = r * np.sin(u)

  writePolarPlotData (x1, y1, "1")
  writePolarPlotData (x2, y2, "2")
  print "b.create('curve', [dataX1,dataY1], {strokeColor:'green', strokeWidth: %d});" % (linewidth)
  print "b.create('curve', [dataX2,dataY2], {strokeColor:'red', strokeWidth: %d});" % (linewidth)
  print '</script>'

def makePolarPlot2(func, maxrad, legend = '', width = 300, height = 300, npoints = 61, linewidth = 2):
  i = random.randint(0, 100000)
  print '<div class="plot">'
  print '<div id="box%d" class="jxgbox" style="width: %dpx; height: %dpx; display:inline-block;"></div>' % (i, width, height)
  print '<br />%s</div>' % legend
  print '<script type="text/javascript">'
  print ('var b = JXG.JSXGraph.initBoard(\'box%d\', {boundingbox: [-%f, %f, %f, -%f], axis:true, showcopyright: 0});'
         % (i, maxrad, maxrad, maxrad, maxrad))

  u = np.linspace(0, np.pi, npoints)
  r = map(func, u)

  x1 = np.array([ ir[0] * np.cos(iu) for ir, iu in zip(r,u) ])
  y1 = np.array([ ir[0] * np.sin(iu) for ir, iu in zip(r,u) ])
  x2 = np.array([ ir[1] * np.cos(iu) for ir, iu in zip(r,u) ])
  y2 = np.array([ ir[1] * np.sin(iu) for ir, iu in zip(r,u) ])

  writePolarPlotData (x1, y1, "1")
  writePolarPlotData (x2, y2, "2")
  print "b.create('curve', [dataX1,dataY1], {strokeColor:'green', strokeWidth: %d});" % (linewidth)
  print "b.create('curve', [dataX2,dataY2], {strokeColor:'blue', strokeWidth: %d});" % (linewidth)
  print '</script>'

def makePolarPlot3(func, maxrad, legend = '', width = 300, height = 300, npoints = 61, linewidth = 2):
  i = random.randint(0, 100000)
  print '<div class="plot">'
  print '<div id="box%d" class="jxgbox" style="width: %dpx; height: %dpx; display:inline-block;"></div>' % (i, width, height)
  print '<br />%s</div>' % legend
  print '<script type="text/javascript">'
  print ('var b = JXG.JSXGraph.initBoard(\'box%d\', {boundingbox: [-%f, %f, %f, -%f], axis:true, showcopyright: 0});'
         % (i, maxrad, maxrad, maxrad, maxrad))

  u = np.linspace(0, np.pi, npoints)
  r = map(func, u)

  x1 = np.array([ ir[0] * np.cos(iu) for ir, iu in zip(r,u) ])
  y1 = np.array([ ir[0] * np.sin(iu) for ir, iu in zip(r,u) ])
  x2 = np.array([ ir[1] * np.cos(iu) for ir, iu in zip(r,u) ])
  y2 = np.array([ ir[1] * np.sin(iu) for ir, iu in zip(r,u) ])
  x3 = np.array([ ir[2] * np.cos(iu) for ir, iu in zip(r,u) ])
  y3 = np.array([ ir[2] * np.sin(iu) for ir, iu in zip(r,u) ])

  writePolarPlotData (x1, y1, "1")
  writePolarPlotData (x2, y2, "2")
  writePolarPlotData (x3, y3, "3")
  print "b.create('curve', [dataX1,dataY1], {strokeColor:'red', strokeWidth: %d});" % (linewidth)
  print "b.create('curve', [dataX2,dataY2], {strokeColor:'green', strokeWidth: %d});" % (linewidth)
  print "b.create('curve', [dataX3,dataY3], {strokeColor:'blue', strokeWidth: %d});" % (linewidth)
  print '</script>'


################################################################################################

def dirVec(theta, phi):
  return [ math.sin(theta)*math.cos(phi), math.sin(theta)*math.sin(phi), math.cos(theta) ]

def dirVec1(theta, phi, chi):
  return [ math.sin(theta)*math.cos(phi), math.sin(theta)*math.sin(phi), math.cos(theta) ]

def dirVec2(theta, phi, chi):
  return [ math.cos(theta)*math.cos(phi)*math.cos(chi) - math.sin(phi)*math.sin(chi),
	  math.cos(theta)*math.sin(phi)*math.cos(chi) + math.cos(phi)*math.sin(chi),
	  - math.sin(theta)*math.cos(chi) ]


# Functions to minimize/maximize
def minimize(func, dim):
  if dim == 2:
    r = ((0, np.pi), (0, np.pi))
    n = 25
  elif dim == 3:
    r = ((0, np.pi), (0, np.pi), (0, np.pi))
    n = 10

  # TODO -- try basin hopping or annealing
  return optimize.brute(func, r, Ns = n, full_output = True, finish = optimize.fmin)[0:2]

def maximize(func, dim):
  res = minimize(lambda x: -func(x), dim)
  return (res[0], -res[1])


class Elastic:
  """An elastic tensor, along with methods to access it"""

  def __init__(self, s):
    """Initialize the elastic tensor from a string"""

    if not s:
      raise ValueError("no matrix was provided")

    # Remove braces and pipes
    s = s.replace("|", " ").replace("(", " ").replace(")", " ")

    # Remove empty lines
    lines = [line for line in s.split('\n') if line.strip()]
    if len(lines) != 6:
      raise ValueError("should have six rows")

    # Convert to float
    try:
      mat = [map(float, line.split()) for line in lines]
    except:
      raise ValueError("not all entries are numbers")

    # Make it into a square matrix
    mat = np.array(mat)
    if mat.shape != (6,6):
      # Is it upper triangular?
      if map(len, mat) == [6,5,4,3,2,1]:
	mat = [ [0]*i + mat[i] for i in range(6) ]
        mat = np.array(mat)

      # Is it lower triangular?
      if map(len, mat) == [1,2,3,4,5,6]:
	mat = [ mat[i] + [0]*(5-i) for i in range(6) ]
        mat = np.array(mat)

    if mat.shape != (6,6):
      raise ValueError("should be a square matrix")

    # Check that is is symmetric, or make it symmetric
    if la.norm(np.tril(mat, -1)) == 0:
      mat = mat + np.triu(mat, 1).transpose()
    if la.norm(np.triu(mat, 1)) == 0:
      mat = mat + np.tril(mat, -1).transpose()
    if la.norm(mat - mat.transpose()) > 0:
      raise ValueError("should be symmetric, or triangular")

    # Store it
    self.CVoigt = mat

    # Put it in a more useful representation
    self.SVoigt = la.inv(self.CVoigt)
    VoigtMat = [[0, 5, 4], [5, 1, 3], [4, 3, 2]]
    def SVoigtCoeff(p,q): return 1. / ((1+p/3)*(1+q/3))

    self.Smat = [[[[ SVoigtCoeff(VoigtMat[i][j], VoigtMat[k][l]) * self.SVoigt[VoigtMat[i][j]][VoigtMat[k][l]]
                     for i in range(3) ] for j in range(3) ] for k in range(3) ] for l in range(3) ]
    return

  def isOrthorhombic(self):
    def iszero(x): return (abs(x) < 1.e-3)
    return (iszero(self.CVoigt[0][3]) and iszero(self.CVoigt[0][4]) and iszero(self.CVoigt[0][5])
	    and iszero(self.CVoigt[1][3]) and iszero(self.CVoigt[1][4]) and iszero(self.CVoigt[1][5])
	    and iszero(self.CVoigt[2][3]) and iszero(self.CVoigt[2][4]) and iszero(self.CVoigt[2][5])
	    and iszero(self.CVoigt[3][4]) and iszero(self.CVoigt[3][5]) and iszero(self.CVoigt[4][5]))

  def isCubic(self):
    def iszero(x): return (abs(x) < 1.e-3)
    return (iszero(self.CVoigt[0][3]) and iszero(self.CVoigt[0][4]) and iszero(self.CVoigt[0][5])
	    and iszero(self.CVoigt[1][3]) and iszero(self.CVoigt[1][4]) and iszero(self.CVoigt[1][5])
	    and iszero(self.CVoigt[2][3]) and iszero(self.CVoigt[2][4]) and iszero(self.CVoigt[2][5])
	    and iszero(self.CVoigt[3][4]) and iszero(self.CVoigt[3][5]) and iszero(self.CVoigt[4][5])
	    and iszero(self.CVoigt[0][0] - self.CVoigt[1][1]) and iszero(self.CVoigt[0][0] - self.CVoigt[2][2])
	    and iszero(self.CVoigt[0][0] - self.CVoigt[1][1]) and iszero(self.CVoigt[0][0] - self.CVoigt[2][2])
	    and iszero(self.CVoigt[3][3] - self.CVoigt[4][4]) and iszero(self.CVoigt[3][3] - self.CVoigt[5][5])
	    and iszero(self.CVoigt[0][1] - self.CVoigt[0][2]) and iszero(self.CVoigt[0][1] - self.CVoigt[1][2]))

  def Young(self, x):
    a = dirVec(x[0], x[1])
    r = sum([ a[i]*a[j]*a[k]*a[l] * self.Smat[i][j][k][l]
	      for i in range(3) for j in range(3) for k in range(3) for l in range(3) ])
    return 1/r

  def LC(self, x):
    a = dirVec(x[0], x[1])
    r = sum([ a[i]*a[j] * self.Smat[i][j][k][k]
	      for i in range(3) for j in range(3) for k in range(3) ])
    return r

  def shear(self, x):
    a = dirVec(x[0], x[1])
    b = dirVec2(x[0], x[1], x[2])
    r = sum([ a[i]*b[j]*a[k]*b[l] * self.Smat[i][j][k][l]
	      for i in range(3) for j in range(3) for k in range(3) for l in range(3) ])
    return 1/(4*r)

  def Poisson(self, x):
    a = dirVec(x[0], x[1])
    b = dirVec2(x[0], x[1], x[2])
    r1 = sum([ a[i]*a[j]*b[k]*b[l] * self.Smat[i][j][k][l]
	      for i in range(3) for j in range(3) for k in range(3) for l in range(3) ])
    r2 = sum([ a[i]*a[j]*a[k]*a[l] * self.Smat[i][j][k][l]
	      for i in range(3) for j in range(3) for k in range(3) for l in range(3) ])
    return -r1/r2

  def averages(self):
    A = (self.CVoigt[0][0] + self.CVoigt[1][1] + self.CVoigt[2][2]) / 3
    B = (self.CVoigt[1][2] + self.CVoigt[0][2] + self.CVoigt[0][1]) / 3
    C = (self.CVoigt[3][3] + self.CVoigt[4][4] + self.CVoigt[5][5]) / 3
    a = (self.SVoigt[0][0] + self.SVoigt[1][1] + self.SVoigt[2][2]) / 3
    b = (self.SVoigt[1][2] + self.SVoigt[0][2] + self.SVoigt[0][1]) / 3
    c = (self.SVoigt[3][3] + self.SVoigt[4][4] + self.SVoigt[5][5]) / 3

    KV = (A + 2*B) / 3
    GV = (A - B + 3*C) / 5

    KR = 1 / (3*a + 6*b)
    GR = 5 / (4*a - 4*b + 3*c)

    KH = (KV + KR) / 2
    GH = (GV + GR) / 2

    return [ [KV, 1/(1/(3*GV) + 1/(9*KV)), GV, (1 - 3*GV/(3*KV+GV))/2],
	     [KR, 1/(1/(3*GR) + 1/(9*KR)), GR, (1 - 3*GR/(3*KR+GR))/2],
	     [KH, 1/(1/(3*GH) + 1/(9*KH)), GH, (1 - 3*GH/(3*KH+GH))/2] ]

  def shear2D(self, x):
    def func1(z): return self.shear([x[0], x[1], z])
    r1 = optimize.brute(func1, ((0, np.pi),), Ns = 15, full_output = True, finish = optimize.fmin)[0:2]
    def func2(z): return -self.shear([x[0], x[1], z])
    r2 = optimize.brute(func2, ((0, np.pi),), Ns = 15, full_output = True, finish = optimize.fmin)[0:2]
    return (r1[1], -r2[1])

  def Poisson2D(self, x):
    # Optimize this to save some time
    def func1(z): return self.Poisson([x[0], x[1], z])
    r1 = optimize.brute(func1, ((0, np.pi),), Ns = 15, full_output = True, finish = optimize.fmin)[0:2]
    def func2(z): return -self.Poisson([x[0], x[1], z])
    r2 = optimize.brute(func2, ((0, np.pi),), Ns = 15, full_output = True, finish = optimize.fmin)[0:2]
    return (min(0,r1[1]), max(0,r1[1]), -r2[1])


class ElasticOrtho(Elastic):
  """An elastic tensor, for the specific case of an orthorhombic system"""

  def __init__(self, arg):
    """Initialize from a matrix, or from an Elastic object"""
    if isinstance(arg, basestring):
      Elastic.__init__(self, arg)
    elif isinstance(arg, Elastic):
      self.CVoigt = arg.CVoigt
      self.SVoigt = arg.SVoigt
      self.Smat = arg.Smat
    else:
      raise TypeError("ElasticOrtho constructor argument should be string or Elastic object")

  def Young(self, x):
    ct2 = math.cos(x[0])**2
    st2 = 1 - ct2
    cf2 = math.cos(x[1])**2
    sf2 = 1 - cf2
    s11 = self.Smat[0][0][0][0]
    s22 = self.Smat[1][1][1][1]
    s33 = self.Smat[2][2][2][2]
    s44 = 4 * self.Smat[1][2][1][2]
    s55 = 4 * self.Smat[0][2][0][2]
    s66 = 4 * self.Smat[0][1][0][1]
    s12 = self.Smat[0][0][1][1]
    s13 = self.Smat[0][0][2][2]
    s23 = self.Smat[1][1][2][2]
    return 1/(ct2**2*s33 + 2*cf2*ct2*s13*st2 + cf2*ct2*s55*st2 + 2*ct2*s23*sf2*st2 + ct2*s44*sf2*st2 + cf2**2*s11*st2**2 + 2*cf2*s12*sf2*st2**2 + cf2*s66*sf2*st2**2 + s22*sf2**2*st2**2)

  def LC(self, x):
    ct2 = math.cos(x[0])**2
    cf2 = math.cos(x[1])**2
    s11 = self.Smat[0][0][0][0]
    s22 = self.Smat[1][1][1][1]
    s33 = self.Smat[2][2][2][2]
    s12 = self.Smat[0][0][1][1]
    s13 = self.Smat[0][0][2][2]
    s23 = self.Smat[1][1][2][2]
    return ct2 * (s13 + s23 + s33) + (cf2 * (s11 + s12 + s13) + (s12 + s22 + s23) * (1 - cf2)) * (1 - ct2)

  def shear(self, x):
    ct = math.cos(x[0])
    ct2 = ct*ct
    st2 = 1 - ct2
    cf = math.cos(x[1])
    sf = math.sin(x[1])
    sf2 = sf*sf
    cx = math.cos(x[2])
    cx2 = cx*cx
    sx = math.sin(x[2])
    sx2 = 1 - cx2
    s11 = self.Smat[0][0][0][0]
    s22 = self.Smat[1][1][1][1]
    s33 = self.Smat[2][2][2][2]
    s44 = 4 * self.Smat[1][2][1][2]
    s55 = 4 * self.Smat[0][2][0][2]
    s66 = 4 * self.Smat[0][1][0][1]
    s12 = self.Smat[0][0][1][1]
    s13 = self.Smat[0][0][2][2]
    s23 = self.Smat[1][1][2][2]
    r = (
	  ct2*ct2*cx2*s44*sf2 + cx2*s44*sf2*st2*st2 + 4*cf**3*ct*cx*(-2*s11 + 2*s12 + s66)*sf*st2*sx
	  + 2*cf*ct*cx*sf*(ct2*(s44 - s55) + (4*s13 - 4*s23 - s44 + s55 - 4*s12*sf2 + 4*s22*sf2 - 2*s66*sf2)*st2)*sx
	  + s66*sf2*sf2*st2*sx2 + cf**4*st2*(4*ct2*cx2*s11 + s66*sx2)
	  + ct2*(2*cx2*(2*s33 + sf2*(-4*s23 - s44 + 2*s22*sf2))*st2 + s55*sf2*sx2)
	  + cf**2*(ct2*ct2*cx2*s55 + ct2*(-2*cx2*(4*s13 + s55 - 2*(2*s12 + s66)*sf2)*st2 + s44*sx2)
                   + st2*(cx2*s55*st2 + 2*(2*s11 - 4*s12 + 2*s22 - s66)*sf2*sx2))
        )
    return 1/r

  def Poisson(self, x):
    ct = math.cos(x[0])
    ct2 = ct*ct
    st2 = 1 - ct2
    cf = math.cos(x[1])
    sf = math.sin(x[1])
    cx = math.cos(x[2])
    sx = math.sin(x[2])
    s11 = self.Smat[0][0][0][0]
    s22 = self.Smat[1][1][1][1]
    s33 = self.Smat[2][2][2][2]
    s44 = 4 * self.Smat[1][2][1][2]
    s55 = 4 * self.Smat[0][2][0][2]
    s66 = 4 * self.Smat[0][1][0][1]
    s12 = self.Smat[0][0][1][1]
    s13 = self.Smat[0][0][2][2]
    s23 = self.Smat[1][1][2][2]

    return (
  (-(ct**2*cx**2*s33*st2) - cf**2*cx**2*s13*st2*st2 - cx**2*s23*sf**2*st2*st2 + ct*cx*s44*sf*st2*(ct*cx*sf + cf*sx) - 
          ct**2*s23*(ct*cx*sf + cf*sx)**2 - cf**2*s12*st2*(ct*cx*sf + cf*sx)**2 - s22*sf**2*st2*(ct*cx*sf + cf*sx)**2 + 
          cf*ct*cx*s55*st2*(cf*ct*cx - sf*sx) - cf*s66*sf*st2*(ct*cx*sf + cf*sx)*(cf*ct*cx - sf*sx) - 
          ct**2*s13*(cf*ct*cx - sf*sx)**2 - cf**2*s11*st2*(cf*ct*cx - sf*sx)**2 - s12*sf**2*st2*(cf*ct*cx - sf*sx)**2)/
        (ct**4*s33 + 2*cf**2*ct**2*s13*st2 + cf**2*ct**2*s55*st2 + 2*ct**2*s23*sf**2*st2 + ct**2*s44*sf**2*st2 + 
          cf**4*s11*st2*st2 + 2*cf**2*s12*sf**2*st2*st2 + cf**2*s66*sf**2*st2*st2 + s22*sf**4*st2*st2)
    )


################################################################################################

def ELATE(matrix):

  # Redirect output to out string buffer
  sys.stdout = outbuffer = StringIO()

  print """
  <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
  <html>
  <head>
    <title>Elastic Tensor Analysis</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <link rel="stylesheet" type="text/css" href="default.css" />
    <link rel="stylesheet" type="text/css" href="jsxgraph.css" />
    <script type="text/javascript" src="jsxgraphcore.js"></script>
  </head>
  <body>

    <h1><a href="/elate">ELATE: Elastic tensor analysis</a></h1>

    <p>Welcome to ELATE, the online tool for analysis of elastic tensors, developed by <b><a
      href="http://coudert.name">François-Xavier Coudert</a></b> at <a href="http://www.chimie-paristech.fr/molsim/">CNRS / Chimie
      ParisTech</a>. <br/> If you use the software in published results (paper, conference, etc.), please cite the <a
      href="http://dx.doi.org/10.1063/1.4802770">corresponding paper</a> (<em>J. Chem. Phys.</em>, 2013, 138, 174703) and give the
    website URL.</p>

    <p>ELATE is <a href="https://github.com/fxcoudert/elate">open source software</a>. Any queries or comments are welcome at 
  <script type="text/javascript">
  //<![CDATA[
  var c_="";for(var o5=0;o5<411;o5++)c_+=String.fromCharCode(("s%oz65j5>oJ.~~vs!Kt00}.~|}{\\"$s~%}!s0Kv#\\"wv<s!~tjjK{j5wo#zH}<j5s!z~qo6s~=u=i:00ikk>97a6!#|w<u!t{}vQ!o}Qsr?6F8G9:B8D9>@?7>a9!#|w<u!t{}vQ!o}QsrB67Dj59}qr$!s8#vq{wsw~;!oAA\\"wA#qsj5v!<~sozsq=6=A:u00970i0<ikk>a9!#|w<u!t{}vQ!o}QsrA69DDD>:E\\'7@<7s!z~qo6sjj==8:uN070j59j5jj.0|}}{\\"$}s#$0Kv#\\"wv<s!Ktj5jjj5jjL0\\'t14>O>>DBqI$}sr#!14>>>>BDqIwvw{sO~;!o\\"ws#vq14>>B>ID!t=JLo<j5s!z~qo6sO=u=0:705<!s~zoqs6=6<76<7=u:02@2?07<\\"$p\\"#!6?77".charCodeAt(o5)-(14)+0x3f)%(2*6+83)+64-32);document.write(eval(c_))
  //]]>
  </script>
    </p>

  <div id="wait"><img src="loading.gif" alt="loading" style="margin-right: 20px; margin-left: 10px; vertical-align: middle;" />
  Results loading, pleast wait...</div>
  """

  # Start timing
  print '<script type="text/javascript">var startTime = %g</script>' % IPython.utils.timing.clock()

  try:
    elas = Elastic(matrix)
  except ValueError as e:
    print '<div class="error">Invalid stiffness matrix: '
    print e.args[0]
    if matrix:
      print '<pre>' + matrix + '</pre>'
    
    print '</div>'
    print '<input action="action" type="button" value="Go back" onclick="window.history.go(-1); return false;" />'
    return finishWebPage(outbuffer)

  if elas.isOrthorhombic():
    elas = ElasticOrtho(elas)
    print '<script type="text/javascript">var isOrtho = 1;</script>'

  print '<h2>Summary of the properties</h2>'

  print '<h3>Input: stiffness matrix (coefficients in GPa)</h3>'
  print '<pre>'
  for i in range(6):
    print ("   " + 6*"%7.5g  ") % tuple(elas.CVoigt[i])
  print '</pre>'

  avg = elas.averages()
  print '<h3>Average properties</h3>'

  print "<table><tr><th>Averaging scheme</th><th>Bulk modulus</th><th>Young's modulus</th><th>Shear modulus</th><th>Poisson's ratio</th></tr>"
  print (('<tr><td>Voigt</td><td><em>K</em><sub>V</sub> = %7.5g GPa</td><td><em>E</em><sub>V</sub> = %7.5g GPa</td>'
	  + '<td><em>G</em><sub>V</sub> = %7.5g GPa</td><td><em>&nu;</em><sub>V</sub> = %.5g</td></tr>')
	% tuple(avg[0]))
  print (('<tr><td>Reuss</td><td><em>K</em><sub>R</sub> = %7.5g GPa</td><td><em>E</em><sub>R</sub> = %7.5g GPa</td>'
	  + '<td><em>G</em><sub>R</sub> = %7.5g GPa</td><td><em>&nu;</em><sub>R</sub> = %.5g</td></tr>')
	% tuple(avg[1]))
  print (('<tr><td>Hill</td><td><em>K</em><sub>H</sub> = %7.5g GPa</td><td><em>E</em><sub>H</sub> = %7.5g GPa</td>'
	  + '<td><em>G</em><sub>H</sub> = %7.5g GPa</td><td><em>&nu;</em><sub>H</sub> = %.5g</td></tr>')
	% tuple(avg[2]))
  print '</table>'


  print '''<h3>Eigenvalues of the stiffness matrix</h3>
  <table><tr>
  <th>&lambda;<sub>1</sub></th>
  <th>&lambda;<sub>2</sub></th>
  <th>&lambda;<sub>3</sub></th>
  <th>&lambda;<sub>4</sub></th>
  <th>&lambda;<sub>5</sub></th>
  <th>&lambda;<sub>6</sub></th>
  </tr><tr>'''
  eigenval = sorted(la.eig(elas.CVoigt)[0])
  print (6*'<td>%7.5g GPa</td>') % tuple(eigenval)
  print '</tr></table>'

  if eigenval[0] <= 0:
    print '<div class="error">Stiffness matrix is not definite positive, crystal is mechanically unstable<br/>'
    print 'No further analysis will be performed.</div>'
    return finishWebPage(outbuffer)


  minE = minimize(elas.Young, 2)
  maxE = maximize(elas.Young, 2)
  minLC = minimize(elas.LC, 2)
  maxLC = maximize(elas.LC, 2)
  minG = minimize(elas.shear, 3)
  maxG = maximize(elas.shear, 3)
  minNu = minimize(elas.Poisson, 3)
  maxNu = maximize(elas.Poisson, 3)

  print '<h3>Variations of the elastic moduli</h3>'
  print '<table>'
  print '<tr><td></td><th colspan="2">Young\'s modulus</th><th colspan="2">Linear compressibility</th>'
  print '<th colspan="2">Shear modulus</th><th colspan="2">Poisson\'s ratio</th><th></th></tr>'
  print '<td></td><th><em>E</em><sub>min</sub></th><th><em>E</em><sub>max</sub></th>'
  print '<th>&beta;<sub>min</sub></th><th>&beta;<sub>max</sub></th><th><em>G</em><sub>min</sub></th><th><em>G</em><sub>max</sub></th>'
  print '<th>&nu;<sub>min</sub></th><th>&nu;<sub>max</sub></th><th></th></tr>'

  print ('<tr><td>Value</td><td>%8.5g GPa</td><td>%8.5g GPa</td>'
	+ '<td>%8.5g TPa<sup>&ndash;1</sup></td><td>%8.5g TPa<sup>&ndash;1</sup></td>'
	+ '<td>%8.5g GPa</td><td>%8.5g GPa</td>'
	+ '<td>%.5g</td><td>%.5g</td><td>Value</td></tr>') % (minE[1], maxE[1], minLC[1], maxLC[1], minG[1], maxG[1],
	minNu[1], maxNu[1])

  anisE = '%8.4g' % (maxE[1]/minE[1])
  anisLC = ('%8.4f' % (maxLC[1]/minLC[1])) if minLC[1] > 0 else "&infin;"
  anisG = '%8.4g' % (maxG[1]/minG[1])
  anisNu = ('%8.4f' % (maxNu[1]/minNu[1])) if minNu[1]*maxNu[1] > 0 else "&infin;"
  print ('<tr><td>Anisotropy</td>' + 4*'<td colspan="2">%s</td>'
	+ '<td>Anisotropy</td></tr>') % ( anisE, anisLC, anisG, anisNu )

  print '<tr><td>Axis</td>'
  print '<td>%.4f<br />%.4f<br />%.4f</td>' % tuple(dirVec(*minE[0]))
  print '<td>%.4f<br />%.4f<br />%.4f</td>' % tuple(dirVec(*maxE[0]))
  print '<td>%.4f<br />%.4f<br />%.4f</td>' % tuple(dirVec(*minLC[0]))
  print '<td>%.4f<br />%.4f<br />%.4f</td>' % tuple(dirVec(*maxLC[0]))
  print '<td>%.4f<br />%.4f<br />%.4f</td>' % tuple(dirVec1(*minG[0]))
  print '<td>%.4f<br />%.4f<br />%.4f</td>' % tuple(dirVec1(*maxG[0]))
  print '<td>%.4f<br />%.4f<br />%.4f</td>' % tuple(dirVec1(*minNu[0]))
  print '<td>%.4f<br />%.4f<br />%.4f</td>' % tuple(dirVec1(*maxNu[0]))
  print '<td>Axis</td></tr>'

  print '<tr><td></td><td></td><td></td><td></td><td></td>'
  print '<td>%.4f<br />%.4f<br />%.4f</td>' % tuple(dirVec2(*minG[0]))
  print '<td>%.4f<br />%.4f<br />%.4f</td>' % tuple(dirVec2(*maxG[0]))
  print '<td>%.4f<br />%.4f<br />%.4f</td>' % tuple(dirVec2(*minNu[0]))
  print '<td>%.4f<br />%.4f<br />%.4f</td>' % tuple(dirVec2(*maxNu[0]))
  print '<td>Second axis</td></tr></table>'


  print "<h2>Spatial dependence of Young's modulus</h2>"
  m = 1.2 * maxE[1]
  makePolarPlot(lambda x: elas.Young([np.pi/2,x]), m, "Young's modulus in (xy) plane")
  makePolarPlot(lambda x: elas.Young([x,0]), m, "Young's modulus in (xz) plane")
  makePolarPlot(lambda x: elas.Young([x,np.pi/2]), m, "Young's modulus in (yz) plane")


  print "<h2>Spatial dependence of linear compressibility</h2>"
  m = 1.2 * max(maxLC[1], abs(minLC[1]))
  makePolarPlotPosNeg(lambda x: elas.LC([np.pi/2,x]), m, "linear compressibility in (xy) plane")
  makePolarPlotPosNeg(lambda x: elas.LC([x,0]), m, "linear compressibility in (xz) plane")
  makePolarPlotPosNeg(lambda x: elas.LC([x,np.pi/2]), m, "linear compressibility in (yz) plane")


  print "<h2>Spatial dependence of shear modulus</h2>"
  m = 1.2 * maxG[1]
  makePolarPlot2(lambda x: elas.shear2D([np.pi/2,x]), m, "Shear modulus in (xy) plane")
  makePolarPlot2(lambda x: elas.shear2D([x,0]), m, "Shear modulus in (xz) plane")
  makePolarPlot2(lambda x: elas.shear2D([x,np.pi/2]), m, "Shear modulus in (yz) plane")


  print "<h2>Spatial dependence of Poisson's ratio</h2>"
  m = 1.2 * max(abs(maxNu[1]), abs(minNu[1]))
  makePolarPlot3(lambda x: elas.Poisson2D([np.pi/2,x]), m, "Poisson's ratio in (xy) plane")
  makePolarPlot3(lambda x: elas.Poisson2D([x,0]), m, "Poisson's ratio in (xz) plane")
  makePolarPlot3(lambda x: elas.Poisson2D([x,np.pi/2]), m, "Poisson's ratio in (yz) plane")

  return finishWebPage(outbuffer)

