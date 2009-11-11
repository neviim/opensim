//===--- run.cc - run manager for OpenSim mark 2 ------------------------===//
//
// Copyright 2009 Bobby Powers
//
// This file is part of OpenSim.
// 
// OpenSim is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// OpenSim is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
// 
// You should have received a copy of the GNU General Public License
// along with OpenSim.  If not, see <http://www.gnu.org/licenses/>.
//
//===--------------------------------------------------------------------===//
//
// This file contains classes and functions to build and rebuild ASTs,
// register passes and manage AST walks.
//
//===--------------------------------------------------------------------===//

#include "opensim/runtime.h"
#include "opensim/c_runtime.h"
#include "opensim/parse.h"

#include <llvm/Support/raw_ostream.h>
#include <llvm/Support/ManagedStatic.h>
#include <llvm/System/Threading.h>

#include <pthread.h>

#include <exception>


using namespace opensim;

Runtime::Runtime() {

}


Runtime::~Runtime() {

}


int Runtime::loadFile(std::string fileName)
{
  modelFileName = fileName;

  try
  {
    Parser parser(fileName);
    parser.parse();
  }
  catch (std::exception& e)
  {
    errs() << "opensim: ERROR: Problem loading '" << fileName << "'\n";
    return -1;
  }

  return 0;
}


int Runtime::simulate() {

  errs() << "simulate stub\n";
  return 0;
}


void startup::init() {

  // enable concurrent access to LLVM API
  llvm::llvm_start_multithreaded();
}


void startup::exit() {

  llvm::llvm_shutdown();
}
