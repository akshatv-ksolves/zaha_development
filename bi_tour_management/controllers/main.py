# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import base64
from odoo import http
from odoo.http import request
import logging
import werkzeug
import odoo.http as http
from odoo import SUPERUSER_ID, _
from odoo.http import request
from odoo.tools.misc import get_lang
from datetime import datetime,date
from odoo.addons.http_routing.models.ir_http import slug
from markupsafe import Markup



class TourBooking(http.Controller):
    

    @http.route(['/thankyou/booking/<string:name>', '/thankyou/inquiry/<string:name>'], auth='user', website=True)
    def thankyou(self,name, **kw):
        form_data = kw.get('form_data', {})
        current_url = request.httprequest.url
        if 'booking' in current_url:
            message = f'Your Booking Request is successfully Generated\nYour Booking ID is {name}'
        else:
            message = f'Your Inquiry Request is successfully Generated\nYour Inquiry ID is {name}'
        return request.render('bi_tour_management.booking_create_message', {'message': message})
    

    @http.route('/booking/', auth='user', website=True)
    def booking(self, **kw):
        if request.env.user.has_group('base.group_system'):
            bookings = request.env['tour.booking'].sudo().search([])
        else:
            bookings = request.env['tour.booking'].sudo().search([('create_uid', '=', request.env.user.id)])
        
        partners = request.env['res.partner'].sudo().search([])
        via_data = request.env['tour.booking'].sudo().search([]).sudo().fields_get(['via'])['via']['selection']
        currency = request.env['res.currency'].sudo().search([])
        t_types = request.env['tour.booking'].sudo().search([]).sudo().fields_get(['tour_type'])['tour_type']['selection']
        tours = request.env['tour.package'].sudo().search([])
        seasons = request.env['tour.season'].sudo().search([])
        payments = request.env['tour.payment.policy'].sudo().search([])
        agents = request.env['res.partner'].sudo().search([('agent', '=', True)])
        dates = request.env['tour.booking'].sudo().search([])

        dict = {'bookings': bookings,
                'partners': partners,
                'via': via_data,
                'currency': currency,
                't_types': t_types,
                'tours': tours,
                'seasons': seasons,
                'payments': payments,
                'agents': agents,
                }
        return request.render('bi_tour_management.tour_booking', dict)
    
    
    @http.route('/booking/data', auth='user', type='json')
    def booking_data(self):
        persons = request.env['res.partner'].sudo().search([('is_hotel', '=', False)]).read(['id','name'])
        gender = request.env['tour.customer.details'].sudo().fields_get(['gender'])['gender']['selection']
        type = request.env['tour.customer.details'].sudo().fields_get(['type'])['type']['selection']
        country = request.env['res.country'].sudo().search([]).read(['id','name'])
        destinations = request.env['tour.destination'].sudo().search([]).read(['id','name'])
        facility = request.env['tour.facility'].sudo().search([]).read(['id','name'])
        sites = request.env['product.product'].sudo().search([]).read(['id','name'])
        v_types = request.env['visa.costing.line'].sudo().fields_get(['visa_type'])['visa_type']['selection']
        hotels = request.env['res.partner'].sudo().search([('is_hotel', '=', True)]).read(['id','name'])
        h_types = request.env['hotel.type'].sudo().search([]).read(['id','name'])
        t_class = request.env['travel.class'].sudo().search([]).read(['id','name'])
        transport = request.env['transport.information'].sudo().search([]).read(['id','name'])
        t_carrier = request.env['transport.carrier'].sudo().search([]).read(['id','name'])
        product = request.env['product.product'].sudo().search([]).read(['id','name'])
        uom = request.env['uom.uom'].sudo().search([]).read(['id','name'])
        insurance = request.env['insurance.type'].sudo().search([]).read(['id','name'])
        return {
            'persons': persons,
            'gender': gender,
            'type': type,
            'country': country,
            'destinations': destinations,
            'facility': facility,
            'sites': sites,
            'v_types': v_types,
            'hotels': hotels,
            'h_types': h_types,
            't_class': t_class,
            'transport': transport,
            't_carrier': t_carrier,
            'product': product,
            'uom': uom,
            'insurance': insurance,
        }
    
    @http.route(['/create-book'], type='json', auth="public", website=True)
    def create_book(self, form_data):
        try:
            if form_data.get('tour_customer_ids', False):
                person_line_ids = []
                for rec in form_data.get('tour_customer_ids'):
                    person_line_ids.append((0, 0, {
                        'partner_id': rec.get('partner_id'),
                        'name': rec.get('name'),
                        'gender': rec.get('gender'),
                        'type': rec.get('type'),
                    }))
                form_data["tour_customer_ids"] = person_line_ids

            if form_data.get('tour_program_book_ids', False):
                program_line_ids = []
                for program in form_data.get('tour_program_book_ids'):
                    program_line_ids.append((0, 0, {
                        'name': program.get('name'),
                        'days': program.get('days'),
                        'description': program.get('description'),
                        'breakfast': program.get('breakfast'),
                        'lunch': program.get('lunch'),
                        'dinner': program.get('dinner'),
                        'expected_line_sale': program.get('expected_line_sale'),
                    }))
                form_data["tour_program_book_ids"] = program_line_ids

            if form_data.get('tour_destination_book_ids', False):
                destinations_line_ids = []
                for rec in form_data.get('tour_destination_book_ids'):
                    destinations_line_ids.append((0, 0, {
                        'destination_id': rec.get('destination_id'),
                        'country_id': rec.get('country_id'),
                        'nights': rec.get('nights'),
                        'visa_chk': rec.get('visa_chk'),
                    }))
                form_data["tour_destination_book_ids"] = destinations_line_ids

            if form_data.get('itinary_cost_include_book_lines', False):
                include_line_ids = []
                for rec in form_data.get('itinary_cost_include_book_lines'):
                    include_line_ids.append((0, 0, {
                        'facility_id': rec.get('facility_id'),
                        'name': rec.get('name'),
                    }))
                form_data["itinary_cost_include_book_lines"] = include_line_ids

            if form_data.get('itinary_cost_exclude_book_lines', False):
                exclude_line_ids = []
                for rec in form_data.get('itinary_cost_exclude_book_lines'):
                    exclude_line_ids.append((0, 0, {
                        'facility_id': rec.get('facility_id'),
                        'name': rec.get('name'),
                    }))
                form_data["itinary_cost_exclude_book_lines"] = exclude_line_ids

            if form_data.get('sites_costing_book_ids', False):
                site_line_ids = []
                for rec in form_data.get('sites_costing_book_ids'):
                    site_line_ids.append((0, 0, {
                        'name': rec.get('site_name'),
                        'new_sale_price': rec.get('new_sale_price'),
                        'total_sale_price': rec.get('total_sale_price'),
                    }))
                form_data["sites_costing_book_ids"] = site_line_ids

            if form_data.get('visa_costing_book_ids', False):
                visa_line_ids = []
                for rec in form_data.get('visa_costing_book_ids'):
                    visa_line_ids.append((0, 0, {
                        'country_id': rec.get('country_id'),
                        'name': rec.get('visa'),
                        'visa_type': rec.get('visa_type'),
                        'sale_price': rec.get('sale_price'),
                        'total_person': rec.get('total_person'),
                        'total_sale_price': rec.get('total_sale_price'),
                    }))
                form_data["visa_costing_book_ids"] = visa_line_ids

            if form_data.get('hotel_planer_book_ids', False):
                hotel_line_ids = []
                for rec in form_data.get('hotel_planer_book_ids'):
                    hotel_line_ids.append((0, 0, {
                        'name': rec.get('name'),
                        'destination_id': rec.get('destination_id'),
                        'hotel_type_id': rec.get('hotel_type_id'),
                        'hotel_id': rec.get('hotel_id'),
                        'room_type_id': rec.get('room_type_id'),
                        'room_req': rec.get('room_req'),
                        'days': rec.get('days'),
                        'customer_price': rec.get('customer_price'),
                        'customer_price_total': rec.get('customer_price_total'),
                    }))
                form_data["hotel_planer_book_ids"] = hotel_line_ids

            if form_data.get('travel_planer_book_ids', False):
                travel_line_ids = []
                for rec in form_data.get('travel_planer_book_ids'):
                    travel_line_ids.append((0, 0, {
                        'name': rec.get('name'),
                        'transport_id': rec.get('transport_id'),
                        'date': rec.get('date'),
                        'transport_carrier_id': rec.get('transport_carrier_id'),
                        'transport_type_id': rec.get('transport_type_id'),
                        'travel_class_id': rec.get('travel_class_id'),
                        'from_dest_id': rec.get('from_dest_id'),
                        'to_dest_id': rec.get('to_dest_id'),
                        'sale_price_adult': rec.get('sale_price_adult'),
                        'sale_price_child': rec.get('sale_price_child'),
                        'total_sale_price_adult': rec.get('cost_price_adult'),
                        'total_sale_price_child': rec.get('cost_price_child'),

                    }))
                form_data["travel_planer_book_ids"] = travel_line_ids

            if form_data.get('service_book_ids', False):
                other_line_ids = []
                for rec in form_data.get('service_book_ids'):
                    other_line_ids.append((0, 0, {
                        'product_id': rec.get('product_id'),
                        'sale_price': rec.get('sale_price'),
                        'product_uom_qty': rec.get('product_uom_qty'),
                        'product_uom_id': rec.get('product_uom_id'),
                        'discount': rec.get('discount'),
                        'price_subtotal': rec.get('price_subtotal'),
                    }))
                form_data["service_book_ids"] = other_line_ids

            if form_data.get('insurance_line_ids', False):
                service_line_ids = []
                for rec in form_data.get('insurance_line_ids'):
                    service_line_ids.append((0, 0, {
                        'insurance_policy_id': rec.get('insurance_policy_id'),
                        'insurance_type_id': rec.get('insurance_type_id'),
                        'insurance_cost_for_adults': rec.get('insurance_cost_for_adults'),
                        'insurance_cost_for_childs': rec.get('insurance_cost_for_childs'),
                        'total_cost': rec.get('total_cost'),
                    }))
                form_data["insurance_line_ids"] = service_line_ids
            

            booking = request.env['tour.booking'].sudo().create(form_data)
            status = {'message': 'Booking Created Successfully','booking':booking.name}
        
        except Exception as e:
            status = {'code': 500, 'message': str(e)}
        return status
    
    # apply onchange on tour
    @http.route('/tour/data', type='json', auth='user', website=True)
    def get_tour_data(self, tour_id, season_id = None, **kwargs):
        if tour_id:
            tour = request.env['tour.package'].sudo().browse(int(tour_id))
            all_dates = request.env['tour.dates'].sudo().search([]).read(['id', 'start_date'])
            dates = []
            
            if tour:
                program = []
                for rec in tour.tour_program_lines:
                    program.append({
                    'name': rec.name ,
                    'days': rec.days,
                    'description': rec.description,
                    'breakfast': rec.breakfast,
                    'lunch': rec.lunch,
                    'dinner': rec.dinner,
                    'expected_line_sale': rec.expected_line_sale,
                    })

                destinations = []
                for rec in tour.tour_destination_lines:
                    destinations.append({
                    'destination_id': rec.destination_id.id or '',
                    'country_id': rec.country_id.id or '',
                    'nights': rec.nights or '',
                    'visa_chk': rec.visa_chk,
                    })

                include = []
                for rec in tour.tour_cost_include_facility_lines:
                    include.append({
                    'include_facility_id': rec.facility_id.id or '',
                    'includename': rec.name or '',
                    })

                exclude = []
                for rec in tour.tour_cost_exclude_facility_lines:
                    exclude.append({
                    'exclude_facility_id': rec.facility_id.id or '',
                    'excludename': rec.name or '',
                    })

                site = []
                for rec in tour.site_costing_tour_ids:
                    site.append({
                    'sitename': rec.name.id or '',
                    'new_cost_price': rec.new_cost_price or '',
                    'new_sale_price': rec.new_sale_price or '',
                    'total_cost_price': rec.total_cost_price or '',
                    'total_sale_price': rec.total_sale_price or '',
                    })

                visa = []
                for rec in tour.visa_costing_tour_ids:
                    visa.append({
                    'country_id': rec.country_id.id or '',
                    'visaname': rec.name or '',
                    'visa_type': rec.visa_type or '',
                    'cost_price': rec.cost_price or '',
                    'sale_price': rec.sale_price or '',
                    'total_person': rec.total_person or '',
                    'total_cost_price': rec.total_cost_price or '',
                    'total_sale_price': rec.total_sale_price or '',
                    })

                hotel = []
                for rec in tour.hotel_planer_tour_ids:
                    hotel.append({
                    'hotelname': rec.name or '',
                    'destination_id': rec.destination_id.id or '',
                    'hotel_type_id': rec.hotel_type_id.id or '',
                    'hotel_id': rec.hotel_id.id or '',
                    'room_type_id': rec.room_type_id.id or '',
                    'room_req': rec.room_req or '',
                    'days': rec.days or '',
                    'supplier_price': rec.supplier_price or '',
                    'customer_price': rec.customer_price or '',
                    'supplier_price_total': rec.supplier_price_total or '',
                    'customer_price_total': rec.customer_price_total or '',
                    })
                travel = []
                for rec in tour.travel_planer_tour_ids:
                    travel.append({
                    'travelname': rec.name or '',
                    'transport_id': rec.transport_id.id or '',
                    'date': rec.date or '',
                    'transport_carrier_id': rec.transport_carrier_id.id or '',
                    'transport_type_id': rec.transport_type_id.id or '',
                    'travel_class_id': rec.travel_class_id.id or '',
                    'from_dest_id': rec.from_dest_id.id or '',
                    'to_dest_id': rec.to_dest_id.id or '',
                    'sale_price_adult': rec.sale_price_adult or '',
                    'sale_price_child': rec.sale_price_child or '',
                    'cost_price_adult': rec.cost_price_adult or '',
                    'cost_price_child': rec.cost_price_child or '',
                    })

                service = []
                for rec in tour.service_tour_ids:
                    service.append({
                    'product_id': rec.product_id.id or '',
                    'sale_price': rec.sale_price or '',
                    'product_uom_qty': rec.product_uom_qty or '',
                    'product_uom_id': rec.product_uom_id.id or '',
                    'discount': rec.discount or '' or 0.00,
                    'price_subtotal': rec.price_subtotal or '',
                    })
                
                                         
                date_dict = {date['start_date']: date['id'] for date in all_dates}          
                for rec in tour.tour_date_lines:
                    start_date = rec.start_date                   
                    tour_date_id = date_dict.get(start_date, '') if start_date else ''                   
                    dates.append({
                        'season_id': rec.season_id.id or '',
                        'tour_dates_id': tour_date_id,
                        'rec_id': rec.start_date,
                    })
 
                dict= {
                    'program' : program,
                    'destinations' : destinations,
                    'include' : include,
                    'exclude' : exclude,
                    'site' : site,
                    'visa' : visa,
                    'hotel' : hotel,
                    'travel' : travel,
                    'service' : service,
                    'dates' : dates
                }
                return dict
        
        return {}

    @http.route('/inquiry/', auth='user', website=True)
    def inquiry(self, **kw):
        if request.env.user.has_group('base.group_system'):
            inquiries = request.env['tour.preference'].sudo().search([])
        else:
            inquiries = request.env['tour.preference'].sudo().search([('create_uid', '=', request.env.user.id)])

        leads = request.env['crm.lead'].sudo().search([('stage_id','=','New')])
        via = request.env['tour.preference'].sudo().search([]).sudo().fields_get(['via'])['via']['selection']
        states = request.env['res.country.state'].sudo().search([])
        countries = request.env['res.country'].sudo().search([])
        hotels = request.env['hotel.type'].sudo().search([])
        rooms = request.env['room.type'].sudo().search([])
        transport = request.env['custom.tour.transport'].sudo().fields_get(['name'])['name']['selection']
        agents = request.env['res.partner'].sudo().search([('agent', '=', True)])

        dict = {
            'inquiries': inquiries,
            'leads': leads,
            'via': via,
            'states': states,
            'countries': countries,
            'hotels': hotels,
            'rooms': rooms,
            'transport': transport,
            'agents': agents,
        }
        return request.render('bi_tour_management.tour_inquiry', dict)

    
    @http.route('/inquiry/data', auth='user', type='json')
    def inquiry_data(self):
        country = request.env['res.country'].sudo().search([]).read(['id','name'])
        destinations = request.env['tour.destination'].sudo().search([]).read(['id','name'])
        transport = request.env['custom.tour.transport'].sudo().fields_get(['name'])['name']['selection']
        type = request.env['product.product'].sudo().search([('type', '=', 'service')]).read(['id','name'])
        travel = request.env['travel.class'].sudo().search([]).read(['id','name'])
        return {
            'country': country,
            'destinations': destinations,
            'transport': transport,
            'type': type,
            'travel': travel,
        }
    
    
    @http.route(['/create-inq'], type='json', auth="public", website=True)
    def create_inq(self, form_data):
        try:
            if form_data.get('destination_lines_ids', False):
                order_line_ids = []
                for rec in form_data.get('destination_lines_ids'):
                    order_line_ids.append((0, 0, {
                        'tour_destination_id': rec.get('tour_destination_id'),
                        'country_id': rec.get('country_id'),
                        'name': rec.get('name'),
                    }))
                form_data["destination_lines_ids"] = order_line_ids
            
            if form_data.get('transport_ids', False):
                transport_line_ids = []
                for rec in form_data.get('transport_ids'):
                    transport_line_ids.append((0, 0, {
                        'travel_class_id': rec.get('travel_class_id'),
                        'product_id': rec.get('product_id'),
                        'name': rec.get('name'),
                    }))
                form_data["transport_ids"] = transport_line_ids

            inquiry = request.env['tour.preference'].sudo().create(form_data)
            status = {'message': 'inquiry Created Successfully','inquiry':inquiry.name}
        
        except Exception as e:
            status = {'code': 500, 'message': str(e)}
        return status
    
    @http.route('/lead/data', type='json', auth='user', website=True)
    def get_lead_data(self, lead_id=None, **kwargs):
        if lead_id:
            lead = request.env['crm.lead'].sudo().browse(int(lead_id))
            if lead:
                return {
                    'street': lead.street or '',
                    'street2': lead.street2 or '',
                    'city': lead.city or '',
                    'zip': lead.zip or '',
                    'country_id': lead.country_id.id or '',
                    'email_id': lead.email_from or '',
                    'contact_name': lead.partner_id.name or '',
                    'state_id': lead.state_id.name or '',
                    'mobile': lead.partner_id.mobile or lead.phone or lead.mobile or '',
                }

        return {}
    
    @http.route('/rate/<string:token>/<int:rate>', type='http', auth="public", website=True)
    def action_open_rating(self, token, rate, **kwargs):
        if rate not in (1, 3, 5):
            raise ValueError(
                _("Incorrect rating: should be 1, 3 or 5 (received %d)"), rate)
        lang = get_lang(request.env).code
        action = request.env['ir.ui.view'].with_context(lang=lang)._render_template('bi_tour_management.tour_rating_external_page_submit', {
            'rate_names': {
                5: _("Satisfied"),
                3: _("Okay"),
                1: _("Dissatisfied"),
            },
            'rate': rate,
            'token': token,
        })
        return action

    @http.route(['/tour/rate_submit_feedback'], type="http", auth="public", methods=['post', 'get'], website=True)
    def action_submit_rating(self, rate=0, **kwargs):
        if request.httprequest.method == "POST":
            rate = int(rate)
            if rate not in (1, 3, 5):
                raise ValueError(
                    _("Incorrect rating: should be 1, 3 or 5 (received %d)"), rate)
            if kwargs.get('token'):
                tour_booking= request.env['tour.booking'].sudo().search([('access_token', '=', kwargs.get('token'))], limit=1)
                if tour_booking:
                    feedback = 'Normal'
                    if rate == 1:
                        feedback = 'Bad'
                    elif rate == 5:
                        feedback = 'Good'
                    message = f"Thank you for rating your tour experience with us! Your feedback: {feedback}"
                    msg = ''
                    if kwargs.get('feedback'):
                        msg = kwargs.get('feedback')
                        message = message + f'Tourist Feedback: {msg}'
                        tour_booking.sudo().message_post(body=message)
        lang = get_lang(request.env).code
        return request.env['ir.ui.view'].with_context(lang=lang)._render_template('bi_tour_management.tour_rating_page_view')
    


    
