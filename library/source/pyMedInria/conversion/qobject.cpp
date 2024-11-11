// Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
// License: BSD-3-Clause

#include "qobject.h"

#include "../conversion.h"

bool pyncppToPython(const QObject* object, PyObject** output)
{
    bool success = true;

    try
    {
        pyncpp::Module pyncppQtModule = pyncpp::Module::import("pymedinria.core.qt");
        pyncpp::Object pythonClass;

        for (const QMetaObject* metaObject = object->metaObject(); metaObject != nullptr; metaObject = metaObject->superClass())
        {
            QString className = metaObject->className();

            try
            {
                pythonClass = pyncppQtModule.callMethod("get_class", qUtf8Printable(className));
            }
            catch (pyncpp::NameError&)
            {
                continue;
            }

            break;
        }

        if (!pythonClass)
        {
            throw pyncpp::NameError("Could not find a PySide class blah blah");
        }

        pyncpp::Object objectPointer = PyLong_FromVoidPtr(const_cast<QObject*>(object));
        pyncpp::Module shibokenModule = pyncpp::Module::import(PYMED_SHIBOKEN_PACKAGE);
        pyncpp::Object wrappedObject = shibokenModule.callMethod("wrapInstance", objectPointer, pythonClass);
        *output = wrappedObject.newReference();
    }
    catch (pyncpp::Exception& e)
    {
        pyncpp::raiseError(&e);
        success = false;
    }

    return success;
}

bool pyncppToCPP(PyObject* nativeObject, QObject** output)
{
    bool success = true;

    try
    {
        pyncpp::Module shibokenModule = pyncpp::Module::import(PYMED_SHIBOKEN_PACKAGE);
        pyncpp::Object objectPointer = shibokenModule.callMethod("getCppPointer", nativeObject)[0];
        *output = (QObject*)PyLong_AsVoidPtr(*objectPointer);
    }
    catch (pyncpp::Exception& e)
    {
        pyncpp::raiseError(&e);
        success = false;
    }

    return success;
}
