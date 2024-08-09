# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError,ValidationError
	
class custom_tour_itinary(models.Model):
	
	_name = "custom.tour.itinary"
	_description = "Custom Tour Itinary"


	name = fields.Char('Itinerary No.',readonly=True)
	state = fields.Selection([
		('draft', 'Draft'),
		('confirm', 'Confirm'),
		('approve', 'Approve'),
		('refuse', 'Refuse'),
		('done', 'Done'),
		],string="status",default="draft", readonly=True)
	product_itinary_id = fields.Many2one('product.product', 'Tour', required=True)
	tour_preference_id = fields.Many2one('tour.preference','Customer Inquiry',required=True)
	tour_name = fields.Char('Tour Name',required=True)
	current_date = fields.Date('Inquiry Date',required=True,default=fields.date.today())
	lead_id = fields.Many2one('crm.lead','Lead',required=True)
	contact_name = fields.Char('Contact Name')
	company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
	street = fields.Char('Street')
	street2 = fields.Char('Street2')
	zip = fields.Char('Zip', change_default=True)
	city = fields.Char('City')
	state_id = fields.Many2one("res.country.state", string='State')
	country_id = fields.Many2one('res.country', string='Origin')

	email_id = fields.Char('Email Id',required=True)
	mobile = fields.Char('Mobile',required=True )
	adult = fields.Integer('Adult',required=True )
	season_id = fields.Many2one('tour.season',string="Season",required=True)
	child = fields.Integer('Child',required=True )
	product_pricelist_id = fields.Many2one('res.currency','Currency',required=True)
	via= fields.Selection([
		('direct', 'Direct'),
		('agent', 'Agent'),
		],string="Via",default="direct",required=True)
	agent_partner_id= fields.Many2one('res.partner','Agent')
	checkin_date = fields.Date('Prefer start Date',required=True)
	checkout_date = fields.Date('Prefer End Date',required=True)
	room_required = fields.Integer('Room Required',readonly=True )
	tour_payment_policy_id=  fields.Many2one('tour.payment.policy','Payment Policy',required=True)
	start_date = fields.Date('Start Date of Tour',required=True)
	book_date = fields.Date('Last Date of Booking',required=True)
	due_date = fields.Date('Payment Due Date',required=True)
	total_seat = fields.Integer('Total Seats', compute="_count_seat", readonly=True )
	adult_cost_price = fields.Float('Sale Price/ Person(Adult)',compute="_count_price",readonly=True )
	child_cost_price = fields.Float('Sale Price/ Person(Child)',compute="_count_price",readonly=True )
	tour_program_ids = fields.One2many('tour.program','iternity_id','Tour Program Lines')
	tour_destination_ids = fields.One2many('tour.destination.line','iternity_id','Tour Destination Line')
	itinary_cost_include_facility_lines = fields.One2many('tour.cost.include.facility','iternity_id','Itinary Cost Include Facility Lines')
	itinary_cost_exclude_facility_lines=  fields.One2many('tour.cost.exclude.facility','iternity_id','Itinary Cost Exclude Facility Lines')
	sites_costing_ids = fields.One2many('sites.costing.line','iternity_id','Site Costing Lines')
	visa_costing_ids =  fields.One2many('visa.costing.line','iternity_id','Visa Costing Lines')
	service_ids = fields.One2many('tour.service.line.details','iternity_id','Others Services')
	hotel_planer_ids = fields.One2many('hotel.planner.details','iternity_id','Hotel Detail Lines')
	travel_planer_ids= fields.One2many('travel.planner.details','iternity_id','Travel Details Lines')
	sale_untax_amt = fields.Float('Sale Untaxed Amount',compute="_count_price",readonly=True)
	sale_tax_amt = fields.Float('Sale Taxes',compute="_count_price",readonly=True)
	sale_total_amt = fields.Float('Sale Total Amount ',compute="_count_price",readonly=True)
	pur_untax_amt = fields.Float('Purchase Untaxed Amount ', compute="_count_price",readonly=True)
	pur_tax_amt = fields.Float('Purchase Taxes',compute="_count_price",readonly=True)
	pur_total_amt= fields.Float('Purchase Total Amount',compute="_count_price",readonly=True)

	travel_pla_etails_id = fields.Many2one("travel.planner.details")
	currency_id = fields.Many2one('res.currency', string='Currency')
	total_days_number = fields.Integer(string="Total Days")
	total_nights_number = fields.Integer(string="Total Nights")
	

	@api.onchange('adult','child')
	def _on_changeitnary_person(self):

		for trevl in self.travel_planer_ids:
			trevl.total_cost_price_adult = self.adult * trevl.cost_price_adult
			trevl.total_sale_price_adult = self.adult * trevl.sale_price_adult

			trevl.total_sale_price_child = self.child * trevl.sale_price_child
			trevl.total_cost_price_child = self.child * trevl.cost_price_child

	@api.constrains('checkin_date')
	def check_checkin_date(self):
		for rec in self:
			if rec.checkin_date > rec.checkout_date:
				raise ValidationError("Prefer Start Date Can not Greater than Prefer End Date.")

	@api.constrains('checkout_date')
	def check_checkout_date(self):
		for rec in self:
			if rec.checkout_date < rec.checkin_date:
				raise ValidationError("Prefer End Date Can not Less than Prefer Start Date.")

	@api.constrains('start_date')
	def check_start_date(self):
		for rec in self:
			if rec.start_date < rec.book_date:
				raise ValidationError(" Last Date of Booking Can not Greater than Start Date.")

	@api.depends('adult','child')
	def _count_seat(self):
		for rec in self:
			rec.total_seat = rec.adult + rec.child

	def action_approve(self):
		for rec in self:
			rec.write({'state':'approve'})

	def _count_price(self):
		for rec in self:

			sale_total = 0.00
			price = 0.00
			sale_price_child = 0.00
			taxes_sale = 0.00
			tax_purchase = 0.00

			for tour_program in rec.tour_program_ids:
				sale_total += tour_program.expected_line_sale
				price += tour_program.expected_line_cost


			for site_cost in rec.sites_costing_ids:
				sale_total += site_cost.total_sale_price
				price += site_cost.total_cost_price

			for visa_cost in rec.visa_costing_ids:
				sale_total += visa_cost.total_sale_price
				price += visa_cost.total_cost_price
				taxes_sale += visa_cost.sale_tax_amount_visa
				tax_purchase += visa_cost.purchse_tax_amount_visa

			for service in rec.service_ids:
				sale_total += service.price_subtotal
				price += service.pur_tour_service
				taxes_sale +=service.sale_tax_amount_tour
				tax_purchase += service.purchse_tax_amount_tour

			for hotel_planner in rec.hotel_planer_ids:
				sale_total += hotel_planner.customer_price_total
				price += hotel_planner.supplier_price_total
				taxes_sale += hotel_planner.sale_tax_amount_htl
				tax_purchase += hotel_planner.purchse_tax_amount_htl
			
			for travel_planner in rec.travel_planer_ids:
				sale_total += travel_planner.total_sale_amount
				price += travel_planner.total_purchase_amount
				taxes_sale += travel_planner.sale_tax_amt_travel
				tax_purchase += travel_planner.pur_tax_amt_travel

				rec.adult_cost_price = travel_planner.sale_price_adult
				rec.child_cost_price = travel_planner.sale_price_child
			
			rec.sale_tax_amt = taxes_sale
			rec.pur_tax_amt = tax_purchase
			rec.sale_untax_amt = sale_total
			rec.pur_untax_amt = price

			rec.sale_total_amt = rec.sale_untax_amt + rec.sale_tax_amt
			rec.pur_total_amt = rec.pur_untax_amt + rec.pur_tax_amt

	@api.onchange('tour_preference_id')
	def tour_preference_id_onchange(self):
		for rec in self:
			rec.contact_name  = rec.tour_preference_id.contact_name  or False
			rec.lead_id  = rec.tour_preference_id.lead_id.id  or False
			rec.mobile  = rec.tour_preference_id.mobile or False
			rec.email_id  = rec.tour_preference_id.email_id or False
			rec.street = rec.tour_preference_id.street or False
			rec.street2 = rec.tour_preference_id.street2 or False
			rec.zip = rec.tour_preference_id.zip or False
			rec.city = rec.tour_preference_id.city or False
			rec.state_id = rec.tour_preference_id.state_id or False
			rec.country_id = rec.tour_preference_id.country_id or False
			rec.adult  = rec.tour_preference_id.adult
			rec.child = rec.tour_preference_id.child
			rec.checkin_date = rec.tour_preference_id.checkin_date or False
			rec.checkout_date = rec.tour_preference_id.checkout_date or False
			rec.via = rec.tour_preference_id.via
			rec.agent_partner_id = rec.tour_preference_id.agent_id.id or False
			rec.room_required = rec.tour_preference_id.room_req or False

			ids = []
			for res in rec.tour_preference_id.destination_lines_ids :
				destination = rec.env['tour.destination.line'].create({
								  'iternity_id' : rec.id,
								  'destination_id' : res.tour_destination_id.id,
								  'country_id' : res.country_id.id,
								  'nights' : res.name,
									})
				ids.append(destination.id)

			if len(ids) != 0:
				rec.tour_destination_ids = [[6,0,ids]]

	@api.model
	def create(self,vals):
		vals['name'] = self.env['ir.sequence'].get('custom.tour.itinary') or '/'
		res = super(custom_tour_itinary, self).create(vals)
		return res
		
	def action_confirm(self):
		for rec in self:
			if rec.book_date < rec.due_date:
				raise UserError('Payment Due Date should not be less than Last Date of Booking.') 
			rec.state = 'confirm'

	def action_create_tour(self):
		self.ensure_one()
		product_obj = self.env['product.product']
		tour_package_obj = self.env['tour.package']
		product_id = product_obj.search([('name', '=', 'Custom Tour')], limit=1)
		if not product_id :
			product_id = product_obj.create({'name':'Custom Tour', 'type': 'service',  'is_tour': 1})
		vals={'name':self.tour_name,'code':' ','product_id':product_id.id,'tour_type':'domastic','current_date':self.current_date,'days':'1'}
		tour_package_id = tour_package_obj.create(vals)
		tour_package_id.tour_date_lines = [(0,0,{
						'season_id':self.season_id.id,
						'start_date':self.start_date,
						'book_date':self.book_date,
						'due_date':self.due_date,
						'total_seat': self.adult + self.child,
						'available_date':self.adult + self.child,
						'state':'available' })]
		
		if self.tour_destination_ids:
			for tour_destination in self.tour_destination_ids:
				tour_package_id.tour_destination_lines = [(0,0,{'destination_id':tour_destination.destination_id.id,'country_id':tour_destination.country_id.id,'nights':tour_destination.nights})]
		if self.tour_program_ids:
			for tour_program in self.tour_program_ids:
				tour_package_id.tour_program_lines  = [(0,0,{'name':tour_program.name,'days':tour_program.days,'description':tour_program.description,'breakfast':tour_program.breakfast,'lunch':tour_program.lunch,'dinner':tour_program.dinner})]
		if self.itinary_cost_include_facility_lines:
			for cost_include in self.itinary_cost_include_facility_lines:
				tour_package_id.tour_cost_include_facility_lines  = [(0,0,{'facility_id':cost_include.facility_id.id,'name':cost_include.name})]
		if self.itinary_cost_exclude_facility_lines:
			for cost_exclude in self.itinary_cost_exclude_facility_lines:
				tour_package_id.tour_cost_exclude_facility_lines  = [(0,0,{'facility_id':cost_exclude.facility_id.id,'name':cost_exclude.name})]
		site_costing_list = []
		if self.sites_costing_ids:
			for site_cost in self.sites_costing_ids:
				site_costing_list.append(site_cost.id)
			tour_package_id.site_costing_tour_ids = [(6, 0, site_costing_list)]
		visa_cost_list = []
		if self.visa_costing_ids:
			for visa_cost in self.visa_costing_ids:
				visa_cost_list.append(visa_cost.id)
			tour_package_id.visa_costing_tour_ids = [(6, 0, visa_cost_list)]

		hotel_planer_list = []
		if self.hotel_planer_ids:
			for hotel_plan in self.hotel_planer_ids:
				hotel_planer_list.append(hotel_plan.id)
			tour_package_id.hotel_planer_tour_ids = [(6, 0, hotel_planer_list)]
		travel_planer_list = []
		if self.travel_planer_ids:
			for travel_plan in self.travel_planer_ids:
				travel_planer_list.append(travel_plan.id)
			tour_package_id.travel_planer_tour_ids = [(6, 0, travel_planer_list)]
		service_list = []
		if self.service_ids:
			for services_datas in self.service_ids:
				service_list.append(services_datas.id)
			tour_package_id.service_tour_ids = [(6, 0, service_list)]
		self.state = 'done'


	def action_sent(self):

		self.ensure_one()
		ir_model_data = self.env['ir.model.data']
		template_id = ir_model_data._xmlid_lookup('bi_tour_management.email_template_edi')[1]
		compose_form_id = ir_model_data._xmlid_lookup('mail.email_compose_message_wizard_form')[1]
		

		ctx = {
			'default_model': 'custom.tour.itinary',
			'default_res_ids': self.ids,
			'default_use_template': bool(template_id),
			'default_template_id': template_id,
			'default_composition_mode': 'comment',
			'mark_so_as_sent': True,
			'force_email': True
		}
		return {
			'type': 'ir.actions.act_window',
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'mail.compose.message',
			'views': [(compose_form_id, 'form')],
			'view_id': compose_form_id,
			'target': 'new',
			'context': ctx,
		}

	def action_refuse(self):
		for rec in self:
			rec.state = 'refuse'

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: