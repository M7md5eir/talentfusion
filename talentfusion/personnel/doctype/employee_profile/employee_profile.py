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
            arabic_parts.append(arabic or "")  # leave empty if no translation found

        full_arabic_name = self.join_names(*arabic_parts)

        # Step 3: Remove old translations for this emp_name
        self.delete_old_name_translations(self.emp_name, full_arabic_name)

        # Step 4: Save or update translation of full name, only if changed
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
            "language": lang
        }, "translated_text")

    def delete_old_name_translations(self, source_text, translated_text):
        # حذف الترجمات اللي ليها نفس source_text أو translated_text تحت نفس السياق
        translations = frappe.get_all("Translation", 
            filters={
                "context": "Employee Profile Name",
                "language": "ar",
                "source_text": source_text
            }, 
            fields=["name"]
        )

        # كمان نحذف أي ترجمة تانية بنفس الـ translated_text (لو اتحرك الاسم أو اتغير مثلاً)
        if translated_text:
            translations += frappe.get_all("Translation", 
                filters={
                    "context": "Employee Profile Name",
                    "language": "ar",
                    "translated_text": translated_text
                }, 
                fields=["name"]
            )

        # استخدم set علشان ما يكونش فيه تكرار
        for tr in {tr["name"] for tr in translations}:
            frappe.delete_doc("Translation", tr, ignore_permissions=True)

    def save_full_name_translation(self, source_text, translated_text):
        if not source_text or not translated_text.strip():
            return

        # Create fresh translation
        frappe.get_doc({
            "doctype": "Translation",
            "source_text": source_text,
            "translated_text": translated_text,
            "language": "ar",
            "context": "Employee Profile Name"
        }).insert(ignore_permissions=True)
