#!/bin/bash

# Script para instalar wkhtmltopdf y fuentes esenciales dentro de un contenedor Docker Debian/Ubuntu.
# ADVERTENCIA: Los cambios realizados por este script en un contenedor en ejecución
# NO SERÁN PERSISTENTES si el contenedor se detiene y se elimina, y luego se
# recrea a partir de la imagen base original.
# La solución recomendada y persistente es modificar el Dockerfile.

set -e # Salir inmediatamente si un comando falla

echo ">>> [INFO] Iniciando la instalación de wkhtmltopdf y fuentes..."

# 0. Asegurar que el script se ejecute como root
if [ "$(id -u)" -ne 0 ]; then
  echo ">>> [ERROR] Este script debe ser ejecutado como root."
  exit 1
fi

# 1. Actualizar lista de paquetes e instalar dependencias y fuentes
echo ">>> [INFO] Actualizando lista de paquetes e instalando dependencias..."
apt-get update -qq && \
apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    dirmngr \
    libxrender1 \
    libjpeg-turbo8 \
    libxext6 \
    libfontconfig1 \
    libssl1.1 \
    fonts-liberation \
    fonts-urw-base35 \
    xfonts-75dpi \
    xfonts-base \
    wget \
    debconf-utils && \
apt-get clean && rm -rf /var/lib/apt/lists/*

# 2. Pre-aceptar la licencia EULA de msttcorefonts
echo ">>> [INFO] Pre-aceptando EULA para ttf-mscorefonts-installer..."
echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | debconf-set-selections

# 3. Instalar ttf-mscorefonts-installer (que podría requerir interacción si debconf no funcionó)
echo ">>> [INFO] Instalando ttf-mscorefonts-installer..."
apt-get update -qq && \
apt-get install -y --no-install-recommends ttf-mscorefonts-installer && \
apt-get clean && rm -rf /var/lib/apt/lists/*


# 4. Descargar e instalar la versión específica de wkhtmltopdf
# Asegúrate de que esta URL y versión son las correctas para tu sistema.
# Ejemplo para Debian Bullseye amd64 con QT parcheado.
WKHTMLTOPDF_VERSION="0.12.6.1-3"
WKHTMLTOPDF_DISTRO="bullseye" # Asegúrate que coincida con tu imagen base (e.g., buster, focal)
WKHTMLTOPDF_ARCH="amd64"
WKHTMLTOPDF_DEB_URL="https://github.com/wkhtmltopdf/packaging/releases/download/${WKHTMLTOPDF_VERSION}/wkhtmltox_${WKHTMLTOPDF_VERSION}.${WKHTMLTOPDF_DISTRO}_${WKHTMLTOPDF_ARCH}.deb"
WKHTMLTOPDF_DEB_LOCAL="/tmp/wkhtmltox.deb"

echo ">>> [INFO] Descargando wkhtmltopdf desde ${WKHTMLTOPDF_DEB_URL}..."
wget --quiet -O "${WKHTMLTOPDF_DEB_LOCAL}" "${WKHTMLTOPDF_DEB_URL}"

echo ">>> [INFO] Instalando wkhtmltopdf..."
dpkg -i "${WKHTMLTOPDF_DEB_LOCAL}" || apt-get -fy install # Intentar arreglar dependencias si dpkg falla

echo ">>> [INFO] Limpiando archivos descargados..."
rm "${WKHTMLTOPDF_DEB_LOCAL}"
apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# 5. Actualizar la caché de fuentes
echo ">>> [INFO] Actualizando caché de fuentes..."
fc-cache -f -v

echo ">>> [SUCCESS] Instalación de wkhtmltopdf y fuentes completada."
echo ">>> [INFO] Por favor, reinicia el servicio de Odoo si es necesario."
echo ">>> [INFO] Verifica la versión con: wkhtmltopdf --version"
echo ">>> [INFO] Verifica las fuentes Courier con: fc-list | grep -i courier"
