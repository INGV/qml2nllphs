##################################################################
##################################################################
##################################################################
##################################################################
### This python3 code contains the parsing part only for full qml
### to extrant any info e put it into a json object.
### The json object is only a facility.
### The key features are
### - Arguments allow to input file or eventid for webservice
### - Arguments have defaults
### - The extracted informations are packed into a jason object 
###   (originally designed by Ivano Carluccio) for any further use
###
### This part and the input arguments can be then completed by a
### output formatter to anything

### IMPORTING LIBRARIES
import os,argparse,subprocess,copy,pwd,socket,time
import sys
if sys.version_info[0] < 3:
   reload(sys)
   sys.setdefaultencoding('utf8')
import math
import decimal
import json
from xml.etree import ElementTree as ET
from six.moves import urllib
from datetime import datetime

## the imports of Obspy are all for version 1.1 and greater
from obspy import read, UTCDateTime
from obspy.core.event import Catalog, Event, Magnitude, Origin, Arrival, Pick
from obspy.core.event import ResourceIdentifier, CreationInfo, WaveformStreamID
try:
    from obspy.core.event import read_events
except:
    from obspy.core.event import readEvents as read_events

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

def parseArguments():
        parser=MyParser()
        parser.add_argument('--qmlin', help='Full path to qml event file')
        parser.add_argument('--eventid', help='INGV event id')
        parser.add_argument('--version', default='preferred',help="Agency coding origin version type (default: %(default)s)\n preferred,all, or an integer for known version numbers")
        parser.add_argument('--conf', default='./ws_agency_route.conf', help="needed with --eventid\n agency webservices routes list type (default: %(default)s)")
        parser.add_argument('--agency', default='ingv', help="needed with --eventid\n agency to query for (see routes list in .conf file) type (default: %(default)s)")
        if len(sys.argv) <= 1:
            parser.print_help()
            sys.exit(1)
        args=parser.parse_args()
        return args
# Nota: per aggiungere scelte fisse non modificabili usa choices=["known_version_number","preferred","all"]

try:
    import ConfigParser as cp
    sys.stderr.write("ConfigParser loaded\n")
except ImportError:
    sys.stderr.write("configparser loaded\n")
    import configparser as cp

# Build a dictionary from config file section
def get_config_dictionary(cfg, section):
    dict1 = {}
    options = cfg.options(section)
    for option in options:
        try:
            dict1[option] = cfg.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


# JSON ENCODER CLASS
class DataEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)

        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)

def json_data_structure():
    null="null"
    event = {"data": {"event": {
            "id_locator": 0,
            "type_event": null,
            "provenance_name": null,
            "provenance_instance": null,
            "provenance_softwarename": self_software,
            "provenance_username": null,
            "provenance_hostname": null,
            "provenance_description": url_to_description,
            "hypocenters": []}}}
    hypocenter = {
            "ot": null,
            "lat": null,
            "lon": null,
            "depth": null,
            "err_ot": null,
            "err_lat": null,
            "err_lon": null,
            "err_depth": null,
            "err_h": null,
            "err_z": null,
            "confidence_lev": null,
            "e0_az": null,
            "e0_dip": null, 
            "e0": null,
            "e1_az": null,
            "e1_dip": null,
            "e1": null,
            "e2_az": null,
            "e2_dip": null,
            "e2": null,
            "fix_depth": null,
            "min_distance": null,
            "max_distance": null,
            "azim_gap": null,
            "sec_azim_gap": null,
            "rms": null,
            "w_rms": null,
            "is_centroid": null,
            "nph": null,
            "nph_s": null,
            "nph_tot": null,
            "nph_fm": null,
            "quality": null,
            "type_hypocenter": "",
            "model": null,
            "loc_program": null,
            "provenance_name": null,
            "provenance_instance": null,
            "provenance_softwarename": self_software,
            "provenance_username": null,
            "provenance_hostname": null,
            "provenance_description": url_to_description,
            "magnitudes": [],
            "phases": []
        }
    magnitude = {
              "mag": null,
              "type_magnitude": null,
              "err": null,
              "mag_quality": null, #?
              "quality": null, #?
              "nsta_used": null,
              # From StationsMag or Amplitude
              "nsta": null,
              "ncha": null,
              # From Boh
              "min_dist": null,
              "azimut": null,
              "provenance_name": null,
              "provenance_instance": null,
              "provenance_softwarename": self_software,
              "provenance_username": null,
              "provenance_hostname": null,
              "provenance_description": url_to_description,
              "amplitudes": []
            }

    amplitude = {
                  "time1": null,
                  "amp1": null,
                  "period1": null,
                  "time2": null,
                  "amp2": null,
                  "period2": null,
                  "type_amplitude": null,
                  "mag": null,
                  "type_magnitude": null,
                  "scnl_net": null,
                  "scnl_sta": null,
                  "scnl_cha": null,
                  "scnl_loc": null, 
                  #"ep_distance": 694,
                  #"hyp_distance": 0, ??
                  # "azimut": 161, ??
                  # "err_mag": 0,
                  # "mag_correction": 0,
                  "is_used": null,
                  "provenance_name": null,
                  "provenance_instance": null,
                  "provenance_softwarename": self_software,
                  "provenance_username": null,
                  "provenance_hostname": null,
                  "provenance_description": url_to_description
                }

    phase = {
              "isc_code": null,
              "weight_picker": null,
              "arrival_time": null,
              "err_arrival_time": null,
              "firstmotion": null,
              "emersio": null,
              "pamp": null,
              "scnl_net": null,
              "scnl_sta": null,
              "scnl_cha": null,
              "scnl_loc": null,
              "ep_distance": null,
              "hyp_distance": null,
              "azimut": 140,
              "take_off": 119,
              "polarity_is_used": null,
              "arr_time_is_used": null,
              "residual": -0.12,
              "teo_travel_time": null,
              "weight_phase_a_priori": null,
              "weight_phase_localization": null,
              "std_error": null,
              "provenance_name": "INGV",
              "provenance_instance": "BULLETIN-INGV",
              "provenance_softwarename": self_software,
              "provenance_username": null,
              "provenance_hostname": null,
              "provenance_description": url_to_description
            }
    return event,hypocenter,magnitude,amplitude,phase
    
# Get QuakeML Full File from webservice
def getqml(event_id,bu,op):
    urltext=bu + "query?eventid=" + str(event_id) + op
    #urltext=bu + "query?eventid=" + str(event_id) + "&includeallmagnitudes=true&includeallorigins=true&includearrivals=true&includeallstationsmagnitudes=true"
    try:
        req = urllib.request.Request(url=urltext)
        try:
            res = urllib.request.urlopen(req)
        except Exception as e:
            print("Query in urlopen")
            if sys.version_info[0] >= 3:
               print(e.read()) 
            else:
               print(str(e))
            sys.exit(1)
    except Exception as e:
        print("Query in Request")
        if sys.version_info[0] >= 3:
           print(e.read()) 
        else:
           print(str(e))
        sys.exit(1)
    return res.read(),urltext

#################### END OF QML PARSER COMMON PART ###########################
###### FROM HERE ADD ON PURPOSE OUTPUT FORMATTERS ############################

###### Functions to format for NonLinLoc ##########
def convert_sispick_quality(q):
    qf=float(q)
    if qf == 0.1:
        w='0'
    elif qf == 0.3:
        w='1'
    elif qf == 0.6:
        w='2'
    elif qf == 1.0:
        w='3'
    elif qf == 3.0:
        w='4'
    elif qf == 10.0:
        w='8'
    return w

def convert_phase_onset(p):
    if p == 'undecidable':
        po='?'
    elif p == 'emergent' or p == 'Emergent' or p == 'E' or p == 'e':
        po='E'
    elif p == 'impulsive' or p == 'Impulsive' or p == 'I' or p == 'i':
        po='I'
    else:
        po='?'
    return po

def convert_first_motion(p):
    if p == 'undecidable' or p == 'None':
        po='?'
    elif p == '' or p == 'u' or p == 'c' or p == 'C' or p == 'U' or p == 'positive':
        po='U'
    elif p == '-' or p == 'd' or p == 'e' or p == 'E' or p == 'D' or p == 'negative':
        po='D'
    else:
        po='?'
    return po

def qml2location(o,la,la_e,lo,lo_e,de,de_e,q,m_e,r_e):
    o_time=str("{0:0>4}".format(int(OT.year)))+" "+\
           str("{0:0>2}".format(int(OT.month)))+" "+\
           str("{0:0>2}".format(int(OT.day)))+"  "+\
           str("{0:0>2}".format(int(OT.hour)))+" "+\
           str("{0:0>2}".format(int(OT.minute)))+" "+\
           str("{0:.4f}".format(float(OT.second)+float(OT.microsecond)/1000000.)).zfill(7)
    gap=q['azimuthal_gap']
    rms=q['standard_error']
    mindist=float(q['minimum_distance'])*100.0
    maxdist=float(q['maximum_distance'])*100.0
    nphs=q['used_phase_count']
    r_e=r_e.replace(' ','_')
    wri_str="# INGVWS  OT " + str(o_time) + " Lat " + str(la) + " Lat_Err " + str(la_e) + " Long " + str(lo) + " Lon_Err " + str(lo_e) + " Depth " + str(de) + " Dep_Err " + str(de_e) + \
            "  QUALITY  GAP " + str(gap) + " RMS " + str(rms) + " NPHS " + str(nphs) + " MinDist " + str(mindist) + " MaxDist " + str(maxdist) + " Magnitude " + str(m_e) + " Region " + str(r_e)
    return wri_str

##############################################################################
################## MAIN ####################
args=parseArguments()

# Getting this code name
self_software=sys.argv[0]

# If a qml input file is given, file_qml is the full or relative path_to_file
if args.qmlin:
   qml_ans=args.qmlin
   url_to_description = "File converted from qml file " + args.qmlin.split(os.sep)[-1]

# This is the version that will be retrieved from the qml
orig_ver=args.version

# If qmlin is not given and an eventid is given, file_qml is the answer from a query and the configuration file is needed
if args.eventid:
   eid=args.eventid
   # Now loading the configuration file
   if os.path.exists(args.conf) and os.path.getsize(args.conf) > 0:
      paramfile=args.conf
   else:
      print("Config file " + args.conf + " not existing or empty")
      sys.exit(2)
   confObj = cp.ConfigParser()
   confObj.read(paramfile)
   # Metadata configuration
   agency_name = args.agency.lower()
   try:
       ws_route = get_config_dictionary(confObj, agency_name)
   except Exception as e:
       if sys.version_info[0] >= 3:
          print(e) 
       else:
          print(str(e))
       sys.exit(1)
   # Now requesting the qml file from the webservice
   qml_ans, url_to_description = getqml(eid,ws_route['base_url'],ws_route['in_options'])
   if not qml_ans or len(qml_ans) == 0:
      print("Void answer with no error handling by the webservice")
      sys.exit(1)

if not args.qmlin and not args.eventid:
       print("Either --qmlin or --eventid are needed")
       sys.exit()

# Now reading in qml to obspy catalog
try:
    cat = read_events(qml_ans)
except Exception as e:
    if sys.version_info[0] >= 3:
       print(e) 
    else:
       print(str(e))
       print("Error reading cat")
    sys.exit(1)
###################################
# Lista delle chiavi del full qml #
###################################
# focal_mechanisms ----------< Ok
# origins ----------< Ok
# picks ----------< Ok
# magnitudes ----------< Ok
# station_magnitudes ----------< Ok
# amplitudes ----------< Ok

# resource_id ----------< Ok
# creation_info ----------< Ok
# event_descriptions ----------< Ok
# event_type ----------< Ok
# event_type_certainty ----------< Ok
# comments ----------< Ok
# _format ----------< Ok

# ----------------------------- #
# i seguenti non li parso       #
# preferred_magnitude_id        #
# preferred_focal_mechanism_id  #
# preferred_origin_id           #
# ----------------------------- #

event,hypocenter,magnitude,amplitude,phase = json_data_structure()
#print(event,hypocenter,magnitude,amplitude,phase)
EARTH_RADIUS=6371 # Defined after eventdb setup (valentino.lauciani@ingv.it)
DEGREE_TO_KM=111.1949 # Defined after eventdb setup (valentino.lauciani@ingv.it)


## Building Header for commented line descibing the content
header="#Station_name Instrument Component P_phase_onset Phase_descriptor First_motion Date Hour_minute Seconds Err_type Err Err_mag Coda_duration Amplitude"
found=False
for event in cat:
    evdict=dict(event)
    #for k, v in evdict.items():
    #    print(k, v)
    pref_mag=evdict['magnitudes'][0]['mag']
    if sys.version_info[0] <= 2:
       region=evdict['event_descriptions'][0].text.encode('utf-8')
    elif sys.version_info[0] >= 3:
       region=evdict['event_descriptions'][0].text
    pref_or_id=str(evdict['preferred_origin_id']).split('=')[-1]
    for origin in evdict['origins']:
        or_id=str(origin['resource_id']).split('=')[-1]
        if origin['creation_info']['version'] == str(orig_ver) or (orig_ver == 'preferred' and or_id == pref_or_id):
            #for k, v in origin.items():
            #    print(k, v)
            found=True
            or_ver=origin['creation_info']['version']
            fileout_name_phase="." + os.sep + str(evdict['resource_id']).split('=')[-1] + "_" + or_id + "_mag_" + str(pref_mag) + "_" + or_ver + ".phsnll"
            # Location Data
            OT=origin['time']
            ola=origin['latitude']
            olo=origin['longitude']
            ode=str(float(origin['depth'])/1000.)
            try:
                ola_u=origin['latitude_errors']['uncertainty']
            except:
                ola_u=False
            try:
                olo_u=origin['longitude_errors']['uncertainty']
            except:
                olo_u=False
            try:
                ode_u=str(float(origin['depth_errors']['uncertainty'])/1000.)
            except:
                ode_u=False
            qual=origin['quality']

            # Writing a first additional commented line to keep the event location of the extracted version
            print(qml2location(OT,ola,ola_u,olo,olo_u,ode,ode_u,qual,pref_mag,region))
            print(header)
            for arrival in origin['arrivals']:
                pickid_str=arrival['pick_id']
                pickid_num=str(arrival['pick_id']).split('=')[-1]
                # Elements to get fot output: names are set accordingly to NLL format phase file
                Phase_descriptor=str(arrival['phase'])
                for pick in evdict['picks']:
                    if pick['resource_id'] == pickid_str:
                        # Uncomment if you want to look at all the real names
                        #for k, v in pick.items():
                        #        print(k, v)
                        Station_Name=pick['waveform_id']['station_code']
                        Instrument='?'
                        Component = '?' if pick['waveform_id']['channel_code'] == "" else pick['waveform_id']['channel_code']
                        # network and location codes are additional not used in standard NLL. In this version the network code is written in the usually empty Instrument
                        Network_Code=pick['waveform_id']['network_code']
                        Location_Code=pick['waveform_id']['location_code']
                        DT=pick['time']
                        Date=str("{0:0>4}".format(int(DT.year)))+str("{0:0>2}".format(int(DT.month)))+str("{0:0>2}".format(int(DT.day)))
                        HhMm=str("{0:0>2}".format(int(DT.hour)))+str("{0:0>2}".format(int(DT.minute)))
                        Seco=str("{0:.4f}".format(float(DT.second)+float(DT.microsecond)/1000000.)).zfill(7)
                        Err_type='QUAL'
                        Err=convert_sispick_quality(pick['time_errors']['uncertainty'])
                        Phase_onset=convert_phase_onset(pick['onset'])
                        First_motion=convert_first_motion(pick['polarity'])
                        minus1=-1
                        Err_mag="{:.2E}".format(minus1)
                        Coda_dur="{:.2E}".format(minus1)
                        Amplitude="{:.2E}".format(minus1)
                        Instrument=Network_Code # Instrument is here 
                        phase=Station_Name + " " + Instrument + " " + Component + " " + Phase_onset + " " + Phase_descriptor + " " + First_motion + " " + Date + " " + HhMm + " " + Seco + " " + Err_type + " " + Err + " " + Err_mag + " " + Coda_dur + " " + Amplitude
                        # Writing the phases line here in NLL format
                        print(phase)
            print("")
if not found:
   sys.stderr.write("Chosen version doesnt match any origin id\n")
   sys.exit(202) # Il codice 202 e' stato scelto per identificare il caso in cui tutto sia corretto ma non ci sia alcuna versione come quella scelta
