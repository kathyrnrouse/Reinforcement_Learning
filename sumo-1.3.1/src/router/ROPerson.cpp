/****************************************************************************/
// Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
// Copyright (C) 2002-2019 German Aerospace Center (DLR) and others.
// This program and the accompanying materials
// are made available under the terms of the Eclipse Public License v2.0
// which accompanies this distribution, and is available at
// http://www.eclipse.org/legal/epl-v20.html
// SPDX-License-Identifier: EPL-2.0
/****************************************************************************/
/// @file    ROPerson.cpp
/// @author  Daniel Krajzewicz
/// @author  Axel Wegener
/// @author  Michael Behrisch
/// @author  Jakob Erdmann
/// @date    Sept 2002
/// @version $Id$
///
// A vehicle as used by router
/****************************************************************************/


// ===========================================================================
// included modules
// ===========================================================================
#include <config.h>

#include <string>
#include <iostream>
#include <utils/common/StringTokenizer.h>
#include <utils/common/ToString.h>
#include <utils/common/StringUtils.h>
#include <utils/common/MsgHandler.h>
#include <utils/geom/GeoConvHelper.h>
#include <utils/vehicle/SUMOVTypeParameter.h>
#include <utils/options/OptionsCont.h>
#include <utils/iodevices/OutputDevice.h>
#include "RORouteDef.h"
#include "RORoute.h"
#include "ROVehicle.h"
#include "ROHelper.h"
#include "RONet.h"
#include "ROLane.h"
#include "ROPerson.h"


// ===========================================================================
// method definitions
// ===========================================================================
ROPerson::ROPerson(const SUMOVehicleParameter& pars, const SUMOVTypeParameter* type)
    : RORoutable(pars, type) {
}


ROPerson::~ROPerson() {
    for (std::vector<PlanItem*>::const_iterator it = myPlan.begin(); it != myPlan.end(); ++it) {
        delete *it;
    }
}


void
ROPerson::addTrip(const ROEdge* const from, const ROEdge* const to, const SVCPermissions modeSet,
                  const std::string& vTypes, const double departPos, const double arrivalPos, const std::string& busStop, double walkFactor) {
    PersonTrip* trip = new PersonTrip(from, to, modeSet, departPos, arrivalPos, busStop, walkFactor);
    RONet* net = RONet::getInstance();
    SUMOVehicleParameter pars;
    pars.departProcedure = DEPART_TRIGGERED;
    if (departPos != 0) {
        pars.departPosProcedure = DEPART_POS_GIVEN;
        pars.departPos = departPos;
        pars.parametersSet |= VEHPARS_DEPARTPOS_SET;
    }
    for (StringTokenizer st(vTypes); st.hasNext();) {
        pars.vtypeid = st.next();
        pars.parametersSet |= VEHPARS_VTYPE_SET;
        SUMOVTypeParameter* type = net->getVehicleTypeSecure(pars.vtypeid);
        if (type == nullptr) {
            delete trip;
            throw InvalidArgument("The vehicle type '" + pars.vtypeid + "' in a trip for person '" + getID() + "' is not known.");
        }
        pars.id = getID() + "_" + toString(trip->getVehicles().size());
        trip->addVehicle(new ROVehicle(pars, new RORouteDef("!" + pars.id, 0, false, false), type, net));
    }
    if (trip->getVehicles().empty()) {
        if ((modeSet & SVC_PASSENGER) != 0) {
            pars.id = getID() + "_0";
            trip->addVehicle(new ROVehicle(pars, new RORouteDef("!" + pars.id, 0, false, false), net->getVehicleTypeSecure(DEFAULT_VTYPE_ID), net));
        }
        if ((modeSet & SVC_BICYCLE) != 0) {
            pars.id = getID() + "_b0";
            pars.vtypeid = DEFAULT_BIKETYPE_ID;
            pars.parametersSet |= VEHPARS_VTYPE_SET;
            trip->addVehicle(new ROVehicle(pars, new RORouteDef("!" + pars.id, 0, false, false), net->getVehicleTypeSecure(DEFAULT_BIKETYPE_ID), net));
        }
    }
    myPlan.push_back(trip);
}


void
ROPerson::addRide(const ROEdge* const from, const ROEdge* const to, const std::string& lines, double arrivalPos, const std::string& destStop) {
    if (myPlan.empty() || myPlan.back()->isStop()) {
        myPlan.push_back(new PersonTrip());
    }
    myPlan.back()->addTripItem(new Ride(from, to, lines, -1., arrivalPos, destStop));
}


void
ROPerson::addWalk(const ConstROEdgeVector& edges, const double duration, const double speed, const double departPos, const double arrivalPos, const std::string& busStop) {
    if (myPlan.empty() || myPlan.back()->isStop()) {
        myPlan.push_back(new PersonTrip());
    }
    myPlan.back()->addTripItem(new Walk(edges, -1., duration, speed, departPos, arrivalPos, busStop));
}


void
ROPerson::addStop(const SUMOVehicleParameter::Stop& stopPar, const ROEdge* const stopEdge) {
    myPlan.push_back(new Stop(stopPar, stopEdge));
}


void
ROPerson::Ride::saveAsXML(OutputDevice& os, const bool extended) const {
    os.openTag(SUMO_TAG_RIDE);
    std::string comment = "";
    if (extended && cost >= 0.) {
        os.writeAttr(SUMO_ATTR_COST, cost);
    }
    if (from != nullptr) {
        os.writeAttr(SUMO_ATTR_FROM, from->getID());
    }
    if (to != nullptr) {
        os.writeAttr(SUMO_ATTR_TO, to->getID());
    }
    if (destStop != "") {
        os.writeAttr(SUMO_ATTR_BUS_STOP, destStop);
        const std::string name = RONet::getInstance()->getStoppingPlaceName(destStop);
        if (name != "") {
            comment =  " <!-- " + name + " -->";
        }
    }
    os.writeAttr(SUMO_ATTR_LINES, lines);
    if (intended != "" && intended != lines) {
        os.writeAttr(SUMO_ATTR_INTENDED, intended);
    }
    if (depart >= 0) {
        os.writeAttr(SUMO_ATTR_DEPART, time2string(depart));
    }
    os.closeTag(comment);
}


void
ROPerson::Walk::saveAsXML(OutputDevice& os, const bool extended) const {
    os.openTag(SUMO_TAG_WALK);
    std::string comment = "";
    if (extended && cost >= 0.) {
        os.writeAttr(SUMO_ATTR_COST, cost);
    }
    if (dur > 0) {
        os.writeAttr(SUMO_ATTR_DURATION, dur);
    }
    if (v > 0) {
        os.writeAttr(SUMO_ATTR_SPEED, v);
    }
    os.writeAttr(SUMO_ATTR_EDGES, edges);
    if (dep != 0.) {
        os.writeAttr(SUMO_ATTR_DEPARTPOS, dep);
    }
    if (arr != 0. && destStop == "") {
        os.writeAttr(SUMO_ATTR_ARRIVALPOS, arr);
    }
    if (destStop != "") {
        os.writeAttr(SUMO_ATTR_BUS_STOP, destStop);
        const std::string name = RONet::getInstance()->getStoppingPlaceName(destStop);
        if (name != "") {
            comment =  " <!-- " + name + " -->";
        }
    }
    os.closeTag(comment);
}

ROPerson::PlanItem*
ROPerson::PersonTrip::clone() const {
    PersonTrip* result = new PersonTrip(from, to, modes, dep, arr, stopDest, walkFactor);
    for (auto* item : myTripItems) {
        result->myTripItems.push_back(item->clone());
    }
    return result;
}

void
ROPerson::PersonTrip::saveVehicles(OutputDevice& os, OutputDevice* const typeos, bool asAlternatives, OptionsCont& options) const {
    for (std::vector<ROVehicle*>::const_iterator it = myVehicles.begin(); it != myVehicles.end(); ++it) {
        (*it)->saveAsXML(os, typeos, asAlternatives, options);
    }
}

void
ROPerson::PersonTrip::saveAsXML(OutputDevice& os, const bool extended, const bool asTrip, const bool writeGeoTrip) const {
    if (asTrip) {
        os.openTag(SUMO_TAG_PERSONTRIP);
        if (writeGeoTrip) {
            Position fromPos = from->getLanes()[0]->getShape().positionAtOffset2D(getDepartPos());
            if (GeoConvHelper::getFinal().usingGeoProjection()) {
                os.setPrecision(gPrecisionGeo);
                GeoConvHelper::getFinal().cartesian2geo(fromPos);
                os.writeAttr(SUMO_ATTR_FROMLONLAT, fromPos);
                os.setPrecision(gPrecision);
            } else {
                os.writeAttr(SUMO_ATTR_FROMXY, fromPos);
            }
        } else {
            os.writeAttr(SUMO_ATTR_FROM, from->getID());
        }
        if (writeGeoTrip) {
            Position toPos = to->getLanes()[0]->getShape().positionAtOffset2D(MIN2(getArrivalPos(), to->getLanes()[0]->getShape().length2D()));
            if (GeoConvHelper::getFinal().usingGeoProjection()) {
                os.setPrecision(gPrecisionGeo);
                GeoConvHelper::getFinal().cartesian2geo(toPos);
                os.writeAttr(SUMO_ATTR_TOLONLAT, toPos);
                os.setPrecision(gPrecision);
            } else {
                os.writeAttr(SUMO_ATTR_TOXY, toPos);
            }
        } else {
            os.writeAttr(SUMO_ATTR_TO, to->getID());
        }
        std::vector<std::string> allowedModes;
        if ((modes & SVC_BUS) != 0) {
            allowedModes.push_back("public");
        }
        if ((modes & SVC_PASSENGER) != 0) {
            allowedModes.push_back("car");
        }
        if ((modes & SVC_BICYCLE) != 0) {
            allowedModes.push_back("bicycle");
        }
        if (allowedModes.size() > 0) {
            os.writeAttr(SUMO_ATTR_MODES, toString(allowedModes));
        }
        if (!writeGeoTrip) {
            if (dep != 0 && dep != std::numeric_limits<double>::infinity()) {
                os.writeAttr(SUMO_ATTR_DEPARTPOS, dep);
            }
            if (arr != 0 && arr != std::numeric_limits<double>::infinity()) {
                os.writeAttr(SUMO_ATTR_ARRIVALPOS, arr);
            }
        }
        if (getStopDest() != "") {
            os.writeAttr(SUMO_ATTR_BUS_STOP, getStopDest());
        }
        if (walkFactor != 1) {
            os.writeAttr(SUMO_ATTR_WALKFACTOR, walkFactor);
        }
        os.closeTag();
    } else {
        for (std::vector<TripItem*>::const_iterator it = myTripItems.begin(); it != myTripItems.end(); ++it) {
            (*it)->saveAsXML(os, extended);
        }
    }
}

SUMOTime
ROPerson::PersonTrip::getDuration() const {
    SUMOTime result = 0;
    for (TripItem* tItem : myTripItems) {
        result += tItem->getDuration();
    }
    return result;
}

bool
ROPerson::computeIntermodal(SUMOTime time, const RORouterProvider& provider,
                            PersonTrip* const trip, const ROVehicle* const veh, MsgHandler* const errorHandler) {
    std::vector<ROIntermodalRouter::TripItem> result;
    provider.getIntermodalRouter().compute(trip->getOrigin(), trip->getDestination(), trip->getDepartPos(), trip->getArrivalPos(), trip->getStopDest(),
                                           getType()->maxSpeed * trip->getWalkFactor(), veh, trip->getModes(), time, result);
    bool carUsed = false;
    for (std::vector<ROIntermodalRouter::TripItem>::const_iterator it = result.begin(); it != result.end(); ++it) {
        if (!it->edges.empty()) {
            if (it->line == "") {
                if (it + 1 == result.end() && trip->getStopDest() == "") {
                    trip->addTripItem(new Walk(it->edges, it->cost, trip->getDepartPos(false), trip->getArrivalPos(false)));
                } else {
                    trip->addTripItem(new Walk(it->edges, it->cost, trip->getDepartPos(false), trip->getArrivalPos(false), it->destStop));
                }
            } else if (veh != nullptr && it->line == veh->getID()) {
                trip->addTripItem(new Ride(it->edges.front(), it->edges.back(), veh->getID(), it->cost, trip->getArrivalPos(), it->destStop));
                veh->getRouteDefinition()->addLoadedAlternative(new RORoute(veh->getID() + "_RouteDef", it->edges));
                carUsed = true;
            } else {
                trip->addTripItem(new Ride(nullptr, nullptr, it->line, it->cost, trip->getArrivalPos(), it->destStop, it->intended, TIME2STEPS(it->depart)));
            }
        }
    }
    if (result.empty()) {
        errorHandler->inform("No route for trip in person '" + getID() + "'.");
        myRoutingSuccess = false;
    }
    return carUsed;
}


void
ROPerson::computeRoute(const RORouterProvider& provider,
                       const bool /* removeLoops */, MsgHandler* errorHandler) {
    myRoutingSuccess = true;
    SUMOTime time = getParameter().depart;
    for (std::vector<PlanItem*>::iterator it = myPlan.begin(); it != myPlan.end(); ++it) {
        if ((*it)->needsRouting()) {
            PersonTrip* trip = static_cast<PersonTrip*>(*it);
            std::vector<ROVehicle*>& vehicles = trip->getVehicles();
            if (vehicles.empty()) {
                computeIntermodal(time, provider, trip, nullptr, errorHandler);
            } else {
                for (std::vector<ROVehicle*>::iterator v = vehicles.begin(); v != vehicles.end();) {
                    if (!computeIntermodal(time, provider, trip, *v, errorHandler)) {
                        v = vehicles.erase(v);
                    } else {
                        ++v;
                    }
                }
            }
        }
        time += (*it)->getDuration();
    }
}


void
ROPerson::saveAsXML(OutputDevice& os, OutputDevice* const typeos, bool asAlternatives, OptionsCont& options) const {
    // write the person's vehicles
    const bool writeTrip = options.exists("write-trips") && options.getBool("write-trips");
    const bool writeGeoTrip = writeTrip && options.getBool("write-trips.geo");
    if (!writeTrip) {
        for (std::vector<PlanItem*>::const_iterator it = myPlan.begin(); it != myPlan.end(); ++it) {
            (*it)->saveVehicles(os, typeos, asAlternatives, options);
        }
    }

    if (typeos != nullptr && getType() != nullptr && !getType()->saved) {
        getType()->write(*typeos);
        getType()->saved = true;
    }
    if (getType() != nullptr && !getType()->saved) {
        getType()->write(os);
        getType()->saved = asAlternatives;
    }

    // write the person
    getParameter().write(os, options, SUMO_TAG_PERSON);

    for (std::vector<PlanItem*>::const_iterator it = myPlan.begin(); it != myPlan.end(); ++it) {
        (*it)->saveAsXML(os, asAlternatives, writeTrip, writeGeoTrip);
    }

    // write params
    getParameter().writeParams(os);
    os.closeTag();
}


/****************************************************************************/

