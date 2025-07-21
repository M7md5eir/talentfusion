import frappe
from frappe.model.document import Document

class EmployeeProfile(Document):

    def validate(self):
        # Step 1: Compose the English name
        name_parts = [
            self.get("1st_emp_name"),
            self.get("2nd_emp_name"),
            self.get("3rd_emp_name"),
            self.get("4th_emp_name")
        ]

        self.emp_name = self.join_names(*name_parts)

        # Step 2: Try to find Arabic translations for each part
        arabic_parts = []
        for part in name_parts:
            arabic = self.get_translation(part, lang="ar")
            arabic_parts.append(arabic or part)  # fallback to original if no translation

        full_arabic_name = self.join_names(*arabic_parts)

        # Step 3: Create or update a Translation record for the full name
        self.save_full_name_translation(self.emp_name, full_arabic_name)

    def remove_extra_spaces(self, text):
        if not text:
            return ""
        return " ".join(text.strip().split())

    def join_names(self, *args):
        return " ".join([self.remove_extra_spaces(part) for part in args if part]).strip()

    def get_translation(self, source_text, lang="ar"):
        if not source_text:
            return ""
        return frappe.db.get_value("Translation", {
            "source_text": source_text,
            "language": lang  # <-- fixed field name here
        }, "translated_text")

    def save_full_name_translation(self, source_text, translated_text):
        if not source_text or not translated_text:
            return

        existing = frappe.db.get_value("Translation", {
            "source_text": source_text,
            "language": "ar",  # <-- fixed field name here
            "context": "Employee Profile Name"
        }, "name")

        if existing:
            # Update existing translation if changed
            tr_doc = frappe.get_doc("Translation", existing)
            if tr_doc.translated_text != translated_text:
                tr_doc.translated_text = translated_text
                tr_doc.save(ignore_permissions=True)
        else:
            # Create new translation
            frappe.get_doc({
                "doctype": "Translation",
                "source_text": source_text,
                "translated_text": translated_text,
                "language": "ar",  # <-- fixed field name here
                "context": "Employee Profile Name"
            }).insert(ignore_permissions=True)
