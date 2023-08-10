odoo.define("stock_barcode.LinesQualityWidget", function (require) {
  "use strict";

  var LinesWidget = require("stock_barcode.LinesWidget");

  var LinesValidationWidget = LinesWidget.include({
    init: function (parent, page, pageIndex, nbPages) {
      this._super.apply(this, arguments);
      this.hide_validation = parent.currentState.state === "recount_done";
    },

    _renderLines: function () {
      this._super.apply(this, arguments);
      var $validate = this.$(".o_validate_page");
      if (this.hide_validation) {
        $validate.addClass("o_hidden");
      }
    },
  });

  return LinesValidationWidget;
});
