// ====================================================
// libnvml_fake.c (FULL SPOOF NVIDIA H100, VRAM 80 GB)
// ====================================================
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <dlfcn.h>
#include <unistd.h> // getpid()

typedef int nvmlReturn_t;
#define NVML_SUCCESS 0
typedef void* nvmlDevice_t;

// === Struct memory info ===
typedef struct __attribute__((packed)) {
    unsigned long long total;
    unsigned long long free;
    unsigned long long used;
} nvmlMemory_t;

// === Utilization struct ===
typedef struct {
    unsigned int gpu;
    unsigned int memory;
} nvmlUtilization_t;

// === Process info struct ===
typedef struct {
    unsigned int pid;
    unsigned long long usedGpuMemory;
} nvmlProcessInfo_t;

// === Attributes struct (resmi di nvml.h) ===
typedef struct {
    unsigned int multiprocessorCount;
    unsigned long long memorySizeMB;
} nvmlDeviceAttributes_t;

// === API inti ===
nvmlReturn_t nvmlInit(void){ return NVML_SUCCESS; }
nvmlReturn_t nvmlInit_v2(void){ return NVML_SUCCESS; }
nvmlReturn_t nvmlInitWithFlags(unsigned int f){ return NVML_SUCCESS; }
nvmlReturn_t nvmlShutdown(void){ return NVML_SUCCESS; }
const char* nvmlErrorString(nvmlReturn_t result){ return "Success"; }

// === Versi & driver ===
nvmlReturn_t nvmlSystemGetDriverVersion(char* v,unsigned int l){ strncpy(v,"550.120.00",l); return NVML_SUCCESS; }
nvmlReturn_t nvmlSystemGetCudaDriverVersion(int* v){ *v=12040; return NVML_SUCCESS; }
nvmlReturn_t nvmlSystemGetCudaDriverVersion_v2(int* v){ *v=12040; return NVML_SUCCESS; }
nvmlReturn_t nvmlSystemGetNVMLVersion(char* v,unsigned int l){ strncpy(v,"12.550.0",l); return NVML_SUCCESS; }

// === Device count & handle ===
nvmlReturn_t nvmlDeviceGetCount(unsigned int* c){ *c=1; return NVML_SUCCESS; }
nvmlReturn_t nvmlDeviceGetCount_v2(unsigned int* c){ *c=1; return NVML_SUCCESS; }
nvmlReturn_t nvmlDeviceGetHandleByIndex(unsigned int i,nvmlDevice_t* d){ *d=(nvmlDevice_t)0x1234; return NVML_SUCCESS; }
nvmlReturn_t nvmlDeviceGetHandleByIndex_v2(unsigned int i,nvmlDevice_t* d){ *d=(nvmlDevice_t)0x1234; return NVML_SUCCESS; }

// === Device info ===
nvmlReturn_t nvmlDeviceGetName(nvmlDevice_t d,char* n,unsigned int l){ strncpy(n,"NVIDIA H100 Tensor Core GPU",l); return NVML_SUCCESS; }
nvmlReturn_t nvmlDeviceGetUUID(nvmlDevice_t d,char* u,unsigned int l){ strncpy(u,"GPU-H100-UUID",l); return NVML_SUCCESS; }
nvmlReturn_t nvmlDeviceGetSerial(nvmlDevice_t d,char* s,unsigned int l){ strncpy(s,"H100-1234567890",l); return NVML_SUCCESS; }

// === Memory Info (80 GB HBM3) ===
nvmlReturn_t nvmlDeviceGetMemoryInfo(nvmlDevice_t d,nvmlMemory_t* m){
    if (!m) return NVML_SUCCESS;
    m->total = 80ULL << 30;   // 80 GB
    m->used  = 10ULL << 30;   // 10 GB digunakan
    m->free  = m->total - m->used;
    return NVML_SUCCESS;
}
nvmlReturn_t nvmlDeviceGetMemoryInfo_v2(nvmlDevice_t d,nvmlMemory_t* m){
    return nvmlDeviceGetMemoryInfo(d,m);
}

// === Utilization & Power ===
nvmlReturn_t nvmlDeviceGetUtilizationRates(nvmlDevice_t d,nvmlUtilization_t* u){ u->gpu=40; u->memory=20; return NVML_SUCCESS; }
nvmlReturn_t nvmlDeviceGetTemperature(nvmlDevice_t d,int t,unsigned int* v){ *v=45; return NVML_SUCCESS; }
nvmlReturn_t nvmlDeviceGetFanSpeed(nvmlDevice_t d,unsigned int* v){ *v=30; return NVML_SUCCESS; }
nvmlReturn_t nvmlDeviceGetPowerUsage(nvmlDevice_t d,unsigned int* v){ *v=700000; return NVML_SUCCESS; } // 700W
nvmlReturn_t nvmlDeviceGetPerformanceState(nvmlDevice_t d,unsigned int* v){ *v=0; return NVML_SUCCESS; }

// === Clock Info ===
nvmlReturn_t nvmlDeviceGetClockInfo(nvmlDevice_t d,int t,unsigned int* clock){
    if(clock){ *clock = 1590; } // MHz base
    return NVML_SUCCESS;
}
nvmlReturn_t nvmlDeviceGetMaxClockInfo(nvmlDevice_t d,int t,unsigned int* clock){
    if(clock){ *clock = 1980; } // MHz boost
    return NVML_SUCCESS;
}

// === Attribute API spoof ===
typedef enum {
    NVML_DEVICE_ATTRIBUTE_MULTIPROCESSOR_COUNT = 39,
    NVML_DEVICE_ATTRIBUTE_TENSOR_CORES = 199,
    NVML_DEVICE_ATTRIBUTE_RT_CORES = 200,
    NVML_DEVICE_ATTRIBUTE_CUDA_CORES = 3
} nvmlDeviceAttribute_t;

#define H100_CUDA_CORES   16896
#define H100_TENSOR_CORES 528
#define H100_RT_CORES     0
#define H100_SM_COUNT     132

nvmlReturn_t nvmlDeviceGetAttribute(nvmlDevice_t d, nvmlDeviceAttribute_t attr, int *value){
    if(attr == NVML_DEVICE_ATTRIBUTE_CUDA_CORES){ *value = H100_CUDA_CORES; return NVML_SUCCESS; }
    if(attr == NVML_DEVICE_ATTRIBUTE_MULTIPROCESSOR_COUNT){ *value = H100_SM_COUNT; return NVML_SUCCESS; }
    if(attr == NVML_DEVICE_ATTRIBUTE_TENSOR_CORES){ *value = H100_TENSOR_CORES; return NVML_SUCCESS; }
    if(attr == NVML_DEVICE_ATTRIBUTE_RT_CORES){ *value = H100_RT_CORES; return NVML_SUCCESS; }
    *value = 1;
    return NVML_SUCCESS;
}

// === Attributes_v2 spoof ===
nvmlReturn_t nvmlDeviceGetAttributes_v2(nvmlDevice_t d, nvmlDeviceAttributes_t *attr) {
    if (!attr) return NVML_SUCCESS;
    attr->multiprocessorCount = H100_SM_COUNT; // 132 SM
    attr->memorySizeMB        = 81920;         // 80 GB dalam MB
    return NVML_SUCCESS;
}

// === PCI Info spoof ===
typedef struct {
    char busId[16];
    unsigned int domain;
    unsigned int bus;
    unsigned int device;
    unsigned int pciDeviceId;
    unsigned int pciSubSystemId;
} nvmlPciInfo_t;

nvmlReturn_t nvmlDeviceGetPciInfo(nvmlDevice_t d, nvmlPciInfo_t* info) {
    if (!info) return NVML_SUCCESS;
    strncpy(info->busId, "00000000:01:00.0", sizeof(info->busId));
    info->domain = 0; info->bus = 1; info->device = 0;
    info->pciDeviceId = 0x2331; info->pciSubSystemId = 0x157A; // contoh ID H100
    return NVML_SUCCESS;
}

// === Inforom & Compute Capability ===
nvmlReturn_t nvmlDeviceGetInforomVersion(nvmlDevice_t d, int obj, char* ver, unsigned int len) {
    strncpy(ver, "200.00.00.00", len);
    return NVML_SUCCESS;
}
nvmlReturn_t nvmlDeviceGetCudaComputeCapability(nvmlDevice_t d, int *major, int *minor) {
    if (major) *major = 9; if (minor) *minor = 0;
    return NVML_SUCCESS;
}
#define NVML_DEVICE_ARCH_HOPPER 300
nvmlReturn_t nvmlDeviceGetArchitecture(nvmlDevice_t d, int *arch) {
    if (arch) *arch = NVML_DEVICE_ARCH_HOPPER;
    return NVML_SUCCESS;
}

// === Process List (dummy) ===
nvmlReturn_t nvmlDeviceGetComputeRunningProcesses_v2(nvmlDevice_t d, unsigned int* c, nvmlProcessInfo_t* infos){
    if(!infos){ *c=1; return NVML_SUCCESS; }
    if(*c >= 1){ infos[0].pid=getpid(); infos[0].usedGpuMemory=1024ULL*1024*1024; }
    *c=1; return NVML_SUCCESS;
}
nvmlReturn_t nvmlDeviceGetGraphicsRunningProcesses(nvmlDevice_t d, unsigned int* c, nvmlProcessInfo_t* infos){
    if(!infos){ *c=1; return NVML_SUCCESS; }
    if(*c >= 1){ infos[0].pid=getpid(); infos[0].usedGpuMemory=256ULL*1024*1024; }
    *c=1; return NVML_SUCCESS;
}
nvmlReturn_t nvmlDeviceGetComputeRunningProcesses(nvmlDevice_t d, unsigned int* c, nvmlProcessInfo_t* infos){
    return nvmlDeviceGetComputeRunningProcesses_v2(d,c,infos);
}

// === Macro helper untuk stub ===
#define STUB(fn) nvmlReturn_t fn(){ return NVML_SUCCESS; }

// === Stub semua API sisa ===
STUB(nvmlDeviceGetEncoderUtilization)
STUB(nvmlGetBlacklistDeviceInfoByIndex)
STUB(nvmlVgpuInstanceGetAccountingStats)
STUB(nvmlVgpuInstanceGetAccountingPids)
STUB(nvmlVgpuInstanceGetAccountingMode)
STUB(nvmlDeviceGetProcessUtilization)
STUB(nvmlVgpuInstanceGetFBCSessions)
STUB(nvmlVgpuInstanceGetEncoderSessions)
STUB(nvmlVgpuInstanceGetEncoderStats)
STUB(nvmlDeviceGetVgpuProcessUtilization)
STUB(nvmlDeviceGetInforomImageVersion)
STUB(nvmlDeviceGetHandleByPciBusId_v2)
STUB(nvmlDeviceGetTemperatureThreshold)
STUB(nvmlDeviceGetPowerManagementLimit)
STUB(nvmlDeviceGetPowerManagementMode)
STUB(nvmlDeviceGetTotalEnergyConsumption)
STUB(nvmlDeviceGetDetailedEccErrors)
STUB(nvmlDeviceGetGridLicensableFeatures_v2)
STUB(nvmlDeviceGetGridLicensableFeatures)
STUB(nvmlVgpuInstanceSetEncoderCapacity)
STUB(nvmlVgpuInstanceGetEncoderCapacity)
STUB(nvmlVgpuInstanceGetFrameRateLimit)
STUB(nvmlVgpuInstanceGetLicenseStatus)
STUB(nvmlVgpuInstanceGetVmDriverVersion)
STUB(nvmlVgpuTypeGetMaxInstancesPerVm)
STUB(nvmlVgpuTypeGetNumDisplayHeads)
STUB(nvmlVgpuTypeGetFramebufferSize)
STUB(nvmlDeviceSetVirtualizationMode)
STUB(nvmlDeviceGetVirtualizationMode)
STUB(nvmlDeviceResetNvLinkUtilizationCounter)
STUB(nvmlDeviceFreezeNvLinkUtilizationCounter)
STUB(nvmlDeviceGetNvLinkUtilizationCounter)
STUB(nvmlDeviceGetNvLinkUtilizationControl)
STUB(nvmlDeviceSetNvLinkUtilizationControl)
STUB(nvmlDeviceResetNvLinkErrorCounters)
STUB(nvmlDeviceGetNvLinkErrorCounter)
STUB(nvmlDeviceGetNvLinkRemotePciInfo_v2)
STUB(nvmlDeviceGetNvLinkRemotePciInfo)
STUB(nvmlDeviceGetTopologyNearestGpus)
STUB(nvmlDeviceGetTopologyCommonAncestor)
STUB(nvmlDeviceGetPcieReplayCounter)
STUB(nvmlDeviceGetRetiredPagesPendingStatus)
STUB(nvmlDeviceGetAccountingBufferSize)
STUB(nvmlDeviceGetSupportedClocksThrottleReasons)
STUB(nvmlDeviceGetCurrentClocksThrottleReasons)
STUB(nvmlDeviceSetPowerManagementLimit)
STUB(nvmlDeviceGetPowerManagementDefaultLimit)
STUB(nvmlDeviceGetPowerManagementLimitConstraints)
STUB(nvmlDeviceSetDefaultAutoBoostedClocksEnabled)
STUB(nvmlDeviceSetAutoBoostedClocksEnabled)
STUB(nvmlDeviceGetAutoBoostedClocksEnabled)
STUB(nvmlDeviceGetSupportedGraphicsClocks)
STUB(nvmlDeviceGetSupportedMemoryClocks)
STUB(nvmlDeviceResetApplicationsClocks)
STUB(nvmlDeviceGetDefaultApplicationsClock)
STUB(nvmlDeviceGetApplicationsClock)
STUB(nvmlDeviceSetApplicationsClocks)
STUB(nvmlDeviceResetGpuLockedClocks)
STUB(nvmlDeviceGetMemoryErrorCounter)
STUB(nvmlDeviceGetInforomConfigurationChecksum)
STUB(nvmlDeviceGetMPSComputeRunningProcesses)
STUB(nvmlDeviceGetSupportedEventTypes)
STUB(nvmlInternalGetExportTable)
STUB(nvmlDeviceSetComputeMode)
STUB(nvmlDeviceGetComputeMode)
STUB(nvmlSetVgpuVersion)
STUB(nvmlGetVgpuVersion)
STUB(nvmlGetBlacklistDeviceCount)
STUB(nvmlVgpuInstanceGetFBCStats)
STUB(nvmlDeviceGetFieldValues)
STUB(nvmlDeviceDiscoverGpus)
STUB(nvmlDeviceGetBoardId)
STUB(nvmlDeviceGetEccMode)
STUB(nvmlDeviceGetDisplayMode)
STUB(nvmlDeviceGetHandleByUUID)
STUB(nvmlDeviceGetHandleBySerial)
STUB(nvmlDeviceGetPowerState)
STUB(nvmlDeviceGetViolationStatus)
STUB(nvmlDeviceSetPersistenceMode)
STUB(nvmlDeviceGetPersistenceMode)
STUB(nvmlDeviceClearCpuAffinity)
STUB(nvmlDeviceSetCpuAffinity)
STUB(nvmlDeviceGetCpuAffinity)
STUB(nvmlDeviceGetBoardPartNumber)
STUB(nvmlDeviceGetBrand)
STUB(nvmlDeviceClearEccErrorCounts)
STUB(nvmlDeviceSetEccMode)
STUB(nvmlDeviceGetTotalEccErrors)
STUB(nvmlDeviceGetMultiGpuBoard)
STUB(nvmlDeviceRemoveGpu_v2)
STUB(nvmlDeviceRemoveGpu)
STUB(nvmlDeviceQueryDrainState)
STUB(nvmlDeviceModifyDrainState)
STUB(nvmlDeviceGetFBCSessions)
STUB(nvmlDeviceGetFBCStats)
STUB(nvmlDeviceGetEncoderSessions)
STUB(nvmlDeviceGetEncoderStats)
STUB(nvmlDeviceGetEncoderCapacity)
STUB(nvmlGetVgpuCompatibility)
STUB(nvmlDeviceGetVgpuMetadata)
STUB(nvmlVgpuInstanceGetMetadata)
STUB(nvmlDeviceGetVgpuUtilization)
STUB(nvmlVgpuInstanceGetType)
STUB(nvmlVgpuInstanceGetFbUsage)
STUB(nvmlVgpuInstanceGetUUID)
STUB(nvmlVgpuInstanceGetVmID)
STUB(nvmlDeviceGetActiveVgpus)
STUB(nvmlVgpuTypeGetMaxInstances)
STUB(nvmlVgpuTypeGetFrameRateLimit)
STUB(nvmlVgpuTypeGetLicense)
STUB(nvmlVgpuTypeGetResolution)
STUB(nvmlVgpuTypeGetDeviceID)
STUB(nvmlVgpuTypeGetName)
STUB(nvmlVgpuTypeGetClass)
STUB(nvmlDeviceGetCreatableVgpus)
STUB(nvmlDeviceGetSupportedVgpus)
STUB(nvmlDeviceGetNvLinkCapability)
STUB(nvmlDeviceGetNvLinkVersion)
STUB(nvmlDeviceGetP2PStatus)
STUB(nvmlDeviceGetNvLinkState)
STUB(nvmlSystemGetTopologyGpuSet)
STUB(nvmlDeviceGetPcieThroughput)
STUB(nvmlDeviceGetSamples)
STUB(nvmlDeviceGetMinorNumber)
STUB(nvmlDeviceGetAPIRestriction)
STUB(nvmlDeviceSetAPIRestriction)
STUB(nvmlDeviceGetRetiredPages_v2)
STUB(nvmlDeviceGetRetiredPages)
STUB(nvmlDeviceGetAccountingPids)
STUB(nvmlDeviceGetAccountingStats)
STUB(nvmlDeviceClearAccountingPids)
STUB(nvmlDeviceSetAccountingMode)
STUB(nvmlDeviceGetAccountingMode)
STUB(nvmlDeviceGetIndex)
STUB(nvmlDeviceGetClock)
STUB(nvmlDeviceSetGpuLockedClocks)
STUB(nvmlDeviceGetDisplayActive)
STUB(nvmlDeviceSetGpuOperationMode)
STUB(nvmlDeviceGetGpuOperationMode)
STUB(nvmlDeviceValidateInforom)
STUB(nvmlDeviceOnSameBoard)
STUB(nvmlSystemGetProcessName)
STUB(nvmlEventSetFree)
STUB(nvmlEventSetWait)
STUB(nvmlDeviceRegisterEvents)
STUB(nvmlEventSetCreate)
STUB(nvmlSystemGetHicVersion)
STUB(nvmlDeviceGetBridgeChipInfo)
STUB(nvmlDeviceGetVbiosVersion)
STUB(nvmlUnitGetDevices)
STUB(nvmlUnitGetUnitInfo)
STUB(nvmlUnitGetTemperature)
STUB(nvmlUnitGetPsuInfo)
STUB(nvmlUnitSetLedState)
STUB(nvmlUnitGetLedState)
STUB(nvmlUnitGetHandleByIndex)
STUB(nvmlUnitGetFanSpeedInfo)
STUB(nvmlUnitGetCount)
