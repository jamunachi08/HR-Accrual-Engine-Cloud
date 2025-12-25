frappe.ui.form.on('Accrual Run', {
    refresh(frm) {
        if (frm.doc.docstatus === 0) {
            frm.add_custom_button(__('Process Accruals'), async () => {
                if (!frm.doc.company || !frm.doc.posting_date) {
                    frappe.msgprint(__('Please set Company and Posting Date.'));
                    return;
                }
                frm.disable_save();
                try {
                    await frappe.call({
                        method: 'hr_accrual_engine.accrual_engine.services.processor.run_accrual',
                        args: { company: frm.doc.company, posting_date: frm.doc.posting_date }
                    });
                    frappe.msgprint(__('Accruals processed. Refreshing...'));
                    frm.reload_doc();
                } finally {
                    frm.enable_save();
                }
            });
        }
    }
});
