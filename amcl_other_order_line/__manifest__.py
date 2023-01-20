# -*- coding: utf-8 -*-
{
    'name': 'AMCL : Sale Other Order Line',
    'category': 'Sale',
    'sequence': 1,
    'version': '15.0.1',
    'license': 'LGPL-3',
    'summary': """AMCL : Sale Other Order Line""",
    'description': """AMCL : Sale Other Order Line""",
    'depends': ['base', 'product', 'sale_management', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_other_order_line_view.xml',
    ],
    'installable': True,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
