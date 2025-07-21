import frappe
from frappe.model.document import Document

class EmployeeProfile(Document):

    def validate(self):
        if self.is_new() or any(self.has_changed(f"{i}st_emp_name") for i in range(1, 5)):
            self._update_emp_name_and_translation()

    def _update_emp_name_and_translation(self):
        parts = [self.get(f"{i}st_emp_name") for i in range(1, 5)]
        self.emp_name = self._join(parts)
        arabic_parts = [self._get_translation(p) for p in parts]
        full_arabic = self._join(arabic_parts)
        self._save_translation(self.emp_name, full_arabic)

    def _join(self, parts):
        return " ".join(p.strip() for p in parts if p).strip()

    def _get_translation(self, source):
        if not source:
            return ""
        return frappe.db.get_value("Translation", {
            "source_text": source,
            "language": "ar"
        }, "translated_text") or ""

    def _save_translation(self, source, translated):
        if not source:
            return

        existing = frappe.db.get_value("Translation", {
            "source_text": source,
            "language": "ar",
            "context": "Employee Profile Name"
        }, ["name", "translated_text"], as_dict=True)

        if existing:
            if existing.translated_text != translated:
                doc = frappe.get_doc("Translation", existing.name)
                doc.translated_text = translated
                doc.save(ignore_permissions=True)
        elif translated.strip():
            frappe.get_doc({
                "doctype": "Translation",
                "source_text": source,
                "translated_text": translated,
                "language": "ar",
                "context": "Employee Profile Name"
            }).insert(ignore_permissions=True)
