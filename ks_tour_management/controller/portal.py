from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError
from datetime import datetime


class Portal(http.Controller):
    @http.route(['/my/enquiry'], type='http', auth="user", website=True)
    def lead_enquiry_form(self, **kwargs):
        states = sorted(request.env['res.country.state'].search([]))
        countries = request.env['res.country'].search([])
        company = request.env['res.company'].search([])
        agent = request.env['res.partner'].sudo().search([('agent', '=', 'True')])
        hotel_list = request.env['hotel.type'].sudo().search([])
        room_list = request.env['room.type'].sudo().search([])
        return request.render("ks_tour_management.lead_enquiry_form_template", {
            'states': states,
            'countries': countries,
            'company': company,
            'agents': agent,
            'hotel_list': hotel_list,
            'room_list': room_list,
        })

    @http.route(['/my/enquiry/submit'], type='http', auth="user", website=True, methods=['POST'])
    def lead_enquiry_form_submit(self, **post):
        lead_id = request.env['crm.lead'].sudo().create({
            'name': post.get("lead"),
            'contact_name': post.get("contact_name"),
            'partner_id': request.env['res.partner'].sudo().create({'name': post.get("contact_name")}).id,
            'partner_name':request.env['res.company'].search([('id','=',post.get('company_id'))]).name,
            'email_from': post.get('email_id'),
            'mobile': post.get('mobile'),
            'street': post.get('street'),
            'street2': post.get('street2'),
            'city': post.get('city'),
            'zip': post.get('zip'),
            'state_id': post.get("state_id"),
            'country_id': post.get("country_id"),
            'type': 'lead',
        }).id

        agent_id = post.get('agent_ids.name')

        # Create new destination line
        destination_id = request.env['tour.destination'].sudo().search([('name', '=', post.get('destination'))]).id
        if not destination_id:
            destination_id = request.env['tour.destination'].sudo().create({
                'name': post.get("destination"),
                'code': (post.get('destination')[0] + post.get('destination')[-1]).upper(),
                'country_id': post.get('dest_country_id'),
            }).id
        destination_lines = []
        destination_line = request.env['custom.tour.destination'].sudo().create({
            'tour_destination_id': destination_id,
            'name': int(post.get('no_of_nights')),
            'country_id': post.get('dest_country_id'),
        })
        destination_lines.append((4, destination_line.id))

        # Create new hotel line records------------------------------------------------------------------------------------
        # hotel_type_id = request.env['hotel.type'].sudo().search([('name', '=', post.get('hotel_type'))]).id
        # if not hotel_type_id:
        #     hotel_type_id = request.env['hotel.type'].sudo().create({'name': post.get('hotel_type')}).id
        # room_type_name = post.get('room_type')
        # room_type = request.env['room.type'].sudo().search([('name', '=', room_type_name)], limit=1).id
        # if not room_type:
        #     product_template = request.env['product.template'].sudo().search([('name', '=', room_type_name)], limit=1)
        #     if not product_template:
        #         product_template = request.env['product.template'].sudo().create({'name': room_type_name})
        #     product = request.env['product.product'].sudo().search([('product_tmpl_id', '=', product_template.id)], limit=1)
        #     if not product:
        #         product = request.env['product.product'].sudo().create({'product_tmpl_id': product_template.id})
        #     room_type = request.env['room.type'].sudo().create({'name': room_type_name, 'room_type_id': product.id}).id

        # create a new trasnport line--------------------------------------------------------------------------------------
        print(post.get('transport_destination'), type(post.get('transport_destination')), '-------')
        transport_lines = []
        transport_type_name = post.get('transport_type')
        if transport_type_name:
            transport_template = request.env['product.template'].sudo().search([('name', '=', transport_type_name)],
                                                                               limit=1)
            if not transport_template:
                transport_template = request.env['product.template'].sudo().create({'name': transport_type_name})
            transport_product = request.env['product.product'].sudo().search(
                [('product_tmpl_id', '=', transport_template.id)], limit=1)
            if not transport_product:
                transport_product = request.env['product.product'].sudo().create(
                    {'product_tmpl_id': transport_template.id})
            transport_prod_id = transport_product.id

            travel_class_id = request.env['travel.class'].sudo().search([('name', '=', post.get('travel_class'))]).id
            if not travel_class_id:
                travel_class_id = request.env['travel.class'].sudo().create({
                    'name': post.get('travel_class'),
                    'transport_type_id': transport_prod_id,
                }).id

            transport_line = request.env['custom.tour.transport'].sudo().create({
                'name': post.get('transport_destination'),
                'product_id': transport_prod_id,
                'travel_class_id': travel_class_id,
            })
            transport_lines.append((4, transport_line.id))

        print("works")

        request.env['tour.preference'].sudo().create({
            'current_date': post.get("inquiry_date"),
            'lead_id': lead_id,
            'email_id': post.get("email_id"),
            'contact_name': post.get("contact_name"),
            'company_id': int(post.get("company_id")),
            'mobile': post.get("mobile"),
            'street2': post.get("street2"),
            'zip': post.get("zip"),
            'city': post.get("city"),
            'state_id': post.get("state_id"),
            'country_id': post.get("country_id"),
            'adult': post.get("adult_persons"),
            'child': post.get("child"),
            'via': post.get("via"),
            'agent_id': post.get("agent_ids"),
            'checkin_date': post.get("arrival_date"),
            'checkout_date': post.get("departure_date"),
            # 'tour_low_price': post.get("budget_min"),
            # 'tour_high_price': post.get("budget_max"),
            'destination_lines_ids': destination_lines,
            'hotel_type_id': post.get('hotel_type'),
            'room_type_id': post.get('room_type'),
            'room_req': post.get("hotel_number_of_rooms"),
            'low_price': post.get("hotel_budget_min"),
            'high_price': post.get("hotel_budget_max"),
            'transport_ids': transport_lines
        })

        return request.redirect('/my/enquiry/submitted')

    @http.route(['/my/booking'], type='http', auth='user', website=True)
    def user_detail_form(self):
        room_lines = request.env['room.type'].search([])
        hotel_name_lines = request.env['res.partner'].search([('is_hotel','=','True')])
        return request.render("ks_tour_management.user_detail_form_template",{
            'room_lines': room_lines,
            'hotel_name_lines': hotel_name_lines
        })

    @http.route(['/my/booking/submit'], type='http', auth='user', website=True)
    def user_detail_form_submit(self, **post):
        current_user = request.env.user
        print(current_user.id,current_user.name)
        max_lead = max(list(request.env['crm.lead'].sudo().search([]).mapped('id')))
        lead_id = request.env['crm.lead'].sudo().create({
            'name': f'New Tour Lead #{max_lead}',
            'contact_name': current_user.name,
            'type': 'lead',
        }).id

        request.env['tour.preference'].sudo().create({
            'current_date': datetime.today().strftime('%Y-%m-%d'),
            'lead_id': lead_id,
            'email_id': current_user.email,
            'mobile': 'N/A',
            'adult': post.get("adultsBooking"),
            'child': post.get("childBooking"),
            'checkin_date': post.get("arrivalDateBooking"),
            'checkout_date': post.get("departureDateBooking"),
            'room_type_id': post.get('room_type'),
            'room_req': post.get("numRooms"),
        })
        return request.redirect('/my/booking')

    @http.route(['/my/enquiry/submitted'], type='http', auth="user", website=True)
    def form_submitted_successfully(self):
        return request.render('ks_tour_management.submitted_form_template')
