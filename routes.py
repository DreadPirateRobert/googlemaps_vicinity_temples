from flask import Flask, redirect, url_for,Response
from flask_cors import CORS, cross_origin
import MySQLdb
import json
app = Flask(__name__)
CORS(app)

@app.route('/maps/<lat>/<lon>/<radius>')
def hello_guest(lat,lon,radius):
    db = MySQLdb.connect("localhost","root","root","interproj" )
    cursor = db.cursor()
    query = "SELECT place_id, name, types, latitude, longitude, ( 3959 * acos( cos( radians('%s') ) * cos( radians( latitude ) ) * cos( radians( longitude ) - radians('%s') ) + sin( radians('%s') ) * sin( radians( latitude ) ) ) ) AS distance FROM place_temples HAVING distance < '%s' ORDER BY distance LIMIT 0 , 20" % (lat,lon,lat,radius)
    cursor.execute(query)
    data = cursor.fetchall()
    print data
    xml = '<?xml version="1.0"?><markers>'
    for key in data:
        xml = xml +  '<marker id="%s" name="%s" address="%s" lat="%s" lng="%s" distance="%s"/>' %(key[0],key[1],key[2],key[3],key[4],key[5])
    xml = xml + '</markers>'
    return Response(xml, mimetype='text/xml')

if __name__ == '__main__':
   app.run(debug = True)
