/****************************************************************************/
// Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
// Copyright (C) 2001-2019 German Aerospace Center (DLR) and others.
// This program and the accompanying materials
// are made available under the terms of the Eclipse Public License v2.0
// which accompanies this distribution, and is available at
// http://www.eclipse.org/legal/epl-v20.html
// SPDX-License-Identifier: EPL-2.0
/****************************************************************************/
/// @file    GUIBusStop.cpp
/// @author  Daniel Krajzewicz
/// @author  Jakob Erdmann
/// @author  Michael Behrisch
/// @date    Wed, 07.12.2005
/// @version $Id$
///
// A lane area vehicles can halt at (gui-version)
/****************************************************************************/


// ===========================================================================
// included modules
// ===========================================================================
#include <config.h>

#include <string>
#include <utils/common/MsgHandler.h>
#include <utils/geom/PositionVector.h>
#include <utils/geom/Boundary.h>
#include <utils/gui/div/GLHelper.h>
#include <utils/common/ToString.h>
#include <microsim/MSNet.h>
#include <microsim/MSLane.h>
#include <microsim/MSEdge.h>
#include "GUINet.h"
#include "GUIEdge.h"
#include "GUIPerson.h"
#include "GUIBusStop.h"
#include <utils/gui/globjects/GUIGLObjectPopupMenu.h>
#include <utils/gui/windows/GUIAppEnum.h>
#include <gui/GUIGlobals.h>
#include <utils/gui/div/GUIParameterTableWindow.h>
#include <gui/GUIApplicationWindow.h>
#include <microsim/logging/FunctionBinding.h>
#include <utils/gui/div/GUIGlobalSelection.h>
#include <foreign/fontstash/fontstash.h>
#include <utils/geom/GeomHelper.h>
#include <guisim/GUIBusStop.h>
#include <utils/gui/globjects/GLIncludes.h>



// ===========================================================================
// method definitions
// ===========================================================================
GUIBusStop::GUIBusStop(const std::string& id, const std::vector<std::string>& lines, MSLane& lane,
                       double frompos, double topos, const std::string name, int personCapacity) :
    MSStoppingPlace(id, lines, lane, frompos, topos, name, personCapacity),
    GUIGlObject_AbstractAdd(GLO_BUS_STOP, id),
    myPersonExaggeration(1) {
    const double offsetSign = MSNet::getInstance()->lefthand() ? -1 : 1;
    myWidth = MAX2(1.0, ceil(personCapacity / getPersonsAbreast()) * SUMO_const_waitingPersonDepth);
    myFGShape = lane.getShape();
    myFGShape.move2side((lane.getWidth() + myWidth) * 0.45 * offsetSign);
    myFGShape = myFGShape.getSubpart(
                    lane.interpolateLanePosToGeometryPos(frompos),
                    lane.interpolateLanePosToGeometryPos(topos));
    myFGShapeRotations.reserve(myFGShape.size() - 1);
    myFGShapeLengths.reserve(myFGShape.size() - 1);
    int e = (int) myFGShape.size() - 1;
    for (int i = 0; i < e; ++i) {
        const Position& f = myFGShape[i];
        const Position& s = myFGShape[i + 1];
        myFGShapeLengths.push_back(f.distanceTo(s));
        myFGShapeRotations.push_back((double) atan2((s.x() - f.x()), (f.y() - s.y())) * (double) 180.0 / (double) M_PI);
    }
    PositionVector tmp = myFGShape;
    tmp.move2side(myWidth / 2 * offsetSign);
    myFGSignPos = tmp.getLineCenter();
    myFGSignRot = 0;
    if (tmp.length() != 0) {
        myFGSignRot = myFGShape.rotationDegreeAtOffset(double((myFGShape.length() / 2.)));
        myFGSignRot -= 90;
    }
}


GUIBusStop::~GUIBusStop() {}


bool
GUIBusStop::addAccess(MSLane* lane, const double pos, const double length) {
    bool added = MSStoppingPlace::addAccess(lane, pos, length);
    if (added) {
        myAccessCoords.push_back(lane->geometryPositionAtOffset(pos));
    }
    return added;
}


GUIGLObjectPopupMenu*
GUIBusStop::getPopUpMenu(GUIMainWindow& app,
                         GUISUMOAbstractView& parent) {
    GUIGLObjectPopupMenu* ret = new GUIGLObjectPopupMenu(app, parent, *this);
    buildPopupHeader(ret, app);
    buildCenterPopupEntry(ret);
    buildNameCopyPopupEntry(ret);
    buildSelectionPopupEntry(ret);
    buildShowParamsPopupEntry(ret);
    buildPositionCopyEntry(ret, false);
    return ret;
}


GUIParameterTableWindow*
GUIBusStop::getParameterWindow(GUIMainWindow& app,
                               GUISUMOAbstractView&) {
    GUIParameterTableWindow* ret =
        new GUIParameterTableWindow(app, *this, 7);
    // add items
    ret->mkItem("name", false, getMyName());
    ret->mkItem("begin position [m]", false, myBegPos);
    ret->mkItem("end position [m]", false, myEndPos);
    ret->mkItem("person capacity [#]", false, myTransportableCapacity);
    ret->mkItem("person number [#]", true, new FunctionBinding<GUIBusStop, int>(this, &MSStoppingPlace::getTransportableNumber));
    ret->mkItem("stopped vehicles[#]", true, new FunctionBinding<GUIBusStop, int>(this, &MSStoppingPlace::getStoppedVehicleNumber));
    ret->mkItem("last free pos[m]", true, new FunctionBinding<GUIBusStop, double>(this, &MSStoppingPlace::getLastFreePos));
    // close building
    ret->closeBuilding();
    return ret;
}


void
GUIBusStop::drawGL(const GUIVisualizationSettings& s) const {
    glPushName(getGlID());
    glPushMatrix();
    // draw the area
    glTranslated(0, 0, getType());
    GLHelper::setColor(s.colorSettings.busStop);
    const double exaggeration = s.addSize.getExaggeration(s, this);
    const double offset = myWidth * 0.5 * MAX2(0.0, exaggeration - 1);
    GLHelper::drawBoxLines(myFGShape, myFGShapeRotations, myFGShapeLengths, myWidth * 0.5 * exaggeration, 0, offset);
    // draw details unless zoomed out to far
    if (s.drawDetail(s.detailSettings.stoppingPlaceDetails, exaggeration)) {
        glPushMatrix();
        // draw the lines
        const double rotSign = MSNet::getInstance()->lefthand() ? 1 : -1;
        // Iterate over every line
        for (int i = 0; i < (int)myLines.size(); ++i) {
            // push a new matrix for every line
            glPushMatrix();
            // traslate and rotate
            glTranslated(myFGSignPos.x(), myFGSignPos.y(), 0);
            glRotated(rotSign * myFGSignRot, 0, 0, 1);
            // draw line
            GLHelper::drawText(myLines[i].c_str(), Position(1.2, (double)i), .1, 1.f, s.colorSettings.busStop, 0, FONS_ALIGN_LEFT);
            // pop matrix for every line
            glPopMatrix();
        }
        for (std::vector<Position>::const_iterator i = myAccessCoords.begin(); i != myAccessCoords.end(); ++i) {
            GLHelper::drawBoxLine(*i, RAD2DEG(myFGSignPos.angleTo2D(*i)) - 90, myFGSignPos.distanceTo2D(*i), .05);
        }
        // draw the sign
        glTranslated(myFGSignPos.x(), myFGSignPos.y(), 0);
        int noPoints = 9;
        if (s.scale * exaggeration > 25) {
            noPoints = MIN2((int)(9.0 + (s.scale * exaggeration) / 10.0), 36);
        }
        glScaled(exaggeration, exaggeration, 1);
        GLHelper::drawFilledCircle((double) 1.1, noPoints);
        glTranslated(0, 0, .1);
        GLHelper::setColor(s.colorSettings.busStop_sign);
        GLHelper::drawFilledCircle((double) 0.9, noPoints);
        if (s.drawDetail(s.detailSettings.stoppingPlaceText, exaggeration)) {
            GLHelper::drawText("H", Position(), .1, 1.6, s.colorSettings.busStop, myFGSignRot);
        }
        glPopMatrix();
    }
    if (s.addFullName.show && getMyName() != "") {
        GLHelper::drawTextSettings(s.addFullName, getMyName(), myFGSignPos, s.scale, s.getTextAngle(myFGSignRot), GLO_MAX - getType());
    }
    if (exaggeration > 1) {
        myPersonExaggeration = s.personSize.getExaggeration(s, nullptr);
    }
    glPopMatrix();
    glPopName();
    drawName(myFGSignPos, s.scale, s.addName, s.angle);
}


Boundary
GUIBusStop::getCenteringBoundary() const {
    Boundary b = myFGShape.getBoxBoundary();
    b.grow(SUMO_const_laneWidth);
    for (const Position& p : myAccessCoords) {
        b.add(p);
    }
    return b;
}

const std::string
GUIBusStop::getOptionalName() const {
    return myName;
}

Position
GUIBusStop::getWaitPosition(MSTransportable* t) const {
    Position result = MSStoppingPlace::getWaitPosition(t);
    if (myPersonExaggeration > 1) {
        Position ref = myLane.getShape().positionAtOffset(myLane.interpolateLanePosToGeometryPos((myBegPos + myEndPos) / 2),
                       myLane.getWidth() / 2);
        result = ref + (result - ref) * myPersonExaggeration;
    }
    return result;
}

/****************************************************************************/
