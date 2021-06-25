package com.socgame.campuswars_app.ui;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;

import com.socgame.campuswars_app.R;
/*
    This is the start / splash screen
    It shows the logo for a few seconds before automatically switching to the login screen
    In the future we might want to call some setup methods here

    written by Jonas (so far)
 */
public class LoadingActivity extends AppCompatActivity
{

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_loading);

        ImageView logo = (ImageView) findViewById(R.id.logo);
        int imageResource = getResources().getIdentifier("@drawable/main_campus_wars_logo", null, this.getPackageName());
        logo.setImageResource(imageResource);
        
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