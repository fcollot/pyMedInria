// Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
// License: BSD-3-Clause

#ifndef MED_QT_QOBJECT_H
#define MED_QT_QOBJECT_H

#include <Python.h>

#include "../external/pyncpp.h"

#include <type_traits>

#include <QObject>

#include "../export.h"

MED_EXPORT bool pyncppToPython(const QObject* object, PyObject** output);
MED_EXPORT bool pyncppToCPP(PyObject* nativeObject, QObject** output);

template <class TYPE, typename = std::enable_if_t<std::is_base_of_v<QObject, TYPE> > >
MED_EXPORT bool pyncppToCPP(PyObject* nativeObject, TYPE** output)
{
    return pyncppToCPP(nativeObject, (QObject**)(output));
}

#endif // MED_QT_QOBJECT_H
