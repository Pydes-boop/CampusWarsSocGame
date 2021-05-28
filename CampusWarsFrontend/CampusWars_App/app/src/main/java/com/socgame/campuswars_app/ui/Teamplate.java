package com.socgame.campuswars_app.ui;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;

import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.socgame.campuswars_app.R;
import com.socgame.campuswars_app.communication.HttpReturn;
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
    }
}