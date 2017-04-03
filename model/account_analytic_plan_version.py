# -*- coding: utf-8 -*-

from openerp.tools.translate import _
from openerp import api, fields, models
from openerp.exceptions import Warning as UserError


class AccountAnalyticPlanVersion(models.Model):
    _inherit = 'account.analytic.plan.version'

    default_resource_plan = fields.Boolean(
        'Default for resource plan',
        default=False
    )

    @api.model
    def _check_default_resource(self, vals):
        if 'default_resource_plan' in vals:
            if vals['default_resource_plan'] is True:
                other_default_resource = self.search(
                    [('default_resource_plan', '=', True)]
                )
                if other_default_resource:
                    raise UserError(
                        _(
                            'Only one default for resource '
                            'plan version can exist.'
                        )
                    )

    @api.model
    def create(self, vals):
        self._check_default_resource(vals)
        res = super(AccountAnalyticPlanVersion, self).create(vals)
        return res

    @api.multi
    def write(self, vals):
        self._check_default_resource(vals)
        return super(AccountAnalyticPlanVersion, self).write(vals)
