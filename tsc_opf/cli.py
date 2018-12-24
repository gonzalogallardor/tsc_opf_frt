from cement.core.foundation import CementApp
from cement.ext.ext_argparse import ArgparseController, expose
import numpy as np

class BaseController(ArgparseController):

    class Meta:

        """
        BaseController arguments definition
        """

        label = 'base'
        description = 'To run a Python-to-GAMS tsc-opf'

    def default(self):

        """
        Print help text if no commands are provided to CLI
        """

        self.app.args.print_help()

    @expose(
        arguments=[
                   (['raw_data_path'],
                    dict(action='store',
                    help='Path to the .raw file in PSS@E format')
                    ),
                   (['instance_name'],
                    dict(action='store',
                    help='Name of the case')
                    ),
                   (['--force'],
                    dict(action='store',
                    help='Generate the case even if they exist',
                    default='False',
                    choices=['True', 'true', 'false', 'False'])
                    )
                   ],

        help='Generate a GAMS file (.gms) to run a tsc-opf'
    )