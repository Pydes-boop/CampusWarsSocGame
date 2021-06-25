package com.socgame.campuswars_app.ui;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseUser;
import com.socgame.campuswars_app.R;
import com.socgame.campuswars_app.communication.BackendCom;
import com.socgame.campuswars_app.communication.FirebaseCom;
import com.socgame.campuswars_app.communication.HttpSingleton;
public class LoginActivity extends AppCompatActivity {
    /**
     *     The standard Login happens here
     *     User enters info
     *     One Button sends it to firebase
     *     The other to the register screen
     *     we save the registered state of the user
     *
     *     written by Daniel and Jonas
     */

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        Context ctx = this.getApplicationContext();
        FirebaseCom fCom = FirebaseCom.getInstance(ctx);

        //FIXME: Eventuell muss hier die id gefixt werden für login
        EditText email = (EditText) findViewById(R.id.editTextTextEmailAddress);
        EditText password = (EditText) findViewById(R.id.editTextTextPassword);
        Button login = (Button) findViewById(R.id.loginButton);

        login.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                //DONE: check info here
                if(email.getText().toString().length() == 0 || password.getText().toString().length() == 0){

                }else{
                    fCom.signIn(email.getText().toString(), password.getText().toString(), new OnCompleteListener<AuthResult>(){
                        @Override
                        public void onComplete(@NonNull Task<AuthResult> task) {
                            if (task.isSuccessful()) {
                                // Sign in success, update UI with the signed-in user's information
                                FirebaseUser user = fCom.getMAuth().getCurrentUser();
                                fCom.setUserProfile();

                                //Saving Logged in State
                                SharedPreferences settings = ctx.getSharedPreferences("userdata", 0);
                                SharedPreferences.Editor editor = settings.edit();
                                editor.putBoolean("loggedIn", true);
                                editor.apply();

                                Intent myIntent = new Intent(view.getContext(), MainScreenActivity.class);
                                startActivityForResult(myIntent, 0);
                            } else {
                                Toast.makeText(ctx, "Login Failed: " + task.getException().toString(), Toast.LENGTH_SHORT).show();
                            }
                        }
                    });
                }
            }
        });

        Button next = (Button) findViewById(R.id.registerButton);
            next.setOnClickListener(new View.OnClickListener() {
                public void onClick(View view) {
                    Intent myIntent = new Intent(view.getContext(), RegisterActivity.class);
                    startActivityForResult(myIntent, 0);
                }
            });

    }
}