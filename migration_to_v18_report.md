# Informe de Migración de Odoo 17 a Odoo 18

Este documento detalla los cambios necesarios y realizados para migrar los módulos personalizados de Odoo 17 a Odoo 18.

## Resumen General de Cambios Clave para Odoo 18:

*   **Frontend de Point of Sale (PoS):** Rediseño completo que requiere una migración y adaptación significativa de personalizaciones JS y QWeb a OWL v2, conforme a la nueva arquitectura de PoS v18.
*   **Contabilidad:** Cambios en el manejo de pagos (posiblemente sin asientos por defecto), almacenamiento de tasas de cambio en facturas, nuevo widget de producto en líneas de factura, configuración global de impuestos incluidos/excluidos, y refactorización de presupuestos.
*   **Framework y UI General:** URLs legibles, Passkeys, evolución de Python/OWL.
*   **Localización Dominicana:** Validación contra módulos base de Odoo 18.

---
## Progreso de Aplicación de Ajustes (Paso 16) para Odoo 18 (Parcialmente Completado):

Se han aplicado las siguientes actualizaciones de manifiestos. Los cambios de código Python se centraron en los archivos problemáticos de fases anteriores (con éxito limitado por herramientas) y en la planificación de la refactorización para la taxonomía de impuestos y la migración de JS.

*   **Actualizaciones de `__manifest__.py` (Versión a `18.0.1.0.0`):**
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
    *   **Archivos con cambios pendientes (debido a fallos persistentes de herramientas, no reintentados o fallaron de nuevo en esta fase):**
        *   `exo_api/models/account_line_load/account_line_load.py`: Actualización de `super().unlink()` pendiente.
        *   `exo_api/models/inherit/account_move_inherit.py`: Actualización de `super().unlink()` pendiente.
        *   `l10n_do_accounting_report/models/dgii_report.py`: Actualizaciones de `super().create()` y `super().write()` pendientes.
    *   **Renombrar `exo_api/controllers/decorators .py`**: Pendiente.
    *   **Validación de Taxonomía de Impuestos y Lógica Contable v18:**
        *   La búsqueda de impuesto por `tax_code = '2OR'` en `exo_api` y la identificación de impuestos en `l10n_do_accounting_report` necesitan validación funcional y posible refactorización contra la estructura final de impuestos de Odoo 18 y `l10n_do`.
        *   Lógica de creación de pagos en `invoice_api` y `exo_api` necesita validarse contra el nuevo comportamiento de "Pagos sin asientos contables".
        *   Cálculos de moneda en `exo_api` deben revisarse por la "Tasa de cambio almacenada en facturas".

*   **JavaScript a OWL:**
    *   `l10n_do_accounting_report/static/src/js/widget.js`: Sobrescrito con un esqueleto de componente OWL. Requiere crear plantilla QWeb, estilos CSS y pruebas exhaustivas.
    *   `l10n_do_rnc_search/static/src/js/l10n_do_accounting.js`: Sobrescrito con un esqueleto de componente OWL. Requiere crear plantilla QWeb, CSS, pruebas y posible renombrado de archivo JS.
    *   **`l10n_do_pos/static/src/js/*` y `static/src/xml/*` (CRÍTICO):** Marcados para reescritura completa manual y adaptación a la nueva arquitectura y rediseño del PoS de Odoo 18. Esta es la tarea de desarrollo más grande y compleja de la migración.

**Próximos Pasos para Completar la Migración a v18:**
*   **Resolución Manual de Problemas de Herramientas:** Aplicar manualmente los cambios de `super()` y el renombrado de archivo donde las herramientas fallaron.
*   **Implementación Completa de Migración JS a OWL:**
    *   Desarrollar las plantillas QWeb y CSS para los widgets OWL de `l10n_do_accounting_report` y `l10n_do_rnc_search`.
    *   Realizar la reescritura completa de todos los componentes y plantillas de `l10n_do_pos`.
*   **Validación Funcional y Refactorización Adicional:**
    *   Probar exhaustivamente la lógica de impuestos, contabilidad, NCF, y flujos de PoS en un entorno Odoo 18.
    *   Refactorizar el código Python según sea necesario basándose en las APIs y comportamientos finales de Odoo 18 y sus módulos base.
*   **Revisión de Vistas XML y Datos:** Adaptar todos los archivos XML (vistas, datos, seguridad, reportes) a Odoo 18.

---
Este informe resume el estado de la migración a Odoo 18. La finalización requerirá un esfuerzo de desarrollo manual significativo, especialmente para el frontend del PoS y la resolución de los problemas con las herramientas de modificación de código.
