package com.socgame.campuswars_app.communication;

import android.content.Context;
import android.util.Log;

import com.android.volley.Response;
import com.android.volley.VolleyError;

import org.json.JSONObject;

import fr.arnaudguyon.xmltojsonlib.XmlToJson;

public class CampusCom {
    private static String pToken = "INSERTTOKENHERE";
    private static Context ctx;
    private static CampusCom instance;

    private CampusCom(Context context) {
        ctx = context;
    }

    public static synchronized CampusCom getInstance(Context context) {
        if (instance == null) {
            instance = new CampusCom(context);
        }
        return instance;
    }

    public void test() {
        HttpSingleton http = HttpSingleton.getInstance(this.ctx);
        http.setUrl("https://campus.tum.de/");
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
