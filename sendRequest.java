import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.ObjectInputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLConnection;
import java.nio.charset.StandardCharsets;

public class sendRequest {
    public static String getAircoStat() {
        try {
            URL url = new URL("http://192.168.178.206:51443/beaver/command/getAirconStat");
            URLConnection con = url.openConnection();
            HttpURLConnection http = (HttpURLConnection) con;
            http.setRequestMethod("POST"); // PUT is another valid option
            http.setDoOutput(true);
            byte[] out = "{\"apiVer\":\"1.0\",\"command\":\"getAirconStat\",\"deviceId\":\"1234567890ABCDEF\",\"operatorId\":\"d2bc4571-1cea-4858-b0f2-34c18bef1901\",\"timestamp\":1649703587}"
                    .getBytes(StandardCharsets.UTF_8);
            int length = out.length;

            http.setFixedLengthStreamingMode(length);
            http.setRequestProperty("Content-Type", "application/json; charset=UTF-8");
            http.connect();

            try (OutputStream os = http.getOutputStream()) {
                os.write(out);
            }

            InputStreamReader isReader = new InputStreamReader(http.getInputStream());
            // Creating a BufferedReader object
            BufferedReader reader = new BufferedReader(isReader);
            StringBuffer sb = new StringBuffer();
            String str;
            while ((str = reader.readLine()) != null) {
                sb.append(str);
            }

            return "response: " + sb.toString();
        } catch (Exception ex) {
            System.out.println(ex.getMessage());
        }

        return "empty";
    }
}
