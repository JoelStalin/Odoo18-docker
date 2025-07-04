docker-compose down
docker-compose up --build -d
docker cp install_wkhtmltopdf_and_fonts.sh odoo18-docker-odoo18-1:/tmp/install_wkhtmltopdf_and_fonts.sh
docker exec -it -uroot odoo18-docker-odoo18-1 chmod +x /tmp/install_wkhtmltopdf_and_fonts.sh
docker exec -it -uroot odoo18-docker-odoo18-1 /tmp/install_wkhtmltopdf_and_fonts.sh
docker exec -it -uroot odoo18-docker-odoo18-1 /bin/bash -c 'cd /mnt/addons/extra/exo_api/ && pip3 install -r requirements.txt && cd /mnt/addons/extra/neo_do_localization && pip3 install -r requirements.txt'
docker-compose restart