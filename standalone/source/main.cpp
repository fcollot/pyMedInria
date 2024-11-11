// Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
// License: BSD-3-Clause

#include <pyMedInria.h>

#include <QDebug>

int main(int argc, char** argv)
{
    bool success = true;
    QString errorMessage;
    QString mode = QString(argv[1]);

    if (mode == "--pip")
    {
        success = pyMedInria::runProgram("pip", argc - 2, argv + 2, errorMessage);
    }
    else if (mode == "--python")
    {
        success = pyMedInria::runPythonCommandLine(argc - 2, argv + 2, errorMessage);
    }
    else
    {
        success = pyMedInria::runProgram("pymedinria", argc - 1, argv + 1, errorMessage);
    }

    if (success)
    {
        return EXIT_SUCCESS;
    }
    else
    {
        if (!errorMessage.isEmpty())
        {
            qDebug() << errorMessage;
        }

        return EXIT_FAILURE;
    }
}
