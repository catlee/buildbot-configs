# Additional branches that start as identical (individual variables can be overriden here)
PROJECT_BRANCHES = {
    ### PLEASE ADD NEW BRANCHES ALPHABETICALLY (twigs at the bottom, also alphabetically)
    'build-system': {},
    'fx-team': {
        'repo_path': 'integration/fx-team',
        'periodic_start_hours': range(2, 24, 3),
        'enable_perproduct_builds': True,
        'enable_nightly': False,
    },
    'graphics': {},
    # Please sync any customizations made to mozilla-inbound to cypress.
    'mozilla-inbound': {
        'repo_path': 'integration/mozilla-inbound',
        'periodic_start_hours': range(1, 24, 3),
        'enable_perproduct_builds': True,
    },
    'b2g-inbound': {
        'repo_path': 'integration/b2g-inbound',
        'periodic_start_hours': range(2, 24, 3),
        'enable_perproduct_builds': True,
        'platforms': {
            'macosx64_gecko': {
                'enable_checktests': False,
            },
            'win32_gecko': {
                'enable_checktests': False,
            },
        },
    },
    'services-central': {
        'repo_path': 'services/services-central'
    },
    # B2G builds not required on the UX branch
    #'ux': {
    #    'branch_name': 'UX',
    #    'mobile_branch_name': 'UX',
    #    'build_branch': 'UX',
    #    'enable_nightly': True,
    #},
    #####  TWIGS aka RENTABLE BRANCHES
    # Booked for Thunderbird
    #'alder': {},
    'ash': {
        'mozharness_repo_path': 'users/asasaki_mozilla.com/ash-mozharness',
        'mozharness_repo': 'https://hg.mozilla.org/users/asasaki_mozilla.com/ash-mozharness',
        'mozharness_tag': 'default',
    },
    # Not needed on Birch at the moment, bug 977420.
    #'birch': {},
    'cedar': {
        'mozharness_tag': 'default',
    },
    'cypress': {
        'mozharness_tag': 'default',
    },
    # B2G builds not required on date
    # 'date': {},
    'fig': {},
    'gum': {},
    # disabled for bug 985718
    #'holly': {},
    'jamun': {},
    'larch': {},
    'maple': {},
    # Customizations for integration work for bugs 481815 and 307181
    'oak': {
        'enable_nightly': True
    },
    'pine': {}
}

# All is the default
ACTIVE_PROJECT_BRANCHES = PROJECT_BRANCHES.keys()
