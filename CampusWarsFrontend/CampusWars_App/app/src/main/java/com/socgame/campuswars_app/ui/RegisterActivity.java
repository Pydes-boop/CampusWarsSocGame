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

import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.FirebaseError;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseUser;
import com.socgame.campuswars_app.R;
import com.socgame.campuswars_app.communication.FirebaseCom;
import com.socgame.campuswars_app.communication.CampusCom;
import com.socgame.campuswars_app.communication.BackendCom;
import com.socgame.campuswars_app.communication.HttpSingleton;

import org.json.JSONObject;

import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;

import fr.arnaudguyon.xmltojsonlib.XmlToJson;

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
        HttpSingleton http = HttpSingleton.getInstance(ctx);

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
                            } else {
                                Toast.makeText(ctx, "Register Failed: " + task.getException().toString(), Toast.LENGTH_SHORT).show();
                            }
                        }
                    });


                    //Generating Token for TumOnline and Generating Secret for TumOnline
                    cCom.generateToken(tumId.getText().toString(), new Response.Listener<String>() {
                        @Override
                        public void onResponse(String Response) {
                            String token = "";
                            boolean Error = false;
                            try {

                                //Extracting Key from XML Response
                                XmlToJson xmlToJson = new XmlToJson.Builder(Response).build();
                                JSONObject jsonObject = xmlToJson.toJson();
                                //Converting
                                token = jsonObject.get("token").toString();
                                //Saving User Data
                                //Im unsure if this works correctly, but i hope it does
                                cCom.saveUserData(tumId.getText().toString(), token);

                                Log.d("HTTP", "Success: Token must be activated via TumOnline");
                            } catch (NullPointerException e) {
                                //When we dont have token in answer XML we get Nullpointer -> this means our TumId was wrong
                                Error = true;
                                Toast.makeText(ctx, "TumToken failed, Wrong TumId: " + e.toString(), Toast.LENGTH_SHORT).show();
                            } catch (Exception e) {
                                Error = true;
                                Log.d("Failure to Convert", e.toString());
                            }


                            //If no Error we upload Secret
                            if(!Error){
                                String key = cCom.generateSecret();
                                //Secret Upload
                                http.getRequestString("tumonline/wbservicesbasic.secretUpload?pToken=" + token + "&pSecret=" + key + "&pToken=" + token, new Response.Listener<String>() {
                                    @Override
                                    public void onResponse(String Response) {
                                        Log.d("HTTP", "Success: " + Response);
                                        try {
                                            XmlToJson xmlToJson = new XmlToJson.Builder(Response).build();
                                            JSONObject jsonObject = xmlToJson.toJson();

                                            //DONE Is this String Comparison okay?
                                            if(jsonObject.get("confirmed").toString().equals("true")){
                                                Log.d("HTTP", "Success: Token is valid and Secret was uploaded");
                                            }

                                        } catch (Exception e) {
                                            Log.d("Failure to Convert", e.toString());
                                        }
                                    }
                                }, new Response.ErrorListener() {
                                    @Override
                                    public void onErrorResponse(VolleyError error) {
                                        //Error Handling
                                        Log.d("HTTP", "Error: " + error.getMessage());
                                    }
                                }, true);
                            }


                            if(!Error){
                                //Register User on our own Server, runs paralell to Secret Upload
                                bCom.register();
                                //On Succesful Server Register
                                //Switching to Main Activity on Success
                                //TODO TOKEN ACTIVATION SCREEN AND THEN AFTERWARDS cCom getLectures() which automatically sends them to backende
                                Intent myIntent = new Intent(view.getContext(), MainScreenActivity.class);
                                startActivityForResult(myIntent, 0);
                            }
                        }
                    }, new Response.ErrorListener() {
                        @Override
                        public void onErrorResponse(VolleyError error) {
                            //Error Handling
                            Toast.makeText(ctx, "TumToken failed: " + error.toString(), Toast.LENGTH_SHORT).show();
                        }
                    });

                } else {
                    Toast.makeText(ctx, "Your Password do not match", Toast.LENGTH_SHORT).show();
                }
            }
        });
    }
}