#指定気圧面の環境場の平均風向を計算する
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pygrib
import time
from datetime import datetime, timedelta
from dateutil import relativedelta
import sys
sys.path.append('/mnt/jet12/makoto/extract_senjo/python')
sys.path.append('/mnt/jet12/makoto/extract_senjo/senjo_wind/script')
from mypackage import exgrid, rrainfo, mycolor
import test_mod as mymod

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.path import Path
import numpy as np
from joblib import Parallel, delayed
from functools import lru_cache

@lru_cache(maxsize=None)
def openRRAwind_cached(ymdh, prs):
    u, v = mymod.openRRAwind(ymdh, prs)
     return u, v

#set out file
edgelen = 20 
region_mode = 2 
mean_time = 3
#hr = '0h'
hour_offset = +3
hPa = '900hPa'
hPa_num = 4 #0-16 1000hPa=0 975hPa=1 950hPa=2 925hPa=3 900hPa=4 875hPa=5 
            #850hPa=6 800hPa=7 750hPa=8 700hPa=9 600hPa=10 500hPa=11 
            #400hPa=12 300hPa=13 200hPa=14 100hPa=15 70hPa=16
outfile = f'/mnt/jet12/makoto/extract_senjo/senjo_wind/makoto_script/angle_data/angledata_{hour_offset}h_{hPa}.csv'

#read csv file
csvfile = '/mnt/jet12/makoto/extract_senjo/RRJ/csv/13reclassify2adddate/alldata_RRJ_1959-2023_reject_seashore_100km.csv'
df = pd.read_csv(csvfile)


rralat = rrainfo.lats()
rralon = rrainfo.lons()
rNX = rrainfo.shape()[1]
rNY = rrainfo.shape()[0]
exlat = exgrid.exlats()
exlon = exgrid.exlons()
NX = exlon.size
NY = exlat.size

results = []

#for i in range(0,len(df)):
#for i in range(0,2):    
def process_one_case(i):
    row = df.iloc[i]
    hrid = str(row["hrid"]) #ID
    dtst = row["dtst"] #開始時間
    dten = row["dten"] #終了時間
    nt  =  row["nt"]   #継続時間
    angle = row["angle"] #走向
    ratio = row["ration"] #アスペクト比
    majorlen = row["len"]
    minorlen = majorlen / ratio
    yearid = str(row["year"])

    print("dtst:", dtst)
#    print("dten:", dten)
#    print("nt:", nt)
    print("angle:", angle)
#    print("ratio:", ratio)
#    print("majorlen:", majorlen)
#    print("minorlen:", minorlen)

    #時間変換
    dt_dt = datetime.strptime(str(dtst), "%Y%m%d%H")
    dt_shifted = dt_dt + timedelta(hours=hour_offset)
    ymdh = dt_shifted.strftime("%Y%m%d%H") + "00"
 #   print(f"【環境場の計算時刻】dtst={dtst}  →  ymdh={ymdh} (offset={hour_offset}h)")

    # --- データ期間外なら除外 ---
    dt_min = datetime(1959, 1, 1, 0)
    dt_max = datetime(2023, 3, 31, 23)

    if not (dt_min <= dt_shifted <= dt_max):
        print(f"[除外] dtst={dtst} → {ymdh} (範囲外)", flush=True)
        return None   # 除外

    print(f"【環境場の計算時刻】dtst={dtst}  →  ymdh={ymdh} (offset={hour_offset}h)")     

    #read dat file
    datfile = '/mnt/jet12/makoto/extract_senjo/RRJ/dist/' + yearid + '0101-1231/heavyrain_ra03_5000m_100-80_040_' + hrid[2:] + '.dat'
    
    # 強雨域の形状
    hra = np.fromfile(datfile, dtype='>f').reshape(NY, NX)  # 個々の事例の位置、形状
    hra2 = np.nan_to_num(hra)                               # 欠損値をゼロに
    hra2[hra2!=0] = 1       

    #長方形領域の作成
    if region_mode == 0:
        clat1, clon1 = mymod.latlon_center(hra2, exlat, exlon)
        clat2, clon2 = mymod.gravity_center(hra2, exlat, exlon)
        clat = (clat1 + clat2) / 2
        clon = (clon1 + clon2) / 2
        
    elif region_mode == 1:
        clat, clon = mymod.latlon_center(hra2, exlat, exlon) # 線状降水帯の緯度経度中心
    elif region_mode == 2:
        clat, clon = mymod.gravity_center(hra2, exlat, exlon) # 線状降水帯の重心
    else:
        raise ValueError('region_mode must be 0 or 1 or 2.')

    print(clat, clon, majorlen, minorlen)
    xy1, xy2, xy3, xy4 = mymod.rotation(majorlen, minorlen, angle, edgelen)
    print(xy1, xy2, xy3, xy4)
    p1, p2, p3, p4 = mymod.toLatLon(xy1, xy2, xy3, xy4, clat, clon)
    print(p1, p2, p3, p4)

     poly = Path(np.array([
             [p1[0], p1[1]],
             [p2[0], p2[1]],
             [p3[0], p3[1]],
             [p4[0], p4[1]],
     ]))

     lon_flat = rralon.flatten()
     lat_flat = rralat.flatten()
     points = np.vstack([lon_flat, lat_flat]).T

     mask_flat = poly.contains_points(points)
     mask = mask_flat.reshape(rralon.shape)
    #領域設定のループを固定
#    yidx, xidx = mymod.loop_region(hra2, exlat, exlon, rralat, rralon)
#    gnum = yidx.size
#    glat = np.zeros(gnum)
#    glon = np.zeros(gnum)
#    for i in range(gnum):
#        glat[i] = rralat[yidx[i]][xidx[i]]
#        glon[i] = rralon[yidx[i]][xidx[i]]

    #長方形領域内の格子点を限定
#    contain = np.zeros(gnum)
#    st = time.time()
#    for i in range(gnum):
#        rralatlon = np.array([glon[i], glat[i]])#; print(rralatlon)
#        contain[i] = mymod.ingrid(rralatlon, p1, p2, p3, p4)
#    et = time.time()
#    print('elapsed time = {} sec.'.format(np.round(et-st, 2)))

#    xidx2 = xidx[contain > 0.5]
#    yidx2 = yidx[contain > 0.5]
#    gnum2 = yidx2.size
#    glat2 = np.zeros(gnum2)
#    glon2 = np.zeros(gnum2)
#    for i in range(gnum2):
#        glat2[i] = rralat[yidx2[i]][xidx2[i]]
#        glon2[i] = rralon[yidx2[i]][xidx2[i]]

    #環境場の風を計算
#    ymdh = f'{dtst}00'
#    print(ymdh)

#    u,v = mymod.openRRAwind(ymdh, hPa_num) #4 -> 900hPa
    u, v = openRRAwind_cached(ymdh, hPa_num)

    u_masked = np.where(mask, u, np.nan)
     v_masked = np.where(mask, v, np.nan)

    #領域内のみ描画（マスキング）
#    poly = Path(np.array([
#        [p1[0], p1[1]],
#        [p2[0], p2[1]],
#        [p3[0], p3[1]],
#        [p4[0], p4[1]],
#    ]))

    # ---- 全格子点を1次元化 ----
#    lon_flat = rralon.flatten()
#    lat_flat = rralat.flatten()
#    points = np.vstack([lon_flat, lat_flat]).T

    # ---- ポリゴン内判定 ----
#    mask_flat = poly.contains_points(points)
#    mask = mask_flat.reshape(rralon.shape)

    # ---- 内側のみの風 ----
    u_masked = np.where(mask, u, np.nan)
    v_masked = np.where(mask, v, np.nan)

    # ---- 平均風速・風向 ----
    u_mean = np.nanmean(u_masked)
    v_mean = np.nanmean(v_masked)

    # ---- 平均風向角（気象学的定義）----
    # 風向 = 風が吹いてくる方向
    dir_rad = np.arctan2(-u_mean, -v_mean)
#    wind_dir_deg = np.degrees(dir_rad)
    wind_dir = (np.degrees(dir_rad) + 360) % 360
    flow_dir = (wind_dir + 180) % 360   # 0～360°（流れの方向）

    #角度の差
    diff_angle = abs((flow_dir - angle + 180) % 360 - 180)

    print(f"平均風向（気象風向）: {flow_dir:.1f}°")
    print(f"平均風向: u={u_mean:.2f}, v={v_mean:.2f}")
    print(f"降水域の走行: angle={angle}")
    print(f"環境場と降水帯の走行の差: diff_angle={diff_angle}")


#save row

    return{
        "hrid": hrid,
        "dtst": dtst,
        "year": yearid,
        "pressure": hPa,
        "belt_angle": angle,
        "wind_from_angle": wind_dir,
        "wind_flow_angle": flow_dir,
        "angle_difference": diff_angle,
        "center_lat": clat,
        "center_lon": clon
    }

N = len(df)  
excluded = 0

#for result in Parallel(n_jobs=16, backend="loky")(
#    delayed(process_one_case)(i) for i in range(N)
#):
#    results.append(result)
#    print(f"[{len(results)}/{N}] done", flush=True)

raw_results = Parallel(n_jobs=16, backend="loky")(
    delayed(process_one_case)(i) for i in range(N)
)

results = []
for r in raw_results:
    if r is None:
        excluded += 1
    else:
        results.append(r)

print(f"===== 除外された事例数（時間シフト範囲外）: {excluded} 件 =====")
print(f"===== 使用された事例数: {len(results)} 件 =====")

#save csv
out_df = pd.DataFrame(results)
out_df.to_csv(outfile, index=False)

print(f"Saved → {outfile}")

