# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SaleHoliday(models.Model):
    _name = "sale.holiday"
    _description = "Holidays"

    name = fields.Char(string="Holiday")
    date = fields.Date(string="Date")
