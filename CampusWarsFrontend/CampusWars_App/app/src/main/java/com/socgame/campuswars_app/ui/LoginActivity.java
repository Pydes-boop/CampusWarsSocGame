package com.socgame.campuswars_app.ui;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
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
import com.socgame.campuswars_app.communication.FirebaseCom;
import com.socgame.campuswars_app.communication.HttpSingleton;

public class LoginActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        Context ctx = this.getApplicationContext();
        FirebaseCom fCom = FirebaseCom.getInstance(ctx);

        //fixme Eventuell muss hier die id gefixt werden für login
        EditText email = (EditText) findViewById(R.id.editTextTextEmailAddress);
        EditText password = (EditText) findViewById(R.id.editTextTextPassword);
        Button login = (Button) findViewById(R.id.loginButton);

        login.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                //DONE: check info here
                fCom.signIn(email.getText().toString(), password.getText().toString(), new OnCompleteListener<AuthResult>(){
                    @Override
                    public void onComplete(@NonNull Task<AuthResult> task) {
                        if (task.isSuccessful()) {
                            // Sign in success, update UI with the signed-in user's information
                            FirebaseUser user = fCom.getMAuth().getCurrentUser();
                            fCom.setUserProfile();
                            Intent myIntent = new Intent(view.getContext(), MainScreenActivity.class);
                            startActivityForResult(myIntent, 0);
                        } else {
                            Toast.makeText(ctx, "Login Failed: " + task.getException().toString(), Toast.LENGTH_SHORT).show();
                        }
                    }
                });
                //
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