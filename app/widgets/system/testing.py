import json
from pprint import pprint

data = (b'{"CpuInfo":{"uiLoad":[2,3,9,11,8,5],"uiTjMax":[0],"uiCoreCnt":6,"uiCPUCnt":1'
 b',"fTemp":[35.375,35.375,35.375,35.375,35.375,35.375],"fVID":1.29374993,"fCPU'
 b'Speed":4116.30469,"fFSBSpeed":99.7892,"fMultiplier":41.25,"CPUName":"AMD Ryz'
 b'en 5 3600X 6-Core (Matisse) ","ucFahrenheit":0,"ucDeltaToTjMax":0,"ucTdpSupp'
 b'orted":0,"ucPowerSupported":1,"uiStructVersion":2,"uiTdp":[0],"fPower":[27.1'
 b'996689],"fMultipliers":[41.25,41.25,41.25,41.25,41.25,41.25]},"MemoryInfo":{'
 b'"TotalPhys":16296,"FreePhys":8195,"TotalPage":18984,"FreePage":6275,"TotalVi'
 b'rtual":134217728,"FreeVirtual":134212980,"FreeExtendedVirtual":1,"MemoryLoad'
 b'":49}}\r\n')

#pprint(data)
pprint(json.loads(data))