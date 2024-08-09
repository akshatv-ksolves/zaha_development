# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################
from odoo import models, fields, api, _

class visa_booking(models.Model):
    
    _name = "visa.booking"
    _description = "Visa Booking"

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('verify', 'Verify Document'),
        ('approve', 'Approved'),
        ('invoice', 'Invoiced'),
        ('in_process', 'In Process'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
        ],string = "Status", readonly=True, default="draft")
    name = fields.Char("Name" , readonly=True)
    customer_id = fields.Many2one('res.partner',"Customer" , required=True)
    current_date = fields.Date('Date', required=True)
    email_id = fields.Char("Email Id" )
    mobile = fields.Char("Mobile Number" )
    country_id = fields.Many2one('res.country',"Country" , required=True)
    product_id = fields.Many2one('product.product',"Service" , required=True)
    scheme_id = fields.Many2one('visa.scheme',"Service Scheme" )
    service_charge = fields.Float('Service Cost', required=True)
    tour_book_id = fields.Many2one('tour.booking',"Tour Booking Ref" )
    tour_id = fields.Many2one('tour.package',"Tour" )
    tour_date = fields.Date("Tour Date" )
    document_line_ids = fields.One2many('visa.document.line', 'visa_book_id',"document Lines")
    attachment_line_ids = fields.One2many('ir.attachment', 'visa_book_id',"Attachment Lines")
    product_cat_id = fields.Many2one("product.category",string="Catagory Id")
    visa_invoice_ids = fields.Many2many('account.move',readonly=True,string="Passport Invoice Lines")
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    
    invoice_count = fields.Integer("Invoice",compute="_Invoice_count")

    @api.onchange('customer_id')
    def onchange_cata(self):
        pro_category = self.env["product.category"]
        product_cat_id = pro_category.search([("name","=","Visa Services")])
        return {'domain' : {'product_id' : [('type', '=', 'service'),('categ_id', '=', product_cat_id.id)]}}

    @api.onchange("customer_id")
    def onchange_customer(self):
        for rec in self:
            rec.email_id = rec.customer_id.email

    def button_confirm(self):
        for rec in self:
            rec.state = 'confirm'
        
    def verify_document(self):
        for rec in self:
            rec.state = 'verify'
        
    def approve_document(self):
        for rec in self:
            rec.state = 'approve'

    def method_done(self):
        for rec in self:
            rec.state = 'done'
    
    def method_cancel(self):
        for rec in self:
            rec.state = "cancel"
    
    def create_invoice(self):
        for rec in self:
            account_obj = rec.env['account.move']
            account_vals={'partner_id':rec.customer_id.id, 
                  'user_id':rec.env.user.id,
                  
                  'currency_id':rec.env.user.company_id.currency_id.id,
                  'move_type':'out_invoice',
                  'company_id':rec.env.user.company_id.id,
                  'name':rec.name,
                  'invoice_line_ids':[(0,0,{'product_id':rec.product_id.id,'name':rec.name,'account_id':rec.product_id.property_account_income_id.id or rec.product_id.categ_id.property_account_income_categ_id.id,'quantity':1,'price_unit':rec.service_charge})]
                  }
            inv = account_obj.create(account_vals)
            rec.state = 'invoice'
   
    def _Invoice_count(self):
        for invoi_count in self:
            if invoi_count.name != False:
                invoice_order_ids = self.env["account.move"].search([('name','=',invoi_count.name)])
                invoi_count.invoice_count = len(invoice_order_ids)
            else:
                invoi_count.invoice_count = 0

    def button_count_invoice(self):
        self.ensure_one()
        return {
                'name': 'Invoice',
                'type': 'ir.actions.act_window',
                'view_mode': 'kanban,tree,form',
                'res_model': 'account.move',
                'domain': [('name','=',self.name)],
                } 
    
    @api.onchange('customer_id')
    def customer_id_onchange(self):
        for rec in self:
            if rec.customer_id:
                rec.mobile = rec.customer_id.mobile
                rec.email_id = rec.customer_id.email
    
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].get('visa.booking') or '/'
        return super(visa_booking, self).create(vals)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: