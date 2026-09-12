from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_laundry_item = fields.Boolean(
        string="Laundry item",
        help="Garments to tag. Uncheck for retail products and services.",
    )
    laundry_lead_days = fields.Integer(
        string="Lead time (days)",
        help="Overrides the POS default. 0 = use the POS setting.",
    )

    @api.model
    def _load_pos_data_fields(self, config):
        return super()._load_pos_data_fields(config) + [
            'is_laundry_item', 'laundry_lead_days',
        ]
