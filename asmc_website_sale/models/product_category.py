# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    lead_time = fields.Integer(string="Lead Time in Days")
    is_shipping = fields.Boolean(
        string="Shipping Category",
        help="Enable this option if all products within this category are\
            'Shipping' products (e.g., UPS, USPS, DHL, etc.). This is\
            important for proper syncing between a customer's shopping\
            cart and the 'Type' of a Sale Order in the Odoo backend.",
    )
