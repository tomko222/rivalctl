#!/usr/bin/python

from __future__ import print_function

import sys
import os
try:
    from rival import *
except ImportError:
    p = os.path.dirname(os.path.realpath(__file__))
    p = os.path.realpath(os.path.join(p, '../rival'))
    sys.path.append(p)
    from rival import *

import argparse


def send_reports(reports):
    for report in reports:
        send(report)


def _main(args):
    reports = []
    if args.reset:
        reports = FACTORY_PROFILE.to_report_list()
    if args.profile:
        profile = Profile.find_profile(args.profile)
        print("Loading profile %s" % (os.path.splitext(profile)[0],))
        profile = Profile.from_yaml(open(profile))
        reports = profile.to_report_list()

    if args.logo_color is not None:
        reports.append(set_logo_color(args.logo_color))
    if args.logo_style is not None:
        reports.append(set_logo_style(args.logo_style))
    if args.wheel_color is not None:
        reports.append(set_wheel_color(args.wheel_color))
    if args.wheel_style is not None:
        reports.append(set_wheel_style(args.wheel_style))
    if args.cpi1 is not None:
        reports.append(set_cpi_1(args.cpi1))
    if args.cpi2 is not None:
        reports.append(set_cpi_2(args.cpi2))
    if args.polling_rate is not None:
        reports.append(set_polling_rate(args.polling_rate))
    if args.commit:
        reports.append(commit())
    send_reports(reports)


parser = argparse.ArgumentParser(description="A tool to configure the SteelSeries Rival Gaming Mouse")
parser.add_argument('--commit', help="Save to firmware", default=False, action='store_true')
parser.add_argument("--reset", help="Reset all options to FACTORY defaults", action='store_true', default=False)
parser.add_argument("--wheel-color", type=str, metavar="COLOR", help="any valid css color name or hex string")
parser.add_argument("--wheel-style", type=int, metavar="STYLE", help="LED Style [1=Steady, 2-4=Breathe Speed]", choices=[1,2,3,4])
parser.add_argument("--logo-color", type=str, metavar="COLOR", help="any valid css color name or hex string")
parser.add_argument("--logo-style", type=int, metavar="STYLE", help="LED Style [1=Steady, 2-4=Breathe Speed]", choices=[1,2,3,4])

parser.add_argument("--cpi1", type=int, metavar="CPI", help="50-6500 in increments of 50 [default 800]")
parser.add_argument("--cpi2", type=int, metavar="CPI", help="50-6500 in increments of 50 [default 1600]")
parser.add_argument("--profile", type=str, metavar="PROFILE", help="profile name or path to file")
parser.add_argument("--polling-rate", metavar="RATE", type=int, help="1000, 500, 250, or 125 [default=1000]", choices=[1000,500,250,125])


def main():
    if len(sys.argv) == 1:
        parser.print_help()
    args = parser.parse_args()
    _main(args)
    return 0
