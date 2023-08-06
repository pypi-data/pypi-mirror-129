#!/usr/local/bin/python3
#
# sonar-tools
# Copyright (C) 2019-2021 Olivier Korach
# mailto:olivier.korach AT gmail DOT com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
'''
    Exports some measures of all projects
    - Either all measures (-m _all)
    - Or the main measures (-m _main)
    - Or a custom selection of measures (-m <measure1,measure2,measure3...>)
'''
import sys
import re
import sonarqube.measures as measures
import sonarqube.metrics as metrics
import sonarqube.projects as projects
import sonarqube.utilities as util
import sonarqube.env as env


def __diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]


def main():
    parser = util.set_common_args('Extract measures of projects')
    parser = util.set_component_args(parser)
    parser.add_argument('-m', '--metricKeys', required=False, help='Comma separated list of metrics or _all or _main')
    parser.add_argument('-b', '--withBranches', required=False, action='store_true',
                        help='Also extract branches metrics')
    parser.add_argument('--withTags', required=False, action='store_true', help='Also extract project tags')
    parser.set_defaults(withBranches=False, withTags=False)
    parser.add_argument('-r', '--ratingsAsLetters', action='store_true', required=False,
                        help='Reports ratings as ABCDE letters instead of 12345 numbers')

    args = util.parse_and_check_token(parser)
    endpoint = env.Environment(url=args.url, token=args.token)
    util.check_environment(vars(args))

    # Mandatory script input parameters
    csv_sep = ","

    main_metrics = metrics.Metric.MAIN_METRICS
    main_metrics_list = re.split(',', main_metrics)
    if args.metricKeys == '_all':
        wanted_metrics = metrics.as_csv(metrics.search(endpoint=endpoint).values())
    elif args.metricKeys == '_main':
        wanted_metrics = main_metrics
    elif args.metricKeys is not None:
        wanted_metrics = args.metricKeys
    else:
        wanted_metrics = main_metrics
    metrics_list = re.split(',', wanted_metrics)

    print("# Project Key%sProject Name%sBranch%sLast Analysis" % (csv_sep, csv_sep, csv_sep), end=csv_sep)

    if args.metricKeys == '_all':
        # Display main metrics first
        print(main_metrics)
        metrics_list = __diff(metrics_list, main_metrics_list)

    for m in metrics_list:
        print("{0}".format(m), end=csv_sep)
    print('')

    if args.componentKeys is not None:
        proj_list = args.componentKeys.replace(' ', '')
        filters = {'projects': proj_list}
    else:
        filters = None
    project_list = projects.search(endpoint=endpoint, params=filters)
    nb_branches = 0
    nb_loc = 0
    for _, project in project_list.items():
        branch_data = project.get_branches()
        branch_list = []
        for b in branch_data:
            if args.withBranches or b.is_main():
                branch_list.append(b)
                util.logger.debug("Branch %s appended", b.name)
        project_loc = 0
        for b in branch_list:
            nb_branches += 1
            p_meas = measures.component(project.key, wanted_metrics, branch=b.name, endpoint=endpoint)
            if b.last_analysis_date() is None:
                last_analysis = "Never"
            else:
                last_analysis = util.date_to_string(b.last_analysis_date())
            line = ''
            if 'ncloc' in p_meas:
                project_loc = max(project_loc, int(p_meas['ncloc']))
            print("{1}{0}{2}{0}{3}{0}{4}".format(csv_sep, project.key, project.name, b.name, last_analysis), end='')
            if args.metricKeys == '_all':
                for metric in main_metrics_list:
                    line = line + csv_sep + p_meas[metric].replace(csv_sep, '|') if metric in p_meas else line + csv_sep
            for metric in metrics_list:
                line = line + csv_sep + p_meas[metric].replace(csv_sep, '|') if metric in p_meas \
                    else line + csv_sep + "None"
            print(line)
        nb_loc += project_loc
    util.logger.info("%d PROJECTS %d branches %d LoCs", len(project_list), nb_branches, nb_loc)
    sys.exit(0)


if __name__ == '__main__':
    main()
