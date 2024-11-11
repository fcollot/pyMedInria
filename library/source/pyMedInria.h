// Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
// License: BSD-3-Clause

// One of Python's structs has a member named slots, and this causes conflicts
// with the Qt keyword of the same name.
#undef slots
#define slots _slots

// This include must be placed first, as pyncpp includes the Python header which
// should be included before all other headers.
#include <pyncpp.h>

#undef slots
#define slots Q_SLOTS

#include "pyMedInria/conversion.h"

namespace pyMedInria
{

struct Config
{
    QString mainModule = "pymedinria";
    bool runMain = false;
    int numArgs = 0;
    char** args = nullptr;
    QString home;
    QString libDir;
};

class Application
{
public:
    Application(const Config& config);
    ~Application();

    bool errorOccured();
    QString errorMessage();
    void clearError();

private:
    QString errorText;

    bool initPython(const Config& config);
    bool initPyncpp(const Config& config);
};

} // namespace pyMedInria
