package com.socgame.campuswars_app.ui;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;

import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.socgame.campuswars_app.R;
import com.socgame.campuswars_app.communication.HttpSingleton;

import org.json.JSONArray;
import org.json.JSONException;

import java.util.HashMap;

public class Teamplate extends Activity//AppCompatActivity
{

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_teamplate);

        //Test for Http Singleton get
        HttpSingleton http = HttpSingleton.getInstance(this.getApplicationContext());
        JSONArray response = null;
        http.getRequest("v1/quiz", new Response.Listener<JSONArray>() {
        @Override
        public void onResponse(JSONArray Response) {
            Log.d("HTTP", "Success: " + Response.toString());
        }
         }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                //Error Handling
                Log.d("HTTP", "Error: " + error.getMessage());
            }
        });

        //Test for Http Singleton post
        response = null;
        try {
            http.postRequest("v1/roomdetection", new Response.Listener<JSONArray>() {
                @Override
                public void onResponse(JSONArray Response) {
                    Log.d("HTTP", "Success: " + Response.toString());
                }
            }, new Response.ErrorListener() {
                @Override
                public void onErrorResponse(VolleyError error) {
                    //Error Handling
                    Log.d("HTTP", "Error: " + error.getMessage());
                }
            });
        } catch (Exception e){
            Log.d("Exception", e.toString());
        }

    }
}