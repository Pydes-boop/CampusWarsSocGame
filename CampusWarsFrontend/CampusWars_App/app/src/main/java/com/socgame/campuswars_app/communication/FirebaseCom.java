package com.socgame.campuswars_app.communication;

import android.app.Activity;
import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.widget.Toast;

import androidx.annotation.NonNull;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;

public class FirebaseCom{

    //from https://firebase.google.com/docs/auth/android/start but modified

    private static FirebaseCom instance;

    private static final String TAG = "EmailPassword";
    private static Context ctx;

    private static FirebaseAuth mAuth;
    private static String name;
    private static String email;
    private static String UID;

    private FirebaseCom(Context ctx){
        this.ctx = ctx;
        this.mAuth = FirebaseAuth.getInstance();

        //This needed?
        FirebaseUser currentUser = mAuth.getCurrentUser();

        //Reloading User Profile and getting newest Data
        this.getUserProfile();

        /*
        if(currentUser != null){
            reload();
        }*/
    }

    public static synchronized FirebaseCom getInstance(Context context){
        if (instance == null) {
            instance = new FirebaseCom(context);
        }
        return instance;
    }

    public FirebaseAuth getMAuth(){
        return this.mAuth;
    }

    public void setUserProfile() {
        FirebaseUser user = mAuth.getCurrentUser();
        //Dont know which one is correct but i hope the first one is
        //user = FirebaseAuth.getInstance().getCurrentUser();
        if (user != null) {
            SharedPreferences settings = ctx.getSharedPreferences("userdata", 0);
            SharedPreferences.Editor editor = settings.edit();
            editor.putString("email", user.getEmail());
            editor.apply();
            //Getting Id Token For User
            user.getIdToken(false).addOnSuccessListener(result -> {
                String idToken = result.getToken();
                editor.putString("UID", idToken);
                editor.apply();
                this.UID = settings.getString("UID", "empty");
            });

            this.email = settings.getString("email", "empty");

            // TODO?
            // Check if user's email is verified
            boolean emailVerified = user.isEmailVerified();

            // The user's ID, unique to the Firebase project. Do NOT use this value to
            // authenticate with your backend server, if you have one. Use
            // FirebaseUser.getIdToken() instead.
            // We dont use this
            // String uid = user.getUid();
        }
    }

    public void getUserProfile() {
        SharedPreferences settings = ctx.getSharedPreferences("userdata", 0);
        //this.name = settings.getString("name", "empty");
        this.email = settings.getString("email", "empty");
        this.UID = settings.getString("UID", "empty");

        //Log.d("Firebase: Email:", this.email);
        //Log.d("Firebase: UID:", this.UID);

    }

    public String getUID(){
        return this.UID;
    }

    public void createAccount(String email, String password, OnCompleteListener<AuthResult> listener) {
        mAuth.createUserWithEmailAndPassword(email, password).addOnCompleteListener(listener);
    }

    public void signIn(String email, String password, OnCompleteListener<AuthResult> listener) {
        mAuth.signInWithEmailAndPassword(email, password).addOnCompleteListener(listener);
    }

    private void sendEmailVerification() {
        // Send verification email
        final FirebaseUser user = mAuth.getCurrentUser();
        user.sendEmailVerification()
                .addOnCompleteListener(new OnCompleteListener<Void>() {
                    @Override
                    public void onComplete(@NonNull Task<Void> task) {
                        // Email sent
                    }
                });
    }
}
