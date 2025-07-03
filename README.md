# Odoo 18 Dockerized Production Environment

Este repositorio contiene una configuración de Odoo 18 dockerizado, diseñada para entornos de producción, con módulos personalizados y un pipeline de despliegue continuo (CI/CD) usando GitHub Actions.

## Contenido del Repositorio

* **`docker-compose.yml`**: Define los servicios Docker necesarios para Odoo y PostgreSQL.
* **`config/odoo.conf`**: Archivo de configuración principal de Odoo.
* **`postgres-config/`**: Contiene configuraciones específicas para PostgreSQL.
* **`addons/`**:
    * **`addons/invoice_api/`**: Módulo personalizado `invoice_api`.
    * **`addons/extra/`**:
        * **`exo_api/`**: Módulo personalizado `exo_api` con sus dependencias Python (`requirements.txt`).
        * **`neo_do_localization/`**: Módulo de localización dominicana `neo_do_localization` con sus dependencias Python (`requirements.txt`).
        * Otros módulos como `web_digital_sign`, `report_xlsx`, `auth_api_key`, `invoice_payment_to`.
* **`.github/workflows/deploy.yml`**: Flujo de trabajo de GitHub Actions para el despliegue automatizado a producción.
* **`restart.sh`**: Script para reiniciar los servicios Docker y gestionar las dependencias Python.

## Características Principales

* **Odoo 18 con Docker**: Contenerización completa para un entorno consistente y escalable.
* **Módulos Personalizados**: Incluye módulos desarrollados a medida para funcionalidades específicas.
* **Localización Dominicana**: Soporte para la localización de la República Dominicana.
* **Despliegue Continuo (CI/CD)**: Automatiza el proceso de despliegue a tu servidor de producción con cada `push` a la rama `main`.
* **Gestión de Dependencias Python**: Utiliza entornos virtuales (venv) dentro de los contenedores Docker para aislar las dependencias de los módulos personalizados.
* **Manejo de Fuentes para PDF**: Configuración para evitar problemas de fuentes en la generación de PDFs con Wkhtmltopdf.

## Configuración del Entorno Local (Desarrollo)

Para levantar el proyecto en tu máquina local:

1.  **Clona el repositorio:**
    ```bash
    git clone [https://github.com/JoelStalin/Odoo18-docker.git](https://github.com/JoelStalin/Odoo18-docker.git)
    cd Odoo18-docker
    ```
2.  **Configura tus variables de entorno (si aplica) y volúmenes de datos.**
3.  **Inicia los servicios Docker:**
    ```bash
    docker-compose up -d --build
    ```
4.  **Accede a Odoo:** Odoo estará disponible en `http://localhost:8069`.

## Despliegue a Producción (GitHub Actions)

Este proyecto está configurado para un despliegue continuo automático a tu servidor de producción ubicado en `/home/ubuntu/odoo18-docker` (asumiendo usuario `ubuntu`).

### Requisitos Previos para el Despliegue:

1.  **Servidor de Producción con SSH configurado:**
    * Asegúrate de que tu servidor Ubuntu tenga SSH habilitado y que puedas acceder a él con un usuario (ej. `ubuntu`).
    * La clave SSH privada asociada a la clave pública que añadas en GitHub debe estar en tu servidor.

2.  **Configuración del Entorno "production" en GitHub:**
    * En tu repositorio de GitHub, ve a `Settings` > `Environments` > `production`.
    * Asegúrate de que tengas configurados los siguientes **Secretos de Entorno**:
        * `PROD_SSH_HOST`: La IP o hostname de tu servidor.
        * `PROD_SSH_USER`: El nombre de usuario SSH (ej. `ubuntu`).
        * `PROD_SSH_KEY`: El contenido **completo** de tu clave SSH privada (ej. `~/.ssh/id_ed25519`).

### Proceso de Despliegue:

El flujo de trabajo `deploy.yml` se activará automáticamente cada vez que se realice un `push` a la rama `main` de este repositorio.

1.  **El flujo de trabajo se inicia.**
2.  **Se conecta a tu servidor** vía SSH usando los secretos configurados.
3.  **Navega al directorio del proyecto** (`/home/ubuntu/odoo18-docker`).
4.  **Realiza un `git pull origin main`** para obtener el último código de GitHub.
5.  **Ejecuta el script `./restart.sh`** para detener los contenedores, reconstruir/actualizar, instalar dependencias Python y reiniciar Odoo.

## Módulos Personalizados y Dependencias

Los módulos `exo_api` y `neo_do_localization` tienen sus propias dependencias Python especificadas en sus respectivos archivos `requirements.txt`. El script de despliegue (`restart.sh`, según lo modificado) y el flujo de trabajo de GitHub Actions se encargan de instalar estas dependencias dentro de entornos virtuales dedicados dentro del contenedor de Odoo.

## Contacto

Si tienes preguntas o necesitas ayuda con este proyecto, puedes contactar a Joel Stalin.

## Licencia

[Considera añadir aquí la licencia de tu proyecto, por ejemplo, MIT, AGPL, etc.]
