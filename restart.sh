docker-compose down
docker-compose up --build -d
docker cp install_wkhtmltopdf_and_fonts.sh odoo18-docker-odoo18-1:/tmp/install_wkhtmltopdf_and_fonts.sh
docker exec -it -uroot odoo18-docker-odoo18-1 chmod +x /tmp/install_wkhtmltopdf_and_fonts.sh
docker exec -it -uroot odoo18-docker-odoo18-1 /tmp/install_wkhtmltopdf_and_fonts.sh
docker exec -it -uroot odoo18-docker-odoo18-1 /bin/bash -c '
    echo "Updating package list and installing system dependencies..."
    
    EXO_API_DIR="/mnt/extra-addons/extra/exo_api"
    NEO_DO_LOC_DIR="/mnt/extra-addons/neo_do_localization"

    # Setup venv and install requirements for exo_api
    if [ -d "$EXO_API_DIR" ]; then
        echo "Setting up venv for exo_api..." && \
        cd "$EXO_API_DIR" && \
        python3 -m venv venv && \
        source venv/bin/activate && \
        if [ -f "requirements.txt" ]; then
            echo "Installing requirements for exo_api..." && \
            pip install -r requirements.txt && \
            echo "exo_api requirements installed."
        else
            echo "requirements.txt not found in $EXO_API_DIR"
        fi
        deactivate && \
        echo "exo_api venv setup complete."
    else
        echo "Directory $EXO_API_DIR not found."
    fi

    # Setup venv and install requirements for neo_do_localization
    if [ -d "$NEO_DO_LOC_DIR" ]; then
        echo "Setting up venv for neo_do_localization..." && \
        cd "$NEO_DO_LOC_DIR" && \
        python3 -m venv venv && \
        source venv/bin/activate && \
        if [ -f "requirements.txt" ]; then
            echo "Installing requirements for neo_do_localization..." && \
            pip install -r requirements.txt && \
            echo "neo_do_localization requirements installed."
        else
            echo "requirements.txt not found in $NEO_DO_LOC_DIR"
        fi
        deactivate && \
        echo "neo_do_localization venv setup complete."
    else
        echo "Directory $NEO_DO_LOC_DIR not found."
    fi

    echo "All custom module dependencies processed."
'
docker-compose restart