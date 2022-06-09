public class test {
    public static void main(String[] args) {
        AirconStat stat = new AirconStat();

        String data = AirconStatCoder.toBase64(stat);

        System.out.println(data);
    }
}
