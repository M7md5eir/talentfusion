import frappe
from frappe.model.document import Document

class EmployeeProfile(Document):

    def validate(self):
        before = self.get_doc_before_save()

        # Check if it's new or name parts changed
        if self.is_new() or self._name_parts_changed(before):
            self._update_emp_name_and_translation()

    def _name_parts_changed(self, before):
        if not before:
            return True
        for i in range(1, 5):
            field = f"{i}st_emp_name"
            if self.get(field) != before.get(field):
                return True
        return False

    def _update_emp_name_and_translation(self):
        # Join name parts (English full name)
        parts = [self.get(f"{i}st_emp_name", "") for i in range(1, 5)]
        self.emp_name = " ".join(p.strip() for p in parts if p).strip()

        # Get Arabic translations if exist
        arabic_parts = [self._get_translation(p) for p in parts]
        arabic_full = " ".join(p.strip() for p in arabic_parts if p).strip()

        # Only update if translation changed
        self._update_translation_if_needed(
            source=self.emp_name,
            translated=arabic_full
        )

    def _get_translation(self, source_text):
        if not source_text:
            return ""
        return frappe.db.get_value("Translation", {
            "source_text": source_text,
            "language": "ar"
        }, "translated_text") or ""

    def _update_translation_if_needed(self, source, translated):
        if not source:
            return

        # Check if translation exists
        existing = frappe.db.get_value("Translation", {
            "source_text": source,
            "language": "ar"
        }, ["name", "translated_text"], as_dict=True)

        if existing:
            # Update only if value changed
            if existing.translated_text != translated:
                doc = frappe.get_doc("Translation", existing.name)
                doc.translated_text = translated
                doc.save(ignore_permissions=True)
        elif translated:  # Only insert if translated text is not empty
            frappe.get_doc({
                "doctype": "Translation",
                "source_text": source,
                "translated_text": translated,
                "language": "ar"
            }).insert(ignore_permissions=True)
