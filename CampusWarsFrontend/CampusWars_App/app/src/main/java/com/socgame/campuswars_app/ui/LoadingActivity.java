package com.socgame.campuswars_app.ui;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.socgame.campuswars_app.R;
import com.socgame.campuswars_app.communication.BackendCom;
import com.socgame.campuswars_app.communication.CampusCom;
import com.socgame.campuswars_app.communication.HttpSingleton;

import org.json.JSONObject;
import org.json.XML;
import org.json.JSONException;

import org.json.JSONArray;
import org.xml.sax.XMLReader;

import javax.xml.parsers.DocumentBuilderFactory;

import fr.arnaudguyon.xmltojsonlib.XmlToJson;

public class LoadingActivity extends AppCompatActivity
{

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_loading);

        //BackendCom com = BackendCom.getInstance(this.getApplicationContext());
        //com.echo();
        //CampusCom comCampus = CampusCom.getInstance(this.getApplicationContext());
        //com.generateToken("ge75lod");
        //comCampus.getLectures();

        
        //Only for Debug
        Button next = (Button) findViewById(R.id.LoadingText);
        next.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                Intent myIntent = new Intent(view.getContext(), LoginActivity.class);
                startActivityForResult(myIntent, 0);
            }
        });


        //There should be actual loading happening here
        //TODO: maybe establish http connection or something


        //Mock Up Loading
        //Just waits before it changes the screen

        Handler handler = new Handler();
        handler.postDelayed
        (
            new Runnable()
            {
                @Override
                public void run()
                {
                    Intent myIntent = new Intent(LoadingActivity.this, LoginActivity.class);
                    startActivityForResult(myIntent, 0);
                }
            }
            , 1000
        );
    }
}