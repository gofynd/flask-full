import re

S3_EXTRA_ARGS = {
    "public_read_image": {'ACL': 'public-read', 'ContentType': "image/jpeg"},
}

ISO_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
AVIS_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

URL_REGEX = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    # r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
    # r'localhost|' # localhost...
    # r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
    # r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
    # r'(?::\d+)?' # optional port
    , re.IGNORECASE)

AUTH_STATES = {
    "company": "company_management",
    "brand": "brand_management",
    "product": "product_management",
    "collection": "collection_management",
    "category": "category_management",
    "styletip": "styletip_management",
    "pulltorefresh": "pulltorefresh_management",
    "offer": "offer_management",
    "discount": "discount_management",
    "store": "store_management",
    "size_guide": "size_guide_management",
    "coupon": "coupon_management",
}

AUTH_PERMISSIONS = {
    "view": "view",
    "update": "update",
    "create": "create",
    "create_update": "create_update",
    "update_status": "update_status",
    "update_order": "update_order",
    "publish": "publish",
    "unpublish": "unpublish",
    "quarantine": "quarantine",
    "clone": "clone",
    "update_fynd_a_fit": "update_fynd_a_fit"
}
