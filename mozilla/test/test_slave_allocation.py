from twisted.trial import unittest

import production_config as prod
import staging_config as stag
import preproduction_config as preprod


class SlaveCheck(unittest.TestCase):

    def test_prod_vs_try(self):
        if hasattr(prod, 'TRY_SLAVES'):
            prod_slaves = [x for k, s in prod.SLAVES.iteritems() for x in s]
            try_slaves = [x for k, s in prod.TRY_SLAVES.iteritems() for x in s]
            common_slaves = set(prod_slaves) & set(try_slaves)
            self.assertEqual(
                common_slaves, set([]),
                'Try slaves must not be used in production, however the ' + \
                'following slaves used for both:\n%s' % \
                '\n'.join(common_slaves)
            )

    def test_stag_not_in_prod(self):
        prod_slaves = [x for k, s in prod.SLAVES.iteritems() for x in s]
        stag_slaves = [x for k, s in stag.STAGING_SLAVES.iteritems() for x in s]
        if hasattr(prod, 'TRY_SLAVES'):
            prod_slaves.extend([x for k, s in prod.TRY_SLAVES.iteritems() for x
                                in s])
        common_slaves = set(prod_slaves) & set(stag_slaves)
        self.assertEqual(
            set([]), common_slaves,
            'Staging-only slaves should not be declared as production '
            'and vice versa. However, the following production slaves '
            'declared as staging-only:\n%s' % '\n'.join(sorted(common_slaves))
        )
