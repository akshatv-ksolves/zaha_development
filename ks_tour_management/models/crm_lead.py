from odoo import fields, models, api

class Lead(models.Model):
    _inherit = 'crm.lead'

    room_type = fields.Char(string='Room Type')
    arrival_date = fields.Date(string='Arrival Date')
    departure_date = fields.Date(string='Departure Date')
    children_ages = fields.One2many('crm.lead.child.age', 'lead_id', string='Children Ages')
    infants_ages = fields.One2many('crm.lead.infant.age', 'lead_id', string='Infant Ages')
    no_of_rooms = fields.Integer(string='Number of Rooms')
    adult_count = fields.Integer(string='Adult count')


class LeadChildAge(models.Model):
    _name = 'crm.lead.child.age'
    _description = 'Lead Child Age'

    lead_id = fields.Many2one('crm.lead', string='Lead')
    age_group = fields.Char(string='Age Group', default='Between 2-12yrs', readonly=True)
    child_count = fields.Integer(string='Child Count')
    age = fields.Float(string='Age')


class LeadInfantAge(models.Model):
    _name = 'crm.lead.infant.age'
    _description = 'Lead Infant Age'

    lead_id = fields.Many2one('crm.lead', string='Lead')
    age_group = fields.Char(string='Age Group', default='Between 0-2yrs', readonly=True)
    infant_count = fields.Integer(string='Infant Count')
    age = fields.Float(string='Age')

