package com.socgame.campuswars_app.ui;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;

import com.socgame.campuswars_app.R;

public class LoadingActivity extends AppCompatActivity
{
    /**
     *     This is the start / splash screen
     *     It shows the logo for a few seconds before automatically switching to the login screen
     *     In the future we might want to call some setup methods here
     *
     *     We check if the User is already logged in/registered and if they are we go directly to the main screen
     *
     *     written by Jonas and Daniel
     */

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_loading);
        Context ctx = this.getApplicationContext();

        //Setting Logo this way so we dont get weird Android Compression
        ImageView logo = (ImageView) findViewById(R.id.logo);
        int imageResource = getResources().getIdentifier("@drawable/main_campus_wars_logo", null, this.getPackageName());
        logo.setImageResource(imageResource);

        //Getting Logged in State
        SharedPreferences settings = ctx.getSharedPreferences("userdata", 0);
        boolean loggedIn = settings.getBoolean("loggedIn", false);
        
        //Only for Debug
        Button next = (Button) findViewById(R.id.LoadingText);
        next.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                Intent myIntent = new Intent(view.getContext(), LoginActivity.class);
                startActivityForResult(myIntent, 0);
            }
        });

        //TODO Add possible preloading Data here
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
                    if(loggedIn){
                        Intent myIntent = new Intent(LoadingActivity.this, MainScreenActivity.class);
                        startActivityForResult(myIntent, 0);
                    }else{
                        Intent myIntent = new Intent(LoadingActivity.this, LoginActivity.class);
                        startActivityForResult(myIntent, 0);
                    }
                }
            }
            , 1000
        );
    }
}