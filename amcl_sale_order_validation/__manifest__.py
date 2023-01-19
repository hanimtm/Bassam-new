# -*- coding: utf-8 -*-
{
    'name': 'AMCL : Validate Sale Order Payment Terms',
    'category': 'Sales',
    'sequence': 1,
    'version': '15.0.1',
    'license': 'LGPL-3',
    'summary': """AMCL : Validate at confirmation of sale order when the payment terms is on credit.""",
    'description': """AMCL : Validate at confirmation of sale order when the payment terms is on credit.""",
    'depends': ['base', 'sale_management'],
    'data': [
        'views/sale_order_view.xml',
    ],
    'installable': True,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
