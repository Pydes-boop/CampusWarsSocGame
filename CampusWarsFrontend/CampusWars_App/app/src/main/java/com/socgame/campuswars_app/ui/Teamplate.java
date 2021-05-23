package com.socgame.campuswars_app.ui;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.os.Bundle;

import com.socgame.campuswars_app.R;

public class Teamplate extends Activity//AppCompatActivity
{

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_teamplate);
    }
}