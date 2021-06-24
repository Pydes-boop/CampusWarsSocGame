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
import com.google.firebase.FirebaseError;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseUser;
import com.socgame.campuswars_app.R;
import com.socgame.campuswars_app.communication.FirebaseCom;
import com.socgame.campuswars_app.communication.CampusCom;
import com.socgame.campuswars_app.communication.BackendCom;

import static com.socgame.campuswars_app.R.layout.activity_register;

public class RegisterActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(activity_register);

        Context ctx = this.getApplicationContext();
        FirebaseCom fCom = FirebaseCom.getInstance(ctx);
        CampusCom cCom = CampusCom.getInstance(ctx);
        BackendCom bCom = BackendCom.getInstance(ctx);

        EditText tumId = (EditText) findViewById(R.id.editTextTumId);
        EditText email = (EditText) findViewById(R.id.editTextEmailAddress);
        EditText password = (EditText) findViewById(R.id.editTextPassword);
        EditText confirmPassword = (EditText) findViewById(R.id.editTextConfirmPassword);

        Button next = (Button) findViewById(R.id.registerButton);

        next.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                if(password.getText().toString().equals(confirmPassword.getText().toString())){
                    //DONE: check info here
                    fCom.createAccount(email.getText().toString(), password.getText().toString(), new OnCompleteListener<AuthResult>(){
                        @Override
                        public void onComplete(@NonNull Task<AuthResult> task) {
                            if (task.isSuccessful()) {
                                // Sign in success, update UI with the signed-in user's information
                                FirebaseUser user = fCom.getMAuth().getCurrentUser();
                                fCom.setUserProfile();

                                //TODO Screen einbauen für Token Aktivierung
                                //TODO Check if TumId ist gültig?
                                //cCom.generateToken(tumId.getText().toString());

                                //TODO Adjust Register for Success?
                                bCom.register();

                                Intent myIntent = new Intent(view.getContext(), MainScreenActivity.class);
                                startActivityForResult(myIntent, 0);
                            } else {
                                Toast.makeText(ctx, "Register Failed: " + task.getException().toString(), Toast.LENGTH_SHORT).show();
                            }
                        }
                    });
                } else {
                    Toast.makeText(ctx, "Your Password do not match", Toast.LENGTH_SHORT).show();
                }
            }
        });
    }
}