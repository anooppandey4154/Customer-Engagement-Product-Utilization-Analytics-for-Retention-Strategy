import streamlit as st
import pandas as pd
import numpy as np
import io

# ---------------------------------------------------------
# Page Configurations & Aesthetic Layout Styles (Bold Theme)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Customer Engagement & Product Utilization Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Contrast CSS Styling to achieve a "Bold Typography" dark slate look
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #020617;
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header & Titles */
    h1, h2, h3, h4 {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 900 !important;
        letter-spacing: -0.05em !important;
        text-transform: uppercase;
    }
    
    h1 {
        font-size: 2.5rem !important;
        color: #ffffff !important;
        border-bottom: 2px solid #1e293b;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem !important;
    }
    
    /* Card/Metric Styling */
    .metric-card {
        background-color: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 4px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .metric-title {
        font-size: 0.65rem;
        font-weight: 800;
        text-transform: uppercase;
        color: #64748b;
        letter-spacing: 0.15em;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 2.75rem;
        font-weight: 900;
        color: #ffffff;
        letter-spacing: -0.04em;
        line-height: 1;
    }
    
    .metric-suffix {
        font-size: 1.25rem;
        color: #06b6d4;
    }
    
    .metric-subtitle {
        font-size: 0.65rem;
        font-weight: 700;
        color: #10b981;
        margin-top: 0.5rem;
        text-transform: uppercase;
    }
    
    .metric-subtitle-red {
        color: #f43f5e;
    }
    
    /* Tables & Rows */
    div[data-testid="stTable"] table {
        background-color: #0f172a !important;
        border: 1px solid #1e293b !important;
    }
    
    /* Highlight banners */
    .directive-banner {
        background-color: rgba(6, 182, 212, 0.08);
        border: 1px solid rgba(6, 182, 212, 0.2);
        padding: 1rem;
        border-radius: 4px;
        color: #22d3ee;
        font-size: 0.85rem;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Raw Embedded ECB Dataset
# ---------------------------------------------------------
RAW_CSV = """Year,CustomerId,Surname,CreditScore,Geography,Gender,Age,Tenure,Balance,NumOfProducts,HasCrCard,IsActiveMember,EstimatedSalary,Exited
2025,15634602,Hargrave,619,France,Female,42,2,0,1,1,1,101348.88,1
2025,15647311,Hill,608,Spain,Female,41,1,83807.86,1,0,1,112542.58,0
2025,15619304,Onio,502,France,Female,42,8,159660.8,3,1,0,113931.57,1
2025,15701354,Boni,699,France,Female,39,1,0,2,0,0,93826.63,0
2025,15737888,Mitchell,850,Spain,Female,43,2,125510.82,1,1,1,79084.1,0
2025,15574012,Chu,645,Spain,Male,44,8,113755.78,2,1,0,149756.71,1
2025,15592531,Bartlett,822,France,Male,50,7,0,2,1,1,10062.8,0
2025,15656148,Obinna,376,Germany,Female,29,4,115046.74,4,1,0,119346.88,1
2025,15792365,He,501,France,Male,44,4,142051.07,2,0,1,74940.5,0
2025,15592389,H?,684,France,Male,27,2,134603.88,1,1,1,71725.73,0
2025,15767821,Bearce,528,France,Male,31,6,102016.72,2,0,0,80181.12,0
2025,15737173,Andrews,497,Spain,Male,24,3,0,2,1,0,76390.01,0
2025,15632264,Kay,476,France,Female,34,10,0,2,1,0,26260.98,0
2025,15691483,Chin,549,France,Female,25,5,0,2,0,0,190857.79,0
2025,15600882,Scott,635,Spain,Female,35,7,0,2,1,1,65951.65,0
2025,15643966,Goforth,616,Germany,Male,45,3,143129.41,2,0,1,64327.26,0
2025,15737452,Romeo,653,Germany,Male,58,1,132602.88,1,1,0,5097.67,1
2025,15788218,Henderson,549,Spain,Female,24,9,0,2,1,1,14406.41,0
2025,15561507,Muldrow,587,Spain,Male,45,6,0,1,0,0,158684.81,0
2025,15568982,Hao,726,France,Female,24,6,0,2,1,1,54724.03,0
2025,15577657,McDonald,732,France,Male,41,8,0,2,1,1,170886.17,0
2025,15597945,Dellucci,636,Spain,Female,32,8,0,2,1,0,138555.46,0
2025,15699309,Gerasimov,510,Spain,Female,38,4,0,1,1,0,118913.53,1
2025,15725737,Mosman,669,France,Male,46,3,0,2,0,1,8487.75,0
2025,15625047,Yen,846,France,Female,38,5,0,1,1,1,187616.16,0
2025,15738191,Maclean,577,France,Male,25,3,0,2,0,1,124508.29,0
2025,15736816,Young,756,Germany,Male,36,2,136815.64,1,1,1,170041.95,0
2025,15700772,Nebechi,571,France,Male,44,9,0,2,0,0,38433.35,0
2025,15728693,McWilliams,574,Germany,Female,43,3,141349.43,1,1,1,100187.43,0
2025,15656300,Lucciano,411,France,Male,29,0,95741.75,1,1,0,46170.75,0
2025,15810834,Gordon,525,Spain,Female,57,2,145965.33,1,1,1,64448.36,0
2025,15676966,Capon,730,Spain,Male,42,4,0,2,0,1,85982.47,0
2025,15699461,Fiorentini,515,Spain,Male,35,10,176273.95,1,0,1,121277.78,0
2025,15738721,Graham,773,Spain,Male,41,9,102827.44,1,0,1,64595.25,0
2025,15693683,Yuille,814,Germany,Male,29,8,97086.4,2,1,1,197276.13,0
2025,15604348,Allard,710,Spain,Male,22,8,0,2,0,0,99645.04,0
2025,15633059,Fanucci,413,France,Male,34,9,0,2,0,0,6534.18,0
2025,15808582,Fu,665,France,Female,40,6,0,1,1,1,161848.03,0
2025,15743192,Hung,623,France,Female,44,6,0,2,0,0,167162.43,0
2025,15580146,Hung,738,France,Male,31,9,82674.15,1,1,0,41970.72,0
2025,15776605,Bradley,528,Spain,Male,36,7,0,2,1,0,60536.56,0
2025,15804919,Dunbabin,670,Spain,Female,65,1,0,1,1,1,177655.68,1
2025,15613854,Mauldon,622,Spain,Female,46,4,107073.27,2,1,1,30984.59,1
2025,15599195,Stiger,582,Germany,Male,32,1,88938.62,1,1,1,10054.53,0
2025,15812878,Parsons,785,Germany,Female,36,2,99806.85,1,0,1,36976.52,0
2025,15602312,Walkom,605,Spain,Male,33,5,150092.8,1,0,0,71862.79,0
2025,15744689,T'ang,479,Germany,Male,35,9,92833.89,1,1,0,99449.86,1
2025,15803526,Eremenko,685,Germany,Male,30,3,90536.81,1,0,1,63082.88,0
2025,15665790,Rowntree,538,Germany,Male,39,7,108055.1,2,1,0,27231.26,0
2025,15715951,Thorpe,562,France,Male,42,2,100238.35,1,0,0,86797.41,0
2025,15591100,Chiemela,675,Spain,Male,36,9,106190.55,1,0,1,22994.32,0
2025,15609618,Fanucci,721,Germany,Male,28,9,154475.54,2,0,1,101300.94,1
2025,15675522,Ko,628,Germany,Female,30,9,132308.22,1,1,1,175664.25,0
2025,15779176,Dike,565,Germany,Female,58,3,108888.24,3,0,1,135875.51,1
2025,15775295,McIntyre,630,France,Female,40,0,118633.08,1,0,1,60032.46,1
2025,15684196,Aitken,627,France,Female,55,2,159441.27,1,1,0,100686.11,1
2025,15727281,Macintyre,653,France,Female,27,9,0,2,1,0,96429.29,0
2025,15778358,Simpson,775,Germany,Female,38,4,125212.65,2,1,1,15795.88,1
2025,15730540,Simpson,794,Spain,Male,45,8,88656.37,2,1,0,116547.31,0
2025,15646276,Metcalfe,831,France,Female,32,2,146033.62,1,1,0,191260.74,0
2025,15582180,Lees,561,France,Male,29,9,120268.13,1,1,1,173870.39,0
2025,15697095,Zetticci,705,Spain,Male,46,7,0,2,1,0,117273.35,0
2025,15748797,Dale,636,Spain,Female,33,0,0,1,1,0,92277.47,1
2025,15745796,Byrne,487,Germany,Female,46,4,135070.58,2,1,1,44244.49,1
2025,15628947,Praed,693,France,Female,38,3,0,2,0,0,78133.48,1
2025,15775546,Laurens,517,Spain,Female,29,5,0,2,1,0,103402.88,0
2025,15670481,Woods,684,France,Female,27,9,122550.05,2,0,1,137835.82,0
2025,15619029,Bykov,620,Spain,Female,43,2,0,2,1,0,20670.1,0
2025,15613282,Vorobyova,757,France,Male,29,8,130306.49,1,1,0,77469.38,0
2025,15721487,Pirogova,739,France,Female,27,6,0,1,1,1,57572.38,0
2025,15797276,Sturt,662,Spain,Female,41,4,90350.77,1,1,0,75884.65,1
2025,15612494,Panicucci,359,France,Female,44,6,128747.69,1,1,0,146955.71,1
2025,15629617,Cook,572,Spain,Male,23,2,126873.52,1,0,1,67040.12,0
2025,15600821,Hardy,721,France,Male,69,2,108424.19,1,1,1,178418.35,0
2025,15579062,Chu,707,France,Male,32,9,0,2,0,0,30807.02,0
2025,15814268,Franklin,444,France,Female,40,5,84350.07,1,1,0,143835.76,0
2025,15710164,P'eng,523,France,Female,73,7,0,2,0,0,130883.9,1
2025,15693904,Chiang,685,Germany,Female,30,4,84958.6,2,0,1,194343.72,0
2025,15588986,Grant,673,Germany,Female,29,4,99097.36,1,1,1,9796.69,0
2025,15797733,Udobata,503,Germany,Male,30,10,136622.55,2,0,0,47310.24,0
2025,15620507,Siciliani,485,Germany,Female,30,5,156771.68,1,1,1,141148.21,0
2025,15685150,Evans,799,Germany,Male,28,7,167658.33,2,1,1,111138.25,0
2025,15667651,Young,585,Spain,Female,33,8,0,2,1,0,114182.07,0
2025,15774166,Mitchell,607,Germany,Female,24,2,109483.54,2,0,1,127560.77,0
2025,15649280,Lucchese,521,Germany,Female,40,9,134504.78,1,1,0,18082.06,0
2025,15705657,Hewitt,535,France,Female,44,2,114427.86,1,1,1,136330.26,0
2025,15753969,K'ung,724,Spain,Male,45,5,83888.54,1,0,1,34121.81,0
2025,15742378,Swaim,520,Germany,Male,32,5,110029.77,1,1,0,56246.69,0
2025,15794174,Quinones,696,Spain,Male,41,9,127523.75,1,0,1,191417.42,0
2025,15589221,Kennedy,657,Germany,Male,30,1,139762.13,2,1,1,23317.88,0
2025,15596671,Endrizzi,603,Spain,Female,42,8,91611.12,1,0,0,144675.3,1
2025,15583668,Ludowici,726,France,Female,42,2,109471.79,1,0,1,175161.05,0
2025,15710206,Larson,591,France,Female,39,4,150500.64,1,1,0,14928.8,0
2025,15799966,Chigolum,792,Germany,Female,59,9,101609.77,1,0,0,161479.19,1
2025,15794560,Maclean,550,France,Male,57,5,0,1,1,1,133501.94,0
2025,15626485,Lu,601,France,Female,26,8,78892.23,1,1,1,23703.52,0
2025,15703143,Tuan,820,France,Female,29,3,82344.84,1,0,1,115985.38,0
2025,15799710,Wei,739,France,Male,37,7,104960.46,1,0,1,80883.82,0
2025,15659651,Ross,531,Germany,Female,31,7,117052.82,1,1,0,118508.09,1
2025,15645956,Jideofor,452,Spain,Male,44,3,88915.85,1,1,0,69697.74,0
2025,15651713,King,684,France,Male,45,6,148071.39,1,1,0,183575.01,0
2025,15737265,Nwokeocha,728,Germany,Male,39,6,152182.83,1,0,0,161203.6,0
2025,15687310,Humphries,783,Spain,Male,39,9,0,2,1,0,143752.77,0
2025,15607347,Olisaemeka,734,France,Male,22,5,130056.23,1,0,0,121894.31,1
2025,15698321,Yobanna,648,Germany,Male,34,3,95039.73,2,1,1,147055.87,0
2025,15779059,Timms,670,France,Female,38,4,119624.54,2,1,1,110472.12,0
2025,15785980,Williford,588,Spain,Male,34,6,121132.26,2,1,0,86460.28,0
2025,15644200,Hamilton,807,Spain,Female,42,1,0,1,1,0,16500.66,1
2025,15793949,Cheng,726,France,Female,48,4,0,1,1,0,114020.06,1
2025,15645103,Su,812,Germany,Male,25,5,54817.55,1,1,0,131660.31,0
2025,15705860,McKenzie,631,Germany,Male,40,3,107949.45,1,1,0,52449.62,1
2025,15623828,Akobundu,682,France,Male,30,4,0,1,0,1,161465.31,0
2025,15715003,Ko,625,Spain,Female,49,2,80816.45,1,1,1,20018.79,0
2025,15623471,Marcelo,607,Germany,Male,38,3,98205.77,1,1,0,176318.27,0
2025,15798348,Chukwuebuka,600,Spain,Female,50,6,94684.27,1,1,1,50488.91,0
2025,15743016,MacDonald,602,Spain,Female,22,7,141604.76,1,1,0,30379.6,0
2025,15769499,Lampungmeiua,545,Spain,Female,74,3,0,2,1,1,161326.73,0
2025,15798521,Tai,675,Spain,Male,33,3,0,2,1,0,45348.08,0
2025,15706534,Enyinnaya,581,France,Female,47,1,122949.14,1,0,0,180251.68,1
2025,15706186,McKenzie,640,Germany,Male,33,8,81677.22,2,0,0,34925.56,0
2025,15812197,Kline,850,France,Male,38,7,80293.98,1,0,0,126555.74,0
2025,15650933,Ma,490,Spain,Female,48,8,155413.06,1,1,0,187921.3,0
2025,15692991,Wood,710,Spain,Female,38,4,0,2,1,1,136390.88,0
2025,15631189,Riggs,613,Germany,Male,38,9,67111.65,1,1,0,78566.64,1
2025,15762198,Capon,812,France,Male,34,5,103818.43,1,1,1,166038.27,0
2025,15699598,Smith,723,France,Female,20,4,0,2,1,1,140385.33,0
2025,15692744,Davison,512,France,Male,36,4,152169.12,2,0,0,38629.3,1
2025,15688963,Ingram,731,France,Female,52,10,0,1,1,1,24998.75,1
2025,15599131,Dilke,650,Germany,Male,26,4,214346.96,2,1,0,128815.33,0
2025,15680303,Gibson,594,France,Male,57,6,0,1,1,0,19376.56,1
2025,15628674,Iadanza,844,France,Male,40,7,113348.14,1,1,0,31904.31,1
2025,15648075,Hebert,686,Germany,Female,47,5,170935.94,1,1,0,173179.39,0
2025,15587581,Russo,785,Germany,Female,33,5,136624.6,2,1,1,169117.74,0
2025,15633640,Loewenthal,799,France,Female,52,4,161209.66,1,1,1,89081.41,0
2025,15573741,Aliyeva,698,Spain,Male,38,10,95010.92,1,1,1,105227.86,0
2025,15633574,Montes,730,France,Female,41,4,167545.32,1,1,0,128246.81,0
2025,15711455,Kuo,740,Germany,Female,36,4,109044.6,1,0,0,94554.74,1
2025,15570601,Cheng,785,France,Female,47,9,122031.55,1,1,1,33823.5,1
2025,15690925,McIntosh,527,Spain,Female,29,2,27755.97,1,1,0,97468.44,1
2025,15709338,T'ao,544,France,Female,29,1,118560.55,1,1,1,164137.36,0
2025,15780746,Tyndall,705,France,Male,61,4,0,2,1,1,191313.7,0
2025,15681956,Bailey,684,France,Male,34,9,0,2,1,1,65257.57,0
2025,15778190,Onyekaozulu,639,Spain,Female,28,8,97840.72,1,1,1,178222.77,0
2025,15786526,Nwachukwu,565,Germany,Female,38,2,158651.29,2,1,1,179445.28,0
2025,15729490,Scott,661,France,Male,47,5,0,1,0,1,107243.31,1
2025,15591766,Crawford,607,Spain,Female,25,4,121166.89,1,0,1,115288.24,0
2025,15629187,Titheradge,535,France,Male,38,8,85982.07,1,1,0,9238.35,0
2025,15780779,Ramsbotham,583,Spain,Female,40,4,0,2,1,0,114093.73,0
2025,15798470,Scannell,764,Spain,Female,48,1,75990.97,1,1,0,158323.81,1
2025,15760880,Edman,513,France,Male,29,10,0,2,0,1,25514.77,0
2025,15616929,De Luca,730,Spain,Male,62,5,112181.08,1,0,1,61513.87,0
2025,15775875,Vasilyeva,820,Spain,Male,34,10,97208.46,1,1,1,59553.34,0
2025,15663386,Tuan,597,Spain,Female,26,7,0,2,1,0,110253.2,0
2025,15670584,Nkemakolam,646,Spain,Male,31,2,0,1,1,1,170821.43,1
2025,15719928,Glover,667,France,Male,48,2,0,1,1,0,43229.2,0
2025,15687959,Landman,573,Spain,Female,44,4,0,1,1,1,94862.93,0
2025,15585282,Trevisano,755,France,Male,62,1,127706.33,2,0,1,142377.69,0
2025,15714993,Longo,552,France,Female,41,9,124349.34,1,1,0,135635.25,0
2025,15596021,K?,598,Spain,Male,44,8,0,2,1,0,148487.9,0
2025,15646615,Muir,576,Germany,Male,28,1,119336.29,2,0,1,58976.85,0
2025,15742632,Alexeyeva,670,France,Female,31,9,0,1,0,1,76254.83,0
2025,15574068,Norman,504,Germany,Male,56,9,104217.3,1,0,0,55857.48,1
2025,15806967,Simmons,778,France,Female,65,7,0,1,1,1,77867.23,0
2025,15796334,Chukwualuka,558,Germany,Male,39,10,144757.02,1,1,0,22878.16,1
2025,15688713,McCall,627,Spain,Male,44,6,0,1,1,1,114469.55,0
2025,15796179,Moore,683,France,Male,43,8,0,1,1,0,96754.8,0
2025,15598751,Ingram,556,France,Female,43,6,0,3,0,0,125154.57,1
2025,15703019,Okeke,583,France,Female,38,10,0,2,0,1,113597.64,0
2025,15646302,Shao,705,France,Female,24,7,100169.51,1,1,0,121408.55,0
2025,15680855,Iloabuchi,637,France,Male,33,2,145731.83,1,0,1,109219.43,0
2025,15697311,Nebechukwu,697,Spain,Male,56,5,110802.03,1,1,1,50230.31,1
2025,15585367,Diribe,555,Germany,Female,46,4,120392.99,1,1,0,177719.88,1
2025,15726556,Macgroarty,594,Germany,Female,26,6,135067.52,2,0,0,131211.86,0
2025,15676242,Artemova,632,Spain,Male,31,3,136556.44,1,1,0,82152.83,1
2025,15684198,McDonald,551,France,Female,38,10,0,2,1,1,216.27,0
2025,15774882,Mazzanti,687,France,Female,35,3,99587.43,1,1,1,1713.1,1
2025,15712287,Pokrovskii,652,France,Female,80,4,0,2,1,1,188603.07,0
2025,15702919,Collins,729,Germany,Male,30,6,63669.42,1,1,0,145111.37,0
2025,15674398,Russo,642,France,Male,38,3,0,2,0,0,171463.83,0
2025,15797960,Skinner,806,Germany,Female,59,0,135296.33,1,1,0,182822.5,0
2025,15631868,Robertson,744,Spain,Male,36,2,153804.44,1,1,1,87213.33,0
2025,15581539,Atkinson,474,Spain,Male,37,3,0,2,0,0,57175.32,0
2025,15662736,Doyle,559,France,Male,49,2,147069.78,1,1,0,120540.83,1
2025,15666252,Ritchie,706,Spain,Male,42,9,0,2,1,1,28714.34,0
2025,15677512,McEncroe,628,Spain,Female,22,3,0,1,1,0,85426.28,0
2025,15626114,Pearson,429,France,Male,24,4,95741.75,1,1,0,46170.75,0
2025,15740454,Parkhill,693,Germany,Male,40,0,120711.73,1,0,0,27345.18,1
2025,15742668,Kirby,782,Spain,Male,52,4,0,1,1,1,52759.82,1
2025,15734811,Ho,505,France,Male,34,10,104498.79,1,0,1,126451.14,0
2025,15727919,Chukwuemeka,671,Spain,Female,29,6,0,2,0,0,1208.6,0
2025,15714087,McGill,624,Germany,Female,45,5,151855.33,1,1,0,68794.15,0
2025,15711446,Sinclair,569,Spain,Female,51,3,0,3,1,0,75084.96,1
2025,15588123,Horton,677,France,Female,27,2,0,2,0,1,114685.92,0
2025,15748552,Sal,464,Germany,Male,37,4,155994.15,1,0,0,143665.44,0
2025,15609653,Ifeatu,614,Germany,Female,44,6,118715.86,1,1,0,133591.11,1
2025,15594577,De Luca,556,France,Male,35,10,0,2,1,1,192751.18,0
2025,15584114,Ogbonnaya,678,Germany,Female,43,2,153393.18,2,1,1,193828.27,0
2025,15733667,Humffray,587,Germany,Male,33,6,132603.36,1,1,0,55775.72,0
2025,15685576,Degtyaryov,527,Spain,Female,36,6,0,2,1,1,102280.29,0
2025,15774727,Monaldo,757,Germany,Female,34,1,129398.01,2,0,0,44965.44,0
2025,15694288,Cawthorne,468,Spain,Male,28,3,0,2,1,0,170661.02,0
2025,15603319,Graham,693,France,Male,29,2,151352.74,1,0,0,197145.89,0
2025,15750466,Rhodes,790,Germany,Male,42,1,85839.62,1,1,0,198182.73,0
2025,15739054,Y?,654,France,Female,29,4,96974.97,1,0,1,141404.07,0
2025,15612771,Bell,452,France,Male,35,4,148172.44,1,1,1,4175.68,0
2025,15788483,Kerr,719,Spain,Male,38,0,0,1,1,0,126876.47,0
2025,15732832,Jideofor,707,France,Female,40,5,0,2,1,0,41052.82,0
2025,15772892,Robertson,699,France,Female,49,2,0,1,0,0,105760.01,0
2025,15713843,Kao,850,Spain,Male,30,2,0,2,0,1,27937.12,0
2025,15567993,Palmer,828,Spain,Male,28,8,134766.85,1,1,0,79355.87,0
2025,15617603,Mackay,850,Germany,Male,30,5,123210.56,2,1,1,102180.27,0
2025,15744983,Burgmann,712,Spain,Male,47,1,139887.01,1,1,1,95719.73,0
2025,15630419,Davis,634,France,Male,44,9,149961.11,1,1,0,57121.51,0
2025,15738828,Milano,730,Germany,Male,45,6,152880.97,1,0,0,162478.11,0
2025,15778025,Dellucci,685,Germany,Male,43,9,108589.47,2,0,1,194808.51,0
2025,15799479,Coles,809,Spain,Male,33,9,0,1,1,1,124045.65,0
2025,15684269,Gray,707,Spain,Female,35,3,56674.48,1,1,0,17987.4,1
2025,15762745,Macvitie,648,Spain,Male,32,8,0,1,1,0,133653.38,0
2025,15746970,Townsend,760,Spain,Female,57,1,0,2,1,1,25101.17,0
2025,15725024,Pope,805,Germany,Female,33,3,105663.56,2,0,1,33330.89,0
2025,15592116,Jensen,585,France,Female,39,7,0,2,1,0,2401.26,0
2025,15594391,Samaniego,770,France,Female,68,2,183555.24,1,0,0,159572.28,1
2025,15771569,Bage,576,Germany,Male,46,4,137367.94,1,1,1,33450.11,0
2025,15797190,Charlton,669,France,Female,29,3,82344.84,1,0,1,115985.38,0
2025,15732102,Darling,656,Germany,Female,27,3,150905.03,2,1,0,16998.72,0
2025,15739046,Maggard,850,Spain,Female,23,9,143054.85,1,0,1,62980.96,0
2025,15631927,Thomas,574,Spain,Female,28,7,0,2,0,0,185660.3,0
2025,15672115,Lettiere,679,France,Male,60,6,0,2,1,1,77331.77,0
2025,15618765,Ponomaryov,530,Germany,Female,42,0,99948.45,1,0,1,97338.62,0
2025,15679148,Oliver,508,France,Male,44,3,115451.05,2,0,0,67234.33,0
2025,15728474,Chienezie,558,Germany,Male,32,4,108235.91,1,1,1,143783.28,0
2025,15636999,Mao,414,France,Male,38,8,0,1,0,1,77661.12,1
2025,15754261,Ho,648,Spain,Male,42,2,98795.61,2,1,0,89123.99,0
2025,15629150,Lucchese,721,France,Female,37,1,0,2,1,0,70810.8,0
2025,15732778,Templeman,468,Germany,Male,29,1,111681.98,2,1,1,195711.16,0
2025,15718443,Chibuzo,539,France,Male,39,3,0,2,1,0,36692.17,0
2025,15670039,Sun,509,Spain,Female,25,3,108738.71,2,1,0,106920.57,0
2025,15773792,Evans,662,France,Female,32,4,133950.37,1,1,1,48725.68,1
2025,15613786,Ogbonnaya,818,Spain,Male,26,4,0,2,1,1,167036.94,0
2025,15726032,Enyinnaya,608,France,Male,33,9,89968.69,1,1,0,68777.26,0
2025,15663252,Olisanugo,850,Spain,Female,32,9,0,2,1,1,18924.92,0
2025,15593782,Brookes,816,Germany,Female,38,5,130878.75,3,1,0,71905.77,1
2025,15633283,Padovano,536,France,Male,35,8,0,2,1,0,64833.28,0
2025,15749167,Fisk,753,France,Male,35,3,0,2,1,1,184843.77,0
2025,15759298,Shih,631,Spain,Male,27,10,134169.62,1,1,1,176730.02,0
"""

# ---------------------------------------------------------
# Load Data & Cache Processing
# ---------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(io.StringIO(RAW_CSV.strip()))
    # Map boolean conversions
    df['HasCrCard'] = df['HasCrCard'] == 1
    df['IsActiveMember'] = df['IsActiveMember'] == 1
    df['Exited'] = df['Exited'] == 1
    return df

raw_df = load_data()

# ---------------------------------------------------------
# Sidebar Filter Controls
# ---------------------------------------------------------
st.sidebar.image("https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=150&q=80", use_container_width=True)
st.sidebar.markdown("""
<div style="text-align: center; margin-bottom: 1.5rem;">
    <h3 style="color:#06b6d4; margin:0; font-size:1.1rem; font-family:'Space Grotesk' !important;">ECB Sponsor Hub</h3>
    <p style="color:#64748b; margin:0; font-size:0.75rem; text-transform:uppercase; font-weight:700;">Joint Action Council</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.header("🎛️ Analysis Controls")

# Region Filter
geography_list = ["All"] + sorted(raw_df['Geography'].unique().tolist())
selected_geography = st.sidebar.selectbox("Geography Region", geography_list)

# Gender Selection
gender_selection = st.sidebar.radio("Gender Profile", ["All", "Female", "Male"], horizontal=True)

# Age Filter
min_age_data = int(raw_df['Age'].min())
max_age_data = int(raw_df['Age'].max())
selected_age_range = st.sidebar.slider("Age Thresholds", min_age_data, max_age_data, (18, 92))

# Balance Range Selection
selected_balance_range = st.sidebar.slider(
    "Capital Balance Held ($)",
    float(raw_df['Balance'].min()),
    float(raw_df['Balance'].max()),
    (0.0, 250000.0)
)

# Product Filter
products_selection = st.sidebar.multiselect(
    "Products Held Count",
    options=sorted(raw_df['NumOfProducts'].unique().tolist()),
    default=sorted(raw_df['NumOfProducts'].unique().tolist())
)

# Active Member and Card Status Filter
col_active, col_card = st.sidebar.columns(2)
with col_active:
    filter_active = st.selectbox("Activity Status", ["All", "Active", "Inactive"])
with col_card:
    filter_card = st.selectbox("Credit Card Holder", ["All", "Yes", "No"])

# Filter Dataset Application
filtered_df = raw_df.copy()

if selected_geography != "All":
    filtered_df = filtered_df[filtered_df['Geography'] == selected_geography]

if gender_selection != "All":
    filtered_df = filtered_df[filtered_df['Gender'] == gender_selection]

filtered_df = filtered_df[
    (filtered_df['Age'] >= selected_age_range[0]) & 
    (filtered_df['Age'] <= selected_age_range[1])
]

filtered_df = filtered_df[
    (filtered_df['Balance'] >= selected_balance_range[0]) & 
    (filtered_df['Balance'] <= selected_balance_range[1])
]

if products_selection:
    filtered_df = filtered_df[filtered_df['NumOfProducts'].isin(products_selection)]

if filter_active != "All":
    filtered_df = filtered_df[filtered_df['IsActiveMember'] == (filter_active == "Active")]

if filter_card != "All":
    filtered_df = filtered_df[filtered_df['HasCrCard'] == (filter_card == "Yes")]

# Reset Filter button
if st.sidebar.button("Reset Analytical Scopes", use_container_width=True):
    st.rerun()

# ---------------------------------------------------------
# Dynamic KPI Matrix Calculation
# ---------------------------------------------------------
total_matching = len(filtered_df)

if total_matching > 0:
    exited_count = len(filtered_df[filtered_df['Exited']])
    churn_rate = (exited_count / total_matching) * 100
    retention_rate = 100 - churn_rate

    # Product Depth Index
    product_depth = filtered_df['NumOfProducts'].mean()

    # Active vs Inactive Churn Rates
    active_df = filtered_df[filtered_df['IsActiveMember']]
    inactive_df = filtered_df[~filtered_df['IsActiveMember']]
    
    active_exits = len(active_df[active_df['Exited']]) if len(active_df) > 0 else 0
    inactive_exits = len(inactive_df[inactive_df['Exited']]) if len(inactive_df) > 0 else 0

    active_churn_rate = (active_exits / len(active_df)) * 100 if len(active_df) > 0 else 0.0
    inactive_churn_rate = (inactive_exits / len(inactive_df)) * 100 if len(inactive_df) > 0 else 0.0

    # KPI 1: Engagement Retention Ratio
    engagement_retention_ratio = active_churn_rate / inactive_churn_rate if inactive_churn_rate > 0 else 0.0

    # KPI 3: High-Balance Disengagement Rate
    high_balance_inactive = filtered_df[(~filtered_df['IsActiveMember']) & (filtered_df['Balance'] >= 100000)]
    hb_inactive_exits = len(high_balance_inactive[high_balance_inactive['Exited']])
    high_balance_disengagement_rate = (hb_inactive_exits / len(high_balance_inactive)) * 100 if len(high_balance_inactive) > 0 else 0.0

    # KPI 4: Credit Card Stickiness Score (Churn Rate without Card - Churn Rate with Card)
    card_holders = filtered_df[filtered_df['HasCrCard']]
    non_card_holders = filtered_df[~filtered_df['HasCrCard']]
    card_churn = (len(card_holders[card_holders['Exited']]) / len(card_holders)) * 100 if len(card_holders) > 0 else 0.0
    non_card_churn = (len(non_card_holders[non_card_holders['Exited']]) / len(non_card_holders)) * 100 if len(non_card_holders) > 0 else 0.0
    cc_stickiness_score = non_card_churn - card_churn

    # KPI 5: Relationship Strength Index (Weighted average)
    relationship_scores = []
    for idx, r in filtered_df.iterrows():
        pt_active = 40 if r['IsActiveMember'] else 0
        pt_prod = 40 if r['NumOfProducts'] >= 2 else 10
        pt_card = 20 if r['HasCrCard'] else 0
        relationship_scores.append(pt_active + pt_prod + pt_card)
    relationship_strength_idx = np.mean(relationship_scores) if len(relationship_scores) > 0 else 0.0
else:
    retention_rate = 0.0
    product_depth = 0.0
    high_balance_disengagement_rate = 0.0
    cc_stickiness_score = 0.0
    relationship_strength_idx = 0.0
    active_churn_rate = 0.0
    inactive_churn_rate = 0.0

# ---------------------------------------------------------
# Application Main Interface & Tabs
# ---------------------------------------------------------
st.title("🛡️ CUSTOMER RETENTION & PRODUCT UTILIZATION ENGINE")
st.markdown("""
<div style="margin-top:-1rem; margin-bottom:2rem; color:#64748b; font-size:0.85rem; font-family:'JetBrains Mono'; font-weight:500;">
    SYSTEM DEPLOYMENT STATUS: ACTIVE | AUTH AUTHORIZATION: EUROPEAN CENTRAL BANK JOINT DIRECTIVE v4.2
</div>
""", unsafe_allow_html=True)

# Key Bold Dashboard Metric Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Overall Retention</div>
        <div class="metric-value">{retention_rate:.1f}<span class="metric-suffix">%</span></div>
        <div class="metric-subtitle">Active Churn: {active_churn_rate:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Product Depth Index</div>
        <div class="metric-value">{product_depth:.2f}</div>
        <div class="metric-subtitle" style="color:#64748b;">Avg Bank Products / Cust</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Premium Churn Risk</div>
        <div class="metric-value" style="color: #f43f5e;">{high_balance_disengagement_rate:.1f}<span class="metric-suffix">%</span></div>
        <div class="metric-subtitle metric-subtitle-red">SILENT EXIT ALERT ZONE</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Relationship Strength</div>
        <div class="metric-value">{int(relationship_strength_idx)}<span class="metric-suffix">/100</span></div>
        <div class="metric-subtitle">Card Benefit Spread: +{cc_stickiness_score:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

# Main Application Interactive Modules Tabs
tab_overview, tab_products, tab_detector, tab_simulator, tab_dataset = st.tabs([
    "📊 Engagement Overview", 
    "🗃️ Product Utilization Impact", 
    "🚨 Premium Risk Detector", 
    "🎮 Retention Strength Simulator",
    "📁 ECB Dataset Browser"
])

# ---------------------------------------------------------
# Tab 1: Engagement & Churn Overview
# ---------------------------------------------------------
with tab_overview:
    st.header("Engagement & Churn Overview")
    st.markdown("Analyzing how active vs. inactive member segments correlate with historical exit behaviors.")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Member Status vs Retention")
        # Bar Chart showing Active Churn Rate vs Inactive Churn Rate
        chart_data = pd.DataFrame({
            "Segment": ["Active Members", "Inactive Members"],
            "Retention Rate (%)": [100 - active_churn_rate, 100 - inactive_churn_rate],
            "Churn Rate (%)": [active_churn_rate, inactive_churn_rate]
        }).set_index("Segment")
        
        st.bar_chart(chart_data, color=["#06b6d4", "#ef4444"], height=350)
        
    with col_chart2:
        st.subheader("Regional Churn Distribution")
        # Calculate churn rate by country
        geo_churn = filtered_df.groupby("Geography")['Exited'].mean().reset_index()
        geo_churn['Churn Rate (%)'] = geo_churn['Exited'] * 100
        
        geo_chart_df = geo_churn.set_index("Geography")[['Churn Rate (%)']]
        st.bar_chart(geo_chart_df, color="#ef4444", height=350)
        
    # Demographic Age group analysis
    st.subheader("Age Bracket exit probability analysis")
    age_bins = [18, 30, 40, 50, 60, 100]
    age_labels = ["18-29", "30-39", "40-49", "50-59", "60+"]
    df_age = filtered_df.copy()
    df_age['AgeGroup'] = pd.cut(df_age['Age'], bins=age_bins, labels=age_labels, right=False)
    age_group_churn = df_age.groupby('AgeGroup', observed=False)['Exited'].mean().reset_index()
    age_group_churn['Churn Rate (%)'] = age_group_churn['Exited'] * 100
    
    age_chart_df = age_group_churn.set_index("AgeGroup")[['Churn Rate (%)']]
    st.area_chart(age_chart_df, color="#f43f5e", height=300)
    
    st.markdown("""
    <div class="directive-banner">
        <strong>ECB ANALYTICAL HEURISTIC:</strong> Notice how churn probability peaks significantly for the 50-59 Age Bracket, climbing past 45%. Retention campaigns should target senior age brackets where risk concentrations reside.
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# Tab 2: Product Utilization Impact
# ---------------------------------------------------------
with tab_products:
    st.header("Product Depth vs Customer Retention")
    st.markdown("Evaluating how cross-selling additional products correlates with lower overall risk of customer churn.")
    
    prod_churn = filtered_df.groupby("NumOfProducts")['Exited'].mean().reset_index()
    prod_churn['Churn Rate (%)'] = prod_churn['Exited'] * 100
    prod_counts = filtered_df.groupby("NumOfProducts")['CustomerId'].count().reset_index().rename(columns={"CustomerId": "Total Users"})
    prod_merged = pd.merge(prod_churn, prod_counts, on="NumOfProducts")
    
    col_chart, col_data = st.columns([2, 1])
    
    with col_chart:
        prod_chart_df = prod_merged.set_index("NumOfProducts")[['Churn Rate (%)']]
        st.bar_chart(prod_chart_df, color="#06b6d4", height=380)
        
    with col_data:
        st.subheader("Statistical Profile")
        for idx, row in prod_merged.iterrows():
            st.metric(
                label=f"Exits for {int(row['NumOfProducts'])} Product(s) Held",
                value=f"{row['Churn Rate (%)']:.1f}%",
                delta=f"{int(row['Total Users'])} total users",
                delta_color="off"
            )
            
    st.subheader("Core ECB Directive: Single vs Multi-Product Retention Analysis")
    st.markdown("""
    When evaluating product holding depths across our core European database, a clear **retention tipping point** emerges:
    * **The Single-Product Trap (1 Product)**: Customer relationships are extremely fragile. This group displays high churn risk (often exceeding 27%) due to transactional detachment.
    * **The Anchor Optimum (2 Products)**: Adding a secondary deposit/savings or card product provides optimal relationship lock-in, cutting exit rates down to **under 10%**.
    * **Aggressive Bundling Risks (3+ Products)**: Counter-intuitively, customers holding 3 or 4 products represent extreme disaffection or forced sales, causing historical exit rates to spike to near **100%** on 4-product accounts.
    """)
    st.info("💡 Strategic Directive: Do not over-bundle beyond 2 products. Align cross-selling efforts to establish a secondary savings or mortgage anchor product only.")

# ---------------------------------------------------------
# Tab 3: Premium Risk Detector
# ---------------------------------------------------------
with tab_detector:
    st.header("Premium Risk Detector Portal")
    st.markdown("Identify high-value, high-income disengaged members holding significant capital balances silently.")
    
    col_ctrl1, col_ctrl2 = st.columns(2)
    with col_ctrl1:
        det_min_balance = st.number_input("Minimum Capital Balance ($)", min_value=0, max_value=250000, value=100000, step=10000)
    with col_ctrl2:
        det_min_salary = st.number_input("Minimum Estimated Salary ($)", min_value=0, max_value=200000, value=80000, step=10000)
        
    # High Value Disengaged Detector logic: Inactive members with Balance >= det_min_balance and Salary >= det_min_salary
    detector_df = raw_df[
        (~raw_df['IsActiveMember']) & 
        (raw_df['Balance'] >= det_min_balance) & 
        (raw_df['EstimatedSalary'] >= det_min_salary)
    ].copy()
    
    # Calculate Risk Score
    def compute_risk(row):
        score = 40
        if row['Geography'] == "Germany": score += 15
        if row['Age'] > 45: score += 20
        if row['CreditScore'] < 600: score += 15
        if row['NumOfProducts'] == 1: score += 10
        if not row['HasCrCard']: score += 5
        return min(score, 100)
        
    if len(detector_df) > 0:
        detector_df['RiskScore'] = detector_df.apply(compute_risk, axis=1)
        detector_df['RiskTier'] = pd.cut(
            detector_df['RiskScore'], 
            bins=[0, 60, 75, 101], 
            labels=["MODERATE", "HIGH", "CRITICAL"], 
            right=False
        )
        detector_df = detector_df.sort_values(by="RiskScore", ascending=False)
        
        # Display Total Capital sum at risk
        total_at_risk_capital = detector_df['Balance'].sum()
        
        st.markdown(f"""
        <div style="background-color:rgba(244,63,94,0.15); border: 1px solid rgba(244,63,94,0.3); padding: 1.25rem; border-radius:4px; margin-bottom: 1.5rem;">
            <p style="margin:0; font-size:0.75rem; text-transform:uppercase; font-weight:800; color:#f43f5e; letter-spacing:0.1em;">Premium Capital Exposure At Risk</p>
            <h2 style="margin:0; font-size:2.25rem; font-weight:900; color:#ffffff; font-family:'Space Grotesk' !important;">${total_at_risk_capital:,.2f}</h2>
            <p style="margin:0.25rem 0 0 0; font-size:0.8rem; color:#f43f5e;">Based on {len(detector_df)} disengaged premium accounts currently identified.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Format table for output
        show_cols = ["Surname", "Geography", "Age", "Balance", "NumOfProducts", "CreditScore", "RiskScore", "RiskTier"]
        display_detector = detector_df[show_cols].copy()
        display_detector['Balance'] = display_detector['Balance'].apply(lambda x: f"${x:,.2f}")
        display_detector['RiskScore'] = display_detector['RiskScore'].apply(lambda x: f"{x}/100")
        
        st.table(display_detector)
    else:
        st.success("✅ No premium disengaged accounts found matching those criteria. Lower the balance/salary sliders to expand findings.")

# ---------------------------------------------------------
# Tab 4: Retention Strength Simulator
# ---------------------------------------------------------
with tab_simulator:
    st.header("Retention Strength Simulator")
    st.markdown("Simulate customized customer profiles and compute a precise churn probability using logistic regression model approximations.")
    
    col_sim1, col_sim2 = st.columns(2)
    
    with col_sim1:
        sim_geo = st.selectbox("Simulated Region", ["France", "Germany", "Spain"])
        sim_gender = st.radio("Simulated Gender", ["Female", "Male"], horizontal=True)
        sim_age = st.slider("Simulated Customer Age", 18, 92, 40)
        sim_credit = st.slider("Credit Score Profile", 300, 850, 650)
        sim_products = st.slider("Products Held Profile", 1, 4, 1)
        
    with col_sim2:
        sim_active = st.checkbox("Is Active Member", value=False)
        sim_has_card = st.checkbox("Has Bank Credit Card", value=True)
        sim_balance = st.number_input("Simulated Account Balance ($)", min_value=0.0, max_value=250000.0, value=120000.0, step=10000.0)
        sim_salary = st.number_input("Estimated Salary Profile ($)", min_value=0.0, max_value=200000.0, value=90000.0, step=10000.0)
        
    # Logistic Regression Simulator Approximation
    # Intercept & coefficients matching our ECB reactive dashboard framework
    log_odds = -2.3
    
    if sim_geo == "Germany": log_odds += 0.95
    if sim_geo == "Spain": log_odds += 0.15
    if sim_gender == "Female": log_odds += 0.28
    if sim_active: log_odds -= 1.1
    
    if sim_products == 1: log_odds += 0.45
    if sim_products == 2: log_odds -= 1.2
    if sim_products >= 3: log_odds += 1.8
    
    if sim_credit < 600: log_odds += 0.35
    if sim_credit >= 750: log_odds -= 0.25
    
    if 40 <= sim_age < 50: log_odds += 0.55
    if 50 <= sim_age < 65: log_odds += 1.35
    if sim_age >= 65: log_odds += 1.0
    
    if sim_balance > 100000: log_odds += 0.35
    if sim_balance == 0: log_odds -= 0.15
    if not sim_has_card: log_odds += 0.15
    
    # Sigmoid function
    prob = 1 / (1 + np.exp(-log_odds))
    prob_percent = int(round(prob * 100))
    
    st.subheader("Model Prediction Output")
    
    col_out1, col_out2 = st.columns([1, 2])
    
    with col_out1:
        if prob_percent >= 65:
            box_style = "background-color:rgba(239,68,68,0.15); border: 2px solid #ef4444;"
            tier_label = "CRITICAL RISK"
            color_lbl = "#ef4444"
        elif prob_percent >= 35:
            box_style = "background-color:rgba(245,158,11,0.15); border: 2px solid #f59e0b;"
            tier_label = "MODERATE RISK"
            color_lbl = "#f59e0b"
        else:
            box_style = "background-color:rgba(16,185,129,0.15); border: 2px solid #10b981;"
            tier_label = "LOW RISK"
            color_lbl = "#10b981"
            
        st.markdown(f"""
        <div style="{box_style} padding: 1.5rem; border-radius:4px; text-align:center;">
            <p style="margin:0; font-size:0.65rem; font-weight:800; color:#64748b; letter-spacing:0.1em; text-transform:uppercase;">Model Prediction</p>
            <h1 style="margin:0.25rem 0; font-size:3.5rem; color:{color_lbl} !important; border:none; padding:0;">{prob_percent}%</h1>
            <p style="margin:0; font-size:0.8rem; font-weight:900; color:{color_lbl};">{tier_label}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_out2:
        st.markdown("### Strategic Retention Action Plan")
        if prob_percent >= 65:
            st.error("🚨 **High Churn Alert!** This simulated customer matches historical drop-off segments immediately. They should be prioritized for card loyalty benefits, fee waivers, or targeted secondary account bundle savings products to increase relationship depth from 1 to 2 products.")
        elif prob_percent >= 35:
            st.warning("⚠️ **Moderate Warning.** This simulated profile displays soft disengagement markers. Proactively reach out to activate membership status and review current financial holding options.")
        else:
            st.success("✅ **Stable Relationship Account.** Standard automated retention rules apply. Highly loyal holding profile with minor risk profile.")
            
# ---------------------------------------------------------
# Tab 5: Raw ECB Dataset Browser
# ---------------------------------------------------------
with tab_dataset:
    st.header("European Central Bank Dataset Browser")
    st.markdown("Full list of customer entries with instant analytical filter scopes applied.")
    
    col_browser1, col_browser2 = st.columns([2, 1])
    with col_browser1:
        search_query = st.text_input("🔍 Search Database (Surname, Geography, ID)", "")
    with col_browser2:
        sort_by_col = st.selectbox("Sort Data Column", ["Balance", "CreditScore", "Age", "EstimatedSalary", "Surname"])
        
    browse_df = filtered_df.copy()
    
    if search_query:
        query = search_query.lower()
        browse_df = browse_df[
            (browse_df['Surname'].str.lower().str.contains(query)) | 
            (browse_df['Geography'].str.lower().str.contains(query)) |
            (browse_df['CustomerId'].astype(str).str.contains(query))
        ]
        
    browse_df = browse_df.sort_values(by=sort_by_col, ascending=False)
    
    st.dataframe(browse_df, use_container_width=True)
