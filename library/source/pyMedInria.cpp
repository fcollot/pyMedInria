// Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
// License: BSD-3-Clause

#include "pyMedInria.h"

#ifdef Q_OS_WIN
#include <windows.h>
#endif

namespace pyMedInria
{

Application::Application(const Config& config)
{
    if (initPython(config))
    {
        if (config.runMain)
        {
            int exitStatus = pyncpp::Manager::instance().runMain();

            if (exitStatus != 0)
            {
                errorText = QString("The application returne %1 on exit.").arg(exitStatus);
            }
        }
    }
}

Application::~Application()
{
    pyncpp::Manager::destroyInstance();
}

bool Application::errorOccured()
{
    return !errorText.isEmpty();
}

QString Application::errorMessage()
{
    return errorText;
}

void Application::clearError()
{
    errorText = "";
}

bool Application::initPython(const Config& config)
{
#ifdef Q_OS_WINDOWS
    SetDllDirectory("Lib\\site-packages\\PYMED_PYSIDE_PACKAGE");
#endif

    if (initPyncpp(config))
    {
        try
        {
            pyncpp::Object sysArgv = pyncpp::Module::import("sys").attribute("argv");

            for (int i = 0; i < config.numArgs; i++)
            {
                sysArgv.append(pyncpp::Object(config.args[i]));
            }
        }
        catch (pyncpp::Exception& e)
        {
            errorText = e.what();
        }
    }

    return !errorOccured();
}

bool Application::initPyncpp(const Config& config)
{
    QString home = config.home;
    QString libDir = config.libDir;

    if (home.isEmpty())
    {
        home = PYTHON_HOME;
    }

    if (libDir.isEmpty())
    {
        libDir = PYTHON_LIB_DIR;
    }

    pyncpp::Manager::setPythonHome(qUtf8Printable(home), qUtf8Printable(libDir));

    if (!config.mainModule.isEmpty())
    {
        pyncpp::Manager::setMainModule(qUtf8Printable(config.mainModule));
    }

    pyncpp::Manager& pyncppManager = pyncpp::Manager::instance();

    if (pyncppManager.errorOccured())
    {
        errorText = pyncppManager.errorMessage();
        return false;
    }
    else
    {
        return true;
    }
}


} // namespace pyMedInria
