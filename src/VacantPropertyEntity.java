package src;

public class VacantPropertyEntity {
    private boolean isVacantProperty;
    private double vacantPropertyAutoTemp = 25.0d;
    private double vacantPropertyCoolTemp = 31.0d;
    private double vacantPropertyDryTemp = 25.0d;
    private double vacantPropertyHotTemp = 10.0d;
    private int vacantPropertyOperationMode = 2;

    public VacantPropertyEntity() {
    }

    public VacantPropertyEntity(boolean z, int i, double d, double d2, double d3, double d4) {
        this.isVacantProperty = z;
        this.vacantPropertyOperationMode = i;
        this.vacantPropertyCoolTemp = d;
        this.vacantPropertyHotTemp = d2;
        this.vacantPropertyAutoTemp = d3;
        this.vacantPropertyDryTemp = d4;
    }

    public boolean isVacantProperty() {
        return this.isVacantProperty;
    }

    public void setVacantProperty(boolean z) {
        this.isVacantProperty = z;
    }

    public int getVacantPropertyOperationMode() {
        return this.vacantPropertyOperationMode;
    }

    public void setVacantPropertyOperationMode(int i) {
        this.vacantPropertyOperationMode = i;
    }

    public double getVacantPropertyCoolTemp() {
        return this.vacantPropertyCoolTemp;
    }

    public void setVacantPropertyCoolTemp(double d) {
        this.vacantPropertyCoolTemp = d;
    }

    public double getVacantPropertyHotTemp() {
        return this.vacantPropertyHotTemp;
    }

    public void setVacantPropertyHotTemp(double d) {
        this.vacantPropertyHotTemp = d;
    }

    public double getVacantPropertyAutoTemp() {
        return this.vacantPropertyAutoTemp;
    }

    public void setVacantPropertyAutoTemp(double d) {
        this.vacantPropertyAutoTemp = d;
    }

    public double getVacantPropertyDryTemp() {
        return this.vacantPropertyDryTemp;
    }

    public void setVacantPropertyDryTemp(double d) {
        this.vacantPropertyDryTemp = d;
    }
}
