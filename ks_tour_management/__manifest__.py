# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Tour Management',
    'version': '1.0.0',
    'category': '',
    'author': 'Ksolves',
    'sequence': -100,
    'summary': 'Tour Management',
    'description': """Ksolves Tour Management""",
    'depends': ['base', 'bi_tour_management', 'portal', 'crm', 'product','mail', 'loyalty'],
    'assets': {
        'web.assets_backend': [
            'ks_tour_management/static/src/js/ks_form_validation.js',
        ],
    },
    'data': [
        'security/ir.model.access.csv',
        'data/mail_template_data.xml',
        'views/tour_booking_view.xml',
        'views/custom_tour_itinary.xml',
        'views/portal_templates.xml',
        'views/portal_enquiry_template.xml',
        'views/portal_booking_templates.xml',
        'views/crm_lead_view.xml',
        'views/seasonal_offer_view.xml',
        'views/tour_hotel_reservation_view.xml',
        'views/loyalty_program_view.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,

    'license': 'LGPL-3',
}
