package src;

public class AirconStat {
    private int airFlow;
    private boolean canHomeLeaveModeStatusRequest = false;
    private int coolHotJudge = 1;
    private double electric = -1.0d;
    private int entrust;
    private String errorCode = "";
    private double indoorTemp = Double.longBitsToDouble(1);
    private boolean isAutoHeating = false;
    private boolean isSelfCleanOperation;
    private boolean isSelfCleanReset;
    private boolean isVacantProperty;
    private int modelNo;
    private int operation;
    private int operationMode;
    private double outdoorTemp = Double.longBitsToDouble(1);
    private double presetTemp;
    private int windDirectionLR;
    private int windDirectionUD;

    public AirconStat() {
    }

    public AirconStat(Aircon aircon) {
        this.operation = aircon.getOperation();
        this.operationMode = aircon.getPresetOperationMode();
        this.presetTemp = aircon.getPresetTemp();
        this.airFlow = aircon.getAirFlow();
        this.windDirectionUD = aircon.getWindDirectionUD();
        this.windDirectionLR = aircon.getWindDirectionLR();
        this.entrust = aircon.getEntrust();
        this.modelNo = aircon.getModelNo();
        this.isSelfCleanOperation = aircon.isSelfCleanOperation();
        this.isSelfCleanReset = aircon.isSelfCleanReset();
        this.isVacantProperty = aircon.getVacantProperty().isVacantProperty();
        this.isAutoHeating = aircon.isAutoHeating();
    }

    public int getOperation() {
        return this.operation;
    }

    public int getOperationMode() {
        return this.operationMode;
    }

    public double getPresetTemp() {
        return this.presetTemp;
    }

    public int getAirFlow() {
        return this.airFlow;
    }

    public int getWindDirectionUD() {
        return this.windDirectionUD;
    }

    public int getWindDirectionLR() {
        return this.windDirectionLR;
    }

    public int getEntrust() {
        return this.entrust;
    }

    public String getErrorCode() {
        return this.errorCode;
    }

    public double getOutdoorTemp() {
        return this.outdoorTemp;
    }

    public double getIndoorTemp() {
        return this.indoorTemp;
    }

    public double getElectric() {
        return this.electric;
    }

    public void setOperation(int i) {
        this.operation = i;
    }

    public void setOperationMode(int i) {
        this.operationMode = i;
    }

    public void setPresetTemp(double d) {
        this.presetTemp = d;
    }

    public void setAirFlow(int i) {
        this.airFlow = i;
    }

    public void setWindDirectionUD(int i) {
        this.windDirectionUD = i;
    }

    public void setWindDirectionLR(int i) {
        this.windDirectionLR = i;
    }

    public void setEntrust(int i) {
        this.entrust = i;
    }

    public void setErrorCode(String str) {
        this.errorCode = str;
    }

    public void setOutdoorTemp(double d) {
        this.outdoorTemp = d;
    }

    public void setIndoorTemp(double d) {
        this.indoorTemp = d;
    }

    public void setElectric(double d) {
        this.electric = d;
    }

    public int getCoolHotJudge() {
        return this.coolHotJudge;
    }

    public void setCoolHotJudge(int i) {
        this.coolHotJudge = i;
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

    public boolean isAutoHeating() {
        return this.isAutoHeating;
    }

    public void setAutoHeating(boolean z) {
        this.isAutoHeating = z;
    }

    public boolean canHomeLeaveModeStatusRequest() {
        return this.canHomeLeaveModeStatusRequest;
    }

    public void setCanHomeLeaveModeStatusRequest(boolean z) {
        this.canHomeLeaveModeStatusRequest = z;
    }

    public boolean isVacantProperty() {
        return this.isVacantProperty;
    }

    public void setVacantProperty(boolean z) {
        this.isVacantProperty = z;
    }
}
