docker-compose down
docker-compose up --build -d
docker exec -it -uroot odoo18-docker-odoo18-1 /bin/bash -c '
    # Install python3.12-venv and font packages
    echo "Installing core fonts and Microsoft fonts..."
    apt update && \
    apt install -y python3.12-venv xfonts-base fontconfig ttf-mscorefonts-installer wget && \
    echo "Updating font cache..." && \
    fc-cache -f -v && \
    
    # Create and activate venv for exo_api
    echo "Setting up venv for exo_api..." && \
    cd /mnt/extra-addons/extra/exo_api/ && python3 -m venv venv && \
    ./venv/bin/pip install -r requirements.txt && \

    # Create and activate venv for neo_do_localization
    cd /mnt/extra-addons/neo_do_localization && python3 -m venv venv && \
    ./venv/bin/pip install -r requirements.txt
'
docker-compose restart