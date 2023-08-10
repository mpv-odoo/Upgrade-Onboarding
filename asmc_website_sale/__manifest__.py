# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    "name": "A Sweet Morsel Co: eCommerce Shipping/Pick-Up",
    "summary": """eCommers customers can select a shipping/pickup date""",
    "description": """
        Task ID: 2673953

        - Adds a 'Shippable' checkbox to products. If any products in an\
            eCommerce order contain a non-shippable product, the only\
            shipping method available will be 'Pick-Up'
        - Adds a 'Lead Time in Days' field to Product Category
        - Adds a 'Holidays' model to track eCommerce holidays
        - The eCommerce 'Confirm Order' page gives customers the ability\
            to select a shipping/pickup date that is computed based off\
            of the longest lead time of any product in the order;\
            holidays and sundays are added as buffer days
        """,
    "author": "Odoo Inc",
    "website": "https://www.odoo.com/",
    "category": "Custom Development",
    "version": "14.0.1.0.2",
    "license": "OPL-1",
    "depends": ["website_sale_delivery"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_template_views.xml",
        "views/product_product_views.xml",
        "views/delivery_carrier_views.xml",
        "views/website_sale_templates.xml",
        "views/website_sale_delivery_templates.xml",
        "views/product_category_views.xml",
        "views/sale_holiday_views.xml",
        "views/sale_holiday_menus.xml",
        "views/sale_order_views.xml",
        "views/static.xml",
    ],
    "application": False,
}
