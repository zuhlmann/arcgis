import arcpy
import copy

def deg_min_sec(dd):
    # https: // stackoverflow.com / questions / 2579535 / convert - dd - decimal - degrees - to - dms - degrees - minutes - seconds - in -python
    # mult = -1 if dd < 0 else 1
    mnt, sec = divmod(abs(dd) * 3600, 60)
    deg, mnt = divmod(mnt, 60)
    deg, mnt, sec = int(deg), int(mnt), int(sec)
    return deg, mnt, sec

def cogo_degrees_to_metes(feat_in):
    '''
    convert degrees from esri updgate cogo tool
    Args:
        feat_in:          feature class to update

    Returns:

    '''
    # Create Fields
    existing_fields = [f.name for f in arcpy.ListFields(feat_in)]
    fld_double = ['Degree', 'Minute', 'Second']
    for fld in fld_double:
        if fld not in existing_fields:
            arcpy.AddField_management(feat_in, fld, 'SHORT')
    if 'Mete_Str' not in existing_fields:
        arcpy.AddField_management(feat_in, r'Mete_Str', 'TEXT')

    with arcpy.da.UpdateCursor(feat_in, ['Direction','Mete_Str','Degree','Minute','Second']) as cursor:
        for row in cursor:
            d = row[0]
            if (d>0) and (d<90):
                # NE
                mete_num = copy.copy(d)
                deg, min, sec = deg_min_sec(mete_num)
                dms_str = '''N {}\N{DEGREE SIGN}{}'{}" E'''.format(deg,min,sec)
            elif (d > 90) and (d < 180):
                # SE
                mete_num = 180-d
                deg, min, sec = deg_min_sec(mete_num)
                dms_str = '''S {}\N{DEGREE SIGN}{}'{}" E'''.format(deg, min, sec)
            elif (d > 180) and (d < 270):
                # SW
                mete_num=abs(d-180)
                deg, min, sec = deg_min_sec(mete_num)
                dms_str = '''S {}\N{DEGREE SIGN}{}'{}" W'''.format(deg, min, sec)
            elif (d > 270) and (d < 360):
                # NW
                mete_num=360-d
                deg, min, sec = deg_min_sec(mete_num)
                dms_str = '''N {}\N{DEGREE SIGN}{}'{}" W'''.format(deg, min, sec)
            else:
                mete_num=int(d)
                # apply dict
                deg = copy.copy(mete_num)
                min=0
                sec=0
                dms_str_dict = {0:'NORTH',90:'EAST',180:'SOUTH',270:'WEST'}
                dms_str = dms_str_dict[mete_num]
            row[1]=dms_str
            row[2]=deg
            row[3]=min
            row[4]=sec
            cursor.updateRow(row)
        del cursor

