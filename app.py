from ourapp import app,db

@app.before_first_request
def create_tables():
    db.create_all()

# ENsuring that our responses doesnt get cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

if __name__ == "__main__":
    app.run(debug=True)
