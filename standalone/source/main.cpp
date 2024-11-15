// Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
// License: BSD-3-Clause

#include <pyMedInria.h>

#ifdef Q_OS_WIN
    #include <windows.h>
#endif

#include <QDebug>

int main(int argc, char** argv)
{
#ifdef Q_OS_WIN
    SetDllDirectory(L"Lib\\site-packages\\PySide2");
#endif

    int exitStatus = EXIT_SUCCESS;

//#ifdef Q_OS_UNIX
    med::Manager::setPythonHome(PYTHON_HOME, PYTHON_LIB_DIR);
//#endif
    med::Manager& pyncppManager = med::Manager::instance();

    if (pyncppManager.errorOccured())
    {
       qCritical() << QString("Python initialization error: %1").arg(pyncppManager.errorMessage());
       exitStatus = EXIT_FAILURE;
    }
    else
    {
        try
        {
            med::Object sysArgv = med::Module::import("sys").attribute("argv");

            for (size_t i = 1; i < argc; i++)
            {
                sysArgv.append(med::Object(argv[i]));
            }

            med::Module::import("pymedinria.app").callMethod("main").toCPP<long>();
        }
        catch (med::Exception& e)
        {
            qCritical() << "Python error: " << e.what();
            exitStatus = EXIT_FAILURE;
        }
        catch (med::SystemExit& e)
        {
            exitStatus = (std::string(e.what()) == "0") ? EXIT_SUCCESS : EXIT_FAILURE;
        }
    }

    med::Manager::destroyInstance();
    return exitStatus;
}
