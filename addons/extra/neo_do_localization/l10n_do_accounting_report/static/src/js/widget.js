/** @odoo-module **/

import { registry }
from "@web/core/registry";
import { CharField }
from "@web/views/fields/char/char_field"; // o el campo base apropiado
import { useInputField }
from "@web/views/fields/input_field_hook";
import { onWillUpdateProps, onMounted, useRef }
from "@odoo/owl";

export class UrlDgiiReportsOwlWidget extends CharField {
    static template = "l10n_do_accounting_report.UrlDgiiReportsOwlWidget"; // Se necesitará crear esta plantilla

    setup() {
        super.setup();
        this.input = useRef("input"); // Si se necesita referencia al input
        // useInputField({ getValue: () => this.props.record.data[this.props.name] || "" , ref: this.input }); // Si es editable

        // Lógica de init original:
        this.isRnc = this.props.nodeOptions.is_rnc || false;
        this.recordField = this.props.nodeOptions.invoice_field || 'invoice_id';
        this.invoiceId = null;
        this.isModify = this.props.nodeOptions.is_modify || false; // Corregido: this.props en lugar de this.nodeOptions directamente

        this._updateInvoiceId(this.props.record);

        onWillUpdateProps((nextProps) => {
            this._updateInvoiceId(nextProps.record);
        });

        onMounted(() => {
            this._renderLink();
        });
    }

    _updateInvoiceId(record) {
        const recordData = record.data[this.recordField];
        if (recordData && typeof recordData === 'object' && recordData.res_id) { // Adaptado para el formato de Many2one en props
            this.invoiceId = recordData.res_id;
        } else if (recordData && typeof recordData === 'number') { // Si ya es un ID
             this.invoiceId = recordData;
        }
         else {
            this.invoiceId = null;
        }
    }

    get displayUrl() {
        let url = `dgii_reports/`;
        const value = this.props.record.data[this.props.name] || ""; // El valor del campo en sí (la URL base)

        if (this.isRnc && value) { // Asumiendo que 'value' es el RNC aquí
            url += `?rnc=${value}`;
        } else if (this.invoiceId) {
            url += `?invoice_id=${this.invoiceId}`;
            if (this.isModify && value) { // Asumiendo que 'value' es el NCF modificado
                 url += `&modify=${value}`;
            }
        } else {
            return value; // Si no hay condiciones, mostrar el valor original
        }
        return url;
    }

    _renderLink() {
        // La plantilla QWeb se encargará del renderizado del enlace '<a>'
        // Esta función podría usarse si se necesita manipulación del DOM post-renderizado,
        // pero con OWL es preferible hacerlo declarativamente en la plantilla.
        // Por ahora, la lógica principal está en el getter 'displayUrl'.
    }
}

// Registrar el nuevo widget OWL
registry.category("fields").add("dgii_reports_url_owl", UrlDgiiReportsOwlWidget);

// Idealmente, la vista XML que usa 'dgii_reports_url' debería actualizarse a 'dgii_reports_url_owl'.
// Si se quiere mantener compatibilidad o usar el mismo nombre, se podría hacer:
// registry.category("fields").add("dgii_reports_url", UrlDgiiReportsOwlWidget);
// Pero esto podría ser confuso si el widget antiguo aún existe en otras partes.
// Es mejor usar un nuevo nombre y actualizar las vistas.
