import pytz
from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PosOrder(models.Model):
    _inherit = 'pos.order'

    laundry_number = fields.Integer(copy=False, index=True, readonly=True)
    laundry_number_display = fields.Char(
        string="Ticket n°",
        compute='_compute_laundry_number_display',
        store=True, index=True,
    )
    pickup_datetime = fields.Datetime(string="Ready for pickup")
    laundry_tags_printed = fields.Boolean(copy=False)

    @api.depends('laundry_number')
    def _compute_laundry_number_display(self):
        for order in self:
            order.laundry_number_display = (
                str(order.laundry_number % 10000).zfill(4)
                if order.laundry_number else False
            )

    @api.model
    def _load_pos_data_fields(self, config):
        return super()._load_pos_data_fields(config) + [
            'laundry_number', 'laundry_number_display',
            'pickup_datetime', 'laundry_tags_printed',
        ]

    @api.model
    def laundry_assign_number(self, order_ids):
        """Assign a laundry number to draft orders. Idempotent."""
        result = {}
        for order in self.browse(order_ids):
            if order.state != 'draft':
                raise UserError(_("Intake is only possible on a draft order."))
            if not order.laundry_number:
                sequence = order.config_id._laundry_get_sequence()
                order.laundry_number = int(sequence.next_by_id())
            result[order.id] = {
                'laundry_number': order.laundry_number,
                'laundry_number_display': order.laundry_number_display,
            }
        return result

    @api.model
    def laundry_compute_pickup(self, config_id, lead_days=0):
        """Authoritative pickup datetime. Returns a naive UTC string."""
        config = self.env['pos.config'].browse(config_id)
        tz = pytz.timezone(self.env.user.tz or 'Europe/Paris')
        local = pytz.utc.localize(fields.Datetime.now()).astimezone(tz)

        days = lead_days or config.laundry_lead_days
        if local.hour + local.minute / 60.0 >= config.laundry_cutoff_hour:
            days += 1

        target = local + timedelta(days=days)
        hour = int(config.laundry_ready_hour)
        target = target.replace(
            hour=hour,
            minute=int((config.laundry_ready_hour - hour) * 60),
            second=0, microsecond=0,
        )

        closed = {int(d) for d in (config.laundry_closed_weekdays or '') if d.isdigit()}
        for _i in range(7):
            if target.weekday() not in closed:
                break
            target += timedelta(days=1)

        return fields.Datetime.to_string(target.astimezone(pytz.utc).replace(tzinfo=None))
