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

    private void setUserProfile() {
        FirebaseUser user = FirebaseAuth.getInstance().getCurrentUser();
        if (user != null) {
            SharedPreferences settings = ctx.getSharedPreferences("userdata", 0);
            SharedPreferences.Editor editor = settings.edit();
            editor.putString("name", user.getDisplayName());
            editor.putString("email", user.getEmail());
            editor.putString("UID", user.getIdToken(false).toString());
            // Apply the edits!
            editor.apply();

            this.name = settings.getString("name", "empty");
            this.email = settings.getString("email", "empty");
            this.UID = settings.getString("UID", "empty");

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
        this.name = settings.getString("name", "empty");
        this.email = settings.getString("email", "empty");
        this.UID = settings.getString("UID", "empty");
    }

    public String getUID(){
        return this.UID;
    }

    private void createAccount(String email, String password) {
        mAuth.createUserWithEmailAndPassword(email, password).addOnCompleteListener(new OnCompleteListener<AuthResult>() {
                    @Override
                    public void onComplete(@NonNull Task<AuthResult> task) {
                        if (task.isSuccessful()) {
                            // Sign in success, update UI with the signed-in user's information
                            Log.d(TAG, "createUserWithEmail:success");
                            FirebaseUser user = mAuth.getCurrentUser();
                        } else {
                            // If sign in fails, display a message to the user.
                            Log.w(TAG, "createUserWithEmail:failure", task.getException());
                            //Toast.makeText(FirebaseCom.this, "Authentication failed.", Toast.LENGTH_SHORT).show();
                        }
                    }
                });
    }

    private void signIn(String email, String password) {
        mAuth.signInWithEmailAndPassword(email, password)
                .addOnCompleteListener(new OnCompleteListener<AuthResult>() {
                    @Override
                    public void onComplete(@NonNull Task<AuthResult> task) {
                        if (task.isSuccessful()) {
                            // Sign in success, update UI with the signed-in user's information
                            Log.d(TAG, "signInWithEmail:success");
                            FirebaseUser user = mAuth.getCurrentUser();
                        } else {
                            // If sign in fails, display a message to the user.
                            Log.w(TAG, "signInWithEmail:failure", task.getException());
                        }
                    }
                });
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
