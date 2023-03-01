###### TASK #######

'''Within our trt00_shp.shp shapefile, we want to find those tracts whose size
are at least 5,000,000 but smaller than 50,000,000. Write a Python program
(using arcpy) to print the OID value, the size, and the centroid coordinates
of each of these tracts. Also, print out how many such tracts there are in the file.
Submit your work in a .py file, and make sure to include all the printout at the
end of the file using a doctstring.'''

## INITIALIZATION ##
'''this file must be run through the arcgis IDLE environment,
i.e "C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\Scripts\idle.exe"'''

import arcpy
shpfile = r'C:\\Users\\steve\\OneDrive - The Ohio State University\\5223' \
          r'\\data\\libraries_data_sources\\trt00_shp.shp'

def justTheRightSize(shpFilePath):
    sCurs = arcpy.da.SearchCursor(shpFilePath, ['OID@','SHAPE@'])
    rightSizeCount = 0
    for tract in sCurs:
        tractOID = tract[0]
        tractSize = tract[1].area
        tractCentroidCoords = [tract[1].centroid.X,tract[1].centroid.Y]
        if tractSize >= 5000000 and tractSize < 50000000:
            print(f'OID: [{tractOID}] --- Tract Size: [{tractSize}] --- Centroid Coordinates' +
                  f' {tractCentroidCoords}')
            rightSizeCount += 1
    print(f"-------- COMPLETE || {rightSizeCount} tracts were the right size -------- ")
## MAIN ##
justTheRightSize(shpfile)

## RESULTS ##
"""
>>> 
====================================== RESTART: C:/Users/steve/OneDrive - The Ohio State University/5223/exercises-Geometry/q2.py ======================================
OID: [20] --- Tract Size: [7182316.408492436] --- Centroid Coordinates [326754.7264221756, 4430371.009380203]
OID: [53] --- Tract Size: [6695198.978483512] --- Centroid Coordinates [324750.16769006604, 4426747.569519824]
OID: [76] --- Tract Size: [11245057.226468807] --- Centroid Coordinates [318019.98926039756, 4444145.747114026]
OID: [77] --- Tract Size: [10314952.081949098] --- Centroid Coordinates [316496.48446084454, 4442523.347375364]
OID: [78] --- Tract Size: [9464367.101493899] --- Centroid Coordinates [319004.50861647364, 4439437.193616829]
OID: [79] --- Tract Size: [30804609.18621275] --- Centroid Coordinates [314658.1147522799, 4438943.232443776]
OID: [88] --- Tract Size: [10169887.4441304] --- Centroid Coordinates [323122.8137574865, 4438440.01713169]
OID: [91] --- Tract Size: [9366885.994270973] --- Centroid Coordinates [321428.2048282153, 4443407.325833916]
OID: [96] --- Tract Size: [6626691.76052687] --- Centroid Coordinates [325591.8312871966, 4443682.940832917]
OID: [123] --- Tract Size: [7843741.141762089] --- Centroid Coordinates [333037.8363065042, 4442888.766724743]
OID: [126] --- Tract Size: [6291040.178981105] --- Centroid Coordinates [330806.05386457714, 4442934.243951266]
OID: [127] --- Tract Size: [8801895.079578683] --- Centroid Coordinates [328379.378587061, 4443588.593739762]
OID: [133] --- Tract Size: [7432034.73440768] --- Centroid Coordinates [337479.1127637621, 4437146.152758084]
OID: [134] --- Tract Size: [5838643.344274485] --- Centroid Coordinates [339980.64577279554, 4437009.548048574]
OID: [138] --- Tract Size: [10033167.518422926] --- Centroid Coordinates [340223.109176028, 4441776.278723977]
OID: [140] --- Tract Size: [27885865.179003417] --- Centroid Coordinates [344517.31116098183, 4433515.900251523]
OID: [141] --- Tract Size: [26017315.65127829] --- Centroid Coordinates [346044.81843290734, 4429795.41872531]
OID: [142] --- Tract Size: [11782730.791825568] --- Centroid Coordinates [338853.15903576004, 4429016.968690064]
OID: [146] --- Tract Size: [7282239.62996996] --- Centroid Coordinates [342109.5879075147, 4429945.963336881]
OID: [148] --- Tract Size: [6273354.284201998] --- Centroid Coordinates [339771.3261986133, 4434184.593188489]
OID: [156] --- Tract Size: [7879704.317111661] --- Centroid Coordinates [336098.84207554715, 4433854.439559394]
OID: [157] --- Tract Size: [6162464.301321306] --- Centroid Coordinates [335572.6782120462, 4430539.202559163]
OID: [167] --- Tract Size: [9994882.107452279] --- Centroid Coordinates [314191.80932802364, 4435096.023307505]
OID: [168] --- Tract Size: [7815531.352484281] --- Centroid Coordinates [317259.459972744, 4435020.103808231]
OID: [170] --- Tract Size: [7345630.77797778] --- Centroid Coordinates [314731.32053113444, 4431956.203441624]
OID: [171] --- Tract Size: [5546352.625840656] --- Centroid Coordinates [317299.9266584982, 4431330.563008228]
OID: [172] --- Tract Size: [7896097.1649446795] --- Centroid Coordinates [320517.170242645, 4429995.728331557]
OID: [173] --- Tract Size: [13297273.118120732] --- Centroid Coordinates [316301.3872413338, 4429075.525448651]
OID: [174] --- Tract Size: [5911723.43076946] --- Centroid Coordinates [319814.4409250585, 4435973.309765049]
OID: [175] --- Tract Size: [8659056.088096924] --- Centroid Coordinates [319843.4255132709, 4433275.975321998]
OID: [181] --- Tract Size: [8483671.495906055] --- Centroid Coordinates [314713.1228244063, 4425535.149764354]
OID: [182] --- Tract Size: [7960841.920834352] --- Centroid Coordinates [317133.1371020038, 4426920.782469734]
OID: [183] --- Tract Size: [17707662.791019153] --- Centroid Coordinates [316673.0628873418, 4419644.990480892]
OID: [184] --- Tract Size: [35903381.87447501] --- Centroid Coordinates [312502.0085271069, 4422272.514694977]
OID: [185] --- Tract Size: [7355348.385611084] --- Centroid Coordinates [320365.3210884906, 4425621.582019528]
OID: [188] --- Tract Size: [5542321.239516255] --- Centroid Coordinates [320859.8542258177, 4427488.685689644]
OID: [194] --- Tract Size: [8629701.940494716] --- Centroid Coordinates [326521.98097918107, 4421474.605898865]
OID: [197] --- Tract Size: [6739005.577694324] --- Centroid Coordinates [322782.8640013015, 4419914.341796228]
OID: [198] --- Tract Size: [11760977.377959415] --- Centroid Coordinates [326675.3929675083, 4418853.04994546]
OID: [204] --- Tract Size: [5081358.949825505] --- Centroid Coordinates [331050.8327483975, 4419466.349078692]
OID: [205] --- Tract Size: [8452719.309144983] --- Centroid Coordinates [333891.7804140607, 4419246.517335303]
OID: [208] --- Tract Size: [6045719.405816016] --- Centroid Coordinates [329001.1992973385, 4417057.565995337]
OID: [213] --- Tract Size: [6396877.343801692] --- Centroid Coordinates [339658.96035143203, 4427287.447907825]
OID: [223] --- Tract Size: [5128873.398656095] --- Centroid Coordinates [339096.8065104279, 4421391.915996048]
OID: [233] --- Tract Size: [6558596.638678822] --- Centroid Coordinates [341980.7076699315, 4425543.574667948]
OID: [238] --- Tract Size: [6403457.6469214605] --- Centroid Coordinates [343764.03786969255, 4420770.442130192]
OID: [245] --- Tract Size: [6657783.917980205] --- Centroid Coordinates [347064.0363371184, 4426432.303213005]
OID: [248] --- Tract Size: [12253998.814720353] --- Centroid Coordinates [337176.37660575367, 4418649.478597314]
OID: [249] --- Tract Size: [9177670.033115491] --- Centroid Coordinates [338570.5754500108, 4413191.594509071]
OID: [250] --- Tract Size: [12525660.967273919] --- Centroid Coordinates [344687.47489364084, 4412134.742013912]
OID: [252] --- Tract Size: [44833796.34757115] --- Centroid Coordinates [340499.88367693155, 4416097.584456475]
OID: [253] --- Tract Size: [13483917.183219079] --- Centroid Coordinates [334274.2407082633, 4409208.107308983]
OID: [254] --- Tract Size: [6451424.04114533] --- Centroid Coordinates [333254.1278431182, 4416343.508416404]
OID: [255] --- Tract Size: [47375899.196612544] --- Centroid Coordinates [330572.54022350896, 4412116.541485818]
OID: [256] --- Tract Size: [6362117.811165618] --- Centroid Coordinates [320938.12310151244, 4417681.137182313]
OID: [259] --- Tract Size: [7593997.884760368] --- Centroid Coordinates [323906.3899730305, 4417397.3261722]
OID: [260] --- Tract Size: [39661951.365439594] --- Centroid Coordinates [325165.7839719684, 4412138.828965837]
OID: [261] --- Tract Size: [27287865.470407516] --- Centroid Coordinates [320765.3901898729, 4411965.644709231]
OID: [262] --- Tract Size: [8055662.7264291] --- Centroid Coordinates [319402.7496923709, 4417162.929753893]
-------- COMPLETE || 59 tracts were the right size -------- 
>>> 
"""
