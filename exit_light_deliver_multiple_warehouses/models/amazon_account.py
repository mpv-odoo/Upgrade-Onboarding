import logging
import psycopg2
from odoo.addons.sale_amazon.models import mws_connector as mwsc
from odoo import api, exceptions, fields, models, _
from odoo.service.model import PG_CONCURRENCY_ERRORS_TO_RETRY

_logger = logging.getLogger(__name__)


class AmazonAccount(models.Model):
    _inherit = 'amazon.account'

    def _get_order(self, order_data, items_data, amazon_order_ref):
        '''
        (Overridden) Override to let the state of the order to be in sale. Call
        super with the context of skip_amazon_orders so that the function
        _action_launch_stock_rule on sale.order.line filters out the amazon
        orders and doesn't make deliveries for them.
        '''
        fulfillment_channel = mwsc.get_string_value(order_data, 'FulfillmentChannel')
        if fulfillment_channel == 'MFN':
            self = self.with_context(skip_amazon_orders=True)
        order, order_found, status = super(AmazonAccount, self)._get_order(order_data, items_data, amazon_order_ref)

        if fulfillment_channel == 'MFN' and order and order.state == 'done':
            order.state = 'sale'

        return order, order_found, status

    def _process_order(self, order_data, orders_api):
        '''
        (Overridden) Overridden to prevent stock moves from being generated
        automatically after an amazon order is created
        Create a sale order from the data of an Amazon order. 
        '''
        self.ensure_one()
        amazon_order_ref = mwsc.get_string_value(order_data, 'AmazonOrderId')
        items_data = []
        has_next, next_token = True, None
        rate_limit_reached = False
        sync_failure = False
        error_message = _("An error was encountered when synchronizing Amazon order items.")
        while has_next and not rate_limit_reached:
            items_data_batch, next_token, rate_limit_reached = mwsc.get_items_data(
                orders_api, amazon_order_ref, error_message)
            items_data += items_data_batch
            has_next = bool(next_token)
        if not rate_limit_reached:
            try:
                with self.env.cr.savepoint():
                    order, order_found, amazon_status = self._get_order(
                        order_data, items_data, amazon_order_ref)
            except Exception as error:
                logging_values = {'error': repr(error), 'order_ref': amazon_order_ref, 'account_id': self.id}
                _logger.warning("error (%(error)s) while syncing sale.order with amazon_order_ref %(order_ref)s for "
                                "amazon.account with id %(account_id)s", logging_values)
                if isinstance(error, psycopg2.OperationalError) and error.pgcode in PG_CONCURRENCY_ERRORS_TO_RETRY:
                    raise
                sync_failure = True
                _logger.exception(error)
            else:
                if amazon_status == 'Canceled' and order_found and order.state != 'cancel':
                    order.with_context(canceled_by_amazon=True).action_cancel()
                    _logger.info("canceled sale.order with amazon_order_ref %s for "
                                 "amazon.account with id %s" % (amazon_order_ref, self.id))
                elif not order_found and order:  # New order created
                    # Custom code (Removed the generate stock moves and state change)
                    if order.amazon_channel == 'fba':
                        self._generate_stock_moves(order)
                    elif order.amazon_channel == 'fbm':
                        pass
                    # Custom Code ended
                    _logger.info("synchronized sale.order with amazon_order_ref %s for "
                                 "amazon.account with id %s" % (amazon_order_ref, self.id))
                elif order_found:  # Order already sync
                    _logger.info("ignored already sync sale.order with amazon_order_ref %s for "
                                 "amazon.account with id %s" % (amazon_order_ref, self.id))
                else:  # Combination of status and fulfillment channel not handled
                    _logger.info("ignored %s amazon order with reference %s for amazon.account "
                                 "with id %s" % (amazon_status.lower(), amazon_order_ref, self.id))
        return amazon_order_ref, rate_limit_reached, sync_failure
