package com.socgame.campuswars_app.communication;

import android.content.Context;
import android.content.SharedPreferences;
import android.util.Log;

import com.android.volley.Response;
import com.android.volley.VolleyError;

import org.json.JSONObject;

import java.security.NoSuchAlgorithmException;
import java.security.NoSuchProviderException;
import java.util.Map;

import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;

import fr.arnaudguyon.xmltojsonlib.XmlToJson;

public class CampusCom {
    private static String pToken;
    private static String tumId;
    private static Context ctx;
    private static CampusCom instance;

    private static HttpSingleton http;

    private Map<String, String> params;
    private String[] lectures;

    private CampusCom(Context context) {
        this.ctx = context;
        // Get from the SharedPreferences
        SharedPreferences settings = ctx.getSharedPreferences("userdata", 0);
        this.pToken = settings.getString("pToken", "empty");
        this.tumId = settings.getString("tumId", "empty");
        this.http = HttpSingleton.getInstance(this.ctx);
    }

    public static synchronized CampusCom getInstance(Context context) {
        if (instance == null) {
            instance = new CampusCom(context);
        }
        return instance;
    }

    public void saveUserData(String tumId, String pToken){
        //This is not the safest way to store User Data, but it should work
        //Saving User Data:
        SharedPreferences settings = ctx.getSharedPreferences("userdata", 0);
        SharedPreferences.Editor editor = settings.edit();
        editor.putString("tumId", tumId);
        editor.putString("pToken", pToken);
        // Apply the edits!
        editor.apply();

        //Overwriting our Variables so we can use it in other methods easily
        this.pToken = settings.getString("pToken", "empty");
        this.tumId = settings.getString("tumId", "empty");
    }

    public String generateSecret(){
        //DONE Secret Generation
        //We just use key.toString() because we dont care
        //Not knowing the key is the most secure method and we dont need data like matr Number anyways
        KeyGenerator kg = null;
        try {
            kg = KeyGenerator.getInstance("AES");
        } catch (Exception e) {
            Log.d("HTTP", "Secret Key generation failed: " + e.toString());
        }
        kg.init(128);
        SecretKey key = kg.generateKey();
        //We honestly dont care about the Key here because we dont need it anyways
        //The securest encryption is the one we dont know
        return key.toString();
    }

    public HttpSingleton getHttp(){
        return http;
    }

    public void generateToken(String Id, Response.Listener<String> listener, Response.ErrorListener error){
        //You should only call this Method once

        //Campus com now gets the general instance of Http Singleton
        //HttpSingleton http = HttpSingleton.getInstance(this.ctx);
        http.getRequestString("tumonline/wbservicesbasic.requestToken?pUsername=" + Id + "&pTokenName=CampusWarsApp", listener, error, true);
    }

    public void getLectures(){
        //https://campus.tum.de/tumonline/wbservicesbasic.veranstaltungenEigene?pToken=pToken

        //Campus com now gets the general instance of Http Singleton
        //HttpSingleton http = HttpSingleton.getInstance(this.ctx);
        http.getRequestString("tumonline/wbservicesbasic.veranstaltungenEigene?pToken=" + pToken, new Response.Listener<String>() {
            @Override
            public void onResponse(String Response) {
                //Remove Log.d ?
                Log.d("HTTP", "Success: " + Response);

                try {
                    XmlToJson xmlToJson = new XmlToJson.Builder(Response).build();
                    JSONObject lectures = xmlToJson.toJson();

                    HttpHeader head = new HttpHeader(ctx);

                    BackendCom bCom = BackendCom.getInstance(ctx);
                    bCom.groups(lectures);

                    Log.d("HTTP", "Success: " + "converted JSON Object and gave it to HTTP Header");
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

    public void getLectureTime(){
        //TODO besprechen --> sehr kompliziert hierfür vlt erstmal eine andere lösung suchen?
        //Vorlesungs basierte Fragen erstmal lassen und fragen nur location basiert machen?
    }

    //Test this with
    //CampusCom com = CampusCom.getInstance(this.getApplicationContext());
    //com.generateToken("ge75lod");
    //com.getLectures();

}
