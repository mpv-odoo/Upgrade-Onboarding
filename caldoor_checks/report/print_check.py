# -*- coding: utf-8 -*-
import logging
from num2words import num2words
from odoo import api, fields, models, tools, _


_logger = logging.getLogger(__name__)

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    '''
    (Overridden) Change amount in words to use fractional cents rather than text
    '''
    @api.onchange('amount','currency_id')
    def _onchange_amount(self):
        res = super(AccountPayment, self)._onchange_amount()
        self.check_amount_in_words = self._amount_in_words_fractional_cents(self.amount, self.currency_id)
        return res

    '''
    (Overridden) Change amount in words to use fractional cents rather than text
    '''
    def set_check_amount_in_words(self):
        for rec in self:
            rec.check_amount_in_words = rec._amount_in_words_fractional_cents(self.amount, self.currency_id)

    '''
    (Overridden) Removed the asterisks from the amount in words
    '''
    def _check_build_page_info(self, i, p):
        page = super(AccountPayment, self)._check_build_page_info(i,p)
        ''' Remove the asterisks from the amount in words '''
        if page['amount_in_word']:
            page['amount_in_word'] = page['amount_in_word'].replace('*', '')
        return page

    '''
    (New) Code copied from res_currency amount_to_text function, but modified to
    allow for the cents part to be displayed as a fraction rather than in text.
    Did not want to override res_currency function because that could be used in
    other places 
    '''
    @api.model
    def _amount_in_words_fractional_cents(self, amount, currency_id):
        self.ensure_one()
        def _num2words(number, lang):
            try:
                return num2words(number, lang=lang).title()
            except NotImplementedError:
                return num2words(number, lang='en').title()

        if num2words is None:
            _logger.warning("The library 'num2words' is missing, cannot render textual amounts.")
            return ""

        formatted = '{total:.2f}'.format(total=amount)
        parts = formatted.partition('.')
        integer_value = int(parts[0])
        fractional_value = int(parts[2] or 0)

        lang_code = self.env.context.get('lang') or self.env.user.lang
        lang = self.env['res.lang'].with_context(active_test=False).search([('code', '=', lang_code)])

        ''' Remove 'And' and commas from num2words output '''
        dollar_words = _num2words(integer_value, lang=lang.iso_code).replace('And ', '').replace(',','')
        cent_words = str(fractional_value).zfill(2) + '/100 ' + (currency_id.currency_unit_label or 'Dollars')

        return dollar_words + ' And ' + cent_words

    '''
    (Overridden) Replace the 'number' field in the stub line with just the
    reference number alone.
    '''
    def _check_make_stub_line(self, invoice):
        res = super(AccountPayment, self)._check_make_stub_line(invoice)
        res['invoice_date'] = invoice.date_invoice
        res['number'] = invoice.number
        res['reference'] = invoice.reference
        return res