# -*- coding: utf-8 -*-
{
    "name": "Wit Games: Two Step Approval",
    "summary": """Two step validation of receipts.""",
    "description": """
Wit Games: Two Step Approval
============================
Creates a two step validation process for receipts. The work flow is as follows:

1. Inventory/User scans in received products.
2. That same user clicks "Validate".
    2a. An email is sent (recipient to be configured by the client)
    2b. The "Done" column is copied to the "Done 1st" column. The "Recount" column is computed.
3. A Purchase/User resets the Done quantity.
4. The Inventory/User rescans items that need recounting.
5. The Purchase/User clicks "Validate".
    5a. An email is sent.

Task ID: 2615051(A)
    """,
    "author": "Odoo Inc",
    "website": "https://www.odoo.com/",
    "category": "Custom Development",
    "version": "15.0.1.0.0",
    "license": "OPL-1",
    "depends": ["purchase_stock","stock_barcode"],
    "data": [
        "security/ir.model.access.csv",
        "data/mail_template_data.xml",
        "views/stock_picking_views.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'wit_stock_two_step_approval/static/src/js/client_action/lines_widget.js',
        ],
    },
}
