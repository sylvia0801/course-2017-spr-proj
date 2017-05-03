price = {'02128': 5136699.3948395215, '02131': 522627.02598838817, '02135': 683935.2188391133, '02125': 839495.2810673724, '02124': 373292.7974247642, '02132': 485106.7459294437, '02136': 415580.3367003367, '02115': 1445432.1369094232, '02186': 412463.62452931685, '02445': 544859.4618909424, '02130': 602647.9295958279, '02119': 1287103.747590808, '02116': 1792803.8381484933, '02026': 708641.7049488972, '02126': 532645.3523017045, '02127': 2046179.1779603527, '02467': 4131795.316067146, '02120': 31410701.51902174, '02121': 366906.32237386267, '02134': 11153126.43678161, '02110': 2627400.075706595, '02109': 1043639.3132169576, '02554': 1944810.701462886, '02129': 1066555.1528858626, '02118': 1358019.7393273585, '02171': 536728.3738872403, '02459': 451668.8811188811, '02114': 17258317.9716647, '02090': 619770.6225680934, '02108': 28670420.8, '02446': 4190460.4583333335, '02215': 11393970.04237288, '02141': 631413.0396825396, '02458': 377245.5}
crime = {'02135': 64, '02110': 40, '02126': 120, '02127': 107, '02115': 71, '02130': 103, '02121': 89, '02119': 141, '02120': 21, '02116': 75, '02128': 59, '02118': 106, '02026': 34, '02445': 25, '02131': 69, '02125': 161, '02132': 48, '02141': 2, '02114': 11, '02186': 22, '02467': 4, '02129': 19, '02134': 13, '02108': 7, '02171': 3, '02124': 67, '02090': 1, '02215': 3, '02554': 362, '02136': 2, '02109': 5, '02446': 6}



def crimeNumber_price():
	zip_to_tuple = {}
	for zipcode1 in crime:
		for zipcode2 in price:
			if zipcode1 == zipcode2:
				zip_to_tuple[zipcode1] = (crime[zipcode1],price[zipcode2])
	return zip_to_tuple