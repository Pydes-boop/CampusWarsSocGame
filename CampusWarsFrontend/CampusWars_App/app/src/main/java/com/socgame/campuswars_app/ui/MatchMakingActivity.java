package com.socgame.campuswars_app.ui;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;

import android.graphics.Color;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.widget.ListView;
import android.widget.TextView;

import com.socgame.campuswars_app.R;

public class MatchMakingActivity extends AppCompatActivity
{
    //The state represents is "what is finished?"
    private enum State  {BEGIN, REQUEST,WAIT, READY};
    private State state = State.BEGIN;

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_match_making);


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
                //send request
                break;
            case REQUEST:
                //now waiting
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