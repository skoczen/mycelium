ACCOUNT_STATII = [
    (0, "Free Trial"),
    (10, "Inactive - Unpaid"), # Free trial expired
    (20, "Active"),
    (30, "Active, Billing Issue"), # Was paid, billing failed.
    (40, "On Hold"),  # no way to get to this currently
    (50, "Cancelled"),   
]

CHARGIFY_STATUS_MAPPING = {
    "trialing" : ACCOUNT_STATII[0],
    "assessing" : ACCOUNT_STATII[0],
    "active" : ACCOUNT_STATII[2],
    "soft_failure" : ACCOUNT_STATII[2],
    "past_due" : ACCOUNT_STATII[3],
    "suspended" : ACCOUNT_STATII[3],
    "canceled" : ACCOUNT_STATII[5],
    "unpaid" : ACCOUNT_STATII[3],
    "expired" : ACCOUNT_STATII[3],
}

HAS_A_SUBSCRIPTION_STATII = [
    ACCOUNT_STATII[2][0],
    ACCOUNT_STATII[3][0],
]
HAD_A_SUBSCRIPTION_STATII = HAS_A_SUBSCRIPTION_STATII + [
    ACCOUNT_STATII[4][0],
    ACCOUNT_STATII[5][0],
]

CANCELLED_SUBSCRIPTION_STATII = [
    ACCOUNT_STATII[5][0],
]