/** @odoo-module **/

import { registry }
from "@web/core/registry";
import { CharField }
from "@web/views/fields/char/char_field";
import { useInputField }
from "@web/views/fields/input_field_hook";
import { useDebounced }
from "@web/core/utils/timing";
import { useService }
from "@web/core/utils/hooks";
import { onWillUpdateProps, onMounted, useRef, useState }
from "@odoo/owl";

export class FieldDgiiAutoCompleteOwl extends CharField {
    static template = "l10n_do_rnc_search.FieldDgiiAutoCompleteOwl"; // Se necesitará crear esta plantilla

    setup() {
        super.setup();
        this.inputRef = useRef("input");
        this.http = useService("http");
        this.orm = useService("orm"); // Para actualizar el campo VAT si es necesario
        this.notification = useService("notification");

        this.state = useState({
            suggestions: [],
            showSuggestions: false,
            activeSuggestionIndex: -1,
        });

        // useInputField({ getValue: () => this.props.record.data[this.props.name] || "", ref: this.inputRef, setValue: (val) => this._onInputChange(val) });
        // Para un campo de autocompletar, el manejo del input es más complejo que el simple useInputField.

        this.debouncedFetchSuggestions = useDebounced(this.fetchSuggestions, 300);

        onMounted(() => {
            // Podríamos añadir event listeners aquí si es necesario, por ejemplo para clics fuera del input.
        });
    }

    async fetchSuggestions(inputValue) {
        if (inputValue.length < 3) {
            this.state.suggestions = [];
            this.state.showSuggestions = false;
            return;
        }
        try {
            const suggestions = await this.http.get(`/dgii_ws/?term=${encodeURIComponent(inputValue)}`);
            if (suggestions && suggestions.length) {
                this.state.suggestions = suggestions.map(s => ({ label: s.name, value: s.rnc, name: s.name, rnc: s.rnc })); // Adaptar según la estructura de la respuesta de /dgii_ws/
                this.state.showSuggestions = true;
                this.state.activeSuggestionIndex = -1;
            } else {
                this.state.suggestions = [];
                this.state.showSuggestions = false;
            }
        } catch (error) {
            console.error("Error fetching DGII suggestions:", error);
            this.notification.add("Error al obtener sugerencias de la DGII.", { type: "danger" });
            this.state.suggestions = [];
            this.state.showSuggestions = false;
        }
    }

    onInput(ev) {
        const inputValue = ev.target.value;
        this.props.record.update({
            [this.props.name]: inputValue
        }); // Actualizar el valor del campo actual (nombre)
        this.debouncedFetchSuggestions(inputValue);
    }

    onFocus() {
        if (this.state.suggestions.length > 0) {
            this.state.showSuggestions = true;
        }
    }

    onBlur() {
        // Retrasar el ocultar para permitir el clic en la sugerencia
        setTimeout(() => {
            this.state.showSuggestions = false;
            this.state.activeSuggestionIndex = -1;
        }, 200);
    }

    onSuggestionClick(suggestion) {
        this.props.record.update({
            [this.props.name]: suggestion.name, // Actualizar el campo actual (nombre)
        });
        // Actualizar el campo VAT (res.partner)
        // Esto asume que el modelo del record actual es res.partner o tiene un campo vat actualizable
        // y que el nombre del campo VAT es 'vat'.
        if ('vat' in this.props.record.fields) {
             this.props.record.update({ 'vat': suggestion.rnc });
        } else {
            // Si el campo 'vat' no está directamente en este modelo, se necesitaría una forma
            // más compleja de actualizarlo, posiblemente a través de un onchange_ en Python
            // o una llamada ORM si el contexto lo permite.
            // Para un widget de campo, idealmente solo modifica su propio valor.
            // La actualización de otros campos es mejor manejarla con onchanges en el modelo.
             _logger.warn("El campo 'vat' no está disponible directamente en el record para actualizar.");
        }

        this.state.suggestions = [];
        this.state.showSuggestions = false;
    }

    onKeydown(ev) {
        switch (ev.key) {
            case "Enter":
                if (this.state.activeSuggestionIndex >= 0 && this.state.suggestions[this.state.activeSuggestionIndex]) {
                    ev.preventDefault();
                    this.onSuggestionClick(this.state.suggestions[this.state.activeSuggestionIndex]);
                } else {
                     this.state.showSuggestions = false; // Ocultar si se presiona Enter sin seleccionar
                }
                break;
            case "ArrowUp":
                ev.preventDefault();
                if (this.state.suggestions.length > 0) {
                    this.state.activeSuggestionIndex = Math.max(0, this.state.activeSuggestionIndex - 1);
                }
                break;
            case "ArrowDown":
                ev.preventDefault();
                if (this.state.suggestions.length > 0) {
                    this.state.activeSuggestionIndex = Math.min(this.state.suggestions.length - 1, this.state.activeSuggestionIndex + 1);
                }
                break;
            case "Escape":
                this.state.showSuggestions = false;
                this.state.activeSuggestionIndex = -1;
                break;
        }
    }
}

registry.category("fields").add("dgii_autocomplete_owl", FieldDgiiAutoCompleteOwl);
// Considerar renombrar el archivo JS a dgii_autocomplete_widget.js o similar.
// Actualizar vistas XML para usar widget="dgii_autocomplete_owl".
// Crear la plantilla QWeb l10n_do_rnc_search.FieldDgiiAutoCompleteOwl
// Ejemplo de plantilla QWeb (muy básica):
// <templates>
//   <t t-name="l10n_do_rnc_search.FieldDgiiAutoCompleteOwl" owl="1">
//     <div class="o_field_dgii_autocomplete">
//       <input type="text" class="o_input" t-ref="input"
//              t-att-id="props.id"
//              t-att-value="props.record.data[props.name] || ''"
//              t-on-input="onInput"
//              t-on-focus="onFocus"
//              t-on-blur="onBlur"
//              t-on-keydown="onKeydown"
//              autocomplete="off"
//       />
//       <ul t-if="state.showSuggestions &amp;&amp; state.suggestions.length" class="dropdown-menu show" style="display: block;">
//         <t t-foreach="state.suggestions" t-as="suggestion" t-key="suggestion.rnc">
//           <li t-att-class="{ active: state.activeSuggestionIndex === suggestion_index }"
//               t-on-mousedown.prevent="() => this.onSuggestionClick(suggestion)">
//             <a href="#" class="dropdown-item"><t t-esc="suggestion.label"/> (<t t-esc="suggestion.rnc"/>)</a>
//           </li>
//         </t>
//       </ul>
//     </div>
//   </t>
// </templates>
// Este QWeb es un ejemplo y necesitaría estilos CSS.
