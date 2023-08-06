#!/usr/bin/env python3
import sys
import os
import importlib
import argparse
import time

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

from ..py_json.LANforge import lfcli_base
LFCliBase = lfcli_base.LFCliBase
from ..py_json.LANforge import LFUtils
from ..py_json.realm import Realm,PortUtils
 


def get_events(event_log, value):
    results = []
    for event in event_log:
        try:
            results.append(list(event.values())[0][value])
        except:
            pass
    return results


def find_new_events(original, new):
    new_times = list()
    new_events = list()
    original_times = get_events(original['events'], 'time-stamp')
    current_times = get_events(new['events'], 'time-stamp')
    for x in current_times:
        if x not in original_times:
            new_times.append(x)
    for x in new['events']:
        if list(x.values())[0]['time-stamp'] in new_times:
            new_events.append(x)
    return new_events


class LoadScenario(Realm):
    def __init__(self,
                 mgr='localhost',
                 mgr_port=8080,
                 scenario=None,
                 action='overwrite',
                 clean_dut=True,
                 clean_chambers=True,
                 start=None,
                 stop=None,
                 quiesce=None,
                 timeout=120,
                 debug=False):
        super().__init__(lfclient_host=mgr,
                         lfclient_port=mgr_port,
                         debug_=debug)
        self.mgr = mgr
        self.scenario = scenario
        self.action = action
        self.clean_dut = clean_dut
        self.clean_chambers = clean_chambers
        self.start = start
        self.stop = stop
        self.quiesce = quiesce
        self.timeout = timeout

        starting_events = self.json_get('/events/since=time/1h')

        if self.scenario is not None:
            data = {
                "name": self.scenario,
                "action": self.action,
                "clean_dut": "no",
                "clean_chambers": "no"
            }
            if self.clean_dut:
                data['clean_dut'] = "yes"
            if self.clean_chambers:
                data['clean_chambers'] = "yes"
            print("Loading database %s" % self.scenario)
            self.json_post("/cli-json/load", data)
        elif self.start is not None:
            print("Starting test group %s..." % self.start)
            self.json_post("/cli-json/start_group", {"name": self.start})
        elif self.stop is not None:
            print("Stopping test group %s..." % self.stop)
            self.json_post("/cli-json/stop_group", {"name": self.stop})
        elif self.quiesce is not None:
            print("Quiescing test group %s..." % self.quiesce)
            self.json_post("/cli-json/quiesce_group", {"name": self.quiesce})

        completed = False
        timer = 0
        while not completed:
            current_events = self.json_get('/events/since=time/1h')
            new_events = find_new_events(starting_events, current_events)
            target_events = [event for event in get_events(new_events, 'event description') if event.startswith('LOAD COMPLETED')]
            if 'LOAD-DB:  Load attempt has been completed.' in get_events(new_events, 'event description'):
                completed = True
                print('Scenario %s fully loaded after %s seconds' % (self.scenario, timer))
            elif len(target_events) > 0:
                completed = True
                print('Scenario %s fully loaded after %s seconds' % (self.scenario, timer))
            else:
                timer += 1
                time.sleep(1)
                if timer > self.timeout:
                    completed = True
                    print('Scenario failed to load after %s seconds' % self.timeout)
                else:
                    print(new_events)
                    print('Waiting %s out of %s seconds to load scenario %s' % (timer, self.timeout, self.scenario))


def main():
    parser = LFCliBase.create_bare_argparse(
        prog='scenario.py',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''Load a database file and control test groups\n''',
        description='''scenario.py
    --------------------
    Generic command example:
    scenario.py --load db1 --action overwrite --clean_dut --clean_chambers
    
    scenario.py --start test_group1
    
    scenario.py --quiesce test_group1
    
    scenario.py --stop test_group1
    ''')

    group = parser.add_mutually_exclusive_group()

    parser.add_argument('--load', help='name of database to load', default=None)

    parser.add_argument('--action', help='action to take with database {overwrite | append}', default="overwrite")

    parser.add_argument('--clean_dut',
                        help='use to cleanup DUT will be when overwrite is selected, otherwise they will be kept',
                        action="store_true")

    parser.add_argument('--clean_chambers',
                        help='use to cleanup Chambers will be when overwrite is selected, otherwise they will be kept',
                        action="store_true")

    group.add_argument('--start', help='name of test group to start', default=None)
    group.add_argument('--quiesce', help='name of test group to quiesce', default=None)
    group.add_argument('--stop', help='name of test group to stop', default=None)
    parser.add_argument('--timeout', help='Stop trying to load scenario after this many seconds', default=120)
    args = parser.parse_args()

    LoadScenario(mgr=args.mgr,
                 scenario=args.load,
                 action=args.action,
                 clean_dut=args.clean_dut,
                 clean_chambers=args.clean_chambers,
                 start=args.start,
                 stop=args.stop,
                 quiesce=args.quiesce,
                 timeout=args.timeout,
                 debug=args.debug)

    # scenario_loader.load_scenario()


if __name__ == '__main__':
    main()
