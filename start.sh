echo 'gunicorn -w 4 -b 0.0.0.0:5000 app:app' > start.sh
chmod +x start.sh