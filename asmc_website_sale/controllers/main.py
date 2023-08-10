# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


import logging
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale_delivery.controllers.main import WebsiteSaleDelivery


_logger = logging.getLogger(__name__)


class ASMCWebsiteSale(WebsiteSale):
    @http.route(
        ["/shop/payment"], type="http", auth="public", website=True, sitemap=False
    )
    def payment(self, **post):
        """Payment step. This page proposes several payment means based on available
        payment.acquirer. State at this point :

         - a draft sales order with lines; otherwise, clean context / session and
           back to the shop
         - no transaction in context / session, or only a draft one, if the customer
           did go to a payment.acquirer website but closed the tab without
           paying / canceling
        """
        order = request.website.sale_get_order()
        redirection = self.checkout_redirection(order) or self.checkout_check_address(
            order
        )
        if redirection:
            return redirection

        render_values = self._get_shop_payment_values(order, **post)
        render_values["only_services"] = order and order.only_services or False

        if render_values["errors"]:
            render_values.pop("acquirers", "")
            render_values.pop("tokens", "")

        # check if the order has non shippable products
        non_shippable_products = order.get_non_shippable_products()
        if non_shippable_products:
            render_values["has_non_shippable"] = True

        # get the earliest ship/pickup date
        earliest_ship_pickup_date = order.get_earliest_ship_pickup_date()
        if earliest_ship_pickup_date:
            render_values["earliest_date"] = str(earliest_ship_pickup_date)

        return request.render("website_sale.payment", render_values)

    @http.route(['/shop/address'], type='http', methods=['GET', 'POST'], auth="public", website=True, sitemap=False)
    def address(self, **kw):
        Partner = request.env['res.partner'].with_context(show_address=1).sudo()
        order = request.website.sale_get_order()

        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        mode = (False, False)
        can_edit_vat = False
        values, errors = {}, {}

        partner_id = int(kw.get('partner_id', -1))

        # IF PUBLIC ORDER
        if order.partner_id.id == request.website.user_id.sudo().partner_id.id:
            mode = ('new', 'billing')
            can_edit_vat = True
        # IF ORDER LINKED TO A PARTNER
        else:
            if partner_id > 0:
                if partner_id == order.partner_id.id:
                    mode = ('edit', 'billing')
                    can_edit_vat = order.partner_id.can_edit_vat()
                else:
                    shippings = Partner.search([('id', 'child_of', order.partner_id.commercial_partner_id.ids)])
                    if order.partner_id.commercial_partner_id.id == partner_id:
                        mode = ('new', 'shipping')
                        partner_id = -1
                    elif partner_id in shippings.mapped('id'):
                        mode = ('edit', 'shipping')
                    else:
                        return Forbidden()
                if mode and partner_id != -1:
                    values = Partner.browse(partner_id)
            elif partner_id == -1:
                mode = ('new', 'shipping')
            else: # no mode - refresh without post?
                return request.redirect('/shop/checkout')

        # IF POSTED
        if 'submitted' in kw:
            pre_values = self.values_preprocess(order, mode, kw)
            errors, error_msg = self.checkout_form_validate(mode, kw, pre_values)
            post, errors, error_msg = self.values_postprocess(order, mode, pre_values, errors, error_msg)

            if errors:
                errors['error_message'] = error_msg
                values = kw
            else:
                partner_id = self._checkout_form_save(mode, post, kw)
                if mode[1] == 'billing':
                    order.partner_id = partner_id
                    order.with_context(not_self_saleperson=True).onchange_partner_id()
                    # This is the *only* thing that the front end user will see/edit anyway when choosing billing address
                    order.partner_invoice_id = partner_id
                    if not kw.get('use_same'):
                        kw['callback'] = kw.get('callback') or \
                            (not order.only_services and (mode[0] == 'edit' and '/shop/checkout' or '/shop/address'))
                elif mode[1] == 'shipping':
                    order.partner_shipping_id = partner_id

                # TDE FIXME: don't ever do this
                order.message_partner_ids = [(4, partner_id), (3, request.website.partner_id.id)]
                if not errors:
                    return request.redirect(kw.get('callback') or '/shop/confirm_order')


        render_values = {
            'website_sale_order': order,
            'partner_id': partner_id,
            'mode': mode,
            'checkout': values,
            'can_edit_vat': can_edit_vat,
            'error': errors,
            'callback': kw.get('callback'),
            'only_services': order and order.only_services,
        }

        # asmc_website_sale -- CUSTOM CODE START
        # check if the order has non shippable products
        non_shippable_products = order.get_non_shippable_products()
        if non_shippable_products:
            render_values["has_non_shippable"] = True
        else:
            render_values["has_non_shippable"] = False
        # asmc_website_sale -- CUSTOM CODE END

        render_values.update(self._get_country_related_render_values(kw, render_values))
        return request.render("website_sale.address", render_values)


class ASMCWebsiteSaleDelivery(WebsiteSaleDelivery):
    @http.route(["/shop/update_date"], type="json", auth="public", methods=["POST"], website=True, csrf=False,)
    def update_eshop_date(self, **post):
        order = request.website.sale_get_order()
        if order:
            order.ship_pickup_date = post["date"]
            _logger.info(
                "%s eCommerce Pick-Up/Ship Date updated to %s" % (order, post["date"])
            )
