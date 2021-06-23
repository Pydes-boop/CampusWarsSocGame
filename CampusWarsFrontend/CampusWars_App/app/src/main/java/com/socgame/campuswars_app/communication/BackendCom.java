package com.socgame.campuswars_app.communication;

import android.content.Context;
import android.content.SharedPreferences;
import android.util.Log;

import com.android.volley.Response;
import com.android.volley.VolleyError;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class BackendCom {
    private static Context ctx;
    private static HttpSingleton http;
    private static BackendCom instance;

    private BackendCom(Context ctx){
        this.ctx = ctx;
        this.http = HttpSingleton.getInstance(ctx);
    }

    public static synchronized BackendCom getInstance(Context context) {
        if (instance == null) {
            instance = new BackendCom(context);
        }
        return instance;
    }

    public void FirebaseRegister(String UID){
        SharedPreferences settings = ctx.getSharedPreferences("userdata", 0);
        SharedPreferences.Editor editor = settings.edit();
        editor.putString("UID", UID);
        // Apply the edits!
        editor.apply();

        //Overwriting our Variables so we can use it in other methods easily
        UID = settings.getString("UID", "empty");
    }

    public void echo(){
        http.getRequestString("/v1/echo", new Response.Listener<String>() {
            @Override
            public void onResponse(String Response) {
                //On Response
                if(Response.toString().contains("Hallo Echo!")){
                    Log.d("HTTP", "Success Echo: " + Response.toString());
                } else {
                    Log.d("HTTP", "Fail Echo: " + Response.toString());
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

    public void register(){
        HttpHeader head = new HttpHeader();
        try {
            http.postRequest("groups",head.getHeaders(), new Response.Listener<JSONArray>() {
                @Override
                public void onResponse(JSONArray Response) {
                    //On Response
                    //Handle Data
                    Log.d("HTTP", "Success: " + Response.toString());
                }
            }, new Response.ErrorListener() {
                @Override
                public void onErrorResponse(VolleyError error) {
                    //Error Handling
                    Log.d("HTTP", "Error: " + error.getMessage());
                }
            });
        } catch (JSONException e) {
            Log.d("Error in Register:", e.toString());
        }
    }

    public void groups(JSONObject lectures){
        HttpHeader head = new HttpHeader();

        try {
            head.buildPersonalLecturesHeader(lectures);
            http.postRequest("groups",head.getHeaders(), new Response.Listener<JSONArray>() {
                @Override
                public void onResponse(JSONArray Response) {
                    //On Response
                    //Handle Data
                    Log.d("HTTP", "Success: " + Response.toString());
                }
            }, new Response.ErrorListener() {
                @Override
                public void onErrorResponse(VolleyError error) {
                    //Error Handling
                    Log.d("HTTP", "Error: " + error.getMessage());
                }
            });
        } catch (JSONException e) {
            Log.d("Error in Register:", e.toString());
        }
    }

    public boolean roomDetection(){
        //empty method stub
        //roomDetection needs to be directly done in the activity as we want to instantly use the data when we get it
        return false;
    }

    public boolean quiz(){
        //empty method stub
        //quiz needs to be directly done in the activity as we want to instantly use the data when we get it
        return false;
    }


}
