package com.socgame.campuswars_app.ui;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import com.socgame.campuswars_app.R;

import static com.socgame.campuswars_app.R.layout.activity_register;

public class RegisterActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(activity_register);

        Button next = (Button) findViewById(R.id.registerButton);
        next.setOnClickListener(new View.OnClickListener()
        {

            //TODO: actually send and check info here

            public void onClick(View view) {
                Intent myIntent = new Intent(view.getContext(), MainScreenActivity.class);
                startActivityForResult(myIntent, 0);
            }
        });
    }
}