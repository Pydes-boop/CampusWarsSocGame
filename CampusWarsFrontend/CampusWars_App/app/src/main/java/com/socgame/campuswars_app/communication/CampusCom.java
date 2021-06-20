package com.socgame.campuswars_app.communication;

import android.content.Context;
import android.util.Log;

import com.android.volley.Response;
import com.android.volley.VolleyError;

import org.json.JSONObject;

import java.util.Map;

import fr.arnaudguyon.xmltojsonlib.XmlToJson;

public class CampusCom {
    private static String pToken = "INSERTTOKENHERE";
    private static Context ctx;
    private static CampusCom instance;

    private Map<String, String> params;
    private String[] lectures;

    private CampusCom(Context context) {
        ctx = context;
    }

    public static synchronized CampusCom getInstance(Context context) {
        if (instance == null) {
            instance = new CampusCom(context);
        }
        return instance;
    }

    public void generateToken(String tumId){
        String test = "https://campus.tum.de/tumonline/wbservicesbasic.secretUpload?pToken=32DCF2A7D06330F56AB7956292A50E2C&pSecret=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDqFFH5SPie6PwptkuAL7dzgQaryN7ymRFRJOaN%250AeLz72mIkWnFQq0zxpQCm%252B1UOO0BgHLERPuI4m76p0%252F1elSJKVJDhL%252F6ewfuqbGKzNnmOYr3jPDUm%250AECPkKQDc2PTh9eqNx%252FbhvjT%252BGZS%252BHiOHflIqHweDojj%252BPmrkbvV5K7gDkQIDAQAB&pToken=32DCF2A7D06330F56AB7956292A50E2C";
        HttpSingleton http = HttpSingleton.getInstance(this.ctx);
        String response = null;
        http.getRequestString("tumonline/wbservicesbasic.requestToken?pUsername=" + tumId + "&pTokenName=CampusWarsApp", new Response.Listener<String>() {
            @Override
            public void onResponse(String Response) {
                Log.d("HTTP", "Success: " + Response);
                try {
                    XmlToJson xmlToJson = new XmlToJson.Builder(Response).build();
                    JSONObject jsonObject = xmlToJson.toJson();
                    //jsonObject = jsonObject.getJSONObject("rowset").getJSONObject("row");
                    pToken = jsonObject.get("token").toString();
                    Log.d("HTTP", "Success: Token must be activated via TumOnline");
                } catch (Exception e) {
                    Log.d("Failure to Convert", e.toString());
                }


                //Secret Upload
                //TODO: SECRET GENERATION

                http.getRequestString("tumonline/wbservicesbasic.secretUpload?pToken=" + pToken + "&pSecret=" + "INSERTSECRETHERE" + "&pToken=" + pToken, new Response.Listener<String>() {
                    @Override
                    public void onResponse(String Response) {
                        Log.d("HTTP", "Success: " + Response);
                        try {
                            XmlToJson xmlToJson = new XmlToJson.Builder(Response).build();
                            JSONObject jsonObject = xmlToJson.toJson();

                            //TODO HOW DO YOU COMPARE STRINGS?
                            if(jsonObject.get("confirmed").toString() == "true"){
                                Log.d("HTTP", "Success: Token is valid and Secret was uploaded");
                            }

                        } catch (Exception e) {
                            Log.d("Failure to Convert", e.toString());
                        }
                    }
                }, new Response.ErrorListener() {
                    @Override
                public void onErrorResponse(VolleyError error) {
                    //Error Handling
                    Log.d("HTTP", "Error: " + error.getMessage());
                }
                }, true);

            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                //Error Handling
                Log.d("HTTP", "Error: " + error.getMessage());
            }
        }, true);
    }

    public void getLectures(){
        //https://campus.tum.de/tumonline/wbservicesbasic.veranstaltungenEigene?pToken=pToken
        //TODO empty method stub
    }

    public void getLectureTime(){

        //TODO besprechen --> sehr kompliziert hierfür vlt erstmal eine andere lösung suchen?
        //Vorlesungs basierte Fragen erstmal lassen und fragen nur location basiert machen?
    }



    public void test() {
        HttpSingleton http = HttpSingleton.getInstance(this.ctx);
        String response = null;
        http.getRequestString("tumonline/wbservicesbasic.id?pToken=" + pToken, new Response.Listener<String>() {
            @Override
            public void onResponse(String Response) {
                Log.d("HTTP", "Success: " + Response);
                try {
                    XmlToJson xmlToJson = new XmlToJson.Builder(Response).build();
                    JSONObject jsonObject = xmlToJson.toJson();
                    jsonObject = jsonObject.getJSONObject("rowset").getJSONObject("row");
                    Log.d("HTTP", "Success: " + jsonObject.get("kennung").toString());
                } catch (Exception e) {
                    Log.d("Failure to Convert", e.toString());
                }
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                //Error Handling
                Log.d("HTTP", "Error: " + error.getMessage());
            }
        });
    }

}
