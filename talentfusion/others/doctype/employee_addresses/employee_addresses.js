// Copyright (c) 2025, Mohamed Kheir and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Addresses', {
  setup: function(frm) {
    frm.set_query('province', function() {
      return {
        filters: {
          country: frm.doc.country || ''
        }
      };
    });
  },

  country: function(frm) {
    frm.set_value('province', null);
  }
});
