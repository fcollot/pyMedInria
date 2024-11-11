// Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
// License: BSD-3-Clause

#include <pyMedInria.h>

#include <QDebug>

int main(int argc, char** argv)
{
    pyMedInria::Config config;

    config.runMain = true;

    if (argc > 1)
    {
        QString option = QString(argv[1]);

        if (option == "--pip")
        {
            config.numArgs = argc - 2;
            config.args = argv + 2;
            config.mainModule = "pip";
        }
        else if (option == "--python")
        {
            config.numArgs = argc - 2;
            config.args = argv + 2;
            config.mainModule = "";
        }
        else
        {
            config.numArgs = argc - 1;
            config.args = argv + 1;
            config.mainModule = "pymedinria";
        }
    }

    pyMedInria::Application app(config);

    if (app.errorOccured())
    {
        qDebug() << app.errorMessage();
        return EXIT_FAILURE;
    }
    else
    {
        return EXIT_SUCCESS;
    }
}
