# Copyright (c) 2024, Mohamed Kheir and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EmployeeProfile(Document):

    def validate(self):
        # دالة جمع الأسماء
        self.emp_name = self.join_names(
            self.get("1st_emp_name"),
            self.get("2nd_emp_name"),
            self.get("3rd_emp_name"),
            self.get("4th_emp_name")
        )

    def remove_extra_spaces(self, text):
        if not text:
            return ""
        return " ".join(text.strip().split())

    def join_names(self, *args):
        return " ".join([self.remove_extra_spaces(part) for part in args if part]).strip()
