package src;

public class Aircon {
    private int airFlow;
    private int airconDisplayOrder;
    private String airconId;
    private String airconName;
    private double autoTemp;
    private double coolTemp;
    private int coolingOnly;
    private double dryTemp;
    private int entrust;
    private String errorCode;
    private String firmType;
    private double hotTemp;
    private double indoorTemp;
    private boolean isAutoHeatintg = false;
    private boolean isInaccurateOutdoorTemp;
    private boolean isSelfCleanOperation;
    private boolean isSelfCleanReset;
    private boolean isTimerSetting = false;
    private double latitude;
    private double longitude;
    private String mcuFirmVer;
    private int modelNo;
    private int operation;
    private int operationMode;
    private double outdoorTemp;
    private Integer result;
    private long statReceiveDate;
    private Integer timestamp;
    private boolean updateFlag;
    private VacantPropertyEntity vacantProperty = new VacantPropertyEntity();
    private int windDirectionLR;
    private int windDirectionUD;
    private String wirelessFirmVer;

    public Aircon() {
    }

    public Aircon(String str, String str2, int i, int i2, double d, double d2, double d3, double d4, int i3, int i4,
            int i5, double d5, double d6, int i6, int i7, boolean z, VacantPropertyEntity vacantPropertyEntity) {
        this.airconId = str;
        this.airconName = str2;
        this.operation = i;
        this.operationMode = i2;
        this.autoTemp = d;
        this.coolTemp = d2;
        this.hotTemp = d3;
        this.dryTemp = d4;
        this.airFlow = i3;
        this.windDirectionUD = i4;
        this.windDirectionLR = i5;
        this.indoorTemp = d5;
        this.outdoorTemp = d6;
        this.entrust = i6;
        this.modelNo = i7;
        this.isSelfCleanOperation = z;
        this.vacantProperty = vacantPropertyEntity;
    }

    public String getAirconId() {
        return this.airconId;
    }

    public void setAirconId(String str) {
        this.airconId = str;
    }

    public int getAirconDisplayOrder() {
        return this.airconDisplayOrder;
    }

    public void setAirconDisplayOrder(int i) {
        this.airconDisplayOrder = i;
    }

    public String getAirconName() {
        return this.airconName;
    }

    public void setAirconName(String str) {
        this.airconName = str;
    }

    public int getCoolingOnly() {
        return this.coolingOnly;
    }

    public void setCoolingOnly(int i) {
        this.coolingOnly = i;
    }

    public int getOperation() {
        return this.operation;
    }

    public void setOperation(int i) {
        this.operation = i;
    }

    public int getOperationMode() {
        return this.operationMode;
    }

    public void setOperationMode(int i) {
        this.operationMode = i;
    }

    public double getAutoTemp() {
        return this.autoTemp;
    }

    public void setAutoTemp(double d) {
        this.autoTemp = d;
    }

    public double getCoolTemp() {
        return this.coolTemp;
    }

    public void setCoolTemp(double d) {
        this.coolTemp = d;
    }

    public double getHotTemp() {
        return this.hotTemp;
    }

    public void setHotTemp(double d) {
        this.hotTemp = d;
    }

    public double getDryTemp() {
        return this.dryTemp;
    }

    public void setDryTemp(double d) {
        this.dryTemp = d;
    }

    /* renamed from: jp.co.mhi_mth.smartmair.model.Aircon$1 */
    static /* synthetic */ class C11301 {

        /*
         * renamed from:
         * $SwitchMap$jp$co$mhi_mth$smartmair$util$Constants$TempSettingType
         */
        static final /* synthetic */ int[] f565x29ea2eab;

        static {
            int[] iArr = new int[Constants.TempSettingType.values().length];
            f565x29ea2eab = iArr;
            try {
                iArr[Constants.TempSettingType.VacantProperty.ordinal()] = 1;
            } catch (NoSuchFieldError unused) {
            }
        }
    }

    public void setPresetTemp(double d) {
        if (C11301.f565x29ea2eab[getTempSettingType().ordinal()] != 1) {
            int i = this.operationMode;
            if (i == 0) {
                this.autoTemp = d;
            } else if (i == 1) {
                this.coolTemp = d;
            } else if (i == 2) {
                this.hotTemp = d;
            } else if (i == 4) {
                this.dryTemp = d;
            }
        } else {
            int vacantPropertyOperationMode = this.vacantProperty.getVacantPropertyOperationMode();
            if (vacantPropertyOperationMode == 0) {
                this.vacantProperty.setVacantPropertyAutoTemp(d);
            } else if (vacantPropertyOperationMode == 1) {
                this.vacantProperty.setVacantPropertyCoolTemp(d);
            } else if (vacantPropertyOperationMode == 2) {
                this.vacantProperty.setVacantPropertyHotTemp(d);
            } else if (vacantPropertyOperationMode == 4) {
                this.vacantProperty.setVacantPropertyDryTemp(d);
            }
        }
    }

    public double getOperationModeTemp() {
        int i = this.operationMode;
        if (i == 0) {
            return this.autoTemp;
        }
        if (i == 1) {
            return this.coolTemp;
        }
        if (i == 2) {
            return this.hotTemp;
        }
        if (i != 4) {
            return 25.0d;
        }
        return this.dryTemp;
    }

    public int getAirFlow() {
        return this.airFlow;
    }

    public void setAirFlow(int i) {
        this.airFlow = i;
    }

    public int getWindDirectionUD() {
        return this.windDirectionUD;
    }

    public void setWindDirectionUD(int i) {
        this.windDirectionUD = i;
    }

    public int getWindDirectionLR() {
        return this.windDirectionLR;
    }

    public void setWindDirectionLR(int i) {
        this.windDirectionLR = i;
    }

    public double getIndoorTemp() {
        return this.indoorTemp;
    }

    public void setIndoorTemp(double d) {
        this.indoorTemp = d;
    }

    public double getOutdoorTemp() {
        return this.outdoorTemp;
    }

    public boolean isInaccurateOutdoorTemp() {
        return this.isInaccurateOutdoorTemp;
    }

    public void setInaccurateOutdoorTemp(boolean z) {
        this.isInaccurateOutdoorTemp = z;
    }

    public double getLatitude() {
        return this.latitude;
    }

    public void setLatitude(double d) {
        this.latitude = d;
    }

    public double getLongitude() {
        return this.longitude;
    }

    public void setLongitude(double d) {
        this.longitude = d;
    }

    public String getErrorCode() {
        return this.errorCode;
    }

    public void setErrorCode(String str) {
        this.errorCode = str;
    }

    public Integer getTimestamp() {
        return this.timestamp;
    }

    public void setTimestamp(Integer num) {
        this.timestamp = num;
    }

    public String getFirmType() {
        return this.firmType;
    }

    public void setFirmType(String str) {
        this.firmType = str;
    }

    public String getWirelessFirmVer() {
        return this.wirelessFirmVer;
    }

    public void setWirelessFirmVer(String str) {
        this.wirelessFirmVer = str;
    }

    public String getMcuFirmVer() {
        return this.mcuFirmVer;
    }

    public void setMcuFirmVer(String str) {
        this.mcuFirmVer = str;
    }

    public boolean isUpdateFlag() {
        return this.updateFlag;
    }

    public void setUpdateFlag(boolean z) {
        this.updateFlag = z;
    }

    public Integer getResult() {
        return this.result;
    }

    public void setResult(Integer num) {
        this.result = num;
    }

    public int getEntrust() {
        return this.entrust;
    }

    public void setEntrust(int i) {
        this.entrust = i;
    }

    public long getStatReceiveDate() {
        return this.statReceiveDate;
    }

    public void setStatReceiveDate(long j) {
        this.statReceiveDate = j;
    }

    public boolean isTimerSetting() {
        return this.isTimerSetting;
    }

    public void setTimerSetting(boolean z) {
        this.isTimerSetting = z;
    }

    public int getModelNo() {
        return this.modelNo;
    }

    public void setModelNo(int i) {
        this.modelNo = i;
    }

    public boolean isSelfCleanOperation() {
        return this.isSelfCleanOperation;
    }

    public void setSelfCleanOperation(boolean z) {
        this.isSelfCleanOperation = z;
    }

    public boolean isSelfCleanReset() {
        return this.isSelfCleanReset;
    }

    public void setSelfCleanReset(boolean z) {
        this.isSelfCleanReset = z;
    }

    public VacantPropertyEntity getVacantProperty() {
        return this.vacantProperty;
    }

    public void setVacantProperty(VacantPropertyEntity vacantPropertyEntity) {
        this.vacantProperty = vacantPropertyEntity;
    }

    public boolean isAutoHeating() {
        return this.isAutoHeatintg;
    }

    public void setAutoHeating(boolean z) {
        this.isAutoHeatintg = z;
    }

    private Constants.TempSettingType getTempSettingType() {
        if (this.modelNo == 1 && this.vacantProperty.isVacantProperty()) {
            return Constants.TempSettingType.VacantProperty;
        }
        return Constants.TempSettingType.Normal;
    }

    public int getPresetOperationMode() {
        if (C11301.f565x29ea2eab[getTempSettingType().ordinal()] != 1) {
            return this.operationMode;
        }
        return this.vacantProperty.getVacantPropertyOperationMode();
    }

    public void setPresetOperationMode(int i) {
        if (C11301.f565x29ea2eab[getTempSettingType().ordinal()] != 1) {
            this.operationMode = i;
        } else {
            this.vacantProperty.setVacantPropertyOperationMode(i);
        }
    }

    public double getPresetTemp() {
        if (C11301.f565x29ea2eab[getTempSettingType().ordinal()] != 1) {
            int i = this.operationMode;
            if (i == 0) {
                return this.autoTemp;
            }
            if (i == 1) {
                return this.coolTemp;
            }
            if (i == 2) {
                return this.hotTemp;
            }
            if (i != 4) {
                return 99.9d;
            }
            return this.dryTemp;
        }
        int vacantPropertyOperationMode = this.vacantProperty.getVacantPropertyOperationMode();
        if (vacantPropertyOperationMode == 0) {
            return this.vacantProperty.getVacantPropertyAutoTemp();
        }
        if (vacantPropertyOperationMode == 1) {
            return this.vacantProperty.getVacantPropertyCoolTemp();
        }
        if (vacantPropertyOperationMode == 2) {
            return this.vacantProperty.getVacantPropertyHotTemp();
        }
        if (vacantPropertyOperationMode != 4) {
            return 99.9d;
        }
        return this.vacantProperty.getVacantPropertyDryTemp();
    }
}
