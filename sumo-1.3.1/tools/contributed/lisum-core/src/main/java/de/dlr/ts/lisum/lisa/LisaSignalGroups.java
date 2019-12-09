/****************************************************************************/
// Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
// Copyright (C) 2016-2019 German Aerospace Center (DLR) and others.
// This program and the accompanying materials
// are made available under the terms of the Eclipse Public License v2.0
// which accompanies this distribution, and is available at
// http://www.eclipse.org/legal/epl-v20.html
// SPDX-License-Identifier: EPL-2.0
/****************************************************************************/
/// @file    LisaSignalGroups.java
/// @author  Maximiliano Bottazzi
/// @date    2016
/// @version $Id$
///
//
/****************************************************************************/
package de.dlr.ts.lisum.lisa;

import de.dlr.ts.commons.logger.DLRLogger;
import de.dlr.ts.lisum.enums.LightColor;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 *
 * @author @author <a href="mailto:maximiliano.bottazzi@dlr.de">Maximiliano
 * Bottazzi</a>
 */
class LisaSignalGroups {

    private final List<LisaSignalGroup> signals = new ArrayList<>();
    private final Map<String, LisaSignalGroup> signalsMap = new HashMap<>();

    /**
     *
     */
    void load(LisaConfigurationFiles.ControlUnit controlUnit) {
        for (int i = 0; i < controlUnit.signalGroups.size(); i++) {
            LisaConfigurationFiles.ControlUnit.SignalGroup sg = controlUnit.signalGroups.get(i);
            LisaSignalGroup lisaSignalGroup = new LisaSignalGroup(sg.index, sg.bezeichnung);
            signals.add(lisaSignalGroup);
            signalsMap.put(sg.bezeichnung, lisaSignalGroup);

            DLRLogger.info(this, "Adding signal group: " + sg.bezeichnung);
        }

        Collections.sort(signals);
    }

    /**
     *
     */
    public void print() {
        for (LisaSignalGroup signal : signals) {
            DLRLogger.info(this, signal.getIndex() + " - " + signal.getName());
        }
    }

    /**
     *
     * @param line
     */
    public void parseStates(String line) {
        line = line.replaceAll("\\{", "");
        line = line.replaceAll("\\}", "");

        String[] split = line.split("/");

        for (int i = 0; i < split.length; i++) {
            int inn = new Integer(split[i]);
            signals.get(i).setColor(LightColor.getPerOcitCode(inn));
        }
    }

    /**
     *
     * @param signalIndex
     * @return
     */
    public LightColor getColor(int signalIndex) {
        if (signalIndex >= signalsCount()) {
            return LightColor.OFF;
        }

        return signals.get(signalIndex).getColor();
    }

    /**
     *
     * @param signalName
     * @return
     */
    public LightColor getColor(String signalName) {
        LisaSignalGroup get = signalsMap.get(signalName);

        if (get == null) {
            return LightColor.OFF;
        }

        return get.getColor();
    }

    /**
     *
     * @return
     */
    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();

        for (LisaSignalGroup signal : signals) {
            sb.append(signal).append(", ");
        }

        return sb.toString();
    }

    /**
     *
     * @return
     */
    public int signalsCount() {
        return this.signals.size();
    }

}
