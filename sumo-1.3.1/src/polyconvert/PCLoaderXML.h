/****************************************************************************/
// Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
// Copyright (C) 2001-2019 German Aerospace Center (DLR) and others.
// This program and the accompanying materials
// are made available under the terms of the Eclipse Public License v2.0
// which accompanies this distribution, and is available at
// http://www.eclipse.org/legal/epl-v20.html
// SPDX-License-Identifier: EPL-2.0
/****************************************************************************/
/// @file    PCLoaderXML.h
/// @author  Daniel Krajzewicz
/// @author  Jakob Erdmann
/// @author  Michael Behrisch
/// @date    Thu, 02.11.2006
/// @version $Id$
///
// A reader for polygons and pois stored in XML-format
/****************************************************************************/
#ifndef PCLoaderXML_h
#define PCLoaderXML_h


// ===========================================================================
// included modules
// ===========================================================================
#include <config.h>

#include <string>
#include "PCPolyContainer.h"
#include "PCTypeMap.h"
#include <utils/shapes/ShapeHandler.h>
#include <utils/common/UtilExceptions.h>


// ===========================================================================
// class definitions
// ===========================================================================
class OptionsCont;


// ===========================================================================
// class declarations
// ===========================================================================
/**
 * @class PCLoaderXML
 * @brief A reader for polygons and pois stored in XML-format
 *
 * Reads pois stored as XML definition. The definitions must match
 *  the format POLYCONVERT generates.
 */
class PCLoaderXML : public ShapeHandler {
public:
    /** @brief Loads pois/polygons assumed to be stored as XML
     *
     * If the option "xml" is set within the given options container,
     *  an instance of PCLoaderXML is built and used as a handler for the
     *  files given in this option.
     *
     * @param[in] oc The options container to get further options from
     * @param[in] toFill The poly/pois container to add loaded polys/pois to
     * @param[in] tm The type map to use for setting values of loaded polys/pois
     * @exception ProcessError if something fails
     */
    static void loadIfSet(OptionsCont& oc, PCPolyContainer& toFill,
                          PCTypeMap& tm);


    Position getLanePos(const std::string& poiID, const std::string& laneID, double lanePos, double lanePosLat);

protected:
    /** @brief Constructor
     * @param[in] toFill The poly/pois container to add loaded polys/pois to
     * @param[in] tm The type map to use for setting values of loaded polys/pois
     * @param[in] oc The options container to get further options from
     */
    PCLoaderXML(PCPolyContainer& toFill,
                PCTypeMap& tm, OptionsCont& oc);


    /// @brief Destructor
    ~PCLoaderXML();


protected:
    /// @name inherited from GenericSAXHandler
    //@{

    /** @brief Called on the opening of a tag;
     *
     * @param[in] element ID of the currently opened element
     * @param[in] attrs Attributes within the currently opened element
     * @exception ProcessError If something fails
     * @see GenericSAXHandler::myStartElement
     */
    virtual void myStartElement(int element, const SUMOSAXAttributes& attrs);
    //@}


private:
    /// @brief The type map to use
    PCTypeMap& myTypeMap;

    /// @brief Settings to use
    OptionsCont& myOptions;

};


#endif

/****************************************************************************/

