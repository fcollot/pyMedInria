// Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
// License: BSD-3-Clause

#include <pyMedInria.h>

#include <QDebug>

int main(int argc, char** argv)
{
    int exitStatus = EXIT_SUCCESS;

    med::Manager::setPythonHome(PYTHON_HOME);
    med::Manager::setCommandLineArguments(argc, argv);
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
            //pyncppManager.prependModulePath(PYMEDINRIA_PACKAGE_PATH);
            exitStatus = med::Module::import("pymedinria").callMethod("run").toCPP<long>();
        }
        catch (med::Exception& e)
        {
            qCritical() << "Python error: " << e.what();
            exitStatus = EXIT_FAILURE;
        }
    }

    med::Manager::destroyInstance();
    return exitStatus;
}
