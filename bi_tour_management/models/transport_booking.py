# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################
from odoo import models, fields, api, _
from odoo.exceptions import  UserError,ValidationError
		
class transport_booking(models.Model):
	_name = "transport.booking"
	_description = "Transport Booking"

	state = fields.Selection([
		('draft', 'Draft'),
		('confirm', 'Confirm'),
		('approve', 'Approved'),
		('invoiced', 'Invoice'),
		('issue', 'Ticket Issue'),
		('done', 'Done'),
		('cancel', 'Cancelled'),
		],string="Status", default="draft")
	name = fields.Char("Registration ID" ,readonly=True)
	current_date=fields.Date('Booking Date',required=True)
	customer_id = fields.Many2one('res.partner','Customer',required=True)
	pricelist_id = fields.Many2one('res.currency',"Currency ", required=True)
	child = fields.Integer("Child" , required=True)
	adult = fields.Integer("Adult" , required=True)
	email_id = fields.Char("Email Id" )
	mobile = fields.Char("Mobile" , required=True)
	transport_id = fields.Many2one('transport.information',"Transport Company " , required=True)
	checkin_date=fields.Date('Journey Date',required=True)
	transport_carrier_id = fields.Many2one('transport.carrier',"Carrier Name " , required=True)
	transport_type_id = fields.Many2one('product.product',"Transport Type " , required=True)
	travel_class_id = fields.Many2one('travel.class',"Travel Class " , required=True)
	from_destination_id=fields.Many2one('tour.destination','From',required=True)
	to_destination_id=fields.Many2one('tour.destination','To',required=True)
	tour_id = fields.Many2one('tour.package','Tour',readonly=True)
	tour_book_id = fields.Many2one('tour.booking','Tour Booking Ref',readonly=True)
	tour_date_id = fields.Many2one('tour.dates','Tour Start Date',readonly=True)
	pnr_no = fields.Char("PNR No." )
	carrier_id = fields.Char("Carrier No" )
	arrival_date = fields.Datetime('Arrival Date')
	depart_date = fields.Datetime('Departure Date')
	cost_price = fields.Float('Cost Price(Adult)')
	cost_price_child = fields.Float('Cost Price(Child)')
	sale_price = fields.Float('Sale Price(Adult)')
	sale_price_child = fields.Float('Sale Price(Child)')
	customer_line_ids = fields.One2many('tour.customer.details','trans_book_id',"Customer Information")
	tax_id = fields.Many2many('account.tax', string="Taxes")
	transport_room_reserve_supplier_invoice_ids = fields.Many2many('account.move',string="Invoice History")
	untax_amt = fields.Float('Untaxed Amount',compute='_compute_amount',readonly=True)
	tax_amt = fields.Float('TAXES',compute='_compute_amount',readonly=True)
	total_amt = fields.Float('Customer Invoice Amount',compute='_compute_amount',readonly=True)
	total_amt_transport = fields.Float('Transport Invoice Amount',compute='_compute_amount',readonly=True)
	invoice_count = fields.Integer("Invoice",compute="_Invoice_count")
	company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

	@api.constrains('arrival_date')
	def check_arrival_date(self):
		for rec in self:
			if rec.arrival_date > rec.depart_date:
				raise ValidationError("Arrival Date Can not Greater than Departure Date.")

	@api.constrains('depart_date')
	def check_depart_date(self):
		for rec in self:
			if rec.depart_date < rec.arrival_date:
				raise ValidationError("Departure Date Can not Less than Arrival Date.")
	
	@api.depends('tax_id','customer_line_ids')
	def _compute_amount(self):
		for rec in self:
			tax = 0.0
			if rec.tax_id :
				tax= sum(tax.amount for tax in rec.tax_id)
			rec.tax_amt = tax
			total = 0.0
			child_total = 0.0
			if rec.customer_line_ids:
				for line in rec.customer_line_ids:
					if line.type == 'adult':
						total += 1.0
					if line.type == 'child':
						child_total  += 1.0
			rec.untax_amt = rec.sale_price * total + rec.sale_price_child * child_total
			rec.total_amt_transport = rec.cost_price * total  + rec.cost_price_child * child_total
			rec.total_amt = rec.untax_amt + rec.tax_amt
		

	@api.model
	def create(self,vals):
		vals['name'] = self.env['ir.sequence'].get('transport.booking') or '/'
		if vals['adult'] == 0:
			raise UserError('Please Check Person for this Booking')
		   
		res = super(transport_booking, self).create(vals)
		return res
 
	def button_confirm(self):
		for rec in self:
			total = rec.adult + rec.child
			if len(rec.customer_line_ids) != total:
				raise UserError('Customer Record Missing.')
			rec.state = 'confirm'
		

	def send_to_hotel(self):
		self.ensure_one()
		ir_model_data = self.env['ir.model.data']
		template_id = ir_model_data._xmlid_lookup('bi_tour_management.email_template_transport_edi')[1]
		compose_form_id = ir_model_data._xmlid_lookup('mail.email_compose_message_wizard_form')[1]
		

		ctx = {
			'default_model': 'transport.booking',
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
	
	def make_approval(self):
		for rec in self:
			rec.state = 'approve'
	

	def create_invoice(self):
		for rec in self:
			account_obj = self.env['account.move']
			account_vals={'partner_id':rec.customer_id.id, 
				  'user_id':rec.env.user.id,
				  
				  'currency_id':rec.pricelist_id.id,
				  'move_type':'out_invoice',
				  'company_id':rec.env.user.company_id.id,
				  'invoice_origin':rec.name,
				  'name':rec.name,
				  'invoice_line_ids':[(0,0,{'product_id':rec.transport_type_id.id,'name':rec.name,'account_id':rec.transport_type_id.property_account_income_id.id or rec.transport_type_id.categ_id.property_account_income_categ_id.id,'quantity':1,'price_unit':rec.untax_amt})]
				  }
			account_final_vals={'partner_id':rec.transport_id.partner_id.id, 
				  'user_id':rec.env.user.id,
				  
				  'currency_id':rec.pricelist_id.id,
				  
				  'company_id':rec.env.user.company_id.id,
				  'move_type':'in_invoice',
				  'invoice_origin':rec.name,
				  'name':rec.name,
				  'invoice_line_ids':[(0,0,{'product_id':rec.transport_type_id.id,'name':rec.name,'account_id':rec.transport_type_id.property_account_expense_id.id or rec.transport_type_id.categ_id.property_account_expense_categ_id.id,'quantity':1,'price_unit':rec.total_amt_transport})]
				  }
			inv = account_obj.create(account_vals)
			rec.transport_room_reserve_supplier_invoice_ids=[(6,0,[inv.id])]
			account_obj.create(account_final_vals)
			rec.state = 'issue'

	def _Invoice_count(self):
		for rec in self:
			if rec.name != False:
				invoice_order_ids = self.env["account.move"].search([('name','=',rec.name)])
				rec.invoice_count = len(invoice_order_ids)
			else:
				rec.invoice_count = 0

	def button_count_invoice(self):
		self.ensure_one()
		return {
			'name': 'Invoice',
			'type': 'ir.actions.act_window',
			'view_mode': 'kanban,tree,form',
			'res_model': 'account.move',
			'domain': [('name','=',self.name)],
		}

	def make_done(self):
		for rec in self:
			rec.state="done"

	def button_cancel(self):
		for rec in self:
			rec.state="cancel"

	@api.onchange('customer_id')
	def partner_id_onchange(self):
		for rec in self:
			if rec.customer_id:
				rec.email_id = rec.customer_id.email
				rec.mobile= rec.customer_id.mobile
 
 # vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:           
