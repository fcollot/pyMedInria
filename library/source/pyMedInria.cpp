// Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
// License: BSD-3-Clause

#include "pyMedInria.h"

#ifdef Q_OS_WIN
    #include <windows.h>
#endif

namespace pyMedInria
{

bool initPyncpp(QString& errorMessage, const char* home, const char* libDir)
{
    if (!home)
    {
        home = PYTHON_HOME;
    }

    if (!libDir)
    {
        libDir = PYTHON_LIB_DIR;
    }

    pyncpp::Manager::setPythonHome(home, libDir);
    pyncpp::Manager& pyncppManager = pyncpp::Manager::instance();

    if (pyncppManager.errorOccured())
    {
       errorMessage = pyncppManager.errorMessage();
       return false;
    }
    else
    {
        return true;
    }
}

bool initPython(int argc, char** argv, QString& errorMessage, const char* home, const char* libDir)
{
#ifdef Q_OS_WINDOWS
    SetDllDirectory("Lib\\site-packages\\PYMED_PYSIDE_PACKAGE");
#endif

    if (initPyncpp(errorMessage, home, libDir))
    {
        try
        {
            pyncpp::Object sysArgv = pyncpp::Module::import("sys").attribute("argv");

            for (size_t i = 0; i < argc; i++)
            {
                sysArgv.append(pyncpp::Object(argv[i]));
            }
        }
        catch (pyncpp::Exception& e)
        {
            errorMessage = e.what();
        }
    }

    if (errorMessage.isEmpty())
    {
        return true;
    }
    else
    {
        pyncpp::Manager::destroyInstance();
        return false;
    }
}

bool runProgram(QString name, int numArgs, char** args, QString& errorMessage, char* home, char* libDir)
{
    pyncpp::Manager::setMainModule(qUtf8Printable(name));
    return runPythonCommandLine(numArgs, args, errorMessage, home, libDir);
}

bool runPythonCommandLine(int numArgs, char** args, QString& errorMessage, char* home, char* libDir)
{
    if (initPython(numArgs, args, errorMessage, home, libDir))
    {
        bool success = (pyncpp::Manager::instance().runMain() == 0);
        pyncpp::Manager::destroyInstance();
        return success;
    }
    else
    {
        return false;
    }
}

} // namespace pyMedInria
