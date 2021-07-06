package com.socgame.campuswars_app.ui;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.socgame.campuswars_app.R;

import org.w3c.dom.Text;

public class ResultActivity extends AppCompatActivity
{
    private TextView loading = null;
    private LinearLayout resultWrapper = null;

    private ImageView image = null;
    private TextView resText = null;

    private TextView name = null;
    private TextView team = null;

    private enum WinState{WIN, TIE, LOSE};

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_result);

        //get needed references
        image = (ImageView) findViewById(R.id.resultImg);
        loading = (TextView) findViewById(R.id.result_loading_text);
        resultWrapper = (LinearLayout) findViewById(R.id.resultWrapper);
        resText = (TextView) findViewById(R.id.resultTxt);
        name = (TextView) findViewById(R.id.enemyName);
        team = (TextView) findViewById(R.id.enemyTeam);


        //Set start visibility
        loading.setVisibility(View.VISIBLE);
        resultWrapper.setVisibility(View.INVISIBLE);

        //Continue Button
        Button next = (Button) findViewById(R.id.resultButton);
        next.setOnClickListener(new View.OnClickListener()
        {
            public void onClick(View view)
            {
                Intent myIntent = new Intent(view.getContext(), MainScreenActivity.class);
                startActivityForResult(myIntent, 0);
            }
        });

        //TODO: get actual info through http here
        //debug
        setUIInfo(WinState.WIN, "Hans", "Wet Fishes");
    }


    private void setUIInfo(WinState result, String oppName, String oppTeam)
    {
        int imageResource = 0;
        String text = "";

        switch (result)
        {
            case WIN:
                imageResource = getResources().getIdentifier("@drawable/img_winning", null, this.getPackageName());
                text = "You Won!";
                break;
            case TIE:
                imageResource = getResources().getIdentifier("@drawable/img_tie", null, this.getPackageName());
                text = "You Tied";
                break;
            case LOSE:
                imageResource = getResources().getIdentifier("@drawable/img_lose", null, this.getPackageName());
                text = "You Lost...";
                break;
        }

        image.setImageResource(imageResource);
        resText.setText(text);

        name.setText(oppName);
        team.setText(oppTeam);

        loading.setVisibility(View.INVISIBLE);
        resultWrapper.setVisibility(View.VISIBLE);
    }
}