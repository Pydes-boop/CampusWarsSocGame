package com.socgame.campuswars_app.communication;

import java.io.DataOutputStream;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;

public class HttpHandler {
    //Reference: https://www.baeldung.com/java-http-request
    private URL url;
    private HttpURLConnection con;

    public HttpHandler(String url){
        try {
            //TODO Add URL
            this.url = new URL("http://example.com");
            //opens connection
            this.con = (HttpURLConnection) this.url.openConnection();
            //con.disconnect();
            //Test
            this.con.setRequestMethod("GET");
        } catch (Exception e) {
            //TODO EXCEPTION HANDLING
            e.printStackTrace();
        }
        //Set max Timeout to 5 Seconds
        this.con.setConnectTimeout(5000);
        this.con.setReadTimeout(5000);
    }

    public URL getUrl() {
        return this.url;
    }

    public HttpURLConnection getCon() {
        return this.con;
    }

    public void HttpTesting(){
        Map<String, String> parameters = new HashMap<>();
        parameters.put("param1", "val");

        try {
            con.setDoOutput(true);
            DataOutputStream out = new DataOutputStream(con.getOutputStream());
            out.writeBytes(ParameterStringBuilder.getParamsString(parameters));
            out.flush();
            out.close();
        } catch (Exception e) {
            //TODO EXCEPTION HANDLING
            e.printStackTrace();
        }



    }
}
