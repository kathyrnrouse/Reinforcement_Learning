import subprocess, sys, os
from os.path import abspath, dirname, join
THIS_DIR = abspath(dirname(__file__))
SUMO_HOME = os.environ.get("SUMO_HOME", dirname(dirname(THIS_DIR)))
os.environ["SUMO_HOME"] = SUMO_HOME
for p in [
    subprocess.Popen([join(SUMO_HOME, "bin", "dfrouter"), "--write-license", "--include-unused-routes", "--measure-files", "input_tri_flows.txt", "--keep-longer-routes", "--net-file=input_tri.net.xml", "--detector-files=input_tri.det.xml", "--routes-output", "routes.rou.xml", "--emitters-output", "emitters.add.xml", "-e", "60"], cwd=join(THIS_DIR, r"dfrouter")),
    subprocess.Popen([join(SUMO_HOME, "bin", "duarouter"), "--no-step-log", "--write-license", "--net-file=input_net.net.xml", "--route-files=input_flows.flows.xml", "-o", "routes.rou.xml"], cwd=join(THIS_DIR, r"duarouter/flows2routes")),
    subprocess.Popen([join(SUMO_HOME, "bin", "duarouter"), "--no-step-log", "--write-license", "--net-file=input_net.net.xml", "--route-files=input_flows.flows.xml", "-o", "routes.rou.xml"], cwd=join(THIS_DIR, r"duarouter/flows2routes_100s_interval")),
    subprocess.Popen([join(SUMO_HOME, "bin", "duarouter"), "--no-step-log", "--write-license", "--net-file=input_net.net.xml", "--route-files=input_flows.flows.xml", "-o", "routes.rou.xml"], cwd=join(THIS_DIR, r"duarouter/flows2routes_100s_interval_ext")),
    subprocess.Popen([join(SUMO_HOME, "bin", "duarouter"), "--no-step-log", "--write-license", "--net-file=input_net.net.xml", "--route-files=input_flows.flows.xml", "-o", "routes.rou.xml"], cwd=join(THIS_DIR, r"duarouter/flows2routes_200s_interval")),
    subprocess.Popen([join(SUMO_HOME, "bin", "duarouter"), "--no-step-log", "--write-license", "--net-file=input_net.net.xml", "--route-files=input_trips.trips.xml", "-o", "routes.rou.xml"], cwd=join(THIS_DIR, r"duarouter/trips2routes")),
    subprocess.Popen([join(SUMO_HOME, "bin", "jtrrouter"), "--no-step-log", "--write-license", "--output-file=routes.rou.xml", "--net-file=input_net.net.xml", "--route-files=input_flows.flows.xml", "--sinks=end", "--turns=input_turns.turns.xml", "--ignore-errors"], cwd=join(THIS_DIR, r"jtrrouter/turns")),
    subprocess.Popen([join(SUMO_HOME, "bin", "jtrrouter"), "--no-step-log", "--write-license", "--net-file=input_net.net.xml", "--route-files=input_flows.flows.xml", "--output-file=routes.rou.xml", "--turn-defaults=0,100,0,0", "--sinks=end", "--ignore-errors"], cwd=join(THIS_DIR, r"jtrrouter/straight_only_sinks")),
    subprocess.Popen([join(SUMO_HOME, "bin", "netconvert"), "--write-license", "--edge-files=input_edges.edg.xml", "--connection-files", "input_connections.con.xml", "--node-files=input_nodes.nod.xml", "--output=net.net.xml", "--speed-in-kmh"], cwd=join(THIS_DIR, r"netconvert/connections/cross3l_edge2edge_conns")),
    subprocess.Popen([join(SUMO_HOME, "bin", "netconvert"), "--write-license", "--edge-files=input_edges.edg.xml", "--connection-files=input_connections.con.xml", "--node-files=input_nodes.nod.xml", "--output=net.net.xml", "--speed-in-kmh"], cwd=join(THIS_DIR, r"netconvert/connections/cross3l_lane2lane_conns")),
    subprocess.Popen([join(SUMO_HOME, "bin", "netconvert"), "--write-license", "--edge-files=input_edges.edg.xml", "--node-files=input_nodes.nod.xml", "--output=net.net.xml", "--speed-in-kmh", "--no-turnarounds"], cwd=join(THIS_DIR, r"netconvert/connections/cross3l_no_turnarounds")),
    subprocess.Popen([join(SUMO_HOME, "bin", "netconvert"), "--write-license", "--edge-files=input_edges.edg.xml", "--connection-files", "input_connections.con.xml", "--node-files=input_nodes.nod.xml", "--output=net.net.xml", "--speed-in-kmh"], cwd=join(THIS_DIR, r"netconvert/connections/cross3l_prohibitions")),
    subprocess.Popen([join(SUMO_HOME, "bin", "netconvert"), "--write-license", "--edge-files=input_edges.edg.xml", "--node-files=input_nodes.nod.xml", "--output=net.net.xml", "--speed-in-kmh"], cwd=join(THIS_DIR, r"netconvert/connections/cross3l_unconstrained")),
    subprocess.Popen([join(SUMO_HOME, "bin", "netconvert"), "--write-license", "--edge-files=input_edges.edg.xml", "--node-files=input_nodes.nod.xml", "--output=net.net.xml", "--plain-output=plain", "--plain.extend-edge-shape"], cwd=join(THIS_DIR, r"netconvert/hokkaido")),
    subprocess.Popen([join(SUMO_HOME, "bin", "netconvert"), "--write-license", "--edge-files=input_edges.edg.xml", "--node-files=input_nodes.nod.xml", "--connection-files=input_connections.con.xml", "--output=net.net.xml", "--no-turnarounds"], cwd=join(THIS_DIR, r"netconvert/dlr-testtrack")),
    subprocess.Popen([join(SUMO_HOME, "bin", "netconvert"), "--write-license", "--edge-files=input_edges.edg.xml", "--node-files=input_nodes.nod.xml", "--output=net.net.xml", "--speed-in-kmh"], cwd=join(THIS_DIR, r"netconvert/speed_in_kmh/cross_notypes_kmh")),
    subprocess.Popen([join(SUMO_HOME, "bin", "netconvert"), "--write-license", "--edge-files=input_edges.edg.xml", "--node-files=input_nodes.nod.xml", "--type-files=input_types.typ.xml", "--output=net.net.xml", "--speed-in-kmh"], cwd=join(THIS_DIR, r"netconvert/speed_in_kmh/cross_usingtypes_kmh")),
    subprocess.Popen([join(SUMO_HOME, "bin", "netconvert"), "--write-license", "--edge-files=input_edges.edg.xml", "--node-files=input_nodes.nod.xml", "--output=net.net.xml"], cwd=join(THIS_DIR, r"netconvert/types/cross_notypes")),
    subprocess.Popen([join(SUMO_HOME, "bin", "netconvert"), "--write-license", "--edge-files=input_edges.edg.xml", "--node-files=input_nodes.nod.xml", "--type-files=input_types.typ.xml", "--output=net.net.xml"], cwd=join(THIS_DIR, r"netconvert/types/cross_usingtypes")),
    subprocess.Popen([join(SUMO_HOME, "bin", "netconvert"), "--write-license", "--no-internal-links", "--osm-files", "osm.xml", "-v", "--proj.utm", "--output.street-names", "--plain-output-prefix", "plain", "--proj.plain-geo", "--output", "net.net.xml", "--tls.red.time", "10"], cwd=join(THIS_DIR, r"netconvert/OSM/adlershof_dlr")),
    subprocess.Popen([join(SUMO_HOME, "bin", "sumo"), "--write-license", "--default.speeddev", "0", "--no-step-log", "--no-duration-log", "--net-file=net.net.xml", "--routes=input_routes.rou.xml", "-b", "0", "-e", "10000"], cwd=join(THIS_DIR, r"sumo/hokkaido")),
    subprocess.Popen([join(SUMO_HOME, "bin", "sumo"), "--write-license", "--default.speeddev", "0", "-b", "0", "-e", "1000", "--no-step-log", "--no-duration-log", "--net-file=net.net.xml", "--routes=input_routes.rou.xml", "-a", "input_additional.add.xml,input_additional2.add.xml"], cwd=join(THIS_DIR, r"sumo/variable_speed_signs")),
    subprocess.Popen([join(SUMO_HOME, "bin", "sumo"), "--write-license", "--default.speeddev", "0", "--no-step-log", "--no-duration-log", "--net-file=net.net.xml", "--routes=input_routes.rou.xml", "--vehroute-output", "vehroutes.xml"], cwd=join(THIS_DIR, r"sumo/vehicle_stops")),
    subprocess.Popen([join(SUMO_HOME, "bin", "sumo"), "--write-license", "--default.speeddev", "0", "--no-step-log", "--no-duration-log", "--net-file=net.net.xml", "-a=input_additional.add.xml", "--vehroutes=vehroutes.xml"], cwd=join(THIS_DIR, r"sumo/busses")),
    subprocess.Popen([join(SUMO_HOME, "bin", "sumo"), "--write-license", "--default.speeddev", "0", "--no-step-log", "--no-duration-log", "-n", "net.net.xml", "--route-files=input_routes.rou.xml", "--additional-files=input_additional.add.xml", "--fcd-output", "fcd.xml", "--fcd-output.signals"], cwd=join(THIS_DIR, r"sumo/angled_roadside_parking")),
    subprocess.Popen([join(SUMO_HOME, "bin", "sumo"), "--write-license", "--default.speeddev", "0", "--no-step-log", "--no-duration-log", "--net-file=net.net.xml", "--routes=input_routes.rou.xml", "--time-to-teleport", "-1"], cwd=join(THIS_DIR, r"sumo/visualization/parade")),
    subprocess.Popen([join(SUMO_HOME, "bin", "sumo"), "--write-license", "--default.speeddev", "0", "--no-step-log", "--no-duration-log", "--emission-output=emissions.xml", "--net-file=net.net.xml", "-r", "input_routes.rou.xml", "-b", "0", "-e", "120"], cwd=join(THIS_DIR, r"sumo/output/cross3ltl_emission")),
    subprocess.Popen([join(SUMO_HOME, "bin", "sumo"), "--write-license", "--default.speeddev", "0", "--no-step-log", "--no-duration-log", "--fcd-output=fcd.xml", "--net-file=net.net.xml", "-r", "input_routes.rou.xml", "-b", "0", "-e", "120"], cwd=join(THIS_DIR, r"sumo/output/cross3ltl_fcd")),
    subprocess.Popen([join(SUMO_HOME, "bin", "sumo"), "--write-license", "--default.speeddev", "0", "--no-step-log", "--no-duration-log", "--full-output=full.xml", "--net-file=net.net.xml", "-r", "input_routes.rou.xml", "-b", "0", "-e", "120"], cwd=join(THIS_DIR, r"sumo/output/cross3ltl_full")),
    subprocess.Popen([join(SUMO_HOME, "bin", "sumo"), "--write-license", "--default.speeddev", "0", "--no-step-log", "--no-duration-log", "--net-file=net.net.xml", "-r", "input_routes.rou.xml", "-a", "input_additional.add.xml", "-b", "0", "-e", "1000"], cwd=join(THIS_DIR, r"sumo/output/cross3ltl_inductloops")),
    subprocess.Popen([join(SUMO_HOME, "bin", "sumo"), "--write-license", "--default.speeddev", "0", "--no-step-log", "--no-duration-log", "--net-file=net.net.xml", "-r", "input_routes.rou.xml", "-a", "input_additional.add.xml", "-b", "0", "-e", "1000"], cwd=join(THIS_DIR, r"sumo/output/cross3ltl_meandata_constrained")),
    subprocess.Popen([join(SUMO_HOME, "bin", "sumo"), "--write-license", "--default.speeddev", "0", "--no-step-log", "--no-duration-log", "--net-file=net.net.xml", "-r", "input_routes.rou.xml", "-a", "input_additional.add.xml", "-b", "0", "-e", "1000"], cwd=join(THIS_DIR, r"sumo/output/cross3ltl_meandata_edges")),
    subprocess.Popen([join(SUMO_HOME, "bin", "sumo"), "--write-license", "--default.speeddev", "0", "--no-step-log", "--no-duration-log", "--net-file=net.net.xml", "-r", "input_routes.rou.xml", "-a", "input_additional.add.xml", "-b", "0", "-e", "1000"], cwd=join(THIS_DIR, r"sumo/output/cross3ltl_meandata_lanes")),
    subprocess.Popen([join(SUMO_HOME, "bin", "sumo"), "--write-license", "--default.speeddev", "0", "--no-step-log", "--no-duration-log", "--queue-output=queue.xml", "--net-file=net.net.xml", "-r", "input_routes.rou.xml", "-b", "0", "-e", "200"], cwd=join(THIS_DIR, r"sumo/output/cross3ltl_queue")),
    subprocess.Popen([join(SUMO_HOME, "bin", "sumo"), "--write-license", "--default.speeddev", "0", "--no-step-log", "--no-duration-log", "--netstate-dump=rawdump.xml", "--net-file=net.net.xml", "-r", "input_routes.rou.xml", "-b", "90", "-e", "120"], cwd=join(THIS_DIR, r"sumo/output/cross3ltl_rawdump")),
    subprocess.Popen([join(SUMO_HOME, "bin", "sumo"), "--write-license", "--default.speeddev", "0", "--no-step-log", "--no-duration-log", "--net-file=net.net.xml", "-r", "input_routes.rou.xml", "--summary=summary.xml", "-b", "0", "-e", "1000"], cwd=join(THIS_DIR, r"sumo/output/cross3ltl_summary")),
    subprocess.Popen([join(SUMO_HOME, "bin", "sumo"), "--write-license", "--default.speeddev", "0", "--no-step-log", "--no-duration-log", "--tripinfo-output=tripinfos.xml", "--net-file=net.net.xml", "-r", "input_routes.rou.xml", "-b", "0", "-e", "1000"], cwd=join(THIS_DIR, r"sumo/output/cross3ltl_tripinfo")),
    subprocess.Popen([join(SUMO_HOME, "bin", "sumo"), "--write-license", "--default.speeddev", "0", "--no-step-log", "--no-duration-log", "--vehroute-output=vehroutes.xml", "--net-file=net.net.xml", "-r", "input_routes.rou.xml", "-b", "0", "-e", "1000"], cwd=join(THIS_DIR, r"sumo/output/cross3ltl_vehroutes")),
    subprocess.Popen([join(SUMO_HOME, "bin", "sumo"), "--write-license", "--default.speeddev", "0", "--no-step-log", "--no-duration-log", "--net-file=net.net.xml", "-r", "input_routes.rou.xml", "-a", "input_additional.add.xml", "-b", "0", "-e", "220"], cwd=join(THIS_DIR, r"sumo/output/cross3ltl_vtypeprobe")),
    subprocess.Popen([join(SUMO_HOME, "bin", "sumo"), "--write-license", "--default.speeddev", "0", "--time-to-teleport", "-1", "--no-step-log", "--no-duration-log", "--net-file=net.net.xml", "--routes=input_routes.rou.xml"], cwd=join(THIS_DIR, r"sumo/simple_nets/cross/cross1ltl")),
    subprocess.Popen([join(SUMO_HOME, "bin", "sumo"), "--write-license", "--default.speeddev", "0", "--time-to-teleport", "-1", "-v", "--no-step-log", "--net-file=net.net.xml", "--routes=input_routes.rou.xml"], cwd=join(THIS_DIR, r"sumo/simple_nets/cross/cross1l")),
    subprocess.Popen([join(SUMO_HOME, "bin", "sumo"), "--write-license", "--default.speeddev", "0", "--time-to-teleport", "-1", "--no-step-log", "--no-duration-log", "--net-file=net.net.xml", "--routes=input_routes.rou.xml"], cwd=join(THIS_DIR, r"sumo/simple_nets/cross/cross3ltl")),
    subprocess.Popen([join(SUMO_HOME, "bin", "sumo"), "--write-license", "--default.speeddev", "0", "--time-to-teleport", "-1", "--no-step-log", "--no-duration-log", "--net-file=net.net.xml", "--routes=input_routes.rou.xml"], cwd=join(THIS_DIR, r"sumo/simple_nets/cross/cross3l")),
    subprocess.Popen([join(SUMO_HOME, "bin", "sumo"), "--write-license", "--default.speeddev", "0", "--time-to-teleport", "-1", "--no-step-log", "--no-duration-log", "--net-file=net.net.xml", "--routes=input_routes.rou.xml"], cwd=join(THIS_DIR, r"sumo/simple_nets/box/box1l")),
    subprocess.Popen([join(SUMO_HOME, "bin", "sumo"), "--write-license", "--default.speeddev", "0", "--time-to-teleport", "-1", "--no-step-log", "--no-duration-log", "--net-file=net.net.xml", "--routes=input_routes.rou.xml"], cwd=join(THIS_DIR, r"sumo/simple_nets/box/box2l")),
    subprocess.Popen([join(SUMO_HOME, "bin", "sumo"), "--write-license", "--default.speeddev", "0", "--time-to-teleport", "-1", "--no-step-log", "--no-duration-log", "--net-file=net.net.xml", "--routes=input_routes.rou.xml"], cwd=join(THIS_DIR, r"sumo/simple_nets/box/box3l")),
    subprocess.Popen([join(SUMO_HOME, "bin", "sumo"), "--write-license", "--default.speeddev", "0", "--time-to-teleport", "-1", "--no-step-log", "--no-duration-log", "--net-file=net.net.xml", "--routes=input_routes.rou.xml"], cwd=join(THIS_DIR, r"sumo/simple_nets/box/box4l")),
    subprocess.Popen([join(SUMO_HOME, "bin", "sumo"), "--write-license", "--default.speeddev", "0", "--no-step-log", "--net-file=net.net.xml", "--routes=input_routes.rou.xml", "--lateral-resolution", "0.64", "--tripinfo-output", "tripinfos.xml", "--duration-log.statistics"], cwd=join(THIS_DIR, r"sumo/sublane_model")),
    subprocess.Popen(["python", join(SUMO_HOME, "tools/assign/duaIterate.py"), "-n", "input_net.net.xml", "-t", "input_trips.trips.xml", "-l", "5"], cwd=join(THIS_DIR, r"tools/dua-iterate")),
    subprocess.Popen(["python", join(SUMO_HOME, "tools/detector/flowrouter.py"), "-n", "input_net.net.xml", "-d", "input_detectors.det.xml", "-f", "input_flows.txt", "--verbose"], cwd=join(THIS_DIR, r"tools/flowrouter")),
    subprocess.Popen(["python", join(SUMO_HOME, "tools/traceExporter.py"), "-i", "fcd.xml", "-n", "net.net.xml", "--ns2mobility-output", "mobilityfile.tcl"], cwd=join(THIS_DIR, r"tools/traceExporter")),
    subprocess.Popen(["python", "./runner.py"], cwd=join(THIS_DIR, r"../tutorial/quickstart")),
    subprocess.Popen(["python", "./runner.py"], cwd=join(THIS_DIR, r"../tutorial/hello")),
    subprocess.Popen(["python", "./runner.py", "--nogui"], cwd=join(THIS_DIR, r"../tutorial/traci_tls")),
    subprocess.Popen(["python", "./runner.py"], cwd=join(THIS_DIR, r"../tutorial/manhattan")),
    subprocess.Popen(["python", "./runner.py", "Main"], cwd=join(THIS_DIR, r"traas")),
]:
    if p.wait() != 0:
        sys.exit(1)
