# -*- coding: utf-8 -*-
{
    'name': 'CalDoor: Check layout change',
    'summary': '''
        Makes several changes to the format of checks in Odoo to allow printing
        checks directly on check templates
    ''',
    'description': '''
        MPV - TASK ID: 2643335
        1. Removed asterisks from the amount in words, made slightly bigger font
        2. Changed the cents in amount in words to be fractional instead
        3. Rearranged amount in words, date, and numeric amount
        4. Made numeric amount bigger and in bolder font
    ''',
    'license': 'OPL-1',
    'author': 'Odoo Inc',
    'website': 'https://www.odoo.com',
    'category': 'Development Services/Custom Development',
    'version': '1.0',
    'depends': [
        'l10n_us_check_printing'
    ],
    'data': [
        'report/print_check.xml',
    ],
    'qweb': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False
}