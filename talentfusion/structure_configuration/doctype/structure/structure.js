// Copyright (c) 2024, Mohamed Kheir and contributors
// For license information, please see license.txt

frappe.ui.form.on('Structure', {
    refresh(frm) {
        frm.set_query('parent_structure', function() {
            return {
                filters: {
                    'structure_level_id': ['<', frm.doc.structure_level_id]
                }
            };
        });
    }
});
