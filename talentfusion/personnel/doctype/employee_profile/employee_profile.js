// Copyright (c) 2024, Mohamed Kheir and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Addresses', {
  country: function(frm, cdt, cdn) {
    frappe.model.set_value(cdt, cdn, 'province', null);
    frm.fields_dict['addresses_table'].grid.get_field('province').get_query = function(doc, cdt2, cdn2) {
      let child = locals[cdt2][cdn2];
      return {
        filters: {
          country: child.country || ''
        }
      };
    };
  }
});

frappe.ui.form.on('Employee Profile', {
  refresh: function(frm) {
    frm.fields_dict['addresses_table'].grid.get_field('province').get_query = function(doc, cdt, cdn) {
      let child = locals[cdt][cdn];
      return {
        filters: {
          country: child.country || ''
        }
      };
    };
  }
});

frappe.ui.form.on('Employee Profile', {
  refresh: function(frm) {
    setTimeout(() => {
      frm.fields_dict.emp_img.$wrapper.find('a').off('mouseenter mouseleave click');
      frm.fields_dict.emp_img.$wrapper.find('a').removeAttr('data-lightbox');
    }, 500);
  }
});
