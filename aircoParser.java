import src.AirconStat;
import src.AirconStatCoder;

public class aircoParser {

    public static void main(String[] args) {

        AirconStat stat = AirconStatCoder.fromBase64(new AirconStat(),
                "AACqn6j/AAAAAAAUCgAAAAAAAf/////CzoAECBcojQAAiAAABAAAAAAAAAKAII3/gBCP/7Rw");

        System.out.println("Indoor Temp:\t\t" + stat.getIndoorTemp() + " °C");
        System.out.println("Outdoor Temp:\t\t" + stat.getOutdoorTemp() + " °C");
        System.out.println("Is Vacant:\t\t" + stat.isVacantProperty());
        System.out.println("Is Auto Heating:\t" + stat.isAutoHeating());
    }
}