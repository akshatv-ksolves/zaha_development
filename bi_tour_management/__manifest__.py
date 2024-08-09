# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################
{
    'name': 'Tours and Travels, Hotel Management in Odoo',
    'version': '17.0.0.3',
    'summary': 'Apps Tour Management tours and travel management Tour Booking tour hotel management tour and travel agency management Tour Agent Commission Passport Booking Visa Booking travel agent Tour itinerary tours and travel agency travel booking Transport Booking',
    'category': 'Industries',
    'description': """ This apps helps to manage 
    odoo Tour Visa and Passport Management with Odoo.
    odoo Tours management Travel management Passport Management Visa Management.
    This Module helps you to odoo create Tours and travels management
    odoo travel management odoo tour management tour and travel mananegement travels and tours management
    odoo tours and hotel management odoo tours and travel management.
    This Module helps Customers to Customize their own Tour for odoo
    This Module helps you to Manage Transport odoo Transport management
    his Module helps you to Manage Hotels odoo Hotels management
    odoo Tours and Travels management.
    odoo travel booking AGENCY tour booking AGENCY
    odoo TRAVEL AGENCY tours and travel agency odoo travel agency app travel booking odoo travels booking
    odoo tour booking odoo booking agency travels
    This Module helps you to Manage odoo Insurance
    This Module also helps you for odoo Passport and Visa booking
    odoo Tour Booking Transport Information tour and travel
    tour and travel management Transport Management
    odoo Transport Booking Manage Hotel Booking
    odoo Custom Tour Booking Custom Tour Iternity
    odoo Tour Agent Commision Passport Booking Visa Booking odoo travel agent odoo
    Do you have Tours and Travels business and want to setup your whole system inside the odoo then this module will be the great choice for you.
    By using this odoo apps Customer can Book a Tours, manage and customize his/her Tour according to his/her choice with insurance
    generate itinerary of Tour 
    Select customize package of tours also choose hotels from the different option. This odoo module also helps to manage Visa and Passport details of the customers.
Also able to create invoice from the tour booking, hotel booking etc.Also you don't need to worry about the commission of Agent, 
We will provide configurable setup for calculate commission for agent and once tour if booked for that specific agent, commission is also generated for that agent
    You can generate supplier invoice for the commission and pay commission amount via register payment
    odoo tour itinerary odoo hotel itinerary odoo tour ticket itinerary odoo hotel ticket itinerary odoo
    
    """,
    'author': 'BrowseInfo',
    'website': 'https://www.browseinfo.com',
    'depends': ['sale_management','account_payment','stock', 'account','crm','sale_stock','website','web','product'],
    'data': [
            'security/tour_security.xml',
            'security/ir.model.access.csv',
            'data/data.xml',
            'wizard/tour_booking_wizard_view.xml',
            'views/tour_booking_sequence.xml',
            'views/custom_tour_sites_view.xml',
            'views/agent_commission_invoice_view.xml',
            'views/custom_tour_destination_view.xml',
            'views/custom_tour_itinary_view.xml',
            'views/tour_booking_view.xml',
            'views/custom_tour_transport_view.xml',
            'views/document_management_view.xml',
            'views/tour_deduction_policy_view.xml',
            'views/hotel_information_view.xml',
            'views/hotel_type_view.xml',
            'views/insurance_policy_view.xml',
            'views/insurance_type_view.xml',
            'views/partner_view.xml',
            'views/passport_booking_view.xml',
            'views/product_view.xml',
            'views/room_type_view.xml',
            'views/sale_view.xml',
            'views/service_scheme_view.xml',
            'views/service_type_view.xml',
            'views/tour_cancellation_view.xml',
            'views/tour_destination_line_view.xml',
            'views/tour_destination_view.xml',
            'views/tour_facility_view.xml',
            'views/tour_hotel_reservation_view.xml',
            'views/tour_package_info_view.xml',
            'views/tour_package_type_view.xml',
            'views/tour_package_view.xml',
            'views/tour_payment_policy_view.xml',
            'views/tour_preference_view.xml',
            'views/tour_season_view.xml',
            'views/transport_booking_view.xml',
            'views/transport_carrier_view.xml',
            'views/transport_information_view.xml',
            'views/travel_class_view.xml',
            'views/visa_booking_view.xml',
            'views/visa_scheme_view.xml',
            'report/tour_itinary_report.xml',
            'report/tour_itinary_report_view.xml',
            'report/tour_creator_report.xml',
            'report/tour_creator_report_view.xml',
            'report/agent_commission_report.xml',
            'report/agent_commission_report_view.xml',
            'report/tour_booking_report.xml',
            'report/tour_booking_report_view.xml',
            'report/transport_booking_report.xml',
            'report/transport_booking_report_view.xml',
            'report/hotel_reservation_report.xml',
            'report/hotel_reservation_report_view.xml',
            'data/mail_template_data.xml',
            'data/website_data.xml',
            'views/website_template.xml',
            'views/rating_templates.xml',
            'views/dashboard_view.xml',
            'data/ir_cron.xml',
            'data/rating_mail_template.xml',     
            'views/crm_lead_view.xml', 
        ],
    'assets': {
        'web.assets_backend': [
            'bi_tour_management/static/src/js/dashboard.js',
            'bi_tour_management/static/src/css/custom.css',
            'bi_tour_management/static/src/xml/dashboard.xml',
            'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.bundle.js',
        ],
        'web.assets_frontend': [
            'bi_tour_management/static/src/js/im_web_frontend.js',
            'bi_tour_management/static/src/xml/booking_template.xml',
            'bi_tour_management/static/src/xml/inquiry_template.xml',
        ],
    },
    'demo': [],
    'test': [],
    'application': True,
    "price": 239,
    "currency": 'EUR',
    'installable': True,
    'auto_install': False,
    "images":['static/description/Banner.gif'],
    'live_test_url':'https://youtu.be/ATmjhL2kocY',
    "license": "OPL-1",
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
