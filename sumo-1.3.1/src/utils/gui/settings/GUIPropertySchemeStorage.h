/****************************************************************************/
// Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
// Copyright (C) 2001-2019 German Aerospace Center (DLR) and others.
// This program and the accompanying materials
// are made available under the terms of the Eclipse Public License v2.0
// which accompanies this distribution, and is available at
// http://www.eclipse.org/legal/epl-v20.html
// SPDX-License-Identifier: EPL-2.0
/****************************************************************************/
/// @file    GUIPropertySchemeStorage.h
/// @author  Michael Behrisch
/// @author  Daniel Krajzewicz
/// @author  Jakob Erdmann
/// @author  Laura Bieker
/// @date    Mon, 20.07.2009
/// @version $Id$
///
//
/****************************************************************************/
#ifndef GUIPropertySchemeStorage_h
#define GUIPropertySchemeStorage_h


// ===========================================================================
// included modules
// ===========================================================================
#include <config.h>

#include <vector>
#include <fx.h>
#include <utils/gui/images/GUIIconSubSys.h>
#include <utils/foxtools/MFXIconComboBox.h>
#include <utils/foxtools/MFXUtils.h>
#include "GUIPropertyScheme.h"


// ===========================================================================
// class declarations
// ===========================================================================
class OutputDevice;


// ===========================================================================
// class definitions
// ===========================================================================
/**
 * @class GUIPropertySchemeStorage
 * @brief Base class for coloring. Allows changing the used colors and sets
 *  the used color in dependence to a value
 */
template<class T>
class GUIPropertySchemeStorage {
public:
    /// @brief Constructor
    GUIPropertySchemeStorage() : myActiveScheme(0) { }

    /// @brief Destructor
    virtual ~GUIPropertySchemeStorage() { }

    /// @brief Fills the given combobox with the names of available colorings
    void fill(MFXIconComboBox& cb) {
        for (const auto& scheme : mySchemes) {
            cb.appendIconItem(scheme.getName().c_str(),
                              scheme.getIcon() == ICON_EMPTY ? nullptr : GUIIconSubSys::getIcon(scheme.getIcon()),
                              MFXUtils::getFXColor(scheme.getBackgroundColor()));
        }
        cb.setCurrentItem((FXint)myActiveScheme);
    }

    void setActive(int scheme) {
        if (scheme < (int)mySchemes.size()) {
            myActiveScheme = scheme;
        }
    }

    int getActive() const {
        return myActiveScheme;
    }

    T& getScheme() {
        return mySchemes[myActiveScheme];
    }

    const T& getScheme() const {
        return mySchemes[myActiveScheme];
    }

    const std::vector<T>& getSchemes() const {
        return mySchemes;
    }

    T* getSchemeByName(std::string name) {
        for (typename std::vector<T>::iterator i = mySchemes.begin(); i != mySchemes.end(); ++i) {
            if ((*i).getName() == name) {
                return &(*i);
            }
        }
        return 0;
    }

    void setSchemeByName(std::string name) {
        for (int i = 0; i < (int)mySchemes.size(); i++) {
            if (mySchemes[i].getName() == name) {
                myActiveScheme = i;
                break;
            }
        }
    }

    void save(OutputDevice& dev) const {
        for (typename std::vector<T>::const_iterator i = mySchemes.begin(); i != mySchemes.end(); ++i) {
            i->save(dev);
        }
    }

    bool operator==(const GUIPropertySchemeStorage& c) const {
        return myActiveScheme == c.myActiveScheme && mySchemes == c.mySchemes;
    }


    void addScheme(T scheme) {
        mySchemes.push_back(scheme);
    }

    int size() const {
        return (int)mySchemes.size();
    }


protected:
    int myActiveScheme;
    std::vector<T> mySchemes;

};

typedef GUIPropertySchemeStorage<GUIColorScheme> GUIColorer;
typedef GUIPropertySchemeStorage<GUIScaleScheme> GUIScaler;

#endif

/****************************************************************************/
