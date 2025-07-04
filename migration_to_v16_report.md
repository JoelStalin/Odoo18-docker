# Informe de Migración de Odoo 15 a Odoo 16

Este documento detalla los cambios necesarios y realizados para migrar los módulos personalizados de Odoo 15 a Odoo 16.

## Resumen General de Cambios Comunes Esperados para Odoo 16:
*   **API de Python:**
    *   Reemplazo de llamadas antiguas a `super(Clase, self).method()` por `super().method()`.
    *   Revisión de la firma y comportamiento de métodos ORM si es necesario.
    *   Asegurar el uso de `self` como recordset en métodos de modelo.
    *   Verificación de dependencias a módulos/modelos/campos renombrados o eliminados en Odoo 16.
*   **Vistas XML:**
    *   Validación de `xpath` en vistas heredadas.
    *   Ajustes en `attrs`, `options`, `modifiers` si es necesario.
    *   Compatibilidad de `domain`.
*   **JavaScript:**
    *   Migración de widgets JS antiguos (basados en `web.basic_fields` o `Widget`) al framework OWL v2. Esto incluye la reescritura de componentes y plantillas QWeb asociadas.
*   **Archivos de Manifiesto (`__manifest__.py`):**
    *   Actualización de la clave `version` a `16.0.x.y.z`.
    *   Revisión y adición de dependencias (ej. `base`, `zeep`, `pycountry`).
    *   Asegurar que las `external_dependencies` estén correctamente listadas.
*   **Otros:**
    *   Revisión de `post_init_hook` para compatibilidad.
    *   Verificación de archivos de datos y seguridad.

---
## Cambios por Módulo:

### Módulo: `invoice_api`

| Archivo Modificado                  | Elemento Obsoleto/Cambiado                                  | Implementación Nueva/Corregida                               | Razón del Cambio                                                                 |
|-------------------------------------|-------------------------------------------------------------|--------------------------------------------------------------|----------------------------------------------------------------------------------|
| `__manifest__.py`                   | `version: "1.0.0"`                                          | `version: "16.0.1.0.0"`                                      | Actualización de versión para compatibilidad con Odoo 16.                        |
| `controllers/test_full.py`        | Uso de `request.env(user=SUPERUSER_ID, db=request.db)`      | Mantenido por ahora, revisar si causa problemas. Idiomático: `request.env['model'].sudo().method()`. | Asegurar compatibilidad y seguir patrones recomendados si es necesario.         |

---
### Módulo: `auth_api_key`

| Archivo Modificado                  | Elemento Obsoleto/Cambiado                                  | Implementación Nueva/Corregida                               | Razón del Cambio                                                                 |
|-------------------------------------|-------------------------------------------------------------|--------------------------------------------------------------|----------------------------------------------------------------------------------|
| `__manifest__.py`                   | `version: "18.0.1.0.0"` (asumido base v15)                 | `version: "16.0.1.0.0"`                                      | Actualización de versión para compatibilidad con Odoo 16.                        |
| `__manifest__.py`                   | Ausencia de clave `depends`.                                | Añadido `'depends': ['base', 'exo_api']`                     | Declarar dependencias explícitas. `exo_api` es necesaria.                      |
| `models/auth_api_key.py`            | `super(AuthApiKey, self).create(vals)`                      | `super().create(vals)`                                       | Actualización a la sintaxis moderna de `super()`.                                  |
| `models/auth_api_key.py`            | `super(AuthApiKey, self).write(vals)`                       | `super().write(vals)`                                        | Actualización a la sintaxis moderna de `super()`.                                  |
| `models/ir_http.py`                 | `super(IrHttp, cls)._auth_method_user()`                    | `super()._auth_method_user()`                                | Actualización a la sintaxis moderna de `super()`. (Aplicado mediante `overwrite_file_with_block`) |
| `models/ir_http.py`                 | Asignación directa `request.uid = 1`.                       | Mantenido por ahora (con comentario en código), marcar como deuda técnica. | Podría causar problemas de seguridad/contexto. Idealmente refactorizar a `sudo()` granular. |
| `models/ir_http.py`                 | Uso de `os.getenv('USER_PASSWORD')` para `session.authenticate`. | Mantenido por ahora (con comentario en código), marcar como deuda técnica. | Práctica de seguridad cuestionable.                                              |

---
### Módulo: `report_xlsx`

| Archivo Modificado                  | Elemento Obsoleto/Cambiado                                  | Implementación Nueva/Corregida                               | Razón del Cambio                                                                 |
|-------------------------------------|-------------------------------------------------------------|--------------------------------------------------------------|----------------------------------------------------------------------------------|
| `__manifest__.py`                   | `version: "18.0.1.0.0"` (asumido base v15)                 | `version: "16.0.1.0.0"`                                      | Actualización de versión para compatibilidad con Odoo 16.                        |
| `models/ir_report.py`               | `super(ReportAction, self)._get_report_from_name(...)`      | `super()._get_report_from_name(...)`                         | Actualización a la sintaxis moderna de `super()`.                                  |
| `controllers/main.py`               | `super(ReportController, self).report_routes(...)`          | `super().report_routes(...)`                                 | Actualización a la sintaxis moderna de `super()`.                                  |
| `controllers/main.py`               | `super(ReportController, self).report_download(...)`        | `super().report_download(...)`                               | Actualización a la sintaxis moderna de `super()`.                                  |

---
### Módulo: `web_digital_sign`

| Archivo Modificado                  | Elemento Obsoleto/Cambiado                                  | Implementación Nueva/Corregida                               | Razón del Cambio                                                                 |
|-------------------------------------|-------------------------------------------------------------|--------------------------------------------------------------|----------------------------------------------------------------------------------|
| `__manifest__.py`                   | `version: "18.0.1.0.0"` (asumido base v15)                 | `version: "16.0.1.0.0"`                                      | Actualización de versión para compatibilidad con Odoo 16.                        |

---
### Módulo: `exo_api`

| Archivo Modificado                  | Elemento Obsoleto/Cambiado                                  | Implementación Nueva/Corregida                               | Razón del Cambio                                                                 |
|-------------------------------------|-------------------------------------------------------------|--------------------------------------------------------------|----------------------------------------------------------------------------------|
| `__manifest__.py`                   | `version: "18.0.1.0.0"` (asumido base v15)                 | `version: "16.0.1.0.0"`                                      | Actualización de versión para compatibilidad con Odoo 16.                        |
| `models/inherit/res_partner_inherit.py` | `super(partner_inherit, self).create(vals)` y `super(partner_inherit, self).write(vals)` | `super().create(vals)` y `super().write(vals)`             | Actualización a la sintaxis moderna de `super()`. (Aplicado mediante `overwrite_file_with_block`) |
| `controllers/account_controller.py` | `super(CustomPortal, self).portal_my_invoices(...)`       | `super().portal_my_invoices(...)`                            | Actualización a la sintaxis moderna de `super()`.                                  |
| `controllers/response.py`           | Uso incorrecto de `http.Response.status = status`.          | Pasar `status` como argumento al constructor de `Response`.  | Forma correcta de establecer el código de estado HTTP. (Aplicado mediante `overwrite_file_with_block`) |
| **Archivo Pendiente/Problemático** `models/account_line_load/account_line_load.py` | `super(account_line_load, self).unlink()`                 | Requiere `super().unlink()`.                                   | Fallaron `replace_with_git_merge_diff` y `overwrite_file_with_block`.            |
| **Archivo Pendiente/Problemático** `models/inherit/account_move_inherit.py`| `super(AccountMoveInherit, self).unlink()`                | Requiere `super().unlink()`.                                   | Fallaron `replace_with_git_merge_diff` y `overwrite_file_with_block`.            |
| **Archivo Pendiente/Problemático** `controllers/decorators .py`        | Nombre de archivo con espacio.                              | Renombrar a `decorators.py`.                                 | Falló `rename_file`.                                                             |

---
### Módulo: `l10n_do_accounting`

| Archivo Modificado                  | Elemento Obsoleto/Cambiado                                  | Implementación Nueva/Corregida                               | Razón del Cambio                                                                 |
|-------------------------------------|-------------------------------------------------------------|--------------------------------------------------------------|----------------------------------------------------------------------------------|
| `__manifest__.py`                   | `version: "18.0.1.0.0"` (asumido base v15)                 | `version: "16.0.1.0.0"`                                      | Actualización de versión para compatibilidad con Odoo 16.                        |
| `__manifest__.py`                   | Ausencia de `zeep` en `external_dependencies`.              | Añadido `'external_dependencies': {'python': ['zeep']}`.      | `zeep` es usado para la validación de RNC/Cédula.                               |
| `models/account_move.py`            | Múltiples llamadas a `super(AccountMove, self).method()`    | Actualizadas a `super().method()` o equivalente.             | Actualización a la sintaxis moderna de `super()`. (Aplicado mediante `overwrite_file_with_block`) |
| `wizard/account_move_reversal.py`   | Múltiples llamadas a `super(AccountMoveReversal, self).method()` | Actualizadas a `super().method()` o equivalente.             | Actualización a la sintaxis moderna de `super()`. (Aplicado mediante `overwrite_file_with_block`) |

---
### Módulo: `l10n_do_accounting_report`

| Archivo Modificado                  | Elemento Obsoleto/Cambiado                                  | Implementación Nueva/Corregida                               | Razón del Cambio                                                                 |
|-------------------------------------|-------------------------------------------------------------|--------------------------------------------------------------|----------------------------------------------------------------------------------|
| `__manifest__.py`                   | `version: "18.0.1.0.0"` (asumido base v15)                 | `version: "16.0.1.0.0"`, dependencia `pycountry` asegurada.  | Actualización de versión y dependencias.                                         |
| `models/account_move.py`            | Cálculo de `invoiced_itbis` basado en `amount == 18`.       | Refactorizado para usar `tax_group_id` (nombre 'ITBIS%').    | Mayor robustez ante cambios en tasas de impuestos.                               |
| **Archivo Pendiente/Problemático** `models/dgii_report.py`             | `super(DgiiReport, self).create(vals)` y `super(DgiiReport, self).write(vals)` | Requieren `super().create(vals)` y `super().write(vals)`. | Falló `overwrite_file_with_block`.                                               |
| `static/src/js/widget.js`           | Widget JS basado en `web.basic_fields.UrlWidget`.           | **Marcado para migración a OWL.**                            | Framework JS antiguo obsoleto.                                                   |

---
### Módulo: `l10n_do_pos`

| Archivo Modificado                  | Elemento Obsoleto/Cambiado                                  | Implementación Nueva/Corregida                               | Razón del Cambio                                                                 |
|-------------------------------------|-------------------------------------------------------------|--------------------------------------------------------------|----------------------------------------------------------------------------------|
| `__manifest__.py`                   | `version: "18.0.1.0.0"` (asumido base v15)                 | `version: "16.0.1.0.0"`                                      | Actualización de versión para compatibilidad con Odoo 16.                        |
| `models/pos_config.py`              | `super(PosConfig, self)._check_company_journal()`           | `super()._check_company_journal()`                           | Actualización a la sintaxis moderna de `super()`.                                  |
| `models/pos_order.py`               | Múltiples llamadas a `super(PosOrder, self).method()`       | Actualizadas a `super().method()`.                       | Actualización a la sintaxis moderna de `super()`. (Aplicado mediante `overwrite_file_with_block`) |
| `static/src/js/*.js` (varios)       | Código JavaScript del framework antiguo de PoS.             | **Marcado para migración completa a OWL v2.**                | Framework JS antiguo obsoleto.                                                   |
| `static/src/xml/**/*.xml`           | Plantillas QWeb para JS antiguo.                            | **Marcado para reescritura/adaptación a OWL.**               | Plantillas deben ser compatibles con componentes OWL.                            |

---
### Módulo: `l10n_do_rnc_search`

| Archivo Modificado                  | Elemento Obsoleto/Cambiado                                  | Implementación Nueva/Corregida                               | Razón del Cambio                                                                 |
|-------------------------------------|-------------------------------------------------------------|--------------------------------------------------------------|----------------------------------------------------------------------------------|
| `__manifest__.py`                   | `version: "18.0.1.0.0"` (asumido base v15)                 | `version: "16.0.1.0.0"`                                      | Actualización de versión para compatibilidad con Odoo 16.                        |
| `static/src/js/l10n_do_accounting.js` | Widget JS `FieldDgiiAutoComplete`.                          | **Marcado para migración a OWL.**                            | Framework JS antiguo obsoleto.                                                   |

---
### Módulo: `l10n_do_e_accounting`

| Archivo Modificado                  | Elemento Obsoleto/Cambiado                                  | Implementación Nueva/Corregida                               | Razón del Cambio                                                                 |
|-------------------------------------|-------------------------------------------------------------|--------------------------------------------------------------|----------------------------------------------------------------------------------|
| `__manifest__.py`                   | `version: "18.0.1.0.0"` (asumido base v15)                 | `version: "16.0.1.0.0"`                                      | Actualización de versión para compatibilidad con Odoo 16.                        |

---
La revisión detallada de archivos XML de vistas y datos, así como la implementación de la migración de JavaScript a OWL, se realizará en etapas posteriores o se detallará como trabajo futuro si la complejidad es muy alta para una sola fase. Los archivos marcados como "Pendiente/Problemático" requieren intervención manual o un enfoque alternativo para aplicar los cambios.
