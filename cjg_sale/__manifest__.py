{
    'name': "cjg_sale",

    'summary': """
        Add Piece Count, Case Pack, Box Count, Box Price, and Total Box Count to sale order lines """,
    'description': """
        Add Pice Count and Case Pack fields to sale order lines.
        Add calculated fields Box Count and Box Price to sale order lines.
        Add calculated field Total Box Count to sum up all sale order line box counts.
        Allow fields to be pulled into trasfer PDF Reports (Delivery Slip and BOL)
    """,

    'author': "Odoo PS",
    'website': "https://www.odoo.com",
    'license': 'OPL-1',
    'version': '0.2',
    'depends': ['sale_stock'],
    'data': [
        'views/view_order_form_inherit.xml',
        'views/product_template_form_view_inherit.xml',
    ],
}
