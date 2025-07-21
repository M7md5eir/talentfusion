# Copyright (c) 2024, Mohamed Kheir and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class EmployeeAddresses(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		active: DF.Check
		apartment: DF.Data | None
		building: DF.Data | None
		city: DF.Link | None
		country: DF.Link | None
		end_date: DF.Date | None
		floor: DF.Data | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		postal_code: DF.Data | None
		province: DF.Link | None
		start_date: DF.Date | None
		street: DF.Data | None
	# end: auto-generated types
	pass
