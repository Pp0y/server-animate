echo 'gunicorn -w 4 -b 0.0.0.0:$PORT server:app' > start.sh
chmod +x start.sh
