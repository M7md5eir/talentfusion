import frappe
from frappe.model.document import Document

class EmployeeProfile(Document):

    def validate(self):
        # Step 1: Compose the English full name
        name_parts = [
            self.get("1st_emp_name"),
            self.get("2nd_emp_name"),
            self.get("3rd_emp_name"),
            self.get("4th_emp_name")
        ]
        self.emp_name = self.join_names(*name_parts)

        # Step 2: Compose the Arabic full name from available translations (leave blank if missing)
        arabic_parts = []
        for part in name_parts:
            arabic = self.get_translation(part, lang="ar")
            arabic_parts.append(arabic or "")

        full_arabic_name = self.join_names(*arabic_parts)

        # Step 3: Save or update translation of full name, only if changed
        self.upsert_name_translation(self.emp_name, full_arabic_name)

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
            "language": lang
        }, "translated_text")

    def upsert_name_translation(self, source_text, translated_text):
        """Update or insert translation for full name if changed"""
        if not source_text:
            return

        existing = frappe.db.get_value("Translation", {
            "source_text": source_text,
            "language": "ar",
            "context": "Employee Profile Name"
        }, ["name", "translated_text"], as_dict=True)

        if existing:
            if existing.translated_text != translated_text:
                # Only update if value changed
                tr_doc = frappe.get_doc("Translation", existing.name)
                tr_doc.translated_text = translated_text
                tr_doc.save(ignore_permissions=True)
        else:
            # Only insert if there is a translation to save
            if translated_text.strip():
                frappe.get_doc({
                    "doctype": "Translation",
                    "source_text": source_text,
                    "translated_text": translated_text,
                    "language": "ar",
                    "context": "Employee Profile Name"
                }).insert(ignore_permissions=True)
