from main import main_app, PORT
if __name__ == '__main__':
    main_app.run(host="0.0.0.0", port=PORT, debug=True, threaded=True,)
