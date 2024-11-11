// Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
// License: BSD-3-Clause

#ifndef MED_QT_QOBJECT_H
#define MED_QT_QOBJECT_H

#include <pyncpp.h>

#include <type_traits>

#include <QObject>

#include "../export.h"

PYMED_EXPORT bool pyncppToPython(const QObject* object, PyObject** output);
PYMED_EXPORT bool pyncppToCPP(PyObject* nativeObject, QObject** output);

template <class TYPE, typename = std::enable_if_t<std::is_base_of_v<QObject, TYPE> > >
bool pyncppToCPP(PyObject* nativeObject, TYPE** output)
{
    return pyncppToCPP(nativeObject, (QObject**)(output));
}

#endif // MED_QT_QOBJECT_H
