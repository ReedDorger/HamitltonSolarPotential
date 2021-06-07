#FinalProject_Dorgerrf
#Reed Dorger 
#Geo 443
#This is the code for the final Project
#In this code we will use all we learned this semester to analyze Geospatial data
#Specifically, this code will identify parcels within 500 ft of all fire hydrants within a
#   subset of municiplaites and townships within Butler county




#Script Sytanx List:
#
#
#
#
#


#Set up try/except block to help deal with potential errors
try:

    #import packages
    import arcpy, sys

    
    ##Set up the data


    #Turn on Overwrite
    arcpy.env.overwriteOutput = True

    #Set current workspace to location of data
    arcpy.env.workspace = r"D:\Geo_443\Final\FinalProject_Data\Code_Data"
    print ("The workspace is currently set to ", arcpy.env.workspace) #This tells the user where the data is exactly 

    #List off all the feature classes in the workspace so the user knows what they have to work with
    featClass = arcpy.ListFeatureClasses()
    print ("The Feature Classes in this file include: ")
    print (featClass)

    #Now we are going to examine the spatial references of the feature classes. This is to ensure everything is the same projection and datum
    #We do this by using a "for" loop to run through the file
    for fc in featClass:
        spatial_ref = arcpy.Describe(fc).spatialReference
        
        #If the spatial reference name is unknown, it tells the user
        if spatial_ref.name == "Unknown":
            print("{0} has an unknown spatial reference".format(fc))

        #Otherwise, it lists the feature class, the {0}, and then its sptial reference, {1}
        else:
            print("The spatial reference of each Feature Class are....")
            print("{0} : {1}".format(fc, spatial_ref.name))


    #Now we create objects of the data for analysis
    Parcel = "CURRENTPARCELS.shp" #All the parcels for Butler County 
    Somverville = "Somverville_hydrants.shp" #Hydrant locations for Somverville, Middletown, and Jacksonburg respectively 
    Middletown = "Middletown_hydrants.shp"
    Jacksonburg = "Jacksonburg_hydrants.shp"

    ##These next sections are going to run Feature Layer selections to identify the parcels within 500 feet of the hydrants

    ###First, Somverville
    
    #Check to see if the data already exists
    #If the data exists, it gets deleted so we can start from scratch
    if arcpy.Exists("Som_subset.shp"):
        print("Somverville subset file exists. Now Deleting")
        arcpy.Delete_management("Som_subset.shp")

    #Now we are going to run the Select By Location query to select all the hydrants within a distance 500 feet of the Somverville hydrants.
    #I attached it to a new object to make later analysis easier
    Selection = arcpy.SelectLayerByLocation_management(Parcel, "WITHIN_A_DISTANCE", Somverville, "500 FEET")
    #Now we copy the features of the spatial query selection into a new shapefile
    arcpy.CopyFeatures_management(Selection, "Som_subset.shp")
    print (arcpy.GetMessages())
    

    #Create a new field in the Somverville subset
    fieldLength = 100 # I added this to make the maximum size of the new field larger than the default because I ran into issues
    #We are adding a field in the Somverville subset called "MailAdrs" that is a text field to hold the address data
    arcpy.AddField_management("Som_subset.shp", "MailAdrs", "TEXT", "", "", fieldLength) 
    print("New field added to Somverville dataset")

    #Populate the new field with data from the different fields we need. These fields are the names on the address, the street number, the zip code, etc
    with arcpy.da.UpdateCursor("Som_subset.shp", ["MailAdrs", "MAILNAM1", "MAILADR1", "MAILADR3"]) as cursor: #The parenthases creats a list for the "for" loop
        #Use a for loop to fill all the empty rows 
        for row in cursor:
            row[0] = row[1] + ", " + row[2] + ", " + row[3] #This is the part that tells what stuff to concatenate into the new field
            cursor.updateRow(row) #This is the part that actually updates each row using the layout from the previous line
    print("Somverville addresses have been added")
            #Now repeat for the next two municipalites 
                
    ###Next, Middletown
    #Check to see if it exists
    if arcpy.Exists("Mid_subset.shp"):
        print("Middletown subset file exists. Now Deleting")
        arcpy.Delete_management("Mid_subset.shp")

    #Spatial querey selection 
    Selection = arcpy.SelectLayerByLocation_management(Parcel, "WITHIN_A_DISTANCE", Middletown, "500 FEET")
    arcpy.CopyFeatures_management(Selection, "Mid_subset.shp")
    print (arcpy.GetMessages())

    #Create a new field for the Middletown parcel subset
    arcpy.AddField_management("Mid_subset.shp", "MailAdrs", "TEXT", "", "", fieldLength)
    print("New field added to Middletown dataset")

    #Update the new field and fill the empty field created
    with arcpy.da.UpdateCursor("Mid_subset.shp", ["MailAdrs", "MAILNAM1", "MAILADR1", "MAILADR3"]) as cursor:
        for row in cursor:
            row[0] = row[1] + ", " + row[2] + ", " + row[3]
            cursor.updateRow(row)
    print("Middletown addresses have been added")


    ###Finally, Jacksonburg
    #Check to see if it exists
    if arcpy.Exists("Jac_subset.shp"):
        print("Jacksonburg subset file exists. Now Deleting")
        arcpy.Delete_management("Jac_subset.shp")

    #Spatial query selection
    Selection = arcpy.SelectLayerByLocation_management(Parcel, "WITHIN_A_DISTANCE", Jacksonburg, "500 FEET")
    arcpy.CopyFeatures_management(Selection, "Jac_subset.shp")
    print (arcpy.GetMessages())


    #Create a new field for the Jacksonburg parcel subset
    arcpy.AddField_management("Jac_subset.shp", "MailAdrs", "TEXT", "", "", fieldLength)
    print("New field added to Jacksonburg dataset")
    
    #Update the new field and fill the empty field created
    with arcpy.da.UpdateCursor("Jac_subset.shp", ["MailAdrs", "MAILNAM1", "MAILADR1", "MAILADR3"]) as cursor:
        for row in cursor:
            row[0] = row[1] + ", " + row[2] + ", " + row[3]
            cursor.updateRow(row)
    print("Jacksonburg addresses have been added")
    

    print("All new shapefiles have had their new fields populated")
    print("Check the shapefiles to find the addressess of all parcels within 500 feet of nearby fire hydrants ")
    print("The shapefiles can be found here: ", arcpy.env.workspace)


    #Turn off overwrite
    arcpy.env.overwriteOutput = False


##############################################################
except Exception as e:
    print(e.messages)

except:
    print(arcpy.GetMessages())
    print("There has been an error in your script.")


