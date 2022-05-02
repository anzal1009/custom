import json
import qrcode
import base64
from io import BytesIO

from odoo import api, models, fields, _
import requests

from datetime import datetime
