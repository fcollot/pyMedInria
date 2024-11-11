// Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
// License: BSD-3-Clause

#include "qobject.h"

#include "../conversion.h"

bool pyncppToPython(const QObject* object, PyObject** output)
{
    bool success = true;

    try
    {
        QString className = object->metaObject()->className();
        med::Module pyncppQtModule = med::Module::import("musicbox.qt");
        med::Object pythonClass = pyncppQtModule.callMethod("get_class", qUtf8Printable(className));
        med::Object objectPointer = PyLong_FromVoidPtr(const_cast<QObject*>(object));
        med::Module shibokenModule = med::Module::import(MED_SHIBOKEN_PACKAGE);
        med::Object wrappedObject = shibokenModule.callMethod("wrapInstance", objectPointer, pythonClass);
        *output = wrappedObject.newReference();
    }
    catch (med::Exception& e)
    {
        med::raiseError(&e);
        success = false;
    }

    return success;
}

bool pyncppToCPP(PyObject* nativeObject, QObject** output)
{
    bool success = true;

    try
    {
        med::Module shibokenModule = med::Module::import(MED_SHIBOKEN_PACKAGE);
        med::Object objectPointer = shibokenModule.callMethod("getCppPointer", nativeObject)[0];
        *output = (QObject*)PyLong_AsVoidPtr(*objectPointer);
    }
    catch (med::Exception& e)
    {
        med::raiseError(&e);
        success = false;
    }

    return success;
}
