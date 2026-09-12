from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_laundry_mode = fields.Boolean(
        related='pos_config_id.laundry_mode', readonly=False)
    pos_laundry_lead_days = fields.Integer(
        related='pos_config_id.laundry_lead_days', readonly=False)
    pos_laundry_cutoff_hour = fields.Float(
        related='pos_config_id.laundry_cutoff_hour', readonly=False)
    pos_laundry_ready_hour = fields.Float(
        related='pos_config_id.laundry_ready_hour', readonly=False)
    pos_laundry_closed_weekdays = fields.Char(
        related='pos_config_id.laundry_closed_weekdays', readonly=False)
