import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Menyiapkan himpunan Fuzzy
suhu      = ctrl.Antecedent(np.arange(0, 41, 1),  'suhu')
kelembapan = ctrl.Antecedent(np.arange(0, 101, 1), 'kelembapan')
kecepatan  = ctrl.Consequent(np.arange(0, 101, 1), 'kecepatan')

# Jenis suhu
suhu['Rendah'] = fuzz.trapmf(suhu.universe, [0,  0, 10, 20])
suhu['Normal']  = fuzz.trimf (suhu.universe, [10, 20, 30])
suhu['Tinggi']  = fuzz.trapmf(suhu.universe, [25, 35, 40, 40])

# Level kelembapan
kelembapan['Kering'] = fuzz.zmf   (kelembapan.universe, 0,  40)
kelembapan['Sedang'] = fuzz.trimf (kelembapan.universe, [20, 50, 80])
kelembapan['Basah']  = fuzz.smf   (kelembapan.universe, 60, 100)

# Level kecepatan kipas
kecepatan['Pelan'] = fuzz.trapmf(kecepatan.universe, [0,  0, 20, 40])
kecepatan['Sedang'] = fuzz.trimf (kecepatan.universe, [30, 50, 70])
kecepatan['Cepat']  = fuzz.trapmf(kecepatan.universe, [60, 80, 100, 100])

suhu.view()
kelembapan.view()
kecepatan.view()
input("Tekan ENTER untuk melanjutkan ke pembuatan aturan...")

aturan1 = ctrl.Rule(suhu['Rendah'], kecepatan['Pelan'])
aturan2 = ctrl.Rule(suhu['Normal'] & kelembapan['Sedang'], kecepatan['Sedang'])
aturan3 = ctrl.Rule(suhu['Tinggi'] | kelembapan['Basah'], kecepatan['Cepat'])
aturan4 = ctrl.Rule(suhu['Normal'] & kelembapan['Kering'], kecepatan['Pelan'])
aturan5 = ctrl.Rule(suhu['Tinggi'] & kelembapan['Kering'], kecepatan['Sedang'])

engine = ctrl.ControlSystem([aturan1, aturan2, aturan3, aturan4, aturan5])
system = ctrl.ControlSystemSimulation(engine)

system.input['suhu']       = 39
system.input['kelembapan'] = 80
system.compute()
print(system.output['kecepatan'])
kecepatan.view(sim=system)
input("Tekan ENTER untuk melanjutkan")