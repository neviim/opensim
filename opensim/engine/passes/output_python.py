#===--- output_python.py - convert an opensim model to python ------------===#
#
# Copyright 2009 Bobby Powers
#
# This file is part of OpenSim.
#
# OpenSim is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OpenSim is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with OpenSim.  If not, see <http://www.gnu.org/licenses/>.
#
#===-----------------------------------------------------------------------===#
#
# This file contains the class to pretty print a model AST as Python.
#
#===-----------------------------------------------------------------------===#

import logging, sys

import common

log = logging.getLogger('opensim.python')

CLASS_NAME = 'PythonPrint'

py_header = """
#!/usr/bin/env python
# python model auto-generated by OpenSim
import math

def frange(lim_start, lim_end, increment = 1.):
  '''
  Range function that allows floating point range increments.

  Standard python range function doesn't allow floating point
  increments in ranges.
  '''
  lim_start = float(lim_start)
  count = int(math.ceil(lim_end - lim_start)/increment + 1)
  return (lim_start + n*increment for n in range(count))


# simple lookup table implementation
def lookup(table, index):
  '''
  Simple lookup table implementation.

  Table takes the format of a list of 2-tuples.
  '''

  if len(table) is 0: return 0

  # if the request is outside the min or max, then we return
  # the nearest element of the array
  if   index < table[0][0]:  return table[0][1]
  elif index > table[-1][0]: return table[-1][1]

  for i in range(0, len(table)):
    x, y = table[i]

    if index == x: return y
    if index < x:
      # slope = deltaY/deltaX
      slope = (y - table[i-1][1])/(x - table[i-1][0])
      return (index-table[i-1][0])*slope + table[i-1][1]

"""


class PythonPrint:
  '''
  This class implements the visitor methods needed to pretty print a model.

  fd is the file decriptor that we will write to, or any object that
  supports the write(str) method.
  '''
  def __init__(self, fd=sys.stdout):
    self.space = ''
    self.fd = fd


  def write(self, string, end='\n'):
    '''
    Writes a string to self.fd and appends a newline
    '''
    self.fd.write(string)
    self.fd.write(end)


  def visit_scope(self, node):
    '''
    Visiting a scope node.

    Eventually we will use this to implement namespaces and have stacks
    of variables to lookup in, but for now we just grab the vars from
    the root scope.
    '''
    if node.name == 'root':
      self.vars = node.vars
      self.write(py_header)
      self.write('# initial values and stock initializations')

    node.child.gen(self)


  def visit_list(self, node):
    '''
    Visit a list of statements.
    '''
    for stmt in node.statements:
      stmt.gen(self)


  def visit_euler(self, node):
    '''
    Visit a euler integration node.

    This is basically a glorified loop, but is used to distinguish
    between a basic loop and a more complicated RK one.
    '''
    self.write('\n# variables related to outputting results')
    self.write('save_count = 0')
    self.write('save_iterations = time_savestep / time_step')
    self.write('do_save = True')

    format = '%s'
    vars_list = 'time'
    for stmt in node.body.statements:
      vars_list += ',' + stmt.var_name
      format += ',%s'
    for stmt in node.stocks.statements:
      vars_list += ',' + stmt.var_name
      format += ',%s'

    # output headers for csv output
    self.write('\nprint \'%s\'' % vars_list)

    self.write('\nfor time in frange(time_start, time_end, time_step):')

    #start = self.vars['time_start'].props.equation.strip()
    #end = self.vars['time_end'].props.equation.strip()
    #step = self.vars['time_step'].props.equation.strip()

    # indent things!
    self.space = self.space + '  '
    self.write('  # calculate flows:')
    node.body.gen(self)

    self.write('\n  # output results:')
    self.write('  if do_save:')
    self.write("    print '" + format + "' % (" + vars_list + ')')

    self.write('\n  # update stocks:')
    node.stocks.gen(self)

    # determine whether we need to write the next round of output to stdout
    self.write('')
    self.write('  # determining whether or not to save results next iteration')
    self.write('  save_count += 1')
    self.write('  if save_count >= save_iterations or time+time_step > time_end:')
    self.write('    do_save = True')
    self.write('    save_count = 0')
    self.write('  else:')
    self.write('    do_save = False')

    self.space = self.space[:-4]


  def visit_assign(self, node):
    '''
    Visiting an assignment statement.
    '''
    self.write(self.space + node.var_name + ' = ', end='')
    node.value.gen(self)
    self.write('')


  def visit_bin_expr(self, node):
    '''
    Visit a node represeting a binary expression.

    We add parentheses becuase when we create the AST we respect
    parenthesis, but they are not represented in the tree
    '''
    self.write('(', end='')
    node.lval.gen(self)
    self.write(' %s ' % node.op, end='')
    node.rval.gen(self)
    self.write(')', end='')



  def visit_unary(self, node):
    self.write(node.op + '(', end='')
    node.lval.gen(self)
    self.write(')', end='')


  def visit_var_ref(self, node):
    '''
    Visit a variable reference.

    Leaf node!
    '''
    self.write(node.name, end='')


  def visit_value(self, node):
    '''
    Visit a node representing a real number.

    Leaf node!
    '''
    self.write(str(node.val), end='')
