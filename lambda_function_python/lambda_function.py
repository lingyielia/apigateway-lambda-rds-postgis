from datetime import datetime
import os
import psycopg2
from botocore.vendored import requests
import json

con = None

def lambda_handler(event, context):
    querytext = ("SELECT time::timestamp AS recenttime, " +
                "ST_X(ST_ClosestPoint(the_geom, ST_GeomFromText('Point(" + str(event['lon']) + " " + str(event['lon']) + ")', 4326))) AS pointLon, " +
                "ST_Y(ST_ClosestPoint(the_geom, ST_GeomFromText('Point(" + str(event['lon']) + " " + str(event['lon']) + ")', 4326))) AS pointLat, " +
                "device " +
                "FROM testtable1 " +
                "WHERE route='" + event['route'] + "' "
                "ORDER BY time DESC " +
                "LIMIT 1;")

    print('Time of user query: {}'.format(str(datetime.now())))
    print(event)

    try:
        host = "****"
        database = "****"
        user = "****"
        password = "****"

        con = psycopg2.connect(host=host, database=database, user=user, password=password)
        cur = con.cursor()
        cur.execute(querytext)
        rows = cur.fetchall()
        print(rows)
        back_time = rows[0][0]
        back_lon = str(rows[0][1])
        back_lat = str(rows[0][2])
        back_device = rows[0][3]
        #print("This location information was in database " + str(datetime.now()-back_time) + " before.")

        API_KEY = 'yourkey'
        url = ('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&' +
              'origins=' + str(event['lat']) + ',' + str(event['lon']) + '&destinations=' +
               str(back_lat) + ',' + str(back_lon) + '&key=' + str(API_KEY))

        req = requests.get(url)
        time_result = req.json()['rows'][0]['elements'][0]['duration']['text']
        return {'expected_time': time_result, 'device': back_device}
        #return event


    except psycopg2.DatabaseError as e:
        print('Error: {}'.format(e))
        raise
    else:
        print('done!')
    finally:
        print('completed at {}'.format(str(datetime.now())))
        if con:
            con.close()
