# Copyright (c) 2024, Mohamed Kheir and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate

#####################################################################################################################
class Structure(Document):
    def before_save(self):
        # set enabled_date to today's date if it is empty
        if not self.enabled_date:
            self.enabled_date = getdate()

        # validate that disabled_date is after enabled_date or blank
        if self.disabled_date and getdate(self.disabled_date) <= getdate(self.enabled_date):
            frappe.throw("Disabled Date must be after Enabled Date or left blank")

        self.update_status_manually()

    def update_status_manually(self):
        today = getdate()
        enabled_date = getdate(self.enabled_date) if self.enabled_date else None
        disabled_date = getdate(self.disabled_date) if self.disabled_date else None

        # determine new status
        new_status = 1 if not disabled_date or (enabled_date <= today <= disabled_date) else 0

        # set the active field value only if it has changed
        if self.active != new_status:self.active = new_status

#####################################################################################################################
def update_status_daily():
    today = getdate()
    doctype_name = "Structure"

    # fetch all records
    current_data = frappe.db.get_list(doctype_name, fields=["name", "enabled_date", "disabled_date", "active"])

    # loop through each record
    for record in current_data:
        enabled_date = record.get("enabled_date")
        disabled_date = record.get("disabled_date")
        current_status = record.get("active", 0)

        # determine new status
        new_status = 1 if not disabled_date or (enabled_date <= today <= disabled_date) else 0

        # update the record if status has changed
        if current_status != new_status:
            frappe.db.set_value(doctype_name, record.get("name"), "active", new_status, update_modified=False)

    frappe.db.commit()
