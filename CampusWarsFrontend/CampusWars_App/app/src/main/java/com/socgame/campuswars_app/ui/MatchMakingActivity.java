package com.socgame.campuswars_app.ui;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;

import android.content.Context;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.widget.ListView;
import android.widget.TextView;

import com.android.volley.Response;
import com.google.android.gms.maps.model.LatLng;
import com.socgame.campuswars_app.R;
import com.socgame.campuswars_app.communication.BackendCom;
import com.socgame.campuswars_app.communication.HttpHeader;

import org.json.JSONObject;

public class MatchMakingActivity extends AppCompatActivity
{
    //The state represents is "what is finished?"
    private enum State  {BEGIN, REQUEST,WAIT, READY};
    private State state = State.BEGIN;
    private Context ctx = this.getApplicationContext();
    private double latitude;
    private double longitude;
    private String roomName;
    private int lid;
    private HttpHeader head;
    private BackendCom bCom;

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_match_making);

        bCom = BackendCom.getInstance(ctx);

        Bundle b = getIntent().getExtras();
        if(b != null){
            this.latitude = b.getDouble("latitude"); //Question
            this.longitude = b.getDouble("longitude"); //Question
            this.roomName = b.getString("roomName"); //Challenger name
            this.lid = b.getInt("lid");
        }

        this.head = new HttpHeader(ctx);
        head.buildQuizHeader(latitude, longitude, lid, roomName);

        //TODO: start calling http and ui
        debugChange();
    }

    //this can be deleted
    private void debugChange()
    {
        for(int i = 1000; state != State.READY; i += 1000)
        {
            state = State.values()[state.ordinal()+1];//iterate state

            Handler handler = new Handler();
            handler.postDelayed
                    (
                            new Runnable()
                            {
                                @Override
                                public void run()
                                {
                                    changeUiState(state);
                                }
                            },
                            i
                    );
        }
    }

    //TODO: @Daniel, you can ue this or discard the code if yo want. You do you
    private void doCommunication(State s)
    {
        switch (s)
        {
            case BEGIN:
                //bCom.quiz("request");
                break;
            case REQUEST:
                //bCom.quiz("refresh");
                break;
            case WAIT:
                //done waiting
                //TODO: slightly confused, do we instantly swithc to ready?
                break;
            case READY:
                //wait a sec and then change to quiz

                /*
                Handler handler = new Handler();
                handler.postDelayed
                (
                    new Runnable()
                    {
                        @Override
                        public void run()
                        {
                            Intent myIntent = new Intent(LoadingActivity.this, QuizActivity.class);
                            //TODO: set quiz info
                            startActivityForResult(myIntent, 0);
                        }
                    },
                    1000
                );
                 */
                break;
        }

        //TODO: always change/iterate state on response
    }

    private Response.Listener<JSONObject> quizRequestListener()
    {
        return new Response.Listener<JSONObject>() {
            @Override
            public void onResponse(JSONObject response) {
                try {

                } catch (Exception e) {
                    Log.d("Error in Quiz Request Call", e.toString());
                }
            }
        };
    }


    //The state represents is "what is finished?"
    private void changeUiState(State s)
    {
        TextView requestText = this.findViewById(R.id.match_request);
        TextView waitText = this.findViewById(R.id.match_waiting);
        TextView readyText = this.findViewById(R.id.match_ready);

        state = s;

        Drawable loading = getResources().getDrawable(R.drawable.ic_sand_clock);
        Drawable done = getResources().getDrawable(R.drawable.ic_check);

        int gray = ContextCompat.getColor(this, R.color.darkAccent);
        int text = ContextCompat.getColor(this, R.color.text);

        switch (s)
        {
            case REQUEST:
                requestText.setCompoundDrawablesWithIntrinsicBounds(done, null, null, null);
                requestText.setTextColor(text);
                break;

            case WAIT:
                waitText.setCompoundDrawablesWithIntrinsicBounds(done, null, null, null);
                waitText.setTextColor(text);
                break;

            case READY:
                readyText.setCompoundDrawablesWithIntrinsicBounds(done, null, null, null);
                readyText.setTextColor(text);
                break;

            default:
                requestText.setCompoundDrawablesWithIntrinsicBounds(loading, null, null, null);
                waitText.setCompoundDrawablesWithIntrinsicBounds(loading, null, null, null);
                readyText.setCompoundDrawablesWithIntrinsicBounds(loading, null, null, null);

                requestText.setTextColor(gray);
                waitText.setTextColor(gray);
                readyText.setTextColor(gray);
        }
    }
}