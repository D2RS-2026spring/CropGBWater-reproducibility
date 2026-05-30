# import system modules
import sys
import os, os.path
import datetime, time
from datetime import date, datetime, timedelta
import pandas as pd
import re
import numpy as np
import logging
import calendar

# import the cropwat modules
# import file_monthly2
# Set up logging
log_file_path = 'batch_processing.log'
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

path = r"yourpath"


fpath = path + "\\" + "INPUT"
ofpath = path + "\\" + "OUTPUT"
fpath_crop =  fpath + "\\CropCalender\\"+ cropi

print (fpath_crop)


fpath_soil =  fpath + "\SOIL"
fpath_precp =  fpath + "\\" + "PRECIP" 
fpath_eto =  fpath  + "\\" + "ETO" 
# version of the model 
__version__ = '$Revision: 2025-06-01$'

# the time definition 
def localtimestrf(frmtopt="datetime"):
    ''' Return the local date-time as a formatted string. 
        frmtopt="datetime" (default)   Return a complete date-time string.
        frmtopt="timeonly"             Return Hour:Minute:Seconds only.
        
    '''
    if frmtopt == "datetime":
        return time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    elif frmtopt == "timeonly":
        return "Time: " + time.strftime("%H:%M:%S", time.localtime())


print ("\n***** Global water footprint assessment model *****")  # no name yet given!!
print ("            " + __version__)
print ("            " + localtimestrf())
print (fpath_crop)
print (fpath_soil)
print (fpath_precp)
print (fpath_eto)



def read_input_files(gridID, fpath_crop, fpath_soil, fpath_precp, fpath_eto):
    '''
    reads input files and create a dataframe
    crop_file - a file with one line of data per grid. It contains all crop parameters - kc, planting and harvest date, length of plant growth stages
                initial and final rooting depth, max yield, nitrogen application rate if 
    soil-file - a file with one line of data per grid. It contains total available water capacity (TAWC, mm/m) and curve number (CN)
    precp_file - daily preciptation data (mm)- first 8 lines are description of the data. The daily data are provided starting line 9 in one column 
    precp_file - daily ETo data (mm)- first 8 lines are description of the data. The daily data are provided starting line 9 in one column
   
    make sure the columns names are proper - need to remove this later or make it permanent  '''
    
    
    crop_file = os.path.join(fpath_crop, cropi + '_' + gridID + '.csv');
    soil_file = os.path.join(fpath_soil, 'SOIL_' + gridID + '.csv');
    prcp_file = os.path.join(fpath_precp, 'PRE_' + gridID + '.DLY');
    eto_file = os.path.join(fpath_eto, 'PET_' + gridID + '.ETO');

    df_crop = pd.read_csv(crop_file, delimiter=',', skiprows=[2]);
    df_soil = pd.read_csv(soil_file, delimiter=',', usecols=['AWC', 'CN']);
    df_prcp = pd.read_csv(prcp_file, delimiter='\s+|\t+', engine='python', skiprows=[i for i in range(0, 8)], usecols=[0]);
    df_eto = pd.read_csv(eto_file, delimiter='\s+|\t+', engine='python', skiprows=[i for i in range(0, 8)], usecols=[0]);
    
    'this need to be commented out for now. No consistent naming of crop column'
    #df_crop.columns = new_columns

    return df_crop, df_soil, df_prcp, df_eto
 

 

def safeDevide(x, y, errorValue = 0): #avoid division by zero
    if y == 0:
        return errorValue
    else:
        return x / y
 
def days_in_year(year):
    # Check if the year is a leap year
    if calendar.isleap(year):
        return 366  # Leap year has 366 days
    else:
        return 365  # Non-leap year has 365 days
 
 
def read_crop_parameters(df_crop):

    # latitude, longitude and ID of the grid

    #X_Grid = df_crop['X_CORD']     # X-grid (latitude) in degree
    #Y_Grid = df_crop['Y_CORD']     # Y-grid (longitude)
    ID = int(float(df_crop['ID'].iloc[0])) # gird ID
    

    # crop parameters
    KCini = float(df_crop['Kc_ini'].iloc[0])      # initial crop coefficient Kc 
    KCmid = float(df_crop['Kc_mid'].iloc[0])      # mid season crop coefficient Kc
    KCend = float(df_crop['Kc_end'].iloc[0])      # final crop coefficient Kc
    Lini = int(df_crop['L_ini'].iloc[0])         # length of crop initial stage
    Ldev = int(df_crop['L_dev'].iloc[0])         # length of crop development stage
    Lmid = int(df_crop['L_mid'].iloc[0])         # length of crop mid stage
    Llate = int(df_crop['L_late'].iloc[0])        # length of crop late stage

    pmonth = int(df_crop['Month'].iloc[0])       # planting month 
    pday = int(df_crop['Day'].iloc[0])       # planting date 

      
    # for rainfed field
    
    Zrmin_rf = float(df_crop['Rdmin'].iloc[0])
    Zrmax_rf = float(df_crop['Rdmax_rf'].iloc[0])

    # for irrigated field
    
    Zrmin_irr = float(df_crop['Rdmin'].iloc[0])    # initial rooting depth, for annual crop Zrmin = 0.2 and for perinnial Zrmin = Zrmax
    Zrmax_irr = float(df_crop['Rdmax_irr'].iloc[0])    # float(cfields[15])   or 1.25 (average    # maximum rooting depth - attained at plant development stage
    
    # for irrigated fieled but rainfed
    Zrmin_irf = float(df_crop['Rdmin'].iloc[0])       # initial rooting depth, for annual crop Zrmin = 0.2 and for perinnial Zrmin = Zrmax
    Zrmax_irf = float(df_crop['Rdmax_irr'].iloc[0])      # or use 1.6 as average -- maximum rooting depth - attained at plant development stage

    Pstd = float(df_crop['P'].iloc[0])        # standard water depletion fraction for no stress for ET = 5 mm/day
    Ky = float(df_crop['Ky'].iloc[0])          # yield response factor - to water stress
    Ym = max(float(df_crop['Ym'].iloc[0]),0.0)                # maximum yield; max is used to avoid novalue of -9999 from the input file
    
    N_ferti = float(df_crop['Nitr_kg_ha'].iloc[0])         # fertilizer application rate 

 
    return ID, KCini, KCmid, KCend, Lini, Ldev, \
           Lmid, Llate, pmonth, pday, Zrmin_rf, Zrmax_rf, Zrmin_irr, \
           Zrmax_irr, Zrmin_irf, Zrmax_irf, Pstd, Ky, Ym, N_ferti


# Loop through grid IDs and process data

def daily_KC (J, Jdev, Jmid, Jlate, Jharv, Ldev, Llate, KCini, KCmid, KCend):
    
    # daily values of KC, based on eqn (66) pp. 132, Fig 34 pp. 126 of FAO-56
    if J <= Jdev:
        KC = KCini
    elif Jdev < J < Jmid:
        KC = KCini + (KCmid - KCini)*(J - Jdev)/Ldev
    elif Jmid <= J <= Jlate:
        KC = KCmid
    elif Jlate < J < Jharv:
        KC = KCmid + (KCend - KCmid)*(J - Jlate)/Llate
    else:
        KC = KCini
        
    return KC

def rooting_depth(J, Jmid, Zrmin, Zrmax, KC, KCini, KCmid):
    # calculation of the root depth. following pp. 279 (Annex 8) of FAO-56 
    
    if J <= Jmid:                                                       
            Zri = Zrmin + (Zrmax - Zrmin)*((KC - KCini)/(KCmid - KCini))
    else: 
            Zri = Zrmax

    return Zri
 
def runoff(PR, CN, crop):
    
    

    # Runoff routing replaced with USDA SCS curve number - adopted from Aquacrop manual v
    # see Chapter 3, page 3-48 eqn (3.7e)
    """
    RO - amount of water lost by surface runoff [mm]
    PR - rainfall amount [mm]
    CN - curve number
    S - potential maximum soil water retention [mm]
    Ia = initial abstraction [mm] or the amount of water that can infiltrate before runoff occurs
    
    Bunds of 200 mm is added for paddy rice under ponding 
    source Steduto et al (2012) - pp 108
    """
    S = 254*(100/CN-1)      
    Ia = 0.05*S 
    
    RO = ((PR - Ia)**2)/(PR + S - Ia)
           
    # after accounting for the 200 bunds, runoff will be zero if it is less than the bunds
    bund = 200
    if crop == 'Rice':
        RO = max((RO - bund), 0.0)
    else:
        RO
    
    return RO

def KS_value (Dri, RAW, St, Pi, TAW):

    """
    #Soil water depletion coefficient as function of soil water depletion (Dri), soil moisture(St),
    # total available water (TAW), and readly availabe water (RAW)
    TAW = TAWC * Zi ; TAWC - total available water capacity (mm/m); Zi = root depth (m)
    St = TAW - Dri ;
    RAW = p*TAW # p is average fraction of Total Available Soil Water (TAW) that can be depleted from 
                #the root zone before moisture stress (reduction in ET) occurs [0 - 1].
    KS = (TAW-Dri)/(TAW-RAW) = St/((1-p)TAW)
    ((St)/((1-Pi)*TAW) 
    """
    ratio1 = safeDevide(St, ((1-Pi)*TAW))
    
    if TAW==0.0:
        KS = 0
    elif Dri > RAW:
        KS = max(0,ratio1)
    else:
        KS = 1

    return KS
 
def deep_percolation(Dri, PR, RO, ETc, IRR):

    # deep percolation (DP) calculation
    # when the soil is at field capacity Dri = 0 so DP follows this equation.
    # The Dr in the equation is Dr,i-1
    "*****Needs updating based on the methodology write up"

    if Dri > 0:                                                     
        DP = 0
    else:                                                           
        DP = max(((PR - RO) + IRR - ETc - Dri),0)  

    return DP
 
def greyWU (N_ferti, Cmax, LR):
    
    # the grey water use (m3/ha)
    # LR -> leaching rate assumed 10%
    # Cmax -> maximum permissiable limit NO3-N [kg/m3] -
    # this corresponds to 10 mg/l (NO3-N) emission standard
    # L -> nitrogen leaching to the ground [kg/ha]
    
    LR = 0.1            
    Cmax = 0.01         
   
    L = LR * N_ferti     
 
    CWU_gy= safeDevide(L, Cmax)

    return CWU_gy

def actual_yield(Ym, Ky, ETa, ETc):

    # yield reduction and actual yield calculation
    # the lower limit is set at 20% of Ym to avoid zero values - if crop earea
    # exists Y should be different from zero
    
    #to avoid div by zero for cases where no data to calculate ETc use 
    #safeDevide(x, y)
    #Ya = max((Ym*(1-Ky*(1-(ETa/ETc)))),0.2*Ym)
    
    # to avoid cases where Ya = 0 when ETa is very small, use 20% of Ym
    # we need also make use to avoid a yield value when ETa=0
    if ETa ==0.0:
        Ya_min = 0.0
    else:
        Ya_min = 0.2*Ym
        
    Ya = max((Ym*(1-Ky*(1-(safeDevide(ETa, ETc))))),Ya_min)

    return Ya

def initialize_parameters (TAWC, Zrmin_rf, Zrmin_irr, Pstd, pYear,pmonth, pday, yearC, monthC, dayC, Lini, Ldev, Lmid, Llate):
    
    # parameters initialization

    KS_rf = 1 ;    KS_irr = 1
    
    # ??? initial root zone depletion => Zro is the initial root depth = 0.2 (FAO-56, pp279);
    #and RAW raidly available soil moisture at the begining (preseason - 5 day averag)
    # for rainfed
    TAW_rf = TAWC * Zrmin_rf ; Dri_rf = TAWC * Zrmin_rf * Pstd                

    
    # for irrigated
    TAW_irr = TAWC * Zrmin_irr ; Dri_irr = TAWC * Zrmin_irr * Pstd

    #IRR = Dri_irr

    # for irrigated field but only rain-fed
    #TAW_irf = TAWC * Zrmin_irr ; Dri_irf = TAWC * Zrmin_irr * Pstd


    St_rf = TAW_rf - Dri_rf ; St_irr = TAW_irr - Dri_irr; #St_irf = TAW_irf - Dri_irf


    
    ETa_rf_total = 0       # total actual evapotranspiration
    ETa_irr_total = 0
    ETc_total = 0       # total maximum evapotranspiration


    RO = 0              # run-off

    IRR = 0             # irrigation at each time step
    
    CR = 0              # capilary rise assumed zero



    #identifying the row number of the climate data, based on the planting and start of the climate data
    #planting date
    #pYear = 2004

    plantingDate = date(pYear,pmonth,pday)
    
    if pday > calendar.monthrange(pYear, pmonth)[1]:
        raise ValueError(f"Invalid day {pday} for the month {pmonth} in year {pYear}")

    climStartDate = date(yearC,monthC,dayC)

    date_to_planting = (plantingDate - climStartDate)
    Jplant = date_to_planting.days 

    #total lenght of growing dates
    gDates = Lini + Ldev + Lmid + Llate -1 # -1 accounts for the planting day and avoid going to next year 
    #delta = datetime.timedelta(days=gDates)
    delta = timedelta(days=gDates)

    #harvest year - we use this for printingout the result
    hYear = (plantingDate + delta).year
    
    #computed dates for the stages
    Jdev = Jplant + Lini
    Jmid = Jdev + Ldev
    Jlate = Jmid + Lmid
    Jharv = (Jlate + Llate) 
    
    #days_in_y = days_in_year(year)

    doy = plantingDate.timetuple().tm_yday   
    
    return KS_rf, KS_irr, TAW_rf, TAW_irr, Dri_rf, Dri_irr, St_rf, St_irr, ETa_rf_total, ETa_irr_total, \
            ETc_total, RO, IRR, CR, Jplant, hYear, Jdev, Jmid, Jlate, Jharv, doy

def calculate_soil_water (TAWC, Zri, Pi, Dri):
    

    ''' soil water content calculation
    TAW -  total available soil water in the root zone (mm); TAWC (mm/m) - total soil water capacity
    RAW    # raidly available soil water in the root zone (mm)
    St     # the actual available soil water content (mm). 
    
    '''
           
    TAW = TAWC * Zri                                                
    RAW = TAW * Pi     
    St = TAW - Dri
    
    return TAW, RAW, St
 
     
def daily_soil_water_balance(PR, ETc, KS, RO, DP, Dri, TAW, IRR):
     

    '''~~~~~~~~~~~~~~ calculation of Ks and actual evapotranspiration ~~~~~~~~~~~~~'''
    # calculation of Ks, actual evapotranspiration, soil water depletion on a daily basis
    # KS - the water stress coefficient calculated 
    # ETa - the the adjusted crop ET (mm/day)
    # Dri - soil water depletion (mm/day)- at end of the current period
    #       it can be 0 <= Dri <= TAW; pp 170 and Annex 8, pp 277
    # DP - deep percolation (mm/day)
    
    
    ETa = ETc * KS  


    # soil water depletion (mm/day) - at end of the current period
    Dri = min((max((Dri - PR + RO - IRR + ETa + DP),0)),TAW)
    
    return ETa, Dri


croplist = ['Potato', 'Maize', 'rCoffee', 'Rubber', 'sBeet', 'Sesameseed', 'sMillet', 'Sorghum', 'Soybean', 'sPotato', 'Sugarcane', 'Maize', 'Tea', 'TemperateF', 'Tobacco', 'Tomato', 'TropicalF', 'Wheat', 'Yams']

firstY = 2018
lastY = 2022
pYears = range(firstY,lastY+1) # +1 so the last year is included in the analysis

#climate start year, month, date in the ETO and prec files
yearC = 2018
monthC = 1
dayC = 1

#df header
wf_header=['CWR', 'CWU_gn_rf', 'CWU_gn_irr', 'CWU_bl', 'CWU_gy', 'IRReq', 'Ya_rf', 'Ya_irr']

#header for grey WF (mm) and yield (t/ha) to be added in the monthly output
y_header = ['CWU_gy', 'Ya_rf', 'Ya_irr']


# record start time
start = time.time()
print(croplist)

for cropi in croplist:
    
    
    # cropFile1 = cropfile
    # (ShortName, Extension) = os.path.splitext(cropFile1)
    gridIDs=[]

    fpath_crop =  path + "\\INPUT\\CropCalender\\"+ cropi
    print (fpath_crop)
    
    for filename in os.listdir(fpath_crop):
        
        # check files and collect the grid id
        if filename.startswith(cropi):
            #print (filename)
            #get the id and add it to the list
            gridIDcr = (os.path.splitext(os.path.basename(filename))[0])
            gridID = re.split("[_]", gridIDcr)[-1]
            gridIDs.append(gridID)
            
    print(gridIDs)
    
     
     
    # to avoid memory problem use chunk, if no problem use the whole grid
    chunk_size = len(gridIDs) #1000
    print (chunk_size)

        
    for pYear in pYears:
        
        
    
        #creat daily list - this should have been in the year loop and use pYear and hYear
                
        firstDate = date(pYear,1,1)
        lastDate = date(pYear+1,12,31)
        
        nDates = (lastDate - firstDate).days
                
        d_header = pd.date_range(firstDate, lastDate).strftime("%Y-%m").tolist()
        
        # initialize array's
        #b = (len(gridIDs), nDates+1) 
        b = (chunk_size, nDates+1) ; c = (chunk_size, 3)
        
        cwr_d = np.zeros(b); cwu_gn_rf_d = np.zeros(b); cwu_gn_ir_d = np.zeros(b);
        cwu_bl_d = np.zeros(b); IRReq_d = np.zeros(b);
        
        y_result = np.zeros(c)
        
        #i=-1 ; j = i
        
        
        # initialize empty DataFrame
        df_cwr = pd.DataFrame(columns=d_header); 
        df_cwu_gn_rf = df_cwr.copy();
        df_cwu_gn_ir = df_cwr.copy();
        df_cwu_bl = df_cwr.copy(); 
        df_IRReq = df_cwr.copy();
        df_y = pd.DataFrame(columns=['cwu_gy', 'Y_rf', 'Y_irr'])
        
        #empty df for the water evaporation before planting
        d = (len(gridIDs), 1)
        et_paddy = np.zeros(d)
        
        
        
        # Keep track of the starting index for each chunk in the result_array
        current_index = 0
        
        
        # Process data in chunks based on gridIDs len(gridIDs)
        for i in range(0, len(gridIDs), chunk_size):
            # Take a chunk of gridIDs
            gridIDs_chunk = gridIDs[i:i + chunk_size]
            
            print ('In loop')
        
            #for each listed grid, do the green/blue separation       
            # Process each grid ID in the chunk
            for gridID in gridIDs_chunk:
                #print (gridID)

                # the input files with daily data and the dataframes

                df_crop, df_soil, df_prcp, df_eto = read_input_files(gridID, fpath_crop, fpath_soil, fpath_precp, fpath_eto)

                ID, KCini, KCmid, KCend, \
                        Lini, Ldev, Lmid, Llate, pmonth, pday, \
                        Zrmin_rf, Zrmax_rf, Zrmin_irr, \
                        Zrmax_irr, Zrmin_irf, Zrmax_irf, \
                        Pstd, Ky, Ym, N_ferti = read_crop_parameters(df_crop)



                #soil parameters (field 3- for FAO and field 4 for ISRIC data)
                TAWC = max(df_soil['AWC'][0],50)          # maximum soil moisture capacity in mm/m - soil water capacity 1000*(FC -WP)?
                                                        # the zero and 15 mm/m values are creating problem on the ET and yield. Used in the rerun
                CN = df_soil['CN'][0]

 

                # parameters initialization
                
                KS_rf, KS_irr, TAW_rf, TAW_irr, Dri_rf, Dri_irr, St_rf, St_irr, ETa_rf_total, \
                ETa_irr_total, ETc_total, RO, IRR, CR, Jplant, hYear, Jdev, Jmid, Jlate, Jharv, \
                doy = initialize_parameters(TAWC, Zrmin_rf, Zrmin_irr, Pstd, pYear,pmonth, pday, yearC, monthC, dayC, Lini, Ldev, Lmid, Llate)

                # 1:Simulation of first day, for j=0
                # 1-1: The green, blue and total composition of the initial soil moisture, in mm [1st day of the simulation]
                # g= green; cr = capillary rise; ir = irrigation, 
                rzsw_g = St_irr  #green soil moisture
                rzsw_cr = 0.0  #capillary rize
                rzsw_ir = 0.0
                rzsw = rzsw_g + rzsw_cr + rzsw_ir

                delta_rzswg = 0.0
                delta_rzswcr = 0.0
                delta_rzswir = 0.0
                
                """ This is for paddy rice - to calculate the open water evaporation"""
                #For paddy rice, read ETo for the 30 days before the planting and calculate ET from paddy
                #ETo_p = round(max(float(df_eto.iloc[J].iloc[0]),0.0001),2)
                # Calculate the start index for aggregation (e.g., J-30)
                start_index = max(Jplant - 30, 0)  # Ensure start index doesn't go below zero

                # Slice the DataFrame to include only the days to aggregate
                df_to_aggregate = df_eto.iloc[start_index:Jplant + 1]

                # Multiply the daily ETo values by the KCini
                df_to_aggregate *= KCini

                # Calculate the aggregate of the modified ETo values over the 30-day period
                eto_dd = round(float(df_to_aggregate.sum().sum()), 2)
                #print (eto_dd)
                #sum_per_grid_df.index = df_et_p['grid_column'].unique()
                
                #for paddy rice, initialize paddy water at 150 mm
                paddy_ac = TAW_irr + 150
                IRR_ad = 150 # initial assume it is full
                
                et_paddy[current_index] = eto_dd
                
                """ for paddy rice"""

                
                # output file to hold monthly and annual results
                #ofile_all = os.path.join(ofpath, cropi + '_all%s_1a.csv'%hYear)

                
                #for loop over the grawing period - from planting to harvest
                for J in range (Jplant, Jharv, 1): 
                    
                    #print (Jplant)
                    #the rzsw need to be adjusted to account for root growth and more water availability
                    # allocate the difference to green and blue rzsw
                    
                    # the soil moisture ratios
                    ratio_rzsw_g = safeDevide(rzsw_g, rzsw)
                    ratio_rzsw_cr = safeDevide(rzsw_cr, rzsw)
                    ratio_rzsw_ir = safeDevide(rzsw_ir, rzsw)

                    rzsw_dif = max(St_irr - rzsw,0.0)

                    rzsw_g = rzsw_g + rzsw_dif * ratio_rzsw_g
                    rzsw_cr = rzsw_cr + rzsw_dif * ratio_rzsw_cr
                    rzsw_ir = rzsw_ir + rzsw_dif * ratio_rzsw_ir


                    #updated root zone soil water - based on previous day depletion          
                    rzsw_g = max(rzsw_g + delta_rzswg,0.0)
                    rzsw_cr = max(rzsw_cr + delta_rzswcr, 0.0)
                    # since root zone soil moisture has to be consistent i.e, St = rzsw = rzsw_g + rzsw_cr + rzsw_ir 
                    # the root zone soil moisture from irrigation is used as a closing or obtained by sub rzsw_g and rzsw_cr
                    rzsw_ir = max(rzsw_ir + delta_rzswir, 0.0)
                    #rzsw_ir = St_irr - (rzsw_g + rzsw_cr)
                    rzsw = rzsw_g + rzsw_cr + rzsw_ir


                    # the soil moisture ratios
                    ratio_rzsw_g = safeDevide(rzsw_g, rzsw)
                    ratio_rzsw_cr = safeDevide(rzsw_cr, rzsw)
                    ratio_rzsw_ir = safeDevide(rzsw_ir, rzsw)
                    
                    #for using day of year as index
                    #t += 1


                    doy += 1

                    #print (J, doy)


                    
                    KC = daily_KC (J, Jdev, Jmid, Jlate, Jharv, Ldev, Llate, KCini, KCmid, KCend)


                    # calculation of the root depth. following pp. 279 (Annex 8) of FAO-56 

                    Zri_rf = rooting_depth(J, Jmid, Zrmin_rf, Zrmax_rf, KC, KCini, KCmid)
                    Zri_irr = rooting_depth(J, Jmid, Zrmin_irr, Zrmax_irr, KC, KCini, KCmid)
                    
                    
                    # the crop growing period of 2022 may go to 2023. Since the climate data is until 2022, 
                    # we need to handle the error and pass to next grid
                    
                    try:
                        

                        # Daily calculation of different parameters
                        PR = round(max(float(df_prcp.iloc[J].iloc[0]),0.0001),2)                # the precipitatin (mm/day) data from CRU has a factor of 10 so check if that factor was accounted for
                                                                                            #added max(PR,0), the data had -PR (close to 0) so to avoi
                        ETo = round(max(float(df_eto.iloc[J].iloc[0]),0.0001),2)               # reference evapotranspiration (mm/day) - got from FAO

                        # Continue with the rest of your code...
                    
                    
                    except IndexError as e:
                        # Handle the exception (you can print an error message or log it)
                        #print(f"Error processing grid {gridID}: {e}")
                        # Log error
                        logging.info(f"Error processing grid {gridID}: {e}")

                        # continue with the next grid or take other actions
                        continue

                                       

                    ETc = ETo * KC                        # crop evapo-transpiration (mm/day)
                    Pi = min((max((Pstd + 0.04*(5 - ETc)),0.1)),0.8)       # depletion fraction 

                    
                    ''' soil water content calculation'''
                    # rain-fed
                  
                    TAW_rf, RAW_rf, St_rf = calculate_soil_water (TAWC, Zri_rf, Pi, Dri_rf)

                    # irrigated
                    TAW_irr, RAW_irr, St_irr = calculate_soil_water (TAWC, Zri_irr, Pi, Dri_irr)
                    
                    # irrigated field but rain-fed (no irrigation water)
                    #TAW_irf, RAW_irf, St_irf = calculate_soil_water (TAWC, Zri_irr, Pi, Dri_irf)
                    
                    
                    if Dri_irr >= RAW_irr:          # irrigation is applied when Dri >= RAW
                        IRR = max(Dri_irr, 0.0)     #and in order to avoid deep percolation IRR <= Dri        

                    else:
                        IRR = 0

                    
                    # runoff (mm/day)
                    RO = runoff(PR, CN, cropi)
                    
                    #~~~~~~paddy rice  ~~~~~~~
                    ''' 
                    # adjust IRR for rice - the paddy rice field needs at least 50-150 mm ponded water
                    # source Steduto et al (2012) - pp 108
                    the irrigation has to fill depletion and 150 ponded water
                    IRR = Dri + 150
                    IRR_ad is additional water needed to keep the paddy
                    '''
                    
                    if cropi == 'Rice' and IRR_ad > 0:
                        IRR = IRR_ad
                    else:
                        IRR
                    
                    #print (round(Dri_irr,2), round(TAW_irr,2), round(paddy_ac,2), round(IRR_ad,0))
                    
                    paddy = TAW_irr+150
                    
                    paddy_ac = max(paddy - Dri_irr, 0) #max(PR + IRR - ETc - RO - DP_irr - Dri_irr,0.0)
                    
                    
                    IRR_ad = max(paddy - paddy_ac,0.0)   # additional water needed to keep the paddy
                    
                    #~~~~~~paddy rice  ~~~~~~~
                    

                    '''~~~~~~~~~~~~~~ calculation of Ks, actual evapotranspiration, soil water depletion ~~~~~~~~~~~~~'''
                    
                    #~~~~~~ rain-fed ~~~~~~~

                    KS_rf = KS_value (Dri_rf, RAW_rf, St_rf, Pi, TAW_rf)
                    
                    # deep percolation (mm/day) 
                    DP_rf = deep_percolation(Dri_rf, PR, RO, ETc, IRR=0)
                  
                    
                    ETa_rf, Dri_rf = daily_soil_water_balance(PR, ETc, KS_rf, RO, DP_rf, Dri_rf, TAW_rf, IRR=0)


                    #~~~~~~ irrigated ~~~~~~

                    KS_irr = KS_value (Dri_irr, RAW_irr, St_irr, Pi, TAW_irr)
                    
                    # deep percolation (mm/day)
                    DP_irr = deep_percolation(Dri_irr, PR, RO, ETc, IRR)

                    ETa_irr, Dri_irr = daily_soil_water_balance(PR, ETc, KS_irr, RO, DP_irr, Dri_irr, TAW_irr, IRR)
                    

                    # 1-2: Green soil waterbalace of 1st day
                    '''
                    The green-blue partitioning of the Drain and ET of this first day and the second day depends on the the green and blue soil water proportion of this day.
                    For each simulation day, runoff is partitioned into green and blue based on the corresponding amount of rain and runoff of the same day
                    '''
                    dp_g = DP_irr*ratio_rzsw_g
                    ro_g = RO*1.0 #safeDevide(PR, (PR+IRR))  # runoff 100% comes from rain
                    ETa_gn_ir = ETa_irr*ratio_rzsw_g


                    # 1-3-1: Blue-capillary soil waterbalance of 1st day
                    dp_cr = DP_irr*ratio_rzsw_cr
                    et_cr = ETa_irr*ratio_rzsw_cr


                    # 1-3-2: Blue-Irrigation soil waterbalance of 1st day  
                    dp_ir = DP_irr*ratio_rzsw_ir
                    ro_ir = 0.0 #RO*safeDevide(IRR, (PR+IRR))  #runoff comes only from rain. Net irr has not contribution
                    et_bl_ir = ETa_irr*ratio_rzsw_ir

                    # 3: Delta/change/ in soil water reservoires: green and blue soil water simimulations after the first day to the end of one season      
                    delta_rzswg = PR - dp_g - ro_g - ETa_gn_ir                
                    delta_rzswcr = CR - dp_cr - et_cr           
                    delta_rzswir = IRR - dp_ir - ro_ir - et_bl_ir
                    
     
                    '''~~~~~~~~~~~~~~ collecting daily values in array for aggregating at monthly level ~~~~~~~~~~~~~'''
                    #daily blue WF
                    ETa_bl = et_bl_ir + et_cr
                    
                   
                    # Ensure that result_array has enough space to accommodate the processed row
                    if current_index >= cwr_d.shape[0]:
                        # Resize result_array to accommodate more rows
                        new_size = current_index + 1
                        
                        #result_array_chunk = np.resize(result_array_chunk, (new_size, 365))
                        
                        cwr_d = np.resize(cwr_d, (new_size, nDates+1)); 
                        cwu_gn_rf_d = np.resize(cwu_gn_rf_d, (new_size, nDates+1));
                        cwu_gn_ir_d = np.resize(cwu_gn_ir_d, (new_size, nDates+1));
                        cwu_bl_d = np.resize(cwu_bl_d, (new_size, nDates+1));
                        IRReq_d = np.resize(IRReq_d, (new_size, nDates+1));
                        y_result = np.resize(y_result, (new_size, 3));
                        
                        

                    # Update the result_array with the processed row

                    cwr_d[current_index][doy] = ETc; cwu_gn_rf_d[current_index][doy] = ETa_rf; 
                    cwu_gn_ir_d[current_index][doy] = ETa_gn_ir; 
                    cwu_bl_d[current_index][doy] = ETa_bl; IRReq_d[current_index][doy] = IRR;
                    
                    # aggregation of the evapotranspiration over the growing period
                    # values are in mm per growing period
                    ETc_total += ETc
                    ETa_rf_total += ETa_rf
                    ETa_irr_total += ETa_irr
                    

            
                    #print(J, round(PR,2), round(IRR,2), round(rzsw_dif,2), round(ro_ir,2), round(dp_g,2),round(dp_ir,2), round(TAW_irr,2), round(St_irr,2), round(Dri_irr,2), round(delta_rzswg,2), round( delta_rzswir,2), round(rzsw,2), round(rzsw_g,2), round( rzsw_ir,2), round(ratio_rzsw_g,2), round( ratio_rzsw_ir,2), round(ETa_irr,2), round(ETa_bl, 2), round( ETa_gn_ir,2))
                # the grey water use in m3/ha

                CWU_gy = greyWU (N_ferti, Cmax = 0.01, LR = 0.1)

                # to be consisten with the other monthly ouput, which are in mm, 
                #we need to convert the annual grey WF into mm

                cwu_gy_mm = CWU_gy / 10.0

                # yield reduction and actual yield calculation
                # values in ton/ha

                Ya_rf = actual_yield(Ym, Ky, ETa_rf_total, ETc_total)
                Ya_irr = actual_yield(Ym, Ky, ETa_irr_total, ETc_total)


                # for the monthly files
                y_result[current_index][0]=cwu_gy_mm; y_result[current_index][1]=Ya_rf; y_result[current_index][2]=Ya_irr ;
                
                # Update the current index for the next row
                current_index += 1
            
            
                
            '''~~~~~~~~~~~~~~ concatenate the batch files and then aggregating daily values at monthly level ~~~~~~~~~~~~~'''

            
            # Trim result_array to the actual size (remove unused rows)
            cwr_d2 = cwr_d[:current_index, :]
            cwu_gn_rf_d2 = cwu_gn_rf_d[:current_index, :]
            cwu_gn_ir_d2 = cwu_gn_ir_d[:current_index, :]
            cwu_bl_d2 = cwu_bl_d[:current_index, :]
            IRReq_d2 = IRReq_d[:current_index, :]
            y_result2 = y_result[:current_index, :]
        
            
            #print (df_cwr.head())
            
        # Update the DataFrame based on the processed data
        df_cwr = pd.concat([df_cwr, pd.DataFrame(cwr_d2.round(2), columns=df_cwr.columns, index=gridIDs[:current_index])]);

        df_cwu_gn_rf = pd.concat([df_cwu_gn_rf, pd.DataFrame(cwu_gn_rf_d2.round(2), columns=df_cwu_gn_rf.columns, index=gridIDs[:current_index])]);
        df_cwu_gn_ir = pd.concat([df_cwu_gn_ir, pd.DataFrame(cwu_gn_ir_d2.round(2), columns=df_cwu_gn_ir.columns, index=gridIDs[:current_index])]);
        df_cwu_bl = pd.concat([df_cwu_bl, pd.DataFrame(cwu_bl_d2.round(2), columns=df_cwu_bl.columns, index=gridIDs[:current_index])]);
        df_IRReq = pd.concat([df_IRReq, pd.DataFrame(IRReq_d2.round(2), columns=df_IRReq.columns, index=gridIDs[:current_index])]);
        df_y = pd.concat([df_y, pd.DataFrame(y_result2.round(2), columns=df_y.columns, index=gridIDs[:current_index])]);

        #print (index_initial, old_current_index, current_index, gridIDs[:current_index])
        # Rename axes
        df_cwr = df_cwr.rename_axis('ID', axis='index')#.rename_axis('Day', axis='columns')
        df_cwu_gn_rf = df_cwu_gn_rf.rename_axis('ID', axis='index')#.rename_axis('Day', axis='columns')
        df_cwu_gn_ir = df_cwu_gn_ir.rename_axis('ID', axis='index')#.rename_axis('Day', axis='columns')
        df_cwu_bl = df_cwu_bl.rename_axis('ID', axis='index')#.rename_axis('Day', axis='columns')
        df_IRReq = df_IRReq.rename_axis('ID', axis='index')#.rename_axis('Day', axis='columns')
        df_y = df_y.rename_axis('ID', axis='index')#.rename_axis('Day', axis='columns')

            
        #print ("t-2", j, df_cwr.head())           
        #Transpose the df so dates are on the rows as index and the values on columns
        #this steps could be heavy on the memory of large number of grids are run over longer periods- will find simple approach
        df_cwr = df_cwr.transpose(); df_cwu_gn_rf = df_cwu_gn_rf.transpose();
        df_cwu_gn_ir = df_cwu_gn_ir.transpose();
        df_cwu_bl = df_cwu_bl.transpose(); df_IRReq = df_IRReq.transpose();

        #convert the date strings to datetime strings
        df_cwr.index = pd.to_datetime(df_cwr.index); df_cwu_gn_rf.index = pd.to_datetime(df_cwu_gn_rf.index);
        df_cwu_gn_ir.index = pd.to_datetime(df_cwu_gn_ir.index); 
        df_cwu_bl.index = pd.to_datetime(df_cwu_bl.index); df_IRReq.index = pd.to_datetime(df_IRReq.index);

        #aggregate at monthly time step
        df_cwr_m = df_cwr.resample('M').sum(); 
        df_cwu_gn_rf_m = df_cwu_gn_rf.resample('M').sum();
        df_cwu_gn_ir_m = df_cwu_gn_ir.resample('M').sum(); 
        df_cwu_bl_m = df_cwu_bl.resample('M').sum(); 
        df_IRReq_m = df_IRReq.resample('M').sum();


        #aggregate annually
        # Calculate the total cumulative sum over the crop growing period
        df_cwr_y = df_cwr.resample('Y').sum(); 
        df_cwu_gn_rf_y = df_cwu_gn_rf.resample('Y').sum();
        df_cwu_gn_ir_y = df_cwu_gn_ir.resample('Y').sum(); 
        df_cwu_bl_y = df_cwu_bl.resample('Y').sum(); 
        df_IRReq_y = df_IRReq.resample('Y').sum();
        
        #for the yield calculation
        df_cwr_total = df_cwr.sum().sum();
        df_cwu_gn_rf_total = df_cwu_gn_rf_y.sum().sum() ;
 


        # transpose back the df to have months on the column
        df_cwr_m = df_cwr_m.transpose(); df_cwu_gn_rf_m = df_cwu_gn_rf_m.transpose();
        df_cwu_gn_ir_m = df_cwu_gn_ir_m.transpose();
        df_cwu_bl_m = df_cwu_bl_m.transpose(); df_IRReq_m = df_IRReq_m.transpose();

        # transpose the annual value
        df_cwr_y = df_cwr_y.transpose(); df_cwu_gn_rf_y = df_cwu_gn_rf_y.transpose();
        df_cwu_gn_ir_y = df_cwu_gn_ir_y.transpose(); 
        df_cwu_bl_y = df_cwu_bl_y.transpose(); df_IRReq_y = df_IRReq_y.transpose();



        # #creat monthly data header replace the headers, which in y-m-d format 
        #with the proper column header
        #ml = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'];
        # Convert to DataFrame and then to datetime
        df = pd.DataFrame({'date': d_header})
        df['date'] = pd.to_datetime(df['date'])

        # Extract YY-MM format
        df['yy_mm'] = df['date'].dt.strftime('%Y%m'); 

        # Extract unique values
        yy_mm_header = df['yy_mm'].unique().tolist();
        ml = yy_mm_header

        cwr_hd = ['cwr' + s for s in ml]; 
        cwu_gn_rf_hd = ['cwu_gn_rf' + s for s in ml];
        cwu_gn_ir_hd = ['cwu_gn_ir' + s for s in ml]; 
        cwu_bl_hd = ['cwu_bl' + s for s in ml]; 
        IRReq_hd = ['IRReq' + s for s in ml];

        cwr_y_hd = ['cwr' + str(s) for s in (pYear, pYear+1)];
        cwu_gn_rf_y_hd = ['cwu_gn_rf' + str(s) for s in (pYear, pYear+1)];
        cwu_gn_ir_y_hd = ['cwu_gn_ir' + str(s) for s in (pYear, pYear+1)];
        cwu_bl_y_hd = ['cwu_bl_ann' + str(s) for s in (pYear, pYear+1)]; 
        IRReq_y_hd = ['IRReq_ann' + str(s) for s in (pYear, pYear+1)];

        
        #assign the header to the df
        df_cwr_m.columns = cwr_hd; 
        df_cwu_gn_rf_m.columns = cwu_gn_rf_hd; 
        df_cwu_gn_ir_m.columns = cwu_gn_ir_hd; 
        df_cwu_bl_m.columns = cwu_bl_hd; 
        df_IRReq_m.columns = IRReq_hd;

        df_cwr_y.columns = cwr_y_hd; 
        df_cwu_gn_rf_y.columns = cwu_gn_rf_y_hd; 
        df_cwu_gn_ir_y.columns = cwu_gn_ir_y_hd; 
        df_cwu_bl_y.columns = cwu_bl_y_hd; 
        df_IRReq_y.columns = IRReq_y_hd;
        
        # only for paddy rice
        df_et_p = pd.DataFrame(list(et_paddy), columns=['ET_paddy'], index = gridIDs).rename_axis('ID')
        
        # merge all monthly and annual value dataframes
        print ('I am here')
        if cropi == 'Rice':
            
            df_result_full = pd.concat([df_cwr_m, df_cwr_y, df_cwu_gn_rf_m, df_cwu_gn_rf_y, df_cwu_gn_ir_m, 
                                    df_cwu_gn_ir_y, df_cwu_bl_m, df_cwu_bl_y, df_IRReq_m, df_IRReq_y, df_y, df_et_p], axis=1);
        else:
            df_result_full = pd.concat([df_cwr_m, df_cwr_y, df_cwu_gn_rf_m, df_cwu_gn_rf_y, df_cwu_gn_ir_m, 
                                    df_cwu_gn_ir_y, df_cwu_bl_m, df_cwu_bl_y, df_IRReq_m, df_IRReq_y, df_y], axis=1);
        
        
        # output file to hold monthly and annual results
        ofile_all = os.path.join(ofpath, cropi + f'_all{hYear}.csv')
        #ofile_all = os.path.join(ofpath, cropi + '_all%s.csv'%hYear)

        #write to file
        df_result_full.to_csv(ofile_all)
        
        '''~~~~~~~~~~~~~~ monthly ~~~~~~~~~~~~~'''



    # Log successful completion
    logging.info("Batch processing completed successfully.")        
    
    print ('         completed running crop: %s file' % (cropi) )

#print ' The file = %s' % (cropFile1), CropPeriod, Zrmin_rf
print ("      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

print ("            %s\n" % localtimestrf())

# record end time
end = time.time()
 
# print the difference between start 
# and end time in milli. secs
print("The time of execution of above program is :",
round((end-start),0),  "s")
