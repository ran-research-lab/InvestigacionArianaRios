## Casos de prueba




def singletonsv02(featClassList, outputName):
        
    LL = featClassListToLL(featClassList)
    # the map of rows to remove from each featClass
    toRemove = {}
    for i in range(len(LL)): 
        toRemove[i] = []
    
    # for each pair of feature classes, loop through their 
    # shapes. If they intersect, the add to the toRemove map
    for fci in range(len(LL)-1):
        fcA = LL[fci]
        for fcj in range(fci+1, len(LL)):
            fcB = LL[fcj]
            print("Comparing feat classes %d %d" %(fci, fcj) )
            for rowA in range(len(fcA)):
                shapeA = fcA[rowA][1]
                rowB = 0
                intersectArea = 0
                while( rowB < len(fcB) and intersectArea <= 0):
                    if rowB not in toRemove[fcj]:
                        shapeB = fcB[rowB][1]
                        intersectArea = shapeA.intersect(shapeB,4).area 
                        if (intersectArea > 0): 
                            print(rowA,rowB)
                            if (rowA not in toRemove[fci]): toRemove[fci].append(rowA)
                            if (rowB not in toRemove[fcj]): toRemove[fcj].append(rowB)
                    rowB = rowB + 1
                   
    print(toRemove)
    
    result = []
    print("singletons (featureClass, shape)")
    for i in range(len(LL)):
        for r in range(len(LL[i])):
            if r not in toRemove[i]:
                print(i, r)
                result.append((featClassList[i],LL[i][r]))
    print (result)
    
    arcpy.CreateFeatureclass_management(r"C:\Users\taller\Desktop\ArianaRiosArcGIS",outputName, "POLYGON")
    arcpy.AddField_management(outputName, "original", "TEXT")

    for p in result:
        with arcpy.da.InsertCursor(outputName, ['SHAPE@', 'original']) as cursor:
                cursor.insertRow([p[1][1], p[0]])