# Informe de Migración de Odoo 16 a Odoo 17

Este documento detalla los cambios necesarios y realizados para migrar los módulos personalizados de Odoo 16 a Odoo 17.

## Resumen General de Cambios Clave para Odoo 17:

*   **Taxonomía de Impuestos:** Priorizar el uso de `xml_id`, códigos de impuesto o `tax_group_id` sobre nombres literales.
*   **Módulos de Contabilidad y Localización:** Validar contra cambios en `account`, `l10n_latam_invoice_document`, `l10n_do` de Odoo 17.
*   **JavaScript (PoS y Web):** Continuar y completar la migración a OWL v2.
*   **API de Python:** Verificar eliminación de métodos obsoletos y cambios en signaturas.
*   **Vistas XML y Reportes QWeb:** Validar XPaths y compatibilidad.
*   **Archivos de Manifiesto (`__manifest__.py`):** Actualizar `version` a `17.0.x.y.z`.
*   **Archivos Problemáticos (Fase v16):** Reintentar correcciones.

---
## Progreso de Aplicación de Ajustes (Paso 11) para Odoo 17 (Mayormente Completado):

Se han aplicado las siguientes actualizaciones de manifiestos. Los cambios de código Python se centraron en los archivos problemáticos de la fase anterior y en la refactorización inicial de la taxonomía de impuestos. La mayoría de los archivos problemáticos persistieron.

*   **Actualizaciones de `__manifest__.py` (Versión a `17.0.1.0.0`):**
    *   `invoice_api`: Aplicado.
    *   `auth_api_key`: Aplicado.
    *   `report_xlsx`: Aplicado.
    *   `web_digital_sign`: Aplicado.
    *   `exo_api`: Aplicado.
    *   `l10n_do_accounting`: Aplicado.
    *   `l10n_do_accounting_report`: Aplicado.
    *   `l10n_do_pos`: Aplicado.
    *   `l10n_do_rnc_search`: Aplicado.
    *   `l10n_do_e_accounting`: Aplicado.

*   **Cambios en Código Python:**
    *   **`l10n_do_accounting_report/models/account_move.py`**:
        *   Refactorizado `_compute_invoiced_itbis` para usar `tax_group_id.name == 'ITBIS%'` (con fallback y log).
        *   Mejorados decoradores `@api.depends` y lógica interna en algunos métodos computados (aplicado mediante `overwrite_file_with_block`).
    *   **Archivos con cambios pendientes (debido a fallos persistentes de herramientas):**
        *   `exo_api/models/account_line_load/account_line_load.py`: Actualización de `super().unlink()` pendiente.
        *   `exo_api/models/inherit/account_move_inherit.py`: Actualización de `super().unlink()` pendiente.
        *   `l10n_do_accounting_report/models/dgii_report.py`: Actualizaciones de `super().create()` y `super().write()` pendientes.
        *   `exo_api/controllers/decorators .py`: Renombrar a `decorators.py` pendiente.
    *   **Validación de Taxonomía de Impuestos:**
        *   La búsqueda de impuesto por `tax_code = '2OR'` en `exo_api/models/inherit/res_partner_inherit.py` necesita validación en un entorno Odoo 17.

*   **JavaScript a OWL:**
    *   La migración de los siguientes archivos JS antiguos a OWL sigue siendo una tarea principal y no se ha implementado código aún:
        *   `l10n_do_accounting_report/static/src/js/widget.js`
        *   Todos los JS en `l10n_do_pos/static/src/js/` (y sus plantillas QWeb asociadas).
        *   `l10n_do_rnc_search/static/src/js/l10n_do_accounting.js`

**Próximos Pasos para la Fase v17 (si se retoma o antes de v18):**
*   Resolver manualmente los problemas con los archivos Python que no pudieron ser modificados por las herramientas.
*   Realizar una revisión exhaustiva de la lógica de impuestos en todos los módulos para asegurar la compatibilidad con la nueva taxonomía de Odoo 17.
*   Proceder con la implementación de la migración de JavaScript a OWL.
*   Validar todos los archivos de datos y vistas XML.

---
Este informe guiará la continuación de la migración.
