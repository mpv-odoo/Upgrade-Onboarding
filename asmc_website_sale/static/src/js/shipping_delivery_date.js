odoo.define("asmc_website_sale.checkout", function (require) {
  "use strict";

  var publicWidget = require("web.public.widget");
  var concurrency = require("web.concurrency");
  var dp = new concurrency.DropPrevious();

  publicWidget.registry.ShippingDatePicker = publicWidget.Widget.extend({
    selector: ".oe_website_sale",
    events: {
      "change #ship_pickup_date": "_onPickupClick",
    },
    /**
     * @private
     * @param {Event} ev
     */
    _onPickupClick: function (ev) {
      var date = $(ev.currentTarget).val();
      dp.add(
        this._rpc({
          route: "/shop/update_date",
          params: {
            date: date,
          },
        })
      );
    },
  });
});
