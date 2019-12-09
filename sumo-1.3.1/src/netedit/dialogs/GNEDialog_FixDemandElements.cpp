/****************************************************************************/
// Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
// Copyright (C) 2001-2019 German Aerospace Center (DLR) and others.
// This program and the accompanying materials
// are made available under the terms of the Eclipse Public License v2.0
// which accompanies this distribution, and is available at
// http://www.eclipse.org/legal/epl-v20.html
// SPDX-License-Identifier: EPL-2.0
/****************************************************************************/
/// @file    GNEDialog_FixDemandElements.cpp
/// @author  Pablo Alvarez Lopez
/// @date    Jul 2017
/// @version $Id$
///
// Dialog used to fix demand elements during saving
/****************************************************************************/

// ===========================================================================
// included modules
// ===========================================================================
#include <config.h>

#include <utils/gui/windows/GUIAppEnum.h>
#include <utils/gui/div/GUIDesigns.h>
#include <netedit/demandelements/GNEDemandElement.h>
#include <netedit/GNENet.h>
#include <netedit/GNEViewNet.h>
#include <netedit/GNEUndoList.h>

#include "GNEDialog_FixDemandElements.h"


// ===========================================================================
// FOX callback mapping
// ===========================================================================

FXDEFMAP(GNEDialog_FixDemandElements) GNEDialog_FixDemandElementsMap[] = {
    FXMAPFUNC(SEL_COMMAND,  MID_CHOOSEN_OPERATION,                  GNEDialog_FixDemandElements::onCmdSelectOption),
    FXMAPFUNC(SEL_COMMAND,  MID_GNE_ADDITIONALDIALOG_BUTTONACCEPT,  GNEDialog_FixDemandElements::onCmdAccept),
    FXMAPFUNC(SEL_COMMAND,  MID_GNE_ADDITIONALDIALOG_BUTTONCANCEL,  GNEDialog_FixDemandElements::onCmdCancel),
};

// Object implementation
FXIMPLEMENT(GNEDialog_FixDemandElements, FXDialogBox, GNEDialog_FixDemandElementsMap, ARRAYNUMBER(GNEDialog_FixDemandElementsMap))

// ===========================================================================
// member method definitions
// ===========================================================================

GNEDialog_FixDemandElements::GNEDialog_FixDemandElements(GNEViewNet* viewNet, const std::vector<GNEDemandElement*>& invalidDemandElements) :
    FXDialogBox(viewNet->getApp(), "Fix demand elements problems", GUIDesignDialogBoxExplicit(500, 420)),
    myViewNet(viewNet) {
    // set busStop icon for this dialog
    setIcon(GUIIconSubSys::getIcon(ICON_ROUTE));
    // create main frame
    myMainFrame = new FXVerticalFrame(this, GUIDesignAuxiliarFrame);
    // create demand list
    myDemandList = new DemandList(this, invalidDemandElements);
    // create fix route options
    myFixRouteOptions = new FixRouteOptions(this);
    // create fix vehicle  options
    myFixVehicleOptions = new FixVehicleOptions(this);
    // create fix stops options
    myFixStopOptions = new FixStopOptions(this);
    // check if fix route options has to be disabled
    if (myDemandList->myInvalidRoutes.empty()) {
        myFixRouteOptions->disableFixRouteOptions();
    }
    // check if fix vehicle options has to be disabled
    if (myDemandList->myInvalidVehicles.empty()) {
        myFixVehicleOptions->disableFixVehicleOptions();
    }
    // check if fix vehicle options has to be disabled
    if (myDemandList->myInvalidVehicles.empty()) {
        myFixStopOptions->disableFixStopOptions();
    }
    // create dialog buttons bot centered
    FXHorizontalFrame* buttonsFrame = new FXHorizontalFrame(myMainFrame, GUIDesignHorizontalFrame);
    new FXHorizontalFrame(buttonsFrame, GUIDesignAuxiliarHorizontalFrame);
    myAcceptButton = new FXButton(buttonsFrame, FXWindow::tr("&Accept"), GUIIconSubSys::getIcon(ICON_ACCEPT), this, MID_GNE_ADDITIONALDIALOG_BUTTONACCEPT, GUIDesignButtonAccept);
    myCancelButton = new FXButton(buttonsFrame, FXWindow::tr("&Cancel"), GUIIconSubSys::getIcon(ICON_CANCEL), this, MID_GNE_ADDITIONALDIALOG_BUTTONCANCEL, GUIDesignButtonCancel);
    new FXHorizontalFrame(buttonsFrame, GUIDesignAuxiliarHorizontalFrame);
    // set focus in accept button
    myAcceptButton->setFocus();
}


GNEDialog_FixDemandElements::~GNEDialog_FixDemandElements() {
}


long
GNEDialog_FixDemandElements::onCmdSelectOption(FXObject* obj, FXSelector, void*) {
    myFixRouteOptions->selectOption(obj);
    myFixVehicleOptions->selectOption(obj);
    myFixStopOptions->selectOption(obj);
    return 1;
}


long
GNEDialog_FixDemandElements::onCmdAccept(FXObject*, FXSelector, void*) {
    bool continueSaving = true;
    // first check options for invalid routes
    if (myDemandList->myInvalidRoutes.size() > 0) {
        if (myFixRouteOptions->removeInvalidRoutes->getCheck() == TRUE) {
            // begin undo list
            myViewNet->getUndoList()->p_begin("delete invalid routes");
            // iterate over invalid routes to delete it
            for (auto i : myDemandList->myInvalidRoutes) {
                myViewNet->getNet()->deleteDemandElement(i, myViewNet->getUndoList());
            }
            // end undo list
            myViewNet->getUndoList()->p_end();
        } else if (myFixRouteOptions->selectInvalidRoutesAndCancel->getCheck() == TRUE) {
            // begin undo list
            myViewNet->getUndoList()->p_begin("select invalid routes");
            // iterate over invalid single lane elements to select all elements
            for (auto i : myDemandList->myInvalidRoutes) {
                i->setAttribute(GNE_ATTR_SELECTED, "true", myViewNet->getUndoList());
            }
            // end undo list
            myViewNet->getUndoList()->p_end();
            // abort saving
            continueSaving = false;
        }
    }
    // first check options for invalid vehicles
    if (myDemandList->myInvalidVehicles.size() > 0) {
        if (myFixVehicleOptions->removeInvalidVehicles->getCheck() == TRUE) {
            // begin undo list
            myViewNet->getUndoList()->p_begin("delete invalid vehicles");
            // iterate over invalid stops to delete it
            for (auto i : myDemandList->myInvalidVehicles) {
                myViewNet->getNet()->deleteDemandElement(i, myViewNet->getUndoList());
            }
            // end undo list
            myViewNet->getUndoList()->p_end();
        } else if (myFixVehicleOptions->selectInvalidVehiclesAndCancel->getCheck() == TRUE) {
            // begin undo list
            myViewNet->getUndoList()->p_begin("select invalid vehicles");
            // iterate over invalid single lane elements to select all elements
            for (auto i : myDemandList->myInvalidVehicles) {
                i->setAttribute(GNE_ATTR_SELECTED, "true", myViewNet->getUndoList());
            }
            // end undo list
            myViewNet->getUndoList()->p_end();
            // abort saving
            continueSaving = false;
        }
    }
    // first check options for stops
    if (myDemandList->myInvalidStops.size() > 0) {
        if (myFixStopOptions->activateFriendlyPositionAndSave->getCheck() == TRUE) {
            // begin undo list
            myViewNet->getUndoList()->p_begin("change " + toString(SUMO_ATTR_FRIENDLY_POS) + " of invalid stops");
            // iterate over invalid stops to enable friendly position
            for (auto i : myDemandList->myInvalidStops) {
                i->setAttribute(SUMO_ATTR_FRIENDLY_POS, "true", myViewNet->getUndoList());
            }
            myViewNet->getUndoList()->p_end();
        } else if (myFixStopOptions->fixPositionsAndSave->getCheck() == TRUE) {
            myViewNet->getUndoList()->p_begin("fix positions of invalid stops");
            // iterate over invalid stops to fix positions
            for (auto i : myDemandList->myInvalidStops) {
                i->fixDemandElementProblem();
            }
            myViewNet->getUndoList()->p_end();
        } else if (myFixStopOptions->selectInvalidStopsAndCancel->getCheck() == TRUE) {
            myViewNet->getUndoList()->p_begin("select invalid stops");
            // iterate over invalid stops to select all elements
            for (auto i : myDemandList->myInvalidStops) {
                i->setAttribute(GNE_ATTR_SELECTED, "true", myViewNet->getUndoList());
            }
            // end undo list
            myViewNet->getUndoList()->p_end();
            // abort saving
            continueSaving = false;
        }
    }
    if (continueSaving) {
        // stop modal with TRUE (continue saving)
        getApp()->stopModal(this, TRUE);
    } else {
        // stop modal with TRUE (abort saving)
        getApp()->stopModal(this, FALSE);
    }
    return 1;
}


long
GNEDialog_FixDemandElements::onCmdCancel(FXObject*, FXSelector, void*) {
    // Stop Modal (abort saving)
    getApp()->stopModal(this, FALSE);
    return 1;
}

// ---------------------------------------------------------------------------
// GNEDialog_FixDemandElements::DemandList - methods
// ---------------------------------------------------------------------------

GNEDialog_FixDemandElements::DemandList::DemandList(GNEDialog_FixDemandElements* fixDemandElementsDialogParents, const std::vector<GNEDemandElement*>& invalidDemandElements) :
    FXGroupBox(fixDemandElementsDialogParents->myMainFrame, "Routes and Vehicles with conflicts", GUIDesignGroupBoxFrameFill) {
    // Create table, copy intervals and update table
    myTable = new FXTable(this, this, MID_GNE_FIXSTOPPINGPLACES_CHANGE, GUIDesignTableAdditionals);
    myTable->setSelBackColor(FXRGBA(255, 255, 255, 255));
    myTable->setSelTextColor(FXRGBA(0, 0, 0, 255));
    myTable->setEditable(false);
    // separate demand elements in three groups
    for (const auto& i : invalidDemandElements) {
        if (i->getTagProperty().isVehicle()) {
            myInvalidVehicles.push_back(i);
        } else if (i->getTagProperty().isStop()) {
            myInvalidStops.push_back(i);
        } else {
            myInvalidRoutes.push_back(i);
        }
    }
    // clear table
    myTable->clearItems();
    // set number of rows
    myTable->setTableSize((int)(myInvalidRoutes.size() + myInvalidVehicles.size()), 3);
    // Configure list
    myTable->setVisibleColumns(4);
    myTable->setColumnWidth(0, GUIDesignTableIconCellWidth);
    myTable->setColumnWidth(1, 160);
    myTable->setColumnWidth(2, 280);
    myTable->setColumnText(0, "");
    myTable->setColumnText(1, toString(SUMO_ATTR_ID).c_str());
    myTable->setColumnText(2, "Conflict");
    myTable->getRowHeader()->setWidth(0);
    // Declare index for rows and pointer to FXTableItem
    int indexRow = 0;
    FXTableItem* item = nullptr;
    // iterate over invalid routes
    for (auto i : myInvalidRoutes) {
        // Set icon
        item = new FXTableItem("", i->getIcon());
        item->setIconPosition(FXTableItem::CENTER_X);
        myTable->setItem(indexRow, 0, item);
        // Set ID
        item = new FXTableItem(i->getID().c_str());
        item->setJustify(FXTableItem::LEFT | FXTableItem::CENTER_Y);
        myTable->setItem(indexRow, 1, item);
        // Set conflict
        item = new FXTableItem(i->getDemandElementProblem().c_str());
        item->setJustify(FXTableItem::LEFT | FXTableItem::CENTER_Y);
        myTable->setItem(indexRow, 2, item);
        // Update index
        indexRow++;
    }
    // iterate over invalid vehicles
    for (auto i : myInvalidVehicles) {
        // Set icon
        item = new FXTableItem("", i->getIcon());
        item->setIconPosition(FXTableItem::CENTER_X);
        myTable->setItem(indexRow, 0, item);
        // Set ID
        item = new FXTableItem(i->getID().c_str());
        item->setJustify(FXTableItem::LEFT | FXTableItem::CENTER_Y);
        myTable->setItem(indexRow, 1, item);
        // Set conflict
        item = new FXTableItem(i->getDemandElementProblem().c_str());
        item->setJustify(FXTableItem::LEFT | FXTableItem::CENTER_Y);
        myTable->setItem(indexRow, 2, item);
        // Update index
        indexRow++;
    }
    // iterate over invalid stops
    for (auto i : myInvalidStops) {
        // Set icon
        item = new FXTableItem("", i->getIcon());
        item->setIconPosition(FXTableItem::CENTER_X);
        myTable->setItem(indexRow, 0, item);
        // Set ID
        item = new FXTableItem(i->getID().c_str());
        item->setJustify(FXTableItem::LEFT | FXTableItem::CENTER_Y);
        myTable->setItem(indexRow, 1, item);
        // Set conflict
        item = new FXTableItem(i->getDemandElementProblem().c_str());
        item->setJustify(FXTableItem::LEFT | FXTableItem::CENTER_Y);
        myTable->setItem(indexRow, 2, item);
        // Update index
        indexRow++;
    }
}


// ---------------------------------------------------------------------------
// GNEDialog_FixDemandElements::FixRouteOptions - methods
// ---------------------------------------------------------------------------

GNEDialog_FixDemandElements::FixRouteOptions::FixRouteOptions(GNEDialog_FixDemandElements* fixDemandElementsDialogParents) :
    FXGroupBox(fixDemandElementsDialogParents->myMainFrame, "Solution for routes", GUIDesignGroupBoxFrame) {
    // create horizontal frames for radio buttons
    FXHorizontalFrame* radioButtonsFrame = new FXHorizontalFrame(this, GUIDesignHorizontalFrame);
    // create radio button for remove invalid routes
    removeInvalidRoutes = new FXRadioButton(radioButtonsFrame, "Remove invalid routes",
                                            fixDemandElementsDialogParents, MID_CHOOSEN_OPERATION, GUIDesignRadioButton);
    // create radio button for save invalid routes
    saveInvalidRoutes = new FXRadioButton(radioButtonsFrame, "Save invalid routes",
                                          fixDemandElementsDialogParents, MID_CHOOSEN_OPERATION, GUIDesignRadioButton);
    // create radio button for select invalid routes
    selectInvalidRoutesAndCancel = new FXRadioButton(radioButtonsFrame, "Select invalid routes",
            fixDemandElementsDialogParents, MID_CHOOSEN_OPERATION, GUIDesignRadioButton);
    // leave option "removeInvalidRoutes" as default
    removeInvalidRoutes->setCheck(true);
}


void
GNEDialog_FixDemandElements::FixRouteOptions::selectOption(FXObject* option) {
    if (option == removeInvalidRoutes) {
        removeInvalidRoutes->setCheck(true);
        saveInvalidRoutes->setCheck(false);
        selectInvalidRoutesAndCancel->setCheck(false);
    } else if (option == saveInvalidRoutes) {
        removeInvalidRoutes->setCheck(false);
        saveInvalidRoutes->setCheck(true);
        selectInvalidRoutesAndCancel->setCheck(false);
    } else if (option == selectInvalidRoutesAndCancel) {
        removeInvalidRoutes->setCheck(false);
        saveInvalidRoutes->setCheck(false);
        selectInvalidRoutesAndCancel->setCheck(true);
    }
}


void
GNEDialog_FixDemandElements::FixRouteOptions::enableFixRouteOptions() {
    removeInvalidRoutes->enable();
    saveInvalidRoutes->enable();
    selectInvalidRoutesAndCancel->enable();
}


void
GNEDialog_FixDemandElements::FixRouteOptions::disableFixRouteOptions() {
    removeInvalidRoutes->disable();
    saveInvalidRoutes->disable();
    selectInvalidRoutesAndCancel->disable();
}

// ---------------------------------------------------------------------------
// GNEDialog_FixDemandElements::FixVehicleOptions - methods
// ---------------------------------------------------------------------------

GNEDialog_FixDemandElements::FixVehicleOptions::FixVehicleOptions(GNEDialog_FixDemandElements* fixDemandElementsDialogParents) :
    FXGroupBox(fixDemandElementsDialogParents->myMainFrame, "Solution for vehicles", GUIDesignGroupBoxFrame) {
    // create horizontal frames for radio buttons
    FXHorizontalFrame* radioButtonsFrame = new FXHorizontalFrame(this, GUIDesignHorizontalFrame);
    // create radio button for remove invalid vehicles
    removeInvalidVehicles = new FXRadioButton(radioButtonsFrame, "Remove invalid vehicles",
            fixDemandElementsDialogParents, MID_CHOOSEN_OPERATION, GUIDesignRadioButton);
    // create radio button for save invalid vehicles
    saveInvalidVehicles = new FXRadioButton(radioButtonsFrame, "Save invalid vehicles",
                                            fixDemandElementsDialogParents, MID_CHOOSEN_OPERATION, GUIDesignRadioButton);
    // create radio button for select invalid vehicles
    selectInvalidVehiclesAndCancel = new FXRadioButton(radioButtonsFrame, "Select invalid vehicle",
            fixDemandElementsDialogParents, MID_CHOOSEN_OPERATION, GUIDesignRadioButton);
    // leave option "buildConnectionBetweenLanes" and "removeInvalidRoutes" as default
    removeInvalidVehicles->setCheck(true);
}


void
GNEDialog_FixDemandElements::FixVehicleOptions::selectOption(FXObject* option) {
    if (option == removeInvalidVehicles) {
        removeInvalidVehicles->setCheck(true);
        saveInvalidVehicles->setCheck(false);
        selectInvalidVehiclesAndCancel->setCheck(false);
    } else if (option == saveInvalidVehicles) {
        removeInvalidVehicles->setCheck(false);
        saveInvalidVehicles->setCheck(true);
        selectInvalidVehiclesAndCancel->setCheck(false);
    } else if (option == selectInvalidVehiclesAndCancel) {
        removeInvalidVehicles->setCheck(false);
        saveInvalidVehicles->setCheck(false);
        selectInvalidVehiclesAndCancel->setCheck(true);
    }
}


void
GNEDialog_FixDemandElements::FixVehicleOptions::enableFixVehicleOptions() {
    removeInvalidVehicles->enable();
    saveInvalidVehicles->enable();
    selectInvalidVehiclesAndCancel->enable();
}


void
GNEDialog_FixDemandElements::FixVehicleOptions::disableFixVehicleOptions() {
    removeInvalidVehicles->disable();
    saveInvalidVehicles->disable();
    selectInvalidVehiclesAndCancel->disable();
}

// ---------------------------------------------------------------------------
// GNEDialog_FixDemandElements::FixStopOptions - methods
// ---------------------------------------------------------------------------

GNEDialog_FixDemandElements::FixStopOptions::FixStopOptions(GNEDialog_FixDemandElements* fixDemandElementsDialogParents) :
    FXGroupBox(fixDemandElementsDialogParents->myMainFrame, "Select a solution for stops", GUIDesignGroupBoxFrame) {
    // create horizontal frames for radio buttons
    FXHorizontalFrame* RadioButtons = new FXHorizontalFrame(this, GUIDesignHorizontalFrame);
    // create Vertical Frame for left options
    FXVerticalFrame* RadioButtonsLeft = new FXVerticalFrame(RadioButtons, GUIDesignAuxiliarVerticalFrame);
    activateFriendlyPositionAndSave = new FXRadioButton(RadioButtonsLeft, "Activate friendlyPos and save",
            fixDemandElementsDialogParents, MID_CHOOSEN_OPERATION, GUIDesignRadioButton);
    saveInvalid = new FXRadioButton(RadioButtonsLeft, "Save invalid positions",
                                    fixDemandElementsDialogParents, MID_CHOOSEN_OPERATION, GUIDesignRadioButton);
    // create Vertical Frame for right options
    FXVerticalFrame* RadioButtonsRight = new FXVerticalFrame(RadioButtons, GUIDesignAuxiliarVerticalFrame);
    selectInvalidStopsAndCancel = new FXRadioButton(RadioButtonsRight, "Select invalid Stops",
            fixDemandElementsDialogParents, MID_CHOOSEN_OPERATION, GUIDesignRadioButton);
    fixPositionsAndSave = new FXRadioButton(RadioButtonsRight, "Fix positions and save",
                                            fixDemandElementsDialogParents, MID_CHOOSEN_OPERATION, GUIDesignRadioButton);
    // leave option "activateFriendlyPositionAndSave" as default
    activateFriendlyPositionAndSave->setCheck(true);
}


void
GNEDialog_FixDemandElements::FixStopOptions::selectOption(FXObject* option) {
    if (option == activateFriendlyPositionAndSave) {
        activateFriendlyPositionAndSave->setCheck(true);
        fixPositionsAndSave->setCheck(false);
        saveInvalid->setCheck(false);
        selectInvalidStopsAndCancel->setCheck(false);
    } else if (option == fixPositionsAndSave) {
        activateFriendlyPositionAndSave->setCheck(false);
        fixPositionsAndSave->setCheck(true);
        saveInvalid->setCheck(false);
        selectInvalidStopsAndCancel->setCheck(false);
    } else if (option == saveInvalid) {
        activateFriendlyPositionAndSave->setCheck(false);
        fixPositionsAndSave->setCheck(false);
        saveInvalid->setCheck(true);
        selectInvalidStopsAndCancel->setCheck(false);
    } else if (option == selectInvalidStopsAndCancel) {
        activateFriendlyPositionAndSave->setCheck(false);
        fixPositionsAndSave->setCheck(false);
        saveInvalid->setCheck(false);
        selectInvalidStopsAndCancel->setCheck(true);
    }
}


void
GNEDialog_FixDemandElements::FixStopOptions::enableFixStopOptions() {
    activateFriendlyPositionAndSave->enable();
    fixPositionsAndSave->enable();
    saveInvalid->enable();
    selectInvalidStopsAndCancel->enable();
}


void
GNEDialog_FixDemandElements::FixStopOptions::disableFixStopOptions() {
    activateFriendlyPositionAndSave->disable();
    fixPositionsAndSave->disable();
    saveInvalid->disable();
    selectInvalidStopsAndCancel->disable();
}

/****************************************************************************/
