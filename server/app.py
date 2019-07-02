from api import app,routes
if __name__ == '__main__':
      app.run(host='0.0.0.0', port=3000,threaded=True,debug=True)
      # app.run(host='0.0.0.0')