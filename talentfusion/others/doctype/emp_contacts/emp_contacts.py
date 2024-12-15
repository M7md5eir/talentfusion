# Copyright (c) 2024, Mohamed Kheir and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EmpContacts(Document):
    def validate(self):
        self.check_duplicate_number()

    def check_duplicate_number(self):
        # Check if a record with the same number already exists
        if frappe.db.exists("Emp Contacts", {"number": self.number, "name": ["!=", self.name]}):
            frappe.throw(f"Number {self.number} already exists in the contact list")
