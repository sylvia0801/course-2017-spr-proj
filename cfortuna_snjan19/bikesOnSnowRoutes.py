import urllib.request
import json
import dml
import prov.model
import datetime
import uuid
import csv
import json
import requests 

class bikesOnSnowRoutes(dml.Algorithm):
    contributor = 'cfortuna_snjan19'
    reads = ['cfortuna_snjan19.SnowRoutes', 'cfortuna_snjan19.BikeRoutes']
    writes = ['cfortuna_snjan19.BikesOnSnowRoutes']

    @staticmethod
    def execute(trial = False):
        '''Retrieve some data sets (not using the API here for the sake of simplicity).'''
        startTime = datetime.datetime.now()

        def intersect(R, S):
            return [t for t in R if t in S]

        def removeDuplicates(seq):
            seen = set()
            seen_add = seen.add
            return [x for x in seq if not (x in seen or seen_add(x)) and x != " "]

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('cfortuna_snjan19', 'cfortuna_snjan19')

        ###### Importing Datasets and putting them inside the mongoDB database #####

        repo.dropCollection("BikesOnSnowRoutes")
        repo.createCollection("BikesOnSnowRoutes")

        snowRoutes = repo['cfortuna_snjan19.SnowRoutes'].find()
        bikeRoutes = repo['cfortuna_snjan19.BikeRoutes'].find()
   
        ##### Perform transformations here #####

        snowData = []
        for element in snowRoutes:
            snowData.append(element["properties"]["FULL_NAME"])
            #print(element["properties"]["FULL_NAME"])
        
        # Need to shorten street to st, etc
        bikeData = []
        for element in bikeRoutes:
            route = element["properties"]["STREET_NAM"]
            if "Avenue" in route:
                route = route[:-3]
                #print(route)
            elif "Street" in route:
                route = route[:-4]
                #print(route)
            elif "Drive" in route:
                route = route[:-3]
                #print(route)
            elif "Road" in route:
                route = route[:-3] + "d"
                #print(route)
            elif "Highway" in route:
                route = route[:-6] + "wy"
                #print(route)
            elif "Boulevard" in route:
                route = route[:-8] + "lvd"
                #print(route)

            bikeData.append(route)
            #print(element["properties"]["STREET_NAM"])
        #print(bikeData)

        snowBikeRoute = removeDuplicates(intersect(snowData, bikeData))

        result = []
        uid = 1
        for route in snowBikeRoute:
            result.append( {'UID': uid, 'route': route})
            uid += 1
        #result["snowBikeRoutes"] = snowBikeRoute

        repo['cfortuna_snjan19.BikesOnSnowRoutes'].insert_many(result) 

        repo.logout()

        endTime = datetime.datetime.now()

        return {"start":startTime, "end":endTime}
    
    @staticmethod
    def provenance(doc = prov.model.ProvDocument(), startTime = None, endTime = None):
        '''
            Create the provenance document describing everything happening
            in this script. Each run of the script will generate a new
            document describing that invocation event.
            '''

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('cfortuna_snjan19', 'cfortuna_snjan19')
        doc.add_namespace('alg', 'http://datamechanics.io/algorithm/') # The scripts are in <folder>#<filename> format.
        doc.add_namespace('dat', 'http://datamechanics.io/data/') # The data sets are in <user>#<collection> format.
        doc.add_namespace('ont', 'http://datamechanics.io/ontology#') # 'Extension', 'DataResource', 'DataSet', 'Retrieval', 'Query', or 'Computation'.
        doc.add_namespace('log', 'http://datamechanics.io/log/') # The event log.
        doc.add_namespace('bdp', 'https://data.cityofboston.gov/resource/')

        this_script = doc.agent('alg:alice_bob#example', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})
        resource = doc.entity('bdp:wc8w-nujj', {'prov:label':'311, Service Requests', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        get_found = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        get_lost = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        doc.wasAssociatedWith(get_found, this_script)
        doc.wasAssociatedWith(get_lost, this_script)
        doc.usage(get_found, resource, startTime, None,
                  {prov.model.PROV_TYPE:'ont:Retrieval',
                  'ont:Query':'?type=Animal+Found&$select=type,latitude,longitude,OPEN_DT'
                  }
                  )
        doc.usage(get_lost, resource, startTime, None,
                  {prov.model.PROV_TYPE:'ont:Retrieval',
                  'ont:Query':'?type=Animal+Lost&$select=type,latitude,longitude,OPEN_DT'
                  }
                  )

        lost = doc.entity('dat:alice_bob#lost', {prov.model.PROV_LABEL:'Animals Lost', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(lost, this_script)
        doc.wasGeneratedBy(lost, get_lost, endTime)
        doc.wasDerivedFrom(lost, resource, get_lost, get_lost, get_lost)

        found = doc.entity('dat:alice_bob#found', {prov.model.PROV_LABEL:'Animals Found', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(found, this_script)
        doc.wasGeneratedBy(found, get_found, endTime)
        doc.wasDerivedFrom(found, resource, get_found, get_found, get_found)

        repo.logout()
                  
        return doc

bikesOnSnowRoutes.execute()
#doc = retrieveData.provenance()
#print(doc.get_provn())
#print(json.dumps(json.loads(doc.serialize()), indent=4))

## eof