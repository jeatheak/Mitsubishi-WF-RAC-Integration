import src.AirconStat;
import src.AirconStatCoder;
import src.refactor.SmallDecoder;

public class aircoParser {

    public static void main(String[] args) {

        // System.out.println(sendRequest.getAircoStat());

        parseAirco("AACqj6j/AAAAAAAQCgAAAAAAAf////9FqIAECAcojgAAiAAAAAAAAAAAAAOAII7/gBCW/5QQAADrgg==");
    }

    private static void parseAirco(String input) {
        AirconStat stat = SmallDecoder.fromBase64(new AirconStat(), input);

        System.out.println("Indoor Temp:\t\t" + stat.getIndoorTemp() + " C");
        System.out.println("Outdoor Temp:\t\t" + stat.getOutdoorTemp() + " C");
        System.out.println("Preset Temp:\t\t" + stat.getPresetTemp());
        System.out.println("Operation:\t\t" + stat.getOperation());
        System.out.println("Operation Mode:\t\t" + stat.getOperationMode());
        System.out.println("Air Flow:\t\t" + stat.getAirFlow());
        System.out.println("Direction UP/DOWN:\t" + stat.getWindDirectionUD());
        System.out.println("Direction LEFT/RIGHT:\t" + stat.getWindDirectionLR());
        System.out.println("3D Auto:\t\t" + stat.getEntrust());
        System.out.println("Error Code:\t\t" + stat.getErrorCode());
        System.out.println("Electric:\t\t" + stat.getElectric());
    }
}