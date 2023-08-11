{
    'name': "cjg_sale_stock",

    'summary': """
        Use Box Count field as demand on deliveries """,
    'description': """
        Use box count field as the initial demand so warehouse 
        can take that many boxes from inventory and deliver them.
        Take amount out of inventory.
    """,

    'author': "Odoo PS",
    'website': "https://www.odoo.com",
    'license': 'OPL-1',
    'version': '0.2',
    'depends': ['sale_stock'],
}
