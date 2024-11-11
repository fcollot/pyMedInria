// Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
// License: BSD-3-Clause

// This include must be placed first, as pyncpp includes the Python header which
// should be included before all other headers.
#include <pyncpp.h>

#include "pyMedInria/conversion.h"

namespace pyMedInria
{

bool initPython(int argc, char** argv, QString& errorMessage, const char* home, const char* libDir);

bool runProgram(QString name, int numArgs, char** args, QString& errorMessage, char* home = nullptr, char* libDir = nullptr);

bool runPythonCommandLine(int numArgs, char** args, QString& errorMessage, char* home = nullptr, char* libDir = nullptr);

} // namespace pyMedInria
