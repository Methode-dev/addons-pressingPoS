from odoo import api, fields, models


class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    treatment_ids = fields.Many2many(
        'laundry.treatment',
        'pos_order_line_laundry_treatment_rel',
        'line_id', 'treatment_id',
        string="Treatments",
    )

    @api.model
    def _load_pos_data_fields(self, config):
        return super()._load_pos_data_fields(config) + ['treatment_ids']
