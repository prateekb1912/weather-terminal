import sys
from argparse import ArgumentParser

from weatherterm.core import parser_loader, ForecastType, Unit

def _validate_forecast_args(args):
    if args.forecast_option is None:
        err_msg = 'One of these arguments must be used: -td/--today, -5d/--fivedays, -10d/--tendays, -w/--weekend'
        print(f'{argparser.prog}: error: {err_msg}', file = sys.stderr)
        sys.exit()

parsers = parser_loader.load('.weatherterm/parsers')

argparser = ArgumentParser(
    prog = 'weatherterm',
    description='Weather info from weather.com on your terminal'
)

reqd = argparser.add_argument_group('required_arguments')
reqd.add_argument(
    '-p', '--parser', 
    choices=parsers.keys(), 
    required=True, 
    dest='parser',
    help = 'Specify which parser to use to scrape weather info.'
)
unit_values = [name.title() for name, value in Unit.__members__.items()]

argparser.add_argument(
    '-u', '--unit',
    choices=unit_values,
    required=False,
    dest='unit',
    help = 'Specify the unit to display the temperatures'
)

reqd.add_argument(
    '-a', '--areacode',
    required=True,
    dest='area_code',
    help='Specify the area code for which the weather has to be known. Can be obtained from https://weather.com'
)

argparser.add_argument(
    '-v', '--version',
    action='version',
    version='%(prog)s 1.0'
)

argparser.add_argument(
    'td', '--today',
    dest='forecast_option',
    action='store_const',
    const=ForecastType.TODAY,
    help='Show the weather forecast for the current day'
)

args = argparser.parse_args()
_validate_forecast_args(args)

cls = parsers[args.parser]

parser = cls()
results = parser.run(args)

for res in results:
    print(res)