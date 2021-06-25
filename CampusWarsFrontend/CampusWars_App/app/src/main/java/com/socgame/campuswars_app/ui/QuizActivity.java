package com.socgame.campuswars_app.ui;

import android.os.Bundle;

import com.google.android.material.snackbar.Snackbar;

import androidx.appcompat.app.AppCompatActivity;

import android.view.View;

import androidx.navigation.NavController;
import androidx.navigation.Navigation;
import androidx.navigation.ui.AppBarConfiguration;
import androidx.navigation.ui.NavigationUI;

import com.socgame.campuswars_app.R;
import com.socgame.campuswars_app.databinding.ActivityQuizBinding;

/*
    Displays the quiz (duel) and reports back

    written by Jonas
*/
public class QuizActivity extends AppCompatActivity
{
    //TODO: Link to the server

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_quiz);
    }
}