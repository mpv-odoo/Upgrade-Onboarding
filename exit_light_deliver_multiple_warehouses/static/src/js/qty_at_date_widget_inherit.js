odoo.define('exit_light_deliver_multiple_warehouses.qty_at_date_widget_inherit', function (require) {
    "use strict";
    const QtyAtDateWidget = require('sale_stock.QtyAtDateWidget');
    
    
    QtyAtDateWidget.include({
        /**
         * Override willStart to call get_quant_data
         */
        willStart: function () {
            const update_popup = this.get_quant_data();
            const defs = [this._super.apply(this, arguments), update_popup];
            return Promise.all(defs);
        },
        /**
         * @quant_data has informaiton on the stock levels of each warehouse
         * @inStock is a boolean that represents whether any of the warehouses
         * have any stock available for this product
         */
        get_quant_data: function () {
            if (this.data.product_id) {
                return this._rpc({
                    model: 'product.product',
                    method: 'get_stock_values_per_warehouse',
                    args: [this.data.product_id.data.id],
                }).then((res) => {
                    this.data.quant_data = res;
                    this.data.inStock = res.map((w) => w.free_qty).some((n) => n > 0);
                });
            }
        }
    });

    return QtyAtDateWidget;
});
