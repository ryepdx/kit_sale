# -*- coding: utf-8 -*-

from openerp import SUPERUSER_ID
from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class product(osv.osv):
    _inherit = "product.product"

    def get_product_available(self, cr, uid, ids, context=None):
        """ Finds whether product is available or not in a particular warehouse.
        @return: Dictionary of values
        """
        bom_pool = self.pool.get("mrp.bom")

        res = super(product, self).get_product_available(cr, uid, ids, context=context)

        if 'done' not in context.get('states', []) or 'in' not in context.get('what', []):
            return res

        for prod_id in res:
            bom = bom_pool.browse(cr, uid, bom_pool.search(cr, uid, [('product_id', '=', prod_id)]))

            if not bom or not bom[0].bom_lines:
                continue

            quantities = []

            for l in bom[0].bom_lines:
                if not l.product_qty:
                    quantities.append(0)
                    break

                quantities.append(
                    (res[l.product_id.id] if l.product_id.id in res else l.product_id.qty_available) / l.product_qty)

            res[prod_id] += min(quantities)

        return res

product()