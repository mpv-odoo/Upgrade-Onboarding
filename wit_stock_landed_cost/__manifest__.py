# -*- coding: utf-8 -*-
{
    'name': "Wit Games: Landed Cost Popup",
    'summary': """Shows a landed cost popup on receipt validation.""",
    'description': """
Wit Games: Landed Cost Popup
============================
When a receipt is validated, creates a landed cost in draft state
and displays in on a popup window for the user to apply landed
cost amount.

Task ID: 2615051(B)
    """,
    'author': 'Odoo Inc',
    'website': 'https://www.odoo.com/',
    'category': 'Custom Development',
    'version': '15.0.1.0.0',
    'license': 'OPL-1',
    'depends': ['stock_landed_costs','purchase_stock'],
    'data': [
        'security/ir.model.access.csv', 
        'data/product.xml'
    ],
}
